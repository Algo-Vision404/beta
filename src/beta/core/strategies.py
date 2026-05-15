import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Optional
from beta.core.engine import TradePlan, MarketState

class BaseStrategy(ABC):
    @abstractmethod
    def generate_plan(self, data: pd.DataFrame, state: MarketState) -> Optional[TradePlan]:
        pass

class MSNRStrategy(BaseStrategy):
    """
    Mean Shift Noise Reduction (Normalized Mean Reversion).
    Identifies overextended moves relative to volatility.
    """
    def __init__(self, window: int = 20, z_threshold: float = 2.0):
        self.window = window
        self.z_threshold = z_threshold

    def generate_plan(self, data: pd.DataFrame, state: MarketState) -> Optional[TradePlan]:
        if len(data) < self.window:
            return None
        
        close = data['Close']
        returns = close.pct_change()
        mean_return = returns.rolling(window=self.window).mean()
        std_return = returns.rolling(window=self.window).std()
        
        last_return = returns.iloc[-1]
        z_score = (last_return - mean_return.iloc[-1]) / std_return.iloc[-1]
        
        direction = ""
        if z_score > self.z_threshold:
            direction = "Short"
        elif z_score < -self.z_threshold:
            direction = "Long"
        
        if direction:
            price = state.price
            atr = (data['High'] - data['Low']).rolling(window=14).mean().iloc[-1]
            
            entry = price
            sl = price - (atr * 1.5) if direction == "Long" else price + (atr * 1.5)
            tp = price + (atr * 2.0) if direction == "Long" else price - (atr * 2.0)
            
            return TradePlan(
                asset=state.asset,
                direction=direction,
                entry=entry,
                stop_loss=sl,
                take_profit=[tp],
                risk_score=0.8,
                reasoning=f"MSNR Z-Score: {z_score:.2f} (Threshold: {self.z_threshold})"
            )
        
        return None

class TrendFollowingStrategy(BaseStrategy):
    """
    Classic EMA Trend Following.
    """
    def __init__(self, fast_ema: int = 20, slow_ema: int = 50):
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema

    def generate_plan(self, data: pd.DataFrame, state: MarketState) -> Optional[TradePlan]:
        # Only trend follow in trending regimes
        if state.trend == "Sideways":
            return None
            
        ema_fast = data['Close'].ewm(span=self.fast_ema).mean().iloc[-1]
        ema_slow = data['Close'].ewm(span=self.slow_ema).mean().iloc[-1]
        
        direction = "Long" if ema_fast > ema_slow else "Short"
        
        # Validation against regime
        if (direction == "Long" and state.trend == "Bearish") or (direction == "Short" and state.trend == "Bullish"):
            return None
            
        entry = state.price
        atr = (data['High'] - data['Low']).rolling(window=14).mean().iloc[-1]
        sl = entry - (atr * 2) if direction == "Long" else entry + (atr * 2)
        tp = entry + (atr * 3) if direction == "Long" else entry - (atr * 3)
        
        return TradePlan(
            asset=state.asset,
            direction=direction,
            entry=entry,
            stop_loss=sl,
            take_profit=[tp],
            risk_score=0.6,
            reasoning=f"EMA Cross ({self.fast_ema}/{self.slow_ema}) aligned with {state.trend} trend"
        )

class LondonBreakoutStrategy(BaseStrategy):
    """
    Session breakout strategy. 
    Trades the high/low of the Asia session during London open.
    """
    def generate_plan(self, data: pd.DataFrame, state: MarketState) -> Optional[TradePlan]:
        # Simple version: look at last 8 hours (Asia session)
        asia_data = data.tail(8)
        session_high = asia_data['High'].max()
        session_low = asia_data['Low'].min()
        
        current_price = state.price
        direction = ""
        if current_price > session_high:
            direction = "Long"
        elif current_price < session_low:
            direction = "Short"
            
        if direction:
            entry = current_price
            sl = session_low if direction == "Long" else session_high
            tp = entry + (entry - sl) * 1.5 # 1:1.5 RR
            
            return TradePlan(
                asset=state.asset,
                direction=direction,
                entry=entry,
                stop_loss=sl,
                take_profit=[tp],
                risk_score=0.7,
                reasoning=f"London Breakout: Price cleared Asia {('High' if direction=='Long' else 'Low')}"
            )
        return None

class LiquiditySweepStrategy(BaseStrategy):
    """
    Detects stop-hunts or liquidity sweeps (wicking through structural levels).
    """
    def generate_plan(self, data: pd.DataFrame, state: MarketState) -> Optional[TradePlan]:
        if len(data) < 20: return None
        
        # Look for a sharp wick through the 20-period high/low
        recent_high = data['High'].iloc[:-1].tail(20).max()
        recent_low = data['Low'].iloc[:-1].tail(20).min()
        
        last_candle = data.iloc[-1]
        
        direction = ""
        # Liquidity sweep of high (Short entry on reversal)
        if last_candle['High'] > recent_high and last_candle['Close'] < recent_high:
            direction = "Short"
        # Liquidity sweep of low (Long entry on reversal)
        elif last_candle['Low'] < recent_low and last_candle['Close'] > recent_low:
            direction = "Long"
            
        if direction:
            return TradePlan(
                asset=state.asset,
                direction=direction,
                entry=state.price,
                stop_loss=last_candle['High'] if direction == "Short" else last_candle['Low'],
                take_profit=[recent_low if direction == "Short" else recent_high],
                risk_score=0.9,
                reasoning=f"Liquidity Sweep detected at structural level."
            )
        return None

class SocialSentimentStrategy(BaseStrategy):
    """
    Generates signals based on aggregated social sentiment from professional traders.
    """
    def generate_plan(self, data: pd.DataFrame, state: MarketState) -> Optional[TradePlan]:
        from beta.core.social import SocialIntelligenceEngine
        sie = SocialIntelligenceEngine()
        sentiment = sie.get_aggregated_sentiment(state.asset)
        
        direction = ""
        if sentiment['score'] > 0.5:
            direction = "Long"
        elif sentiment['score'] < -0.5:
            direction = "Short"
            
        if direction:
            entry = state.price
            atr = (data['High'] - data['Low']).rolling(window=14).mean().iloc[-1]
            sl = entry - (atr * 2) if direction == "Long" else entry + (atr * 2)
            tp = entry + (atr * 4) if direction == "Long" else entry - (atr * 4)
            
            return TradePlan(
                asset=state.asset,
                direction=direction,
                entry=entry,
                stop_loss=sl,
                take_profit=[tp],
                risk_score=0.5, # Sentiment based trades have lower base confidence
                reasoning=f"Social Sentiment {sentiment['status']} (Score: {sentiment['score']:.2f}). {sentiment['top_signal']}"
            )
        return None
