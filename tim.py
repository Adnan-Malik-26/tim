#!/usr/bin/env python3
import os
import sqlite3
from datetime import datetime, timedelta, date, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich.prompt import Prompt
from rich.layout import Layout
from rich.align import Align
from rich import box
import typer
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
import calendar

app = typer.Typer()
console = Console()

# Catppuccin Mocha palette (hex codes)
CATPPUCCIN = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay1": "#7f849c",
    "overlay0": "#6c7086",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
}

DB_PATH = os.path.expanduser("~/.tim.db")


# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, name TEXT UNIQUE)"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                tag_id INTEGER,
                start TEXT,
                end TEXT,
                FOREIGN KEY(tag_id) REFERENCES tags(id))"""
    )
    conn.commit()
    conn.close()


init_db()


# --- Utility functions ---
def get_tags():
    """Get all the Tags"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM tags")
    tags = [r[0] for r in c.fetchall()]
    conn.close()
    return tags


def get_daily_activity():
    """Get daily activity data for contributions graph"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """SELECT start, end FROM sessions 
           WHERE end IS NOT NULL"""
    )
    rows = c.fetchall()
    conn.close()

    daily_minutes = {}
    for start_str, end_str in rows:
        start_dt = datetime.fromisoformat(start_str)
        end_dt = datetime.fromisoformat(end_str)
        day = start_dt.date()
        duration = (end_dt - start_dt).total_seconds() / 60  # minutes
        daily_minutes[day] = daily_minutes.get(day, 0) + duration

    return daily_minutes


def get_contribution_level(minutes):
    """Convert minutes to GitHub-style contribution level (0-4)"""
    if minutes == 0:
        return 0
    elif minutes < 30:
        return 1
    elif minutes < 60:
        return 2
    elif minutes < 120:
        return 3
    else:
        return 4


def get_contribution_color(level):
    """Get color for contribution level"""
    colors = {
        0: CATPPUCCIN["surface0"],  # No activity
        1: CATPPUCCIN["green"] + " dim",  # Light activity
        2: CATPPUCCIN["green"],  # Medium activity
        3: CATPPUCCIN["teal"],  # High activity
        4: CATPPUCCIN["blue"],  # Very high activity
    }
    return colors.get(level, CATPPUCCIN["surface0"])


# --- Commands ---
@app.command()
def add_tag(name: str):
    """Create a new tag for categorizing time tracking sessions."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO tags(name) VALUES (?)", (name,))
        conn.commit()
        console.print(f"[bold {CATPPUCCIN['green']}]Added tag:[/] {name}")
    except sqlite3.IntegrityError:
        console.print(f"[bold {CATPPUCCIN['red']}]Tag already exists:[/] {name}")
    finally:
        conn.close()


@app.command()
def tags():
    """List all available tags."""
    tag_list = get_tags()
    table = Table(
        title="Tags",
        style=CATPPUCCIN["subtext1"],
        box=box.ROUNDED,
        header_style=f"bold {CATPPUCCIN['mauve']}",
    )
    table.add_column("ID", style=CATPPUCCIN["yellow"], justify="center")
    table.add_column("Name", style=CATPPUCCIN["blue"])
    for i, t in enumerate(tag_list, 1):
        table.add_row(str(i), t)
    console.print(table)


@app.command()
def start():
    """Start a new time tracking session."""
    tag_list = get_tags()
    if not tag_list:
        console.print(
            f"[bold {CATPPUCCIN['red']}]No tags available. Add one with 'tim add-tag NAME'"
        )
        raise typer.Exit()
    completer = FuzzyWordCompleter(tag_list)
    tag_name = prompt("Select tag: ", completer=completer)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM tags WHERE name=?", (tag_name,))
    row = c.fetchone()
    if not row:
        console.print(f"[bold {CATPPUCCIN['red']}]Tag not found")
        return
    tag_id = row[0]

    start = datetime.now(timezone.utc).isoformat()
    c.execute("INSERT INTO sessions(tag_id, start) VALUES (?, ?)", (tag_id, start))
    conn.commit()
    sid = c.lastrowid
    conn.close()

    console.print(
        Panel(
            f"Started session for [bold]{tag_name}[/]\nSession id: {sid}\nStart: [italic]{start}[/]",
            title=f"tim — {tag_name}",
            style=CATPPUCCIN["surface1"],
        )
    )


@app.command()
def stop():
    """Stop the currently active time tracking session"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, start FROM sessions WHERE end IS NULL ORDER BY id DESC LIMIT 1"
    )
    row = c.fetchone()
    if not row:
        console.print(f"[bold {CATPPUCCIN['red']}]No active session found")
        return
    sid, start = row
    start_dt = datetime.fromisoformat(start)
    now = datetime.now(timezone.utc)
    c.execute("UPDATE sessions SET end=? WHERE id=?", (now.isoformat(), sid))
    conn.commit()
    conn.close()

    duration = now - start_dt
    minutes, seconds = divmod(duration.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    console.print(
        f"[bold {CATPPUCCIN['green']}]Stopped session[/] — duration: {hours}h {minutes}m {seconds}s"
    )


@app.command()
def summary():
    """Get Summary and Analytics of your sessions"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT tags.name, start, end FROM sessions JOIN tags ON sessions.tag_id=tags.id"
    )
    rows = c.fetchall()
    conn.close()

    table = Table(
        title="Study Sessions",
        box=box.SIMPLE_HEAVY,
        header_style=f"bold {CATPPUCCIN['lavender']}",
    )
    table.add_column("Tag", style=CATPPUCCIN["mauve"])
    table.add_column("Start", style=CATPPUCCIN["subtext1"])
    table.add_column("End", style=CATPPUCCIN["subtext0"])
    table.add_column("Duration", style=CATPPUCCIN["green"])

    for tag, start, end in rows:
        if end:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            dur = end_dt - start_dt
            h, rem = divmod(dur.seconds, 3600)
            m, s = divmod(rem, 60)
            duration_str = f"{h}h {m}m"
        else:
            duration_str = "⏳ Active"
        table.add_row(tag, start, end or "—", duration_str)

    console.print(table)


