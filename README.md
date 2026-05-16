# BETA: Institutional Quantitative Intelligence OS

[![Architecture](https://img.shields.io/badge/Architecture-Institutional--Grade-blueviolet)](#system-architecture)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)

> **Autonomous Multi-Asset Intelligence for Terminal-First Financial Research.**

BETA is a high-performance quantitative operating system designed for terminal-based financial research, risk management, and strategy execution. It bridges the gap between raw market telemetry and actionable institutional trade planning through an adversarial multi-agent architecture.

---

## Core Platform Features

### Institutional Execution Suite
- **RiskEngine**: Automated position sizing based on fractional capital risk and current account balance.
- **Statistical Modeling**: Volatility-adjusted ATR-based Stop Losses and Multi-Tier Take Profit levels.
- **High-Fidelity Tickets**: Synthesis of complete trade tickets including Lot Sizing, Entry Strategy, and real-time R:R Ratio validation.

### Advanced Quantitative Visuals
- **Tracer Charts**: Institutional ASCII charts featuring dashed historical trails and real-time structural mapping.
- **Volatility Heatmaps**: Cross-asset risk intensity matrices to identify market-wide stress.
- **Correlation Matrices**: Statistical coupling detection across FX, Commodities, and Crypto.

### Social Intelligence Engine
- **ML-Driven Sentiment**: BERT-based classification of signals from Reddit, Discord, Telegram, and Professional feeds.
- **Institutional Weighting**: Advanced signal filtering to prioritize "Whale" activity and institutional bias.

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

---

## System Architecture

BETA is designed as a modular, event-driven ecosystem where intelligence agents, market engines, and risk authorities interact.

### High-Level Design

```mermaid
graph TD
    A[Market Data Ingestion] --> B[Regime Engine]
    B --> C[Neural Pattern Recognition]
    
    subgraph "Agentic Intelligence Layer"
        C --> D[Agent Orchestrator]
        D --> D1[Bullish Specialist]
        D --> D2[Bearish Specialist]
        D --> D3[Risk Monitor]
        D1 & D2 & D3 --> E[Adversarial Debate Protocol]
    end
    
    E --> F[Final Authority Engine]
    F --> G[Execution Ready Ticket]
    
    subgraph "Observability Layer"
        H[Institutional UI]
        I[Command Center Dashboard]
        J[Social Intel Engine]
    end
    
    G -.-> H
    J -.-> D
```

### Core Components

#### 1. The Adversarial Agent Layer
- **Orchestrator**: Manages the lifecycle of specialized sub-agents.
- **Debate Protocol**: A multi-turn reasoning process where agents present conflicting evidence (Bullish vs. Bearish) and a "Risk Monitor" agent adjudicates the final conviction score.

#### 2. Risk & Authority Engine
- **Fractional Risk Model**: Automatically calculates position sizing based on account equity and ATR-adjusted stop losses.
- **Final Authority (Circuit Breaker)**: A hard-coded logic layer that rejects any trade setup exceeding institutional parameters.

#### 3. Observability Suite
- **Cyber-Minimalist CLI**: A high-density information display optimized for low-latency system management.
- **Neural Stream**: Real-time logging of agent reasoning processes.

---

"Standardizing the chaos of market data."
