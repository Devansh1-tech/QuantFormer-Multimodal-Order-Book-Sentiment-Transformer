from src.models.position_encoding import (
    PositionalEncoding
)

from src.models.feed_forward import (
    PositionwiseFeedForward
)

import torch
import torch.nn as nn

from src.models.layers import (
    GatedResidualNetwork,
    GateAddNorm
)

from src.models.attention import (
    InterpretableMultiHeadAttention
)

from src.config import (
    NUM_FEATURES,
    HIDDEN_SIZE,
    LSTM_LAYERS,
    ATTENTION_HEADS,
    DROPOUT,
    NUM_CLASSES
)


# ==========================================================
# Input Projection
# ==========================================================

class InputProjection(nn.Module):
    """
    Projects raw FI-2010 features into the hidden dimension.
    """

    def __init__(
        self,
        input_size,
        hidden_size
    ):

        super().__init__()

        self.projection = nn.Linear(
            input_size,
            hidden_size
        )

    def forward(self, x):

        return self.projection(x)


# ==========================================================
# LSTM Encoder
# ==========================================================

class LSTMEncoder(nn.Module):
    """
    Local temporal encoder.
    """

    def __init__(
        self,
        hidden_size,
        num_layers,
        dropout
    ):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )

    def forward(self, x):

        output, _ = self.lstm(x)

        return output

# ==========================================================
# Temporal Fusion Transformer
# ==========================================================

class TemporalFusionTransformer(nn.Module):
    """
    QuantFormer Temporal Fusion Transformer
    """

    def __init__(self):

        super().__init__()

        # ---------------------------------------------
        # Input Projection
        # ---------------------------------------------

        self.input_projection = InputProjection(
            NUM_FEATURES,
            HIDDEN_SIZE
        )

        # ---------------------------------------------
        # Positional Encoding
        # ---------------------------------------------

        self.position_encoding = PositionalEncoding(
            hidden_size=HIDDEN_SIZE
        )

        # ---------------------------------------------
        # LSTM Encoder
        # ---------------------------------------------

        self.encoder = LSTMEncoder(
            HIDDEN_SIZE,
            LSTM_LAYERS,
            DROPOUT
        )

        # ---------------------------------------------
        # Gated Residual Network
        # ---------------------------------------------

        self.grn = GatedResidualNetwork(
            input_size=HIDDEN_SIZE,
            hidden_size=HIDDEN_SIZE,
            output_size=HIDDEN_SIZE,
            dropout=DROPOUT
        )

        # ---------------------------------------------
        # Multi Head Attention
        # ---------------------------------------------

        self.attention = InterpretableMultiHeadAttention(
            hidden_size=HIDDEN_SIZE,
            num_heads=ATTENTION_HEADS,
            dropout=DROPOUT
        )

        self.post_attention_grn = GatedResidualNetwork(
            input_size=HIDDEN_SIZE,
            hidden_size=HIDDEN_SIZE,
            output_size=HIDDEN_SIZE,
            dropout=DROPOUT
        )

        # ---------------------------------------------
        # Feed Forward Network
        # ---------------------------------------------

        self.feed_forward = PositionwiseFeedForward(
            hidden_size=HIDDEN_SIZE,
            dropout=DROPOUT
        )

        # ---------------------------------------------
        # Gate Add Norm
        # ---------------------------------------------

        self.gate_norm = GateAddNorm(
            HIDDEN_SIZE
        )

        # ---------------------------------------------
        # Classification Head
        # ---------------------------------------------

        self.classifier = nn.Sequential(

            nn.Linear(
                HIDDEN_SIZE,
                HIDDEN_SIZE // 2
            ),

            nn.ReLU(),

            nn.Dropout(DROPOUT),

            nn.Linear(
                HIDDEN_SIZE // 2,
                NUM_CLASSES
            )
        )
        
    def forward(self, x):
    


        x = self.input_projection(x)

        
        x = self.position_encoding(x)


        lstm_features = self.encoder(x)


        grn_features = self.grn(lstm_features)


        attention_features, attention_weights = self.attention(
            grn_features
        )

        refined_features = self.post_attention_grn(
            attention_features
        )


        refined_features = self.feed_forward(
            refined_features
        )


        fused_features = self.gate_norm(
            refined_features,
            grn_features
        )

        pooled_features = fused_features.mean(dim=1)


        logits = self.classifier(
            pooled_features
        )

        return logits, attention_weights