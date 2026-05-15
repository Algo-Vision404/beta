import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import StandardScaler
from typing import Tuple

class HMMRegimeDetector:
    def __init__(self, n_components: int = 3):
        self.n_components = n_components
        self.model = hmm.GaussianHMM(
            n_components=n_components, 
            covariance_type="full", 
            n_iter=1000
        )
        self.scaler = StandardScaler()

    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for HMM (Returns, Volatility, Range)."""
        returns = df['Close'].pct_change().dropna()
        volatility = returns.rolling(window=20).std().dropna()
        range_hl = (df['High'] - df['Low']) / df['Close']
        range_hl = range_hl.iloc[returns.index[0]:] # Align
        
        features = np.column_stack([returns.iloc[19:], volatility.iloc[19:], range_hl.iloc[19:]])
        return self.scaler.fit_transform(features)

    def train_and_predict(self, df: pd.DataFrame) -> np.ndarray:
        """Train HMM and predict hidden states (regimes)."""
        features = self.prepare_features(df)
        self.model.fit(features)
        states = self.model.predict(features)
        return states

    def get_regime_characteristics(self, df: pd.DataFrame, states: np.ndarray) -> dict:
        """Analyze what each state represents (Bullish/Bearish/Volatile)."""
        # Logic to map numeric states to human-readable regimes
        return {i: f"Regime {i}" for i in range(self.n_components)}
