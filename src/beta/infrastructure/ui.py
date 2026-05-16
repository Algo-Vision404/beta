from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from datetime import datetime
import json
import numpy as np
import sys
import time
from typing import Any, Dict, List, Optional

# --- PROFESSIONAL COLOR SYSTEM ---
C_PROFIT = "bold green"
C_BULLISH = "green"
C_LOSS = "bold red"
C_BEARISH = "red"
C_RISK = "bold red"
C_WARNING = "bold yellow"
C_VOLATILE = "yellow"
C_INFO = "cyan"
C_ANALYTICS = "blue"
C_METADATA = "dim white"
C_BG = "black"

console = Console()

class InstitutionalUI:
    @staticmethod
    def banner() -> RenderableType:
        now = datetime.now().strftime("%H:%M:%S")
        logo_ascii = """
[bold blue]██████╗ ███████╗████████╗ █████╗ [/bold blue]
[bold blue]██╔══██╗██╔════╝╚══██╔══╝██╔══██╗[/bold blue]
[bold cyan]██████╔╝█████╗     ██║   ███████║[/bold cyan]
[bold cyan]██╔══██╗██╔══╝     ██║   ██╔══██║[/bold cyan]
[bold white]██████╔╝███████╗   ██║   ██║  ██║[/bold white]
[bold white]╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝[/bold white]
"""
        logo_text = Text.assemble(
            ("\n B E T A   Q U A N T I T A T I V E   I N T E L L I G E N C E\n", "bold white"),
            ("─" * 60, "dim blue")
        )
        header_table = Table.grid(expand=True)
        header_table.add_column(justify="left")
        header_table.add_column(justify="right")
        header_table.add_row(
            Text.assemble(
                (" SYSTEM: ", C_METADATA), ("BETA v1.0", "bold white"),
                (" | MODE: ", C_METADATA), ("PAPER", "bold yellow"),
                (" | STATUS: ", C_METADATA), ("CONNECTED", "green")
            ),
            Text(f"T: {now}", style=C_METADATA)
        )
        stats_table = Table.grid(expand=True)
        stats_table.add_column(justify="left")
        stats_table.add_row(
            Text.assemble(
                (" REGIME: ", C_METADATA), ("RISK-OFF", "bold red"),
                (" | ", C_METADATA), ("VOL: ", C_METADATA), ("HIGH", "bold yellow"),
                (" | ", C_METADATA), ("STRATEGIES: ", C_METADATA), ("14", "bold cyan"),
                (" | ", C_METADATA), ("LATENCY: ", C_METADATA), ("12ms", "green"),
                (" | ", C_METADATA), ("PnL: ", C_METADATA), ("+$1,242.10", "bold green")
            )
        )
        main_content = Table.grid(expand=True)
        main_content.add_row(logo_ascii)
        main_content.add_row(logo_text)
        main_content.add_row(header_table)
        main_content.add_row(stats_table)
        return Panel(main_content, box=box.HEAVY_EDGE, border_style="blue", padding=(0, 1))

    @staticmethod
    def table(title: str, columns: List[str]) -> Table:
        table = Table(
            title=Text(title.upper(), style="bold white"),
            box=box.SIMPLE_HEAD,
            header_style="bold blue",
            border_style="dim blue",
            show_edge=False,
            collapse_padding=True
        )
        table.title_align = "left"
        for col in columns: table.add_column(col)
        return table

    @staticmethod
    def section_header(title: str) -> RenderableType:
        return Text.assemble(
            ("\n[ ", "dim blue"),
            (title.upper(), "bold white"),
            (" ]", "dim blue"),
            (" " + "─" * (console.width - len(title) - 10), "dim blue")
        )

    @staticmethod
    def render_json(data: Any):
        print(json.dumps(data, indent=2, default=str))

    @staticmethod
    def heatmap(data: Dict[str, float], title: str = "VOLATILITY HEATMAP") -> RenderableType:
        grid = Table.grid(padding=1)
        for i in range(4): grid.add_column()
        items = list(data.items())
        for i in range(0, len(items), 4):
            row = []
            for j in range(4):
                if i + j < len(items):
                    asset, val = items[i+j]
                    color = "red" if val > 0.8 else "yellow" if val > 0.5 else "green"
                    row.append(Panel(Text(f"{asset}\n{val*100:.0f}%", justify="center", style="bold white"), border_style=color, width=15))
                else: row.append("")
            grid.add_row(*row)
        return Panel(grid, title=f"[bold white]{title}[/]", border_style="blue", expand=False)

    @staticmethod
    def correlation_matrix(assets: List[str], matrix: np.ndarray) -> Table:
        table = Table(title="CORRELATION MATRIX", box=box.SIMPLE_HEAD, border_style="dim blue")
        table.add_column("Asset", style="bold cyan")
        for asset in assets: table.add_column(asset, justify="right")
        for i, asset in enumerate(assets):
            row = [asset]
            for j, val in enumerate(matrix[i]):
                color = "green" if val > 0.7 else "red" if val < -0.7 else "white"
                row.append(f"[{color}]{val:.2f}[/]")
            table.add_row(*row)
        return table

    @staticmethod
    def rendered_chart(prices: np.ndarray, title: str = "PRICE STRUCTURE") -> Panel:
        chart = Text()
        max_p = max(prices)
        min_p = min(prices)
        range_p = max_p - min_p + 1e-9
        norm_prices = (prices - min_p) / range_p
        for i, val in enumerate(norm_prices):
            bar_len = int(val * 40)
            is_last = i == len(norm_prices) - 1
            line = Text()
            line.append(f" {i:02d} ", style="dim white")
            if is_last:
                diff = prices[i] - prices[i-1] if i > 0 else 0
                color = "bold green" if diff > 0 else "bold red" if diff < 0 else "bold cyan"
                status = "ASCENDING" if diff > 0 else "DESCENDING" if diff < 0 else "STABLE"
                line.append("█" * bar_len, style=color)
                line.append(f" [{status}]", style=color)
                line.append("  -- SYSTEM TRACK", style="bold white")
            else:
                line.append("█" * bar_len, style="dim blue")
                line.append(" |", style="dim blue")
            chart.append(line)
            chart.append("\n")
        return Panel(chart, title=f"[bold white]{title}[/]", border_style="blue", padding=(0, 1))

    @staticmethod
    def render_debate(history: List[Any]) -> Panel:
        """Renders an adversarial agent debate."""
        debate_text = Text()
        for msg in history:
            role_color = "bold green" if "BULLISH" in msg.content else "bold red" if "BEARISH" in msg.content else "bold magenta"
            debate_text.append(f"\n{msg.sender.upper()} [{msg.role.upper()}]:\n", style=role_color)
            debate_text.append(f"{msg.content}\n", style="white")
        return Panel(debate_text, title="[bold cyan]ADVERSARIAL AGENT DEBATE[/]", border_style="blue")

    @staticmethod
    def render_authority_report(report: Dict[str, Any]) -> Panel:
        """Renders the Final Authority validation report."""
        status_color = "bold green" if report['authorized'] else "bold red"
        status_text = "AUTHORIZED" if report['authorized'] else "REJECTED"
        
        content = Text()
        content.append(f"EXECUTION STATUS: ", style="bold white")
        content.append(f"{status_text}\n\n", style=status_color)
        
        if not report['authorized']:
            content.append("REJECTION REASONS:\n", style="bold red")
            for reason in report['rejections']:
                content.append(f" - {reason}\n", style="white")
        else:
            content.append("Institutional clearance granted. Security signature valid.\n", style="dim white")
            
        content.append(f"\nSIGNATURE: {report['authority_signature']}", style="dim cyan")
        
        return Panel(content, title="[bold blue]FINAL AUTHORITY REPORT[/bold blue]", border_style=status_color if not report['authorized'] else "blue", expand=False)

