from __future__ import annotations as _annotations

from functools import partial
from time import perf_counter_ns
from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.terminal import TerminalReport
    from _pytest.reports import TestReport

    SummaryStats = tuple[list[tuple[str, dict[str, bool]]], str]

__version__ = '0.0.1'
start_time = 0


def pytest_sessionstart(session):
    global start_time
    start_time = perf_counter_ns()


def pytest_terminal_summary(terminalreporter: TerminalReport, exitstatus: int, config: Config) -> None:
    terminalreporter.short_test_summary = lambda: None
    time_taken_ns = perf_counter_ns() - start_time
    summary_stats: SummaryStats = terminalreporter.build_summary_stats_line()
    terminalreporter.summary_stats = partial(print_summary, summary_stats, terminalreporter.stats, time_taken_ns)


def print_summary(summary_stats: SummaryStats, stats: dict[str, list[TestReport]], time_taken_ns: int) -> None:
    summary_items, _ = summary_stats
    console = Console()
    fail_reports = stats.get('failed', [])
    if fail_reports:
        table = Table(title='Summary of Failures', padding=(0, 2), border_style='cyan')
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
    console.print(f'[bold]Results ({time_taken_ns / 1_000_000_000:0.2f}s):[/]')
    for summary_item in summary_items:
        msg, text_format = summary_item
        text_format.pop('bold', None)
        color = next(k for k, v in text_format.items() if v)
        count, label = msg.split(' ', 1)
        console.print(f'{count:>10} {label}', style=color)
