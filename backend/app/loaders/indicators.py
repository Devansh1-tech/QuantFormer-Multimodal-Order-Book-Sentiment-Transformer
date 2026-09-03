import numpy as np
import pandas as pd
from typing import List

def synthesize_market_features(ohlcv_df: pd.DataFrame, target_sequence_length: int = 100, target_features: int = 143) -> np.ndarray:
    """
    Synthesizes a 143-feature tensor from basic OHLCV data.
    Since real L2 order book data is not available via standard yfinance,
    this creates a pseudo-representation matching the TFT input shape.
    
    Args:
        ohlcv_df: DataFrame with 'Open', 'High', 'Low', 'Close', 'Volume'
        target_sequence_length: Expected sequence length (100)
        target_features: Expected feature dimension (143)
        
    Returns:
        np.ndarray of shape (target_sequence_length, target_features)
    """
    df = ohlcv_df.copy()
    
    # Base features
    df['Returns'] = df['Close'].pct_change().fillna(0)
    df['LogReturns'] = np.log(df['Close'] / df['Close'].shift(1)).fillna(0)
    df['Volatility'] = df['Returns'].rolling(window=5).std().fillna(0)
    df['Spread'] = (df['High'] - df['Low']) / df['Close']
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    # We only have ~10 base features. We will project/pad them to 143 features.
    base_features = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'LogReturns', 'Volatility', 'Spread', 'VWAP']].values
    
    # Pad sequences to target_sequence_length
    if len(base_features) < target_sequence_length:
        pad_length = target_sequence_length - len(base_features)
        padding = np.zeros((pad_length, base_features.shape[1]))
        base_features = np.vstack((padding, base_features))
    elif len(base_features) > target_sequence_length:
        base_features = base_features[-target_sequence_length:]
        
    # Project to 143 features (repeating and adding some noise/variations for structure)
    num_base = base_features.shape[1]
    repeats = target_features // num_base
    remainder = target_features % num_base
    
    synthetic_features = np.tile(base_features, (1, repeats))
    if remainder > 0:
        synthetic_features = np.hstack((synthetic_features, base_features[:, :remainder]))
        
    # Normalize features to mean 0, std 1 column-wise
    means = synthetic_features.mean(axis=0)
    stds = synthetic_features.std(axis=0)
    stds[stds == 0] = 1.0  # Prevent division by zero
    
    normalized_features = (synthetic_features - means) / stds
    
    return normalized_features