class CLIAnimations:
    @staticmethod
    def pulse(message: str):
        return console.status(f"[bold blue]-[/] [white]{message}...[/]", spinner="dots")

    @staticmethod
    def progress_track(title: str):
        return Progress(SpinnerColumn(spinner_name="dots", style="bold blue"), TextColumn("[bold white]{task.description}"), BarColumn(bar_width=40, style="dim blue", complete_style="bold blue"), TaskProgressColumn(), TimeElapsedColumn(), console=console, transient=True)

    @staticmethod
    def stream_text(text: str, delay: float = 0.01):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def format_setup(pair: str, setup_type: str, regime: str, entry: Dict, sl: float, tp: List[float], risk: Dict, lot_size: float = 0.0):
    content = Text()
    content.append("PAIR:   ", style=C_METADATA)
    content.append(f"{pair}\n", style="bold white")
    content.append("SETUP:  ", style=C_METADATA)
    content.append(f"{setup_type}\n", style="bold cyan")
    content.append("REGIME: ", style=C_METADATA)
    content.append(f"{regime}\n\n", style="bold magenta")
    content.append("ENTRY:\n", style="bold blue")
    content.append("  Limit:    ", style=C_METADATA)
    content.append(f"{entry.get('limit', 0):.4f}\n", style="green")
    content.append("  Breakout: ", style=C_METADATA)
    content.append(f"{entry.get('breakout', 0):.4f}\n\n", style="bold green")
    content.append("STOP LOSS:\n", style="bold red")
    content.append("  Hard SL:  ", style=C_METADATA)
    content.append(f"{sl:.4f}\n\n", style=C_LOSS)
    content.append("TAKE PROFIT:\n", style="bold green")
    for i, val in enumerate(tp):
        content.append(f"  TP{i+1}:      ", style=C_METADATA)
        content.append(f"{val:.4f}\n", style="bold white")
    content.append("\nRISK PROFILE:\n", style="bold yellow")
    content.append("  LOT SIZE:   ", style="bold white")
    content.append(f"{lot_size:.2f} Standard Lots\n", style="bold green")
    content.append("  Volatility: ", style=C_METADATA)
    content.append(f"{risk['volatility']}\n", style="yellow")
    content.append("  Confidence: ", style=C_METADATA)
    content.append(f"{risk['confidence']*100:.0f}%\n", style="bold cyan")
    content.append("  R:R Ratio:  ", style=C_METADATA)
    content.append(f"1:{risk['rr']:.1f}", style="bold green")
    return Panel(content, title="[bold blue]INSTITUTIONAL TRADE SETUP[/bold blue]", border_style="blue", expand=False)
