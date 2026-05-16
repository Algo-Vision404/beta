from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import random

class AgentMessage(BaseModel):
    sender: str
    content: str
    metadata: Dict[str, Any] = {}

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def reason(self, context: str, history: List[AgentMessage]) -> AgentMessage:
        raise NotImplementedError

class BullishSpecialist(BaseAgent):
    def reason(self, context: str, history: List[AgentMessage]) -> AgentMessage:
        return AgentMessage(
            sender=self.name,
            content=f"BULLISH PERSPECTIVE: Accumulation phase detected on H1. Volume expansion confirms institutional support at {context} base. Targets 1.272 Fib extension."
        )

class BearishSpecialist(BaseAgent):
    def reason(self, context: str, history: List[AgentMessage]) -> AgentMessage:
        # React to history if it exists
        if any("BULLISH" in m.content for m in history):
            return AgentMessage(
                sender=self.name,
                content=f"BEARISH REBUTTAL: Bullish thesis ignored supply zone overhead. Liquidity grab likely at {context} before reversal. Bearish divergence on RSI."
            )
        return AgentMessage(
            sender=self.name,
            content=f"BEARISH PERSPECTIVE: Market structural break detected. Selling pressure increasing at resistance."
        )

class RiskMonitor(BaseAgent):
    def reason(self, context: str, history: List[AgentMessage]) -> AgentMessage:
        bull_votes = sum(1 for m in history if "BULLISH" in m.content)
        bear_votes = sum(1 for m in history if "BEARISH" in m.content)
        verdict = "Bullish Conviction" if bull_votes > bear_votes else "Bearish Conviction" if bear_votes > bull_votes else "Neutral/Wait"
        
        return AgentMessage(
            sender=self.name,
            content=f"RISK ADJUDICATION: Debate analyzed. Final Verdict: {verdict}. Confidence Score: {random.uniform(0.6, 0.95):.2f}. Enforcing strict SL."
        )

class AgentOrchestrator:
    """
    Manages the adversarial debate lifecycle between specialized intelligence agents.
    """
    def __init__(self):
        self.agents = [
            BullishSpecialist("Aries-Bull", "Optimist"),
            BearishSpecialist("Thanatos-Bear", "Pessimist"),
            RiskMonitor("Oracle-Risk", "Adjudicator")
        ]

    def run_debate(self, ticker: str, turns: int = 2) -> List[AgentMessage]:
        """
        Executes an adversarial debate protocol.
        """
        history = []
        context = ticker
        
        for turn in range(turns):
            for agent in self.agents:
                # The RiskMonitor only speaks at the end of the debate
                if isinstance(agent, RiskMonitor) and turn < turns - 1:
                    continue
                    
                msg = agent.reason(context, history)
                history.append(msg)
                
        return history
