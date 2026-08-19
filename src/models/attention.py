"""
===========================================================
Interpretable Multi-Head Attention

Temporal Fusion Transformer

Author : Team QuantFormer
===========================================================
"""

import math
import torch
import torch.nn as nn


class InterpretableMultiHeadAttention(nn.Module):
    """
    Interpretable Multi-Head Attention used in the
    Temporal Fusion Transformer.
    """

    def __init__(
        self,
        hidden_size: int,
        num_heads: int,
        dropout: float = 0.1
    ):

        super().__init__()

        assert hidden_size % num_heads == 0

        self.hidden_size = hidden_size
        self.num_heads = num_heads

        self.head_dim = hidden_size // num_heads

        self.query = nn.Linear(hidden_size, hidden_size)

        self.key = nn.Linear(hidden_size, hidden_size)

        self.value = nn.Linear(hidden_size, hidden_size)

        self.output = nn.Linear(hidden_size, hidden_size)

        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x
    ):

        batch_size = x.size(0)

        seq_len = x.size(1)

        Q = self.query(x)

        K = self.key(x)

        V = self.value(x)

        Q = Q.view(
            batch_size,
            seq_len,
            self.num_heads,
            self.head_dim
        ).transpose(1, 2)

        K = K.view(
            batch_size,
            seq_len,
            self.num_heads,
            self.head_dim
        ).transpose(1, 2)

        V = V.view(
            batch_size,
            seq_len,
            self.num_heads,
            self.head_dim
        ).transpose(1, 2)

        scores = torch.matmul(
            Q,
            K.transpose(-2, -1)
        )

        scores = scores / math.sqrt(self.head_dim)

        attention = torch.softmax(
            scores,
            dim=-1
        )

        attention = self.dropout(attention)

        context = torch.matmul(
            attention,
            V
        )

        context = context.transpose(
            1,
            2
        ).contiguous()

        context = context.view(
            batch_size,
            seq_len,
            self.hidden_size
        )

        output = self.output(context)

        return output, attention