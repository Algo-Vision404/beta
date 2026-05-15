import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class MemorySystem:
    def __init__(self, db_path: str = "beta_memory.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Trade history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    asset TEXT,
                    direction TEXT,
                    entry REAL,
                    sl REAL,
                    tp TEXT,
                    outcome REAL,
                    regime TEXT
                )
            """)
            # Strategy performance
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS strategy_stats (
                    strategy_id TEXT PRIMARY KEY,
                    win_rate REAL,
                    total_trades INTEGER,
                    last_updated TEXT
                )
            """)
            conn.commit()

    def log_trade(self, trade_data: Dict[str, Any]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trades (timestamp, asset, direction, entry, sl, tp, outcome, regime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                trade_data['asset'],
                trade_data['direction'],
                trade_data['entry'],
                trade_data['sl'],
                json.dumps(trade_data['tp']),
                trade_data.get('outcome', 0),
                trade_data['regime']
            ))
            conn.commit()

    def get_trades(self, limit: int = 10) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def update_strategy_stats(self, strategy_id: str, win_rate: float, total_trades: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO strategy_stats (strategy_id, win_rate, total_trades, last_updated)
                VALUES (?, ?, ?, ?)
            """, (strategy_id, win_rate, total_trades, datetime.now().isoformat()))
            conn.commit()

    def get_strategy_lineage(self, strategy_id: str) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM strategy_stats WHERE strategy_id = ?", (strategy_id,))
            return [dict(row) for row in cursor.fetchall()]
