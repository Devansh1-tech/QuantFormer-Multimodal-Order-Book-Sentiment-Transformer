"""
===========================================================
FinBERT News Feature Extractor (Inference Only)
===========================================================

Loads the pretrained HuggingFace ProsusAI/finbert model and
extracts 768-dimensional contextual sentence embeddings from
financial news headlines.

Author : Team QuantFormer
Project: Multimodal Order Book & Sentiment Transformer
===========================================================
"""

import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel


class FinBERTExtractor(nn.Module):
    """
    Inference-only feature extractor wrapping ProsusAI/finbert.
    """

    def __init__(
        self,
        model_name: str = "ProsusAI/finbert",
        device: torch.device = None
    ):
        super().__init__()

        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model_name = model_name

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        self.model.to(self.device)
        self.model.eval()

        # Freeze FinBERT parameters for inference-only usage
        for param in self.model.parameters():
            param.requires_grad = False

    def extract_embedding(self, text: str, max_length: int = 128) -> torch.Tensor:
        """
        Generate a 768-dimensional embedding for a financial headline.

        Parameters
        ----------
        text : str, news headline text
        max_length : int, maximum token length

        Returns
        -------
        torch.Tensor of shape (768,) on CPU
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=max_length
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mean pooling across tokens -> (1, 768) -> (768,)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze(0).cpu()
        return embedding

    def extract_batch(self, texts: list, max_length: int = 128) -> torch.Tensor:
        """
        Generate a batch of 768-dimensional embeddings for multiple headlines.

        Parameters
        ----------
        texts : list of str
        max_length : int, maximum token length

        Returns
        -------
        torch.Tensor of shape (len(texts), 768) on CPU
        """
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=max_length
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1).cpu()
        return embeddings