@app.command()
def streak():
    """Analyze and display streak information for each tag"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT tags.name, start, end FROM sessions JOIN tags ON sessions.tag_id=tags.id"
    )
    rows = c.fetchall()
    conn.close()

    streaks = {}
    for tag, start, end in rows:
        if not end:
            continue
        day = datetime.fromisoformat(start).date()
        streaks.setdefault(tag, set()).add(day)

    table = Table(
        title="Streaks", box=box.ROUNDED, header_style=f"bold {CATPPUCCIN['yellow']}"
    )
    table.add_column("Tag", style=CATPPUCCIN["blue"])
    table.add_column("Current Streak", style=CATPPUCCIN["green"], justify="center")
    table.add_column("Best Streak", style=CATPPUCCIN["peach"], justify="center")

    today = date.today()
    for tag, days in streaks.items():
        sorted_days = sorted(days)
        best = cur = 1
        for i in range(1, len(sorted_days)):
            if (sorted_days[i] - sorted_days[i - 1]).days == 1:
                cur += 1
                best = max(best, cur)
            else:
                cur = 1
        # current streak check
        current_streak = 0
        d = today
        while d in days:
            current_streak += 1
            d = d - timedelta(days=1)

        table.add_row(tag, str(current_streak), str(best))

    console.print(table)


@app.command()
def graph(
    weeks: int = typer.Option(
        52, "--weeks", "-w", help="Number of weeks to show (default: 52)"
    )
):
    """Display a GitHub-style contributions graph"""
    daily_activity = get_daily_activity()

    # Calculate date range
    today = date.today()
    start_date = today - timedelta(weeks=weeks)

    # Find the Monday of the week containing start_date
    days_since_monday = start_date.weekday()
    start_date = start_date - timedelta(days=days_since_monday)

    # Create the graph
    console.print()
    console.print(
        Panel(
            f"[bold {CATPPUCCIN['lavender']}]📊 Contributions in the last {weeks} weeks[/]",
            style=CATPPUCCIN["surface1"],
            box=box.ROUNDED,
        )
    )

    # Month labels
    month_labels = []
    current_date = start_date
    while current_date <= today:
        if current_date.day <= 7:  # First week of month
            month_labels.append(
                (
                    current_date.strftime("%b"),
                    ((current_date - start_date).days // 7) * 3,
                )
            )
        current_date += timedelta(days=7)

    # Print month labels
    month_line = " " * 4  # Offset for day labels
    for month, pos in month_labels:
        month_line += " " * (pos - len(month_line) + 4) + month
    console.print(f"[{CATPPUCCIN['subtext1']}]{month_line}[/]")

    # Day labels and graph
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for day_idx in range(7):
        if day_idx % 2 == 0:  # Only show Mon, Wed, Fri, Sun
            day_label = f"{days[day_idx]:>3} "
        else:
            day_label = "    "

        line = f"[{CATPPUCCIN['subtext1']}]{day_label}[/]"

        current_date = start_date + timedelta(days=day_idx)
        week = 0

        while current_date <= today and week < weeks:
            minutes = daily_activity.get(current_date, 0)
            level = get_contribution_level(minutes)
            color = get_contribution_color(level)

            if current_date > today:
                symbol = "  "
            else:
                symbol = "██"

            line += f"[{color}]{symbol}[/] "
            current_date += timedelta(weeks=1)
            week += 1

        console.print(line)

    # Legend
    console.print()
    legend_text = f"[{CATPPUCCIN['subtext1']}]Less [/]"
    for level in range(5):
        color = get_contribution_color(level)
        legend_text += f"[{color}]██[/] "
    legend_text += f"[{CATPPUCCIN['subtext1']}] More[/]"

    console.print("    " + legend_text)

    # Statistics
    total_days = len([d for d in daily_activity.values() if d > 0])
    total_minutes = sum(daily_activity.values())
    avg_daily = (
        total_minutes / max(1, (today - start_date).days) if daily_activity else 0
    )

    stats_text = f"""
[{CATPPUCCIN['green']}]📈 {total_days}[/] days active
[{CATPPUCCIN['blue']}]⏱️  {total_minutes:.0f}[/] total minutes
[{CATPPUCCIN['yellow']}]📊 {avg_daily:.1f}[/] minutes/day average
"""

    console.print(
        Panel(
            stats_text,
            title="Statistics",
            style=CATPPUCCIN["surface1"],
            box=box.ROUNDED,
        )
    )


if __name__ == "__main__":
    app()
