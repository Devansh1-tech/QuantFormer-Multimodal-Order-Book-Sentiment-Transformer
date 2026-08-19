"""
===========================================================
FI-2010 Dataset

Project : QuantFormer

Converts processed NumPy arrays into
PyTorch datasets.

Author : Team QuantFormer
===========================================================
"""

import torch
from torch.utils.data import Dataset


class FI2010Dataset(Dataset):
    """
    Dataset for FI-2010.

    Returns
    -------
    features : Tensor
        Shape = (sequence_length, num_features)

    label : Tensor
    """

    def __init__(
        self,
        features,
        labels
    ):

        self.features = torch.tensor(
            features,
            dtype=torch.float32
        )

        self.labels = torch.tensor(
            labels,
            dtype=torch.long
        )

    def __len__(self):

        return len(self.labels)

    def __getitem__(
        self,
        index
    ):

        return (
            self.features[index],
            self.labels[index]
        )