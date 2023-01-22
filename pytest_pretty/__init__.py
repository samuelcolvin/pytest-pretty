from __future__ import annotations as _annotations

import sys
from time import perf_counter_ns
from typing import TYPE_CHECKING

import pytest
from _pytest.terminal import TerminalReporter
from rich.console import Console
from rich.markup import escape
from rich.table import Table

if TYPE_CHECKING:
    from _pytest.reports import TestReport

    SummaryStats = tuple[list[tuple[str, dict[str, bool]]], str]

__version__ = '1'
start_time = 0
end_time = 0
console = Console()


def pytest_sessionstart(session):
    global start_time
    start_time = perf_counter_ns()


def pytest_sessionfinish(session, exitstatus):
    global end_time
    end_time = perf_counter_ns()


class CustomTerminalReporter(TerminalReporter):
    def pytest_runtest_logreport(self, report: TestReport) -> None:
        super().pytest_runtest_logreport(report)
        if report.failed:
            file, line, func = report.location
            self._write_progress_information_filling_space()
            self.ensure_newline()
            summary = f'{file}:{line} {func}'
            self._tw.write(summary, red=True)
            try:
                msg = report.longrepr.reprcrash.message
            except AttributeError:
                pass
            else:
                msg = msg.replace('\n', ' ')
                available_space = self._tw.fullwidth - len(summary) - 15
                if available_space > 5:
                    self._tw.write(f' - {msg[:available_space]}…')

    def summary_stats(self) -> None:
        time_taken_ns = end_time - start_time
        summary_items, _ = self.build_summary_stats_line()
        console.print(f'[bold]Results ({time_taken_ns / 1_000_000_000:0.2f}s):[/]', highlight=False)
        for summary_item in summary_items:
            msg, text_format = summary_item
            text_format.pop('bold', None)
            color = next(k for k, v in text_format.items() if v)
            count, label = msg.split(' ', 1)
            console.print(f'{count:>10} {label}', style=color)

    def short_test_summary(self) -> None:
        summary_items, _ = self.build_summary_stats_line()
        fail_reports = self.stats.get('failed', [])
        if fail_reports:
            table = Table(title='Summary of Failures', padding=(0, 2), border_style='cyan')
            table.add_column('File')
            table.add_column('Function', style='bold')
            table.add_column('Function Line', style='bold')
            table.add_column('Error Line')
            table.add_column('Error')
            for report in fail_reports:
                file, function_line, func = report.location
                try:
                    repr_entries = report.longrepr.chain[-1][0].reprentries
                except AttributeError:
                    error_line = ''
                    error = ''
                else:
                    error_line = str(repr_entries[0].reprfileloc.lineno)
                    error = repr_entries[-1].reprfileloc.message
                table.add_row(
                    escape(file),
                    escape(func),
                    str(function_line + 1),
                    escape(error_line),
                    escape(error),
                )
            console.print(table)


@pytest.mark.trylast
def pytest_configure(config):
    # Get the standard terminal reporter plugin and replace it with our
    standard_reporter = config.pluginmanager.getplugin('terminalreporter')
    custom_reporter = CustomTerminalReporter(config, sys.stdout)
    config.pluginmanager.unregister(standard_reporter)
    config.pluginmanager.register(custom_reporter, 'terminalreporter')
