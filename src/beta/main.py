import typer
import sys
import time
import json
import difflib
import numpy as np
import questionary
import shlex
from typing import List, Dict, Any, Optional
from datetime import datetime

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from prompt_toolkit.completion import WordCompleter

from beta.core.engine import MarketEngine, RegimeEngine, RiskEngine
from beta.core.social import SocialIntelligenceEngine
from beta.infrastructure.ui import InstitutionalUI, format_setup, CLIAnimations
from beta.agents.orchestrator import AgentOrchestrator

# --- SYSTEM INITIALIZATION ---
console = Console()
market_engine = MarketEngine()
regime_engine = RegimeEngine()
risk_engine = RiskEngine(initial_capital=100000.0)
sie = SocialIntelligenceEngine()
orchestrator = AgentOrchestrator()

app = typer.Typer(
    name="beta",
    help="BETA: Institutional-Grade Quantitative Intelligence Operating System.",
    add_completion=False,
    rich_markup_mode="rich"
)

# --- STRATEGY SUB-APP ---
strategy_app = typer.Typer(help="QUANTITATIVE STRATEGY WORKBENCH.")
app.add_typer(strategy_app, name="strategy")

# Ensure UTF-8 for Windows terminals
if sys.stdout.encoding != 'utf-8':
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass

def boot_sequence():
    """Professional System Boot Animation."""
    console.clear()
    with CLIAnimations.progress_track("INITIALIZING BETA CORE") as progress:
        task1 = progress.add_task("Loading Neural Layers...", total=100)
        task2 = progress.add_task("Connecting Global Telemetry...", total=100)
        task3 = progress.add_task("Authenticating Risk Engines...", total=100)
        while not progress.finished:
            progress.update(task1, advance=np.random.randint(5, 15))
            progress.update(task2, advance=np.random.randint(2, 10))
            progress.update(task3, advance=np.random.randint(10, 25))
            time.sleep(0.1)
    console.print(InstitutionalUI.banner())
    CLIAnimations.stream_text("[SYSTEM] Neural networks synchronized. Institutional gates open.\n", delay=0.02)

def print_banner():
    console.print(InstitutionalUI.banner())

def print_header(title: str):
    console.print(InstitutionalUI.section_header(title))

def print_error(error: str):
    msg = Text.assemble(("EXECUTION REJECTED: ", "bold red"), (error, "white"))
    console.print(Panel(msg, border_style="red", expand=False))

# --- CORE COMMANDS ---

@app.command()
def scan(json_mode: bool = typer.Option(False, "--json", help="Output machine-readable JSON.")):
    """GLOBAL MARKET SCANNER: High-density regime matrix and opportunity detection."""
    if not json_mode: print_header("Global Market Scan")
    assets = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "XAU/USD", "BTC/USD", "SPX", "NDX"]
    results = []
    table = InstitutionalUI.table("Market Regime Matrix", ["Asset", "Price", "Trend", "Vol", "Conf", "Status"])
    with CLIAnimations.progress_track("SCANNING GLOBAL MARKETS") as progress:
        task = progress.add_task("Ingesting Telemetry...", total=len(assets))
        for asset in assets:
            try:
                df = market_engine.fetch_data(asset)
                state = regime_engine.detect_regime(df)
                trend_style = "green" if state.trend == "Bullish" else "red" if state.trend == "Bearish" else "white"
                signal = "LONG" if state.trend == "Bullish" and state.regime_confidence > 0.8 else "SHORT" if state.trend == "Bearish" and state.regime_confidence > 0.8 else "Neutral"
                results.append({"asset": asset, "price": state.price, "regime": state.trend, "vol": state.volatility, "signal": signal})
                table.add_row(asset, f"{state.price:.4f}", f"[{trend_style}]{state.trend}[/]", state.volatility, f"{state.regime_confidence*100:.0f}%", signal)
                progress.update(task, advance=1, description=f"Processing {asset}...")
                time.sleep(0.1)
            except: continue
    if json_mode: InstitutionalUI.render_json(results)
    else: console.print(table)

@app.command()
def setup(
    asset: str = typer.Argument("EUR/USD", help="Asset to analyze."),
    risk_pct: float = typer.Option(1.0, "--risk", help="Risk percentage.")
):
    """INSTITUTIONAL TRADE SETUP: Statistical modeling of entry, exit, and risk parameters."""
    print_header(f"Institutional Trade Setup: {asset}")
    with CLIAnimations.pulse(f"Synthesizing statistical setup for {asset}"):
        df = market_engine.fetch_data(asset)
        state = regime_engine.detect_regime(df)
        plan = risk_engine.generate_setup(state, risk_pct=risk_pct)
        time.sleep(1.2)
    prices = df['Close'].tail(15).values
    console.print(InstitutionalUI.rendered_chart(prices, title=f"{asset} STRUCTURE EVOLUTION"))
    risk_meta = {"volatility": state.volatility, "confidence": plan.confidence, "rr": plan.risk_reward}
    entry_meta = {"limit": plan.entry, "breakout": plan.entry * 1.001}
    console.print(format_setup(asset, plan.type, f"{state.trend} / {state.volatility} Vol", entry_meta, plan.sl, plan.tp, risk_meta, lot_size=plan.position_size))

