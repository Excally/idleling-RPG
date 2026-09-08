import os
import re
import sys
import time

from .constants import RESET

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def visible_length(value):
    return len(ANSI_RE.sub("", str(value)))


def terminal_width(default=100):
    try:
        return max(60, os.get_terminal_size().columns)
    except OSError:
        return default


def fit_text(value, width):
    value = str(value)
    if visible_length(value) <= width:
        return value
    if width <= 3:
        return ANSI_RE.sub("", value)[:width]
    return ANSI_RE.sub("", value)[:width - 3] + "..."


def print_table(headers, rows, widths=None):
    if widths is None:
        available = terminal_width() - (len(headers) * 3) - 1
        widths = [max(8, min(28, available // len(headers))) for _ in headers]
    widths = list(widths)
    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def row(values):
        cells = [fit_text(value, width) for value, width in zip(values, widths)]
        padded = [cell + " " * max(0, width - visible_length(cell)) for cell, width in zip(cells, widths)]
        return "| " + " | ".join(padded) + " |"

    print(separator)
    print(row(headers))
    print(separator)
    for values in rows:
        print(row(values))
    print(separator)


def marquee(text, width=70, delay=None, cycles=1):
    text = str(text)
    if len(text) <= width:
        print(text)
        return
    delay = delay if delay is not None else min(0.12, max(0.03, 2.5 / len(text)))
    padded = " " * width + text + " " * width
    positions = list(range(0, len(text) + width, 2))
    positions += list(range(len(text) + width, 0, -2))
    for _ in range(cycles):
        for position in positions:
            visible = padded[position:position + width]
            sys.stdout.write("\r" + visible[:width])
            sys.stdout.flush()
            time.sleep(delay)
    print("\r" + fit_text(text, width) + " " * max(0, width - len(text)))


def show_detail(title, lines):
    print(f"\n--- {title.upper()} ---")
    for line in lines:
        marquee(line, width=min(terminal_width() - 4, 88))
