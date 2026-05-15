import requests
import json
from typing import List, Dict, Any
from pydantic import BaseModel
import time

class SocialSignal(BaseModel):
    platform: str
    author: str
    ticker: str
    sentiment: float # -1 to 1
    content: str
    timestamp: float

class SocialIntelligenceEngine:
    def __init__(self):
        self.sources = ["Reddit", "Twitter/X", "Telegram-VIP", "Discord-Institutional"]
        self.ml_confidence_threshold = 0.85

    def fetch_reddit_signals(self, ticker: str) -> List[SocialSignal]:
        """
        Simulates fetching signals from professional subreddits like r/Investing, r/Trading.
        """
        signals = [
            SocialSignal(
                platform="Reddit",
                author="ProTrader_Alpha",
                ticker=ticker,
                sentiment=0.8,
                content=f"Strong bullish divergence on {ticker} daily chart. RSI oversold and institutional buying detected in dark pools.",
                timestamp=time.time() - 3600
            ),
            SocialSignal(
                platform="Reddit",
                author="MacroAnalyst_99",
                ticker=ticker,
                sentiment=-0.3,
                content=f"{ticker} facing headwinds from macro rotation. Better entries likely below current support.",
                timestamp=time.time() - 7200
            )
        ]
        return signals

    def fetch_telegram_signals(self, ticker: str) -> List[SocialSignal]:
        """Mocking encrypted VIP Telegram signals from top-tier analysts."""
        return [
            SocialSignal(
                platform="Telegram",
                author="Alpha_Elite_Group",
                ticker=ticker,
                sentiment=0.85,
                content=f"VIP INSIGHT: {ticker} whale accumulation detected at current VWAP. Target +120 pips.",
                timestamp=time.time() - 900
            )
        ]

    def fetch_discord_signals(self, ticker: str) -> List[SocialSignal]:
        """Mocking institutional Discord server intelligence."""
        return [
            SocialSignal(
                platform="Discord",
                author="Quant_Vault_Sec",
                ticker=ticker,
                sentiment=0.75,
                content=f"Structural breakout confirmed on {ticker}. ML models projecting 88% probability of trend continuation.",
                timestamp=time.time() - 450
            )
        ]

    def classify_signal_ml(self, content: str) -> float:
        """Mocking a BERT-based financial NLP classifier for signal confidence."""
        if "whale" in content.lower() or "institutional" in content.lower():
            return 0.92
        return 0.75

    def fetch_pro_signals(self, ticker: str) -> List[SocialSignal]:
        """
        Simulates fetching from professional trader feeds/APIs.
        """
        signals = [
            SocialSignal(
                platform="ProFeed",
                author="Institutional_Signals",
                ticker=ticker,
                sentiment=0.9,
                content=f"ORDER FLOW ALERT: Large buy orders hitting the tape for {ticker} at key psychological level.",
                timestamp=time.time() - 1800
            )
        ]
        return signals

    def get_aggregated_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Aggregates signals from all sources using ML-weighted scoring.
        """
        reddit = self.fetch_reddit_signals(ticker)
        pro = self.fetch_pro_signals(ticker)
        telegram = self.fetch_telegram_signals(ticker)
        discord = self.fetch_discord_signals(ticker)
        
        all_signals = reddit + pro + telegram + discord
        if not all_signals:
            return {"score": 0.0, "signal_count": 0, "status": "Neutral", "ml_confidence": 0.0}
            
        weighted_sum = sum(s.sentiment * self.classify_signal_ml(s.content) for s in all_signals)
        total_weight = sum(self.classify_signal_ml(s.content) for s in all_signals)
        avg_sentiment = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        status = "Strong Buy" if avg_sentiment > 0.6 else \
                 "Buy" if avg_sentiment > 0.2 else \
                 "Strong Sell" if avg_sentiment < -0.6 else \
                 "Sell" if avg_sentiment < -0.2 else "Hold"
                 
        return {
            "score": avg_sentiment,
            "signal_count": len(all_signals),
            "status": status,
            "top_signal": all_signals[0].content,
            "ml_confidence": sum(self.classify_signal_ml(s.content) for s in all_signals) / len(all_signals)
        }
