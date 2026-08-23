import torch
from torch.utils.data import Dataset


class FI2010Dataset(Dataset):
    """
    Memory-efficient FI-2010 Dataset.
    """

    def __init__(self, features, labels):

        # Keep NumPy arrays
        self.features = features
        self.labels = labels

    def __len__(self):

        return len(self.labels)

    def __getitem__(self, index):

        feature = torch.from_numpy(
            self.features[index]
        ).float()

        label = torch.tensor(
            self.labels[index],
            dtype=torch.long
        )

        return feature, label