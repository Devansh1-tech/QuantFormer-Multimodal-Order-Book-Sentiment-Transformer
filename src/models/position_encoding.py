"""
===========================================================
Positional Encoding

Project : QuantFormer

Author : Team QuantFormer
===========================================================
"""

import math
import torch
import torch.nn as nn


class PositionalEncoding(nn.Module):
    """
    Sinusoidal Positional Encoding

    Adds positional information to sequential
    representations before passing them into
    the Temporal Fusion Transformer.
    """

    def __init__(
        self,
        hidden_size: int,
        max_length: int = 5000
    ):

        super().__init__()

        pe = torch.zeros(max_length, hidden_size)

        position = torch.arange(
            0,
            max_length,
            dtype=torch.float
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                hidden_size,
                2
            ).float()
            *
            (-math.log(10000.0) / hidden_size)
        )

        pe[:, 0::2] = torch.sin(
            position * div_term
        )

        pe[:, 1::2] = torch.cos(
            position * div_term
        )

        pe = pe.unsqueeze(0)

        self.register_buffer(
            "pe",
            pe
        )

    def forward(
        self,
        x
    ):

        seq_length = x.size(1)

        x = x + self.pe[:, :seq_length]

        return x