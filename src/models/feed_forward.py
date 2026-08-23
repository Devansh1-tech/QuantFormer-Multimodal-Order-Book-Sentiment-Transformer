"""
===========================================================
Feed Forward Network

Project : QuantFormer

Author : Team QuantFormer
===========================================================
"""

import torch.nn as nn


class PositionwiseFeedForward(nn.Module):
    """
    Position-wise Feed Forward Network.

    Applied after the attention layer to
    refine learned sequence representations.
    """

    def __init__(
        self,
        hidden_size: int,
        dropout: float = 0.2
    ):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(
                hidden_size,
                hidden_size * 4
            ),

            nn.ReLU(),

            nn.Dropout(
                dropout
            ),

            nn.Linear(
                hidden_size * 4,
                hidden_size
            )
        )

    def forward(
        self,
        x
    ):

        return self.network(x)