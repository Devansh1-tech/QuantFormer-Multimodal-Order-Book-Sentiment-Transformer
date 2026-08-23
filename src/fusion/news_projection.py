import torch
import torch.nn as nn

from src.config import (
    HIDDEN_SIZE,
    DROPOUT
)


class NewsProjection(nn.Module):
    """
    Projects a 768-dimensional FinBERT embedding
    into the TFT hidden dimension.
    """

    def __init__(
        self,
        input_size=768,
        hidden_size=HIDDEN_SIZE,
        dropout=DROPOUT
    ):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(
                input_size,
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
        news_embedding
    ):

        return self.network(
            news_embedding
        )