# BETA: Institutional Quantitative Intelligence OS

BETA is a high-performance, autonomous multi-asset quantitative intelligence operating system designed for terminal-based financial research, risk management, and strategy execution. It bridges the gap between raw market telemetry and actionable institutional trade planning.

---

## Core Platform Features

### Institutional Execution Suite
- **RiskEngine**: Automated position sizing based on fractional capital risk (e.g., 1% risk/trade) and current account balance.
- **Statistical Modeling**: Volatility-adjusted **ATR-based Stop Losses** and **Multi-Tier Take Profit** levels.
- **High-Fidelity Tickets**: Synthesis of complete trade tickets including Lot Sizing, Entry Strategy (Limit/Breakout), and real-time R:R Ratio validation.

### Advanced Quantitative Visuals
- **Tracer Charts**: Institutional ASCII charts featuring dashed historical trails and real-time structural mapping.
- **Volatility Heatmaps**: Cross-asset risk intensity matrices to identify market-wide stress.
- **Correlation Matrices**: Statistical coupling detection across FX, Commodities, and Crypto.

### Social Intelligence Engine
- **ML-Driven Sentiment**: BERT-based classification of signals from Reddit, Discord, Telegram, and Professional feeds.
- **Institutional Weighting**: Advanced signal filtering to prioritize "Whale" activity and institutional bias over retail sentiment.

### Beta-Bot 3000 (Full CLI Toy)
- **Autonomous Simulation**: A dedicated, animated trader bot that physically climbs and falls based on simulated market noise.
- **Emotive States**: Real-time bot reactions (BULLISH, BEARISH, PANIC) providing a creative soul to the quantitative workspace.

---

## Command Center Reference

Launch the interactive command center:
```bash
python src/beta/main.py
```

### Intelligence Commands
| Command | Feature | Output |
| :--- | :--- | :--- |
| `scan` | Global Market Scanner | Multi-asset regime matrix & opportunity scan. |
| `setup` | Institutional Ticket | Statistical Entry/SL/TP & Lot Sizing. |
| `dashboard` | Command Center | Real-time multi-pane operational workstation. |
| `analyze` | Quant Suite | Volatility Heatmaps & Correlation Matrices. |
| `sentiment` | Social Intel | ML-weighted institutional sentiment aggregation. |
| `toy` | Beta-Bot 3000 | Animated autonomous trader bot simulation. |

---

## System Architecture

- **Regime Engine**: HMM-based (Hidden Markov Model) market regime detection (Bullish/Bearish/Sideways).
- **Machine Readable**: All core commands support `--json` output for automated backtesting and CI/CD integration.
- **Agentic Orchestrator**: Multi-agent debate loops for adversarial evaluation of trade signals.
- **Cyber-Minimalist UI**: High-density information display using `Rich` and `Typer`, optimized for keyboard-first operation.

## Requirements

- **Python**: 3.9+
- **Key Dependencies**: `rich`, `typer`, `prompt_toolkit`, `pandas`, `numpy`, `scikit-learn`, `pydantic`.

---
*BETA: Precise. Professional. Autonomous.*
