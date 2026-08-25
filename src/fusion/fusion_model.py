"""
===========================================================
QuantFormer Multimodal Fusion Model
===========================================================

This module implements the feature-level fusion of:
1. Limit Order Book (LOB) temporal representations from a
   pretrained Temporal Fusion Transformer (TFT).
2. Financial news sentiment representations from FinBERT.

Architecture:
- TFT (Frozen Feature Extractor) -> Market Features (dynamic dim)
- FinBERT Embeddings (768-dim) -> NewsProjection -> News Features (dynamic dim)
- [Market Features || News Features] -> FusionLayer -> Fused Representation
- Fused Representation -> Final Classifier -> 3-Class Prediction

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from src.models.tft_model import TemporalFusionTransformer
from src.project_config import DROPOUT, NUM_CLASSES


# ==========================================================
# News Projection Layer
# ==========================================================

class NewsProjection(nn.Module):
    """
    Projects a 768-dimensional FinBERT news embedding into the
    dynamically determined market feature dimension.
    """

    def __init__(
        self,
        input_dim: int = 768,
        output_dim: int = 128,
        dropout: float = DROPOUT
    ):
        super().__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim

        self.projection = nn.Sequential(
            nn.Linear(input_dim, output_dim),
            nn.LayerNorm(output_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

    def forward(self, news_embedding: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for news projection.

        Parameters
        ----------
        news_embedding : torch.Tensor of shape (batch_size, 768)

        Returns
        -------
        torch.Tensor of shape (batch_size, output_dim)
        """
        return self.projection(news_embedding)


# ==========================================================
# Cross-Modal Fusion Layer
# ==========================================================

