import torch
import torch.nn as nn

from src.models.tft_model import TFTModel


class QuantFormerFusion(nn.Module):

    def __init__(self):

        super().__init__()

        # --------------------------------------------------
        # Market Model (Your trained TFT)
        # --------------------------------------------------

        self.market_model = TFTModel()

        # --------------------------------------------------
        # News Projection
        # 768 -> 128
        # --------------------------------------------------

        self.news_projection = nn.Sequential(

            nn.Linear(768, 256),

            nn.ReLU(),

            nn.Dropout(0.2),

            nn.Linear(256, 128),

            nn.ReLU()

        )

        # --------------------------------------------------
        # Fusion Layer
        # 128 + 128 = 256
        # --------------------------------------------------
        print("Market :", market_features.shape)
        print("News   :", news_features.shape)

        fused_features = torch.cat(
            (
                market_features,
                news_features
            ),
            dim=1
        )

        print("Fused :", fused_features.shape)

        print(self.fusion)

        fused_features = self.fusion(
            fused_features
        )

        self.fusion = nn.Sequential(

            nn.Linear(256, 128),

            nn.ReLU(),

            nn.Dropout(0.2)

        )

        # --------------------------------------------------
        # Final Classifier
        # --------------------------------------------------

        self.classifier = nn.Sequential(

            nn.Linear(128, 64),

            nn.ReLU(),

            nn.Dropout(0.2),

            nn.Linear(64, 3)

        )

    def forward(
        self,
        market_data,
        news_embedding
    ):

        # ------------------------------------------
        # Market Features
        # ------------------------------------------

        _, market_features, attention = self.market_model(
            market_data
        )

        # ------------------------------------------
        # News Features
        # ------------------------------------------

        news_features = self.news_projection(
            news_embedding
        )

        # ------------------------------------------
        # Concatenate
        # ------------------------------------------

        fused_features = torch.cat(

            (
                market_features,
                news_features
            ),

            dim=1

        )

        # ------------------------------------------
        # Fusion Network
        # ------------------------------------------

        fused_features = self.fusion(
            fused_features
        )

        # ------------------------------------------
        # Prediction
        # ------------------------------------------

        logits = self.classifier(
            fused_features
        )

        return (
            logits,
            market_features,
            news_features,
            attention
        )