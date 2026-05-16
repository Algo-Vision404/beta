from typing import Dict, Any, List, Optional
import logging
from pydantic import BaseModel

logger = logging.getLogger("FinalAuthority")

class AuthorityLimits(BaseModel):
    max_risk_pct: float = 2.0
    min_rr_ratio: float = 1.5
    min_confidence: float = 0.7
    allowed_regimes: List[str] = ["Bullish", "Bearish"]

class FinalAuthority:
    """
    Institutional circuit breaker for trade execution.
    Validates proposed trade plans against hard safety limits.
    """
    
    def __init__(self, limits: Optional[AuthorityLimits] = None):
        self.limits = limits or AuthorityLimits()

    def validate_setup(self, plan: Any, regime_state: Any) -> Dict[str, Any]:
        """
        Adjudicates a trade setup and returns an authorization decision.
        """
        rejections = []
        
        # 1. Check Risk Percentage
        if plan.risk_pct > self.limits.max_risk_pct:
            rejections.append(f"Risk {plan.risk_pct}% exceeds institutional limit of {self.limits.max_risk_pct}%")
            
        # 2. Check Risk:Reward Ratio
        if plan.risk_reward < self.limits.min_rr_ratio:
            rejections.append(f"R:R Ratio {plan.risk_reward:.2f} is below minimum requirement of {self.limits.min_rr_ratio}")
            
        # 3. Check Regime Consistency
        if regime_state.trend not in self.limits.allowed_regimes:
            rejections.append(f"Regime '{regime_state.trend}' is not authorized for execution")
            
        # 4. Check Conviction/Confidence
        if plan.confidence < self.limits.min_confidence:
            rejections.append(f"Conviction {plan.confidence:.2%2f} is below institutional threshold")

        authorized = len(rejections) == 0
        
        return {
            "authorized": authorized,
            "rejections": rejections,
            "timestamp": regime_state.timestamp if hasattr(regime_state, 'timestamp') else None,
            "authority_signature": "BETA-AUTH-GATE-01"
        }