class FusionLayer(nn.Module):
    """
    Combines market features and projected news features using
    feature concatenation followed by a gated linear residual layer.
    """

    def __init__(
        self,
        feature_dim: int,
        dropout: float = DROPOUT
    ):
        super().__init__()

        self.feature_dim = feature_dim

        # Fuses concatenated representations [Market || News] -> feature_dim
        self.fusion_block = nn.Sequential(
            nn.Linear(feature_dim * 2, feature_dim),
            nn.LayerNorm(feature_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        # Gating layer to modulate news impact relative to market features
        self.gate = nn.Sequential(
            nn.Linear(feature_dim * 2, feature_dim),
            nn.Sigmoid()
        )

    def forward(
        self,
        market_features: torch.Tensor,
        news_features: torch.Tensor
    ) -> torch.Tensor:
        """
        Forward pass for multimodal fusion.

        Parameters
        ----------
        market_features : torch.Tensor of shape (batch_size, feature_dim)
        news_features   : torch.Tensor of shape (batch_size, feature_dim)

        Returns
        -------
        torch.Tensor of shape (batch_size, feature_dim)
        """
        # Concatenate market and news features along feature dimension
        combined = torch.cat([market_features, news_features], dim=-1)

        fused = self.fusion_block(combined)
        gate_weight = self.gate(combined)

        # Gated combination with residual market feature connection
        output = gate_weight * fused + (1.0 - gate_weight) * market_features
        return output


# ==========================================================
# QuantFormer Multimodal Fusion Model
# ==========================================================

class QuantFormerFusion(nn.Module):
    """
    End-to-end Multimodal Fusion Model combining Temporal Fusion
    Transformer market features and FinBERT news embeddings.

    The TFT model is frozen as a fixed feature extractor. The market
    feature dimension is dynamically inferred from the pooled output
    tensor of the TFT rather than hardcoded.
    """

    def __init__(
        self,
        tft_model: TemporalFusionTransformer = None,
        num_classes: int = NUM_CLASSES,
        dropout: float = DROPOUT,
        news_embedding_dim: int = 768
    ):
        super().__init__()

        # Instantiate or assign TFT model
        if tft_model is None:
            self.market_model = TemporalFusionTransformer()
        else:
            self.market_model = tft_model

        # Freeze all pretrained TFT parameters (fixed feature extractor)
        for param in self.market_model.parameters():
            param.requires_grad = False

        self.num_classes = num_classes
        self.dropout_rate = dropout
        self.news_embedding_dim = news_embedding_dim

        # Dynamic sub-modules (lazily built upon inspecting market_features tensor)
        self.market_dim = None
        self.news_projection = None
        self.fusion_layer = None
        self.classifier = None

    def _build_fusion_modules(self, market_dim: int, device: torch.device):
        """
        Dynamically initializes fusion and classification modules based on the
        feature dimension returned by the TFT forward pass.
        """
        self.market_dim = market_dim

        # 1. News Projection: 768 -> market_dim
        self.news_projection = NewsProjection(
            input_dim=self.news_embedding_dim,
            output_dim=market_dim,
            dropout=self.dropout_rate
        ).to(device)

        # 2. Fusion Layer: combines market_dim + market_dim -> market_dim
        self.fusion_layer = FusionLayer(
            feature_dim=market_dim,
            dropout=self.dropout_rate
        ).to(device)

        # 3. Final Multimodal Classifier Head: market_dim -> num_classes
        hidden_dim = max(market_dim // 2, self.num_classes)
        self.classifier = nn.Sequential(
            nn.Linear(market_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(self.dropout_rate),
            nn.Linear(hidden_dim, self.num_classes)
        ).to(device)

    def forward(
        self,
        market_data: torch.Tensor,
        news_embedding: torch.Tensor = None
    ):
        """
        Forward pass of the Multimodal Fusion Model.

        Parameters
        ----------
        market_data    : torch.Tensor of shape (batch_size, seq_len, num_features)
        news_embedding : torch.Tensor of shape (batch_size, 768) or (768,) or None

        Returns
        -------
        logits          : torch.Tensor of shape (batch_size, num_classes)
        prediction      : torch.Tensor of shape (batch_size,) - Predicted class indices
        confidence      : torch.Tensor of shape (batch_size,) - Probability of predicted class
        attention       : torch.Tensor of shape (batch_size, heads, seq_len, seq_len)
        market_features : torch.Tensor of shape (batch_size, market_dim)
        news_features   : torch.Tensor of shape (batch_size, market_dim)
        """
        batch_size = market_data.size(0)
        device = market_data.device

        # --------------------------------------------------
        # 1. Extract Market Features from Frozen TFT
        # --------------------------------------------------
        with torch.no_grad():
            _, pooled_market_features, attention = self.market_model(market_data)

        # Dynamically discover market feature dimension from tensor shape
        dynamic_market_dim = pooled_market_features.shape[-1]

        if self.news_projection is None or self.market_dim != dynamic_market_dim:
            self._build_fusion_modules(dynamic_market_dim, device)

        # --------------------------------------------------
        # 2. Process News Embeddings
        # --------------------------------------------------
        if news_embedding is None:
            # When no news is available, provide a neutral zero embedding
            news_embedding = torch.zeros(
                batch_size,
                self.news_embedding_dim,
                dtype=torch.float32,
                device=device
            )
        else:
            news_embedding = news_embedding.to(device=device, dtype=torch.float32)
            # Ensure correct 2D shape (batch_size, news_dim)
            if news_embedding.dim() == 1:
                news_embedding = news_embedding.unsqueeze(0)
            if news_embedding.size(0) == 1 and batch_size > 1:
                news_embedding = news_embedding.expand(batch_size, -1)

        # Project 768-dim news embedding to market_dim
        news_features = self.news_projection(news_embedding)

        # --------------------------------------------------
        # 3. Fuse Market & News Representations
        # --------------------------------------------------
        fused_features = self.fusion_layer(
            pooled_market_features,
            news_features
        )

        # --------------------------------------------------
        # 4. Final Classification Head & Probability Stats
        # --------------------------------------------------
        logits = self.classifier(fused_features)
        probabilities = F.softmax(logits, dim=-1)
        confidence, prediction = torch.max(probabilities, dim=-1)

        return (
            logits,
            prediction,
            confidence,
            attention,
            pooled_market_features,
            news_features
        )