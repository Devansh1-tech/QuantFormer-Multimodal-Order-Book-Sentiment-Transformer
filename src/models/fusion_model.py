import torch
import torch.nn as nn


class FeatureProjection(nn.Module):
    """
    Projects FinBERT embeddings to a lower-dimensional space.
    """

    def __init__(
        self,
        input_dim=768,
        output_dim=128
    ):
        super().__init__()

        self.projection = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, output_dim),
            nn.ReLU()
        )

    def forward(self, x):
        return self.projection(x)


class QuantFormerFusion(nn.Module):
    """
    Multimodal Fusion Network

    Input
    -----
    Market Features : (B,128)

    News Features : (B,768)

    Output
    ------
    (B,3)
    """

    def __init__(
        self,
        market_dim=128,
        news_dim=768,
        hidden_dim=256,
        num_classes=3
    ):
        super().__init__()

        self.news_projection = FeatureProjection(
            input_dim=news_dim,
            output_dim=market_dim
        )

        fusion_dim = market_dim + market_dim

        self.classifier = nn.Sequential(

            nn.Linear(fusion_dim, hidden_dim),

            nn.ReLU(),

            nn.Dropout(0.30),

            nn.Linear(hidden_dim, 128),

            nn.ReLU(),

            nn.Dropout(0.20),

            nn.Linear(128, num_classes)

        )

    def forward(
        self,
        market_features,
        news_embeddings
    ):

        projected_news = self.news_projection(
            news_embeddings
        )

        fused = torch.cat(
            [
                market_features,
                projected_news
            ],
            dim=1
        )

        logits = self.classifier(
            fused
        )

        return logits