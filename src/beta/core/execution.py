from typing import Dict, Any, Optional
from beta.core.engine import TradePlan

class ExecutionEngine:
    def __init__(self, mode: str = "paper"):
        self.mode = mode

    def execute_trade(self, plan: TradePlan) -> Dict[str, Any]:
        """
        Execute a trade via broker API.
        """
        if self.mode == "paper":
            return self._execute_paper(plan)
        else:
            return self._execute_oanda(plan)

    def _execute_paper(self, plan: TradePlan) -> Dict[str, Any]:
        return {
            "status": "Success",
            "order_id": "PAPER-12345",
            "filled_price": plan.entry,
            "units": 1000,
            "message": "Paper trade executed successfully"
        }

    def _execute_oanda(self, plan: TradePlan) -> Dict[str, Any]:
        # Placeholder for real OANDA API calls
        return {
            "status": "Pending",
            "message": "OANDA API integration required (set API keys in .env)"
        }
