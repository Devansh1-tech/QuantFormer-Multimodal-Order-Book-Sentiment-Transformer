import torch
from torch.utils.data import Dataset


class MultiModalDataset(Dataset):
    """
    Dataset containing:

    - LOB Features
    - News Embeddings
    - Labels
    """

    def __init__(
        self,
        lob_features,
        news_embeddings,
        labels
    ):

        self.lob_features = torch.as_tensor(
            lob_features,
            dtype=torch.float32
        )

        self.news_embeddings = torch.as_tensor(
            news_embeddings,
            dtype=torch.float32
        )

        self.labels = torch.as_tensor(
            labels,
            dtype=torch.long
        )

    def __len__(self):

        return len(self.labels)

    def __getitem__(self, index):

        return (
            self.lob_features[index],
            self.news_embeddings[index],
            self.labels[index]
        )