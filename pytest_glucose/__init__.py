from __future__ import annotations as _annotations

from typing import TYPE_CHECKING

from functools import partial
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.terminal import TerminalReport
    from _pytest.reports import TestReport

    SummaryStats = tuple[list[tuple[str, dict[str, bool]]], str]

__version__ = '0.0.1'


def pytest_terminal_summary(terminalreporter: TerminalReport, exitstatus: int, config: Config) -> None:
    terminalreporter.short_test_summary = lambda: None
    summary_stats: SummaryStats = terminalreporter.build_summary_stats_line()
    terminalreporter.summary_stats = partial(print_summary, summary_stats, terminalreporter.stats)


def print_summary(summary_stats: SummaryStats, stats: dict[str, list[TestReport]]) -> None:
    summary_items, _ = summary_stats
    console = Console()
    console.print('[bold]Results:[/]')
    for summary_item in summary_items:
        msg, text_format = summary_item
        text_format.pop('bold', None)
        color = next(k for k, v in text_format.items() if v)
        count, label = msg.split(' ', 1)
        console.print(f'{count:>10} {label}', style=color)
    fail_reports = stats.get('failed', [])
    if fail_reports:
        table = Table(padding=(0, 2), border_style='cyan')
        table.add_column('File')
        table.add_column('Function', style='bold')
        table.add_column('Function Line', style='bold')
        table.add_column('Error Line')
        table.add_column('Error')
        for report in fail_reports:
            file, function_line, func = report.location
            repr_entries = report.longrepr.chain[-1][0].reprentries
            table.add_row(
                file,
                func,
                str(function_line + 1),
                str(repr_entries[0].reprfileloc.lineno),
                repr_entries[-1].reprfileloc.message,
            )
        console.print(table)