@app.command()
def fx(pair: str = typer.Argument("EUR/USD")):
    """DEEP INTELLIGENCE ANALYSIS: Alias for setup."""
    setup(asset=pair)

@app.command()
def dashboard():
    """OPERATIONAL COMMAND CENTER: Real-time multi-pane workstation."""
    layout = Layout()
    layout.split_column(Layout(name="header", size=4), Layout(name="body"), Layout(name="footer", size=3))
    layout["body"].split_row(Layout(name="watchlist", ratio=1), Layout(name="main", ratio=2), Layout(name="reasoning", ratio=1))
    layout["header"].update(InstitutionalUI.banner())
    with Live(layout, refresh_per_second=4, screen=True):
        while True:
            wl_table = InstitutionalUI.table("Watchlist", ["Asset", "Price", "Chg"])
            wl_table.add_row("EUR/USD", "1.0842", f"[{'green' if np.random.random() > 0.5 else 'red'}]+0.12%[/]")
            wl_table.add_row("BTC/USD", "64,242", "[green]+2.4%[/]")
            layout["watchlist"].update(Panel(wl_table, border_style="blue"))
            chart_prices = np.random.normal(1.08, 0.005, 15)
            layout["main"].update(InstitutionalUI.rendered_chart(chart_prices, title="LIVE TRADER STREAM"))
            reasoning = Text.assemble(("ANALYSIS:\n", "bold cyan"), ("Liquidity sweep at 1.0820.\n\n", "white"), ("INVALIDATION:\n", "bold red"), ("Close below 1.0785.", "white"))
            layout["reasoning"].update(Panel(reasoning, title="[bold magenta]AGENT REASONING[/]", border_style="magenta"))
            layout["footer"].update(Panel(Text(f"SYSTEM OPERATIONAL | LATENCY: {np.random.randint(8,15)}ms", style="dim green"), border_style="dim blue"))
            time.sleep(0.2)

@app.command()
def toy():
    """
    BETA-BOT 3000: Full High-Fidelity CLI Trader Toy.
    
    Launches an animated simulation of an autonomous trader bot.
    The bot physically climbs and falls based on simulated market noise.
    """
    offset = 5
    state = "IDLE"
    with Live(InstitutionalUI.render_toy_bot(state, offset), refresh_per_second=10, screen=True) as live:
        for _ in range(200):
            # Random walk logic for "climbing" and "falling"
            move = np.random.choice([-1, 0, 1], p=[0.3, 0.3, 0.4])
            offset = max(0, min(8, offset + move))
            
            # State transitions based on movement
            if move > 0: state = "BULLISH"
            elif move < 0: state = "BEARISH"
            else: state = "IDLE"
            
            # Occasional Panic
            if np.random.random() > 0.95: state = "PANIC"
            
            live.update(InstitutionalUI.render_toy_bot(state, offset))
            time.sleep(0.15)

@app.command()
def sentiment(ticker: str = typer.Argument("BTC/USD")):
    """SOCIAL INTELLIGENCE ENGINE: ML-driven sentiment aggregation."""
    print_header(f"Social Intelligence: {ticker}")
    with CLIAnimations.pulse("Aggregating multi-platform intelligence"):
        data = sie.get_aggregated_sentiment(ticker)
        time.sleep(1.0)
    table = InstitutionalUI.table("Sentiment Metrics", ["Metric", "Value"])
    table.add_row("Composite Score", f"{data['score']:.2f}")
    table.add_row("ML Confidence", f"[bold green]{data['ml_confidence']*100:.1f}%[/]")
    table.add_row("Signal Count", str(data['signal_count']))
    table.add_row("Recommendation", f"[bold]{data['status']}[/bold]")
    console.print(table)
    CLIAnimations.stream_text(f"\n[bold magenta][!] TOP SIGNAL:[/bold magenta] {data['top_signal']}", delay=0.01)

# --- INTERACTIVE SHELL ---
def interactive_shell():
    all_cmds = ["scan", "fx", "setup", "dashboard", "analyze", "sentiment", "strategy", "toy", "help", "exit", "quit", "clear"]
    completer = WordCompleter(all_cmds, ignore_case=True)
    boot_sequence()
    while True:
        try:
            cmd_line = questionary.text("BETA>", instruction="(TAB for autocomplete)", completer=completer).ask()
            if not cmd_line: continue
            if cmd_line.lower() in ["exit", "quit"]: break
            if cmd_line.lower() == "clear":
                console.clear()
                print_banner()
                continue
            args = shlex.split(cmd_line)
            app(args)
        except SystemExit: pass
        except Exception as e: print_error(str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1: app()
    else: interactive_shell()
