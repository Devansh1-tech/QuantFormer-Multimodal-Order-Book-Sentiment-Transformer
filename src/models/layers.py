"""
===========================================================
Temporal Fusion Transformer Layers

This module contains the reusable neural network layers
used in the Temporal Fusion Transformer (TFT).

Implemented Layers:
1. Gated Linear Unit (GLU)
2. Gate Add & Layer Normalization

Author : Team QuantFormer
Project: QuantFormer
===========================================================
"""

import torch
import torch.nn as nn


# ==========================================================
# Gated Linear Unit (GLU)
# ==========================================================

class GLU(nn.Module):
    """
    Gated Linear Unit.

    GLU learns which information should pass through
    the network by using a sigmoid gate.

    Output:
        y = Linear(x) * Sigmoid(Gate(x))
    """

    def __init__(self, input_size: int):

        super().__init__()

        self.linear = nn.Linear(
            input_size,
            input_size
        )

        self.gate = nn.Linear(
            input_size,
            input_size
        )

    def forward(self, x):

        value = self.linear(x)

        gate = torch.sigmoid(
            self.gate(x)
        )

        return value * gate


# ==========================================================
# Gate Add & Layer Normalization
# ==========================================================

class GateAddNorm(nn.Module):
    """
    Gate Add Normalization Block.

    Structure

        Input
          │
          ▼
        GLU
          │
          ▼
      Residual Add
          │
          ▼
    Layer Normalization

    This block improves gradient flow and stabilizes
    training in deep Transformer architectures.
    """

    def __init__(self, input_size: int):

        super().__init__()

        self.glu = GLU(input_size)

        self.layer_norm = nn.LayerNorm(
            input_size
        )

    def forward(
        self,
        x,
        residual
    ):

        gated = self.glu(x)

        output = gated + residual

        output = self.layer_norm(output)

        return output

# ==========================================================
# Gated Residual Network (GRN)
# ==========================================================

class GatedResidualNetwork(nn.Module):
    """
    Gated Residual Network (GRN)

    The GRN is one of the core building blocks of the
    Temporal Fusion Transformer.

    Architecture

          Input
            │
      Linear Layer
            │
          ELU
            │
      Linear Layer
            │
       Dropout
            │
      GateAddNorm
            │
          Output
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int = None,
        dropout: float = 0.1
    ):

        super().__init__()

        if output_size is None:
            output_size = input_size

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # First fully connected layer
        self.fc1 = nn.Linear(
            input_size,
            hidden_size
        )

        # Activation
        self.activation = nn.ELU()

        # Second fully connected layer
        self.fc2 = nn.Linear(
            hidden_size,
            output_size
        )

        # Dropout
        self.dropout = nn.Dropout(dropout)

        # Residual projection
        if input_size != output_size:
            self.skip = nn.Linear(
                input_size,
                output_size
            )
        else:
            self.skip = nn.Identity()

        # Gate + Residual + LayerNorm
        self.gate_add_norm = GateAddNorm(
            output_size
        )

    def forward(self, x):

        residual = self.skip(x)

        out = self.fc1(x)

        out = self.activation(out)

        out = self.fc2(out)

        out = self.dropout(out)

        out = self.gate_add_norm(
            out,
            residual
        )

        return out