from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel
import pandas as pd
import numpy as np
from beta.models.regime_models import HMMRegimeDetector
from beta.core.social import SocialIntelligenceEngine

class MarketState(BaseModel):
    asset: str
    price: float
    volatility: str
    trend: str
    liquidity: str
    regime_confidence: float
    atr: float = 0.0

class TradePlan(BaseModel):
    asset: str
    direction: str
    entry: float
    stop_loss: float
    take_profit: List[float]
    status: str = "Pending"

class TradeSetup(BaseModel):
    asset: str
    type: str # BUY_LIMIT, SELL_LIMIT, etc.
    entry: float
    sl: float
    tp: List[float]
    position_size: float
    risk_reward: float
    confidence: float

class BaseEngine(ABC):
    @abstractmethod
    def initialize(self):
        pass

class MarketEngine(BaseEngine):
    """Handles raw data ingestion and structural mapping."""
    def __init__(self):
        self.cache = {}

    def initialize(self):
        pass

    def fetch_data(self, ticker: str) -> pd.DataFrame:
        """Simulates fetching real-time OHLCV data."""
        # Mocking data for institutional simulation
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='h')
        df = pd.DataFrame({
            'Open': np.random.normal(1.08, 0.01, 100),
            'High': np.random.normal(1.085, 0.01, 100),
            'Low': np.random.normal(1.075, 0.01, 100),
            'Close': np.random.normal(1.08, 0.01, 100),
            'Volume': np.random.randint(1000, 5000, 100)
        }, index=dates)
        return df

class RegimeEngine(BaseEngine):
    """AI-powered regime detection using HMM and technical volatility."""
    def __init__(self):
        self.hmm_detector = HMMRegimeDetector(n_components=3)

    def initialize(self):
        pass

    def detect_regime(self, data: pd.DataFrame) -> MarketState:
        """Analyze data to detect current market regime using HMM and technicals."""
        if data is None or data.empty or len(data) < 50:
            return MarketState(
                asset="Unknown", 
                price=0.0, 
                volatility="Low", 
                trend="Neutral", 
                liquidity="Low", 
                regime_confidence=0.0,
                atr=0.0
            )
        
        last_price = data['Close'].iloc[-1]
        volatility = "High" if data['Close'].pct_change().std() > 0.01 else "Low"
        
        # Simple trend logic for simulation
        ma_short = data['Close'].rolling(20).mean().iloc[-1]
        ma_long = data['Close'].rolling(50).mean().iloc[-1]
        trend = "Bullish" if ma_short > ma_long else "Bearish"
        
        # HMM Confidence (Mocked)
        confidence = 0.85 if abs(ma_short - ma_long) / ma_long > 0.005 else 0.45
        
        # ATR Calculation
        atr = data['Close'].diff().abs().rolling(14).mean().iloc[-1]
        
        return MarketState(
            asset="Simulated",
            price=last_price,
            volatility=volatility,
            trend=trend,
            liquidity="High",
            regime_confidence=confidence,
            atr=atr
        )

class RiskEngine:
    def __init__(self, initial_capital: float = 100000.0):
        self.capital = initial_capital
        self.max_drawdown = 0.1 # 10%
        self.current_drawdown = 0.0

    def calculate_position(self, risk_pct: float, entry: float, sl: float) -> float:
        """Calculates lot size based on risk amount and SL distance."""
        risk_amount = self.capital * (risk_pct / 100)
        sl_distance = abs(entry - sl)
        if sl_distance == 0: return 0.0
        # Simulating standard lot size (100k units)
        units = risk_amount / sl_distance
        return round(units / 100000, 2)

    def generate_setup(self, state: MarketState, risk_pct: float = 1.0) -> TradeSetup:
        """Synthesizes a full trade setup using statistical models."""
        is_bullish = state.trend == "Bullish"
        entry = state.price * 0.999 if is_bullish else state.price * 1.001
        
        # ATR-based SL/TP calculation
        sl_mult = 1.5
        tp_mults = [1.5, 3.0, 5.0]
        
        sl = entry - (state.atr * sl_mult) if is_bullish else entry + (state.atr * sl_mult)
        tps = [
            entry + (state.atr * m) if is_bullish else entry - (state.atr * m)
            for m in tp_mults
        ]
        
        pos_size = self.calculate_position(risk_pct, entry, sl)
        rr = abs(tps[1] - entry) / abs(entry - sl) if abs(entry - sl) != 0 else 0.0
        
        return TradeSetup(
            asset=state.asset,
            type="BUY_LIMIT" if is_bullish else "SELL_LIMIT",
            entry=entry,
            sl=sl,
            tp=tps,
            position_size=pos_size,
            risk_reward=rr,
            confidence=state.regime_confidence
        )

    def validate_plan(self, plan: TradePlan, current_equity: float = 100000.0) -> Tuple[bool, str]:
        """Final authority for trade execution safety."""
        if self.current_drawdown > self.max_drawdown:
            return False, "Max drawdown reached. Trading suspended."
            
        risk_per_unit = abs(plan.entry - plan.stop_loss)
        if risk_per_unit / plan.entry > 0.05:
            return False, f"Risk per unit ({risk_per_unit/plan.entry:.2%}) exceeds safety limit."

        return True, "Validated"
