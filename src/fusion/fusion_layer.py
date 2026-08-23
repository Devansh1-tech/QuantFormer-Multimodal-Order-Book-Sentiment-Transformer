import torch
import torch.nn as nn

from src.config import (
    HIDDEN_SIZE,
    DROPOUT
)


class FusionLayer(nn.Module):
    """
    Feature-level fusion of LOB and News representations.
    """

    def __init__(
        self,
        hidden_size=HIDDEN_SIZE,
        dropout=DROPOUT
    ):

        super().__init__()

        self.fusion = nn.Sequential(

            nn.Linear(
                hidden_size * 2,
                hidden_size
            ),

            nn.LayerNorm(
                hidden_size
            ),

            nn.ReLU(),

            nn.Dropout(
                dropout
            )
        )

    def forward(
        self,
        lob_features,
        news_features
    ):
        """
        Parameters
        ----------
        lob_features : (B, T, H)

        news_features : (B, H)

        Returns
        -------
        fused_features : (B, T, H)
        """

        batch_size = lob_features.size(0)

        seq_len = lob_features.size(1)

        news_features = news_features.unsqueeze(1)

        news_features = news_features.expand(
            batch_size,
            seq_len,
            -1
        )

        fused = torch.cat(
            [
                lob_features,
                news_features
            ],
            dim=-1
        )

        fused = self.fusion(fused)

        return fused