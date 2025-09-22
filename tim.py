#!/usr/bin/env python3
"""
Beautiful TUI Time Tracker with Catppuccin Mocha colors and Vim keybindings
Similar to Timewarrior functionality with interactive interface
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header,
    Footer,
    DataTable,
    Static,
    Input,
    Button,
    Label,
    ListItem,
    ListView,
    Collapsible,
)
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual import events
from textual.reactive import reactive
from textual.message import Message
from textual.timer import Timer
from rich.text import Text
from rich.table import Table
from rich import box

# Catppuccin Mocha CSS with bufferline-style tabs
CATPPUCCIN_CSS = """
/* Catppuccin Mocha Colors */
/* Base colors with transparency support */
App {
    background: #1e1e2e;
    color: #cdd6f4;
}

Header {
    background: #181825;
    color: #cba6f7;
    border: none;
}

Footer {
    background: #1e1e2e;
    color: #bac2de;
}

/* Footer key bindings */
Footer .footer--key {
    background: #313244;
    color: #f9e2af;
}

Footer .footer--key-text {
    color: #cdd6f4;
}

Footer .footer--description {
    color: #a6adc8;
}

/* Bufferline-style View Bar - all tabs visible and centered */
#view-bar {
    background: #181825;
    height: 1;
    dock: top;
    border: none;
    padding: 0;
}

#view-bar Horizontal {
    height: 1;
    align: center middle;
    background: #181825;
    width: 100%;
}

/* Inactive tabs - visible but muted */
.view-tab {
    background: #181825;
    color: #6c7086;
    margin: 0 1;
    padding: 0 2;
    border: none;
    text-style: none;
    min-height: 1;
    height: 1;
    text-align: center;
    width: 12;
}

.view-tab:hover {
    background: #313244;
    color: #a6adc8;
}

/* Active tab - green text like bufferline */
.view-tab.-active {
    background: #181825;
    color: #a6e3a1;
    text-style: bold;
    border: none;
    margin: 0 1;
    height: 1;
}

/* Clean tab separations - simplified for Textual CSS */

/* Panels and containers */
Static {
    background: #1e1e2e;
    color: #cdd6f4;
    border: solid #45475a;
}

Container {
    background: #1e1e2e;
}

#main-container {
    background: #1e1e2e;
}

#content {
    background: #1e1e2e;
    margin: 1 1;
}

#start-modal {
    background: #1e1e2e;
    border: solid #cba6f7;
    padding: 2;
    margin: 5 10;
}

.title {
    color: #cba6f7;
    text-style: bold;
    text-align: center;
    margin: 0 0 1 0;
}

/* Tables */
DataTable {
    background: #1e1e2e;
    color: #cdd6f4;
    scrollbar-background: #313244;
    scrollbar-color: #585b70;
    border: solid #45475a;
}

DataTable > .datatable--header {
    background: #313244;
    color: #cba6f7;
    text-style: bold;
}

DataTable > .datatable--cursor {
    background: #45475a;
    color: #f9e2af;
}

DataTable:focus > .datatable--cursor {
    background: #585b70;
    color: #f9e2af;
    text-style: bold;
}

/* Input fields */
Input {
    background: #313244;
    color: #cdd6f4;
    border: solid #45475a;
}

Input:focus {
    border: solid #cba6f7;
}

Input > .input--placeholder {
    color: #6c7086;
}

Input.-valid {
    border: solid #a6e3a1;
}

Input.-invalid {
    border: solid #f38ba8;
}

/* Buttons */
Button {
    background: #313244;
    color: #cdd6f4;
    border: solid #45475a;
    margin: 0 1;
}

Button:hover {
    background: #45475a;
    color: #cba6f7;
}

Button:focus {
    border: solid #cba6f7;
}

Button.-primary {
    background: #89b4fa;
    color: #11111b;
    border: solid #89b4fa;
}

Button.-primary:hover {
    background: #74c7ec;
    border: solid #74c7ec;
}

Button.-success {
    background: #a6e3a1;
    color: #11111b;
    border: solid #a6e3a1;
}

Button.-success:hover {
    background: #94e2d5;
    border: solid #94e2d5;
}

Button.-warning {
    background: #f9e2af;
    color: #11111b;
    border: solid #f9e2af;
}

Button.-warning:hover {
    background: #fab387;
    border: solid #fab387;
}

Button.-danger {
    background: #f38ba8;
    color: #11111b;
    border: solid #f38ba8;
}

Button.-danger:hover {
    background: #eba0ac;
    border: solid #eba0ac;
}

/* Lists */
ListView {
    background: #1e1e2e;
    color: #cdd6f4;
    border: solid #45475a;
}

ListItem {
    background: transparent;
    color: #cdd6f4;
}

ListItem:hover {
    background: #313244;
}

ListItem.-highlighted {
    background: #45475a;
    color: #f9e2af;
}

/* Labels */
Label {
    color: #cdd6f4;
    margin: 1 0 0 0;
}

/* Status indicators */
.status-active {
    color: #a6e3a1;
}

.status-inactive {
    color: #6c7086;
}

.duration {
    color: #f9e2af;
}

.tags {
    color: #cba6f7;
}

.description {
    color: #bac2de;
}

.warning {
    color: #fab387;
}

.error {
    color: #f38ba8;
}

.success {
    color: #a6e3a1;
}

/* Scrollbars */
ScrollableContainer {
    scrollbar-background: #313244;
    scrollbar-color: #585b70;
}

/* Notification styling */
.notification {
    background: #313244;
    color: #cdd6f4;
    border: solid #45475a;
}
"""


class TimeEntry:
    def __init__(
        self,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        tags: List[str] = None,
        description: str = "",
    ):
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags or []
        self.description = description
        self.id = int(start_time.timestamp())

    def duration(self) -> timedelta:
        end = self.end_time or datetime.now()
        return end - self.start_time

    def is_active(self) -> bool:
        return self.end_time is None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "tags": self.tags,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        entry = cls(
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=(
                datetime.fromisoformat(data["end_time"]) if data["end_time"] else None
            ),
            tags=data["tags"],
            description=data["description"],
        )
        entry.id = data["id"]
        return entry


class TimeTracker:
    def __init__(self, data_file: str = None):
        self.data_file = data_file or os.path.expanduser("~/.timetracker.json")
        self.entries: List[TimeEntry] = []
        self.load_data()

    def load_data(self):
        """Load time entries from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.entries = [TimeEntry.from_dict(entry) for entry in data]
            except (json.JSONDecodeError, KeyError):
                self.entries = []

    def save_data(self):
        """Save time entries to JSON file"""
        with open(self.data_file, "w") as f:
            json.dump([entry.to_dict() for entry in self.entries], f, indent=2)

    def start_tracking(self, tags: List[str] = None, description: str = ""):
        """Start a new time tracking session"""
        self.stop_tracking()

        entry = TimeEntry(
            start_time=datetime.now(), tags=tags or [], description=description
        )
        self.entries.append(entry)
        self.save_data()
        return entry

    def stop_tracking(self):
        """Stop the current active tracking session"""
        active_entry = self.get_active_entry()
        if active_entry:
            active_entry.end_time = datetime.now()
            self.save_data()
            return active_entry
        return None

    def get_active_entry(self) -> Optional[TimeEntry]:
        """Get the currently active time entry"""
        for entry in reversed(self.entries):
            if entry.is_active():
                return entry
        return None

    def delete_entry(self, entry_id: int):
        """Delete a time entry"""
        self.entries = [entry for entry in self.entries if entry.id != entry_id]
        self.save_data()

    def get_entries_by_tags(self, tags: List[str]) -> List[TimeEntry]:
        """Get entries filtered by tags"""
        if not tags:
            return self.entries
        return [
            entry for entry in self.entries if any(tag in entry.tags for tag in tags)
        ]

    @staticmethod
    def format_duration(duration: timedelta) -> str:
        """Format duration as HH:MM:SS"""
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @staticmethod
    def format_time(dt: datetime) -> str:
        """Format datetime for display"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class StartTrackingModal(ModalScreen):
    """Modal for starting a new tracking session"""

    BINDINGS = [
        Binding("escape", "dismiss", "Cancel"),
        Binding("ctrl+c", "dismiss", "Cancel"),
    ]

    def __init__(self, tracker: TimeTracker):
        super().__init__()
        self.tracker = tracker

    def compose(self) -> ComposeResult:
        with Container(id="start-modal"):
            yield Static("Start Time Tracking", classes="title")
            yield Label("Description:")
            yield Input(placeholder="What are you working on?", id="description")
            yield Label("Tags (comma-separated):")
            yield Input(placeholder="work,python,api", id="tags")
            with Horizontal():
                yield Button("Start", variant="success", id="start-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-btn":
            description = self.query_one("#description", Input).value
            tags_input = self.query_one("#tags", Input).value
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

            self.tracker.start_tracking(tags=tags, description=description)
            self.dismiss(True)
        elif event.button.id == "cancel-btn":
            self.dismiss(False)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Allow Enter to submit from either input
        self.on_button_pressed(Button.Pressed(self.query_one("#start-btn", Button)))


class ViewTab(Static):
    """Clickable view tab widget"""

    def __init__(self, text: str, view_name: str, app_ref, **kwargs):
        super().__init__(text, **kwargs)
        self.view_name = view_name
        self.app_ref = app_ref
        self.can_focus = True

    def on_click(self) -> None:
        """Handle tab click to switch views"""
        if self.view_name == "status":
            self.app_ref.action_show_status()
        elif self.view_name == "entries":
            self.app_ref.action_show_entries()
        elif self.view_name == "summary":
            self.app_ref.action_show_summary()


class ViewBar(Static):
    """Top view bar with tabs"""

    def __init__(self, app_ref):
        super().__init__(id="view-bar")
        self.app_ref = app_ref
        self.current_view = "status"

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ViewTab(
                "1.Status",
                "status",
                self.app_ref,
                classes="view-tab -status -active",
                id="tab-status",
            )
            yield ViewTab(
                "2.Entry",
                "entries",
                self.app_ref,
                classes="view-tab -entries",
                id="tab-entries",
            )
            yield ViewTab(
                "3.Summ",
                "summary",
                self.app_ref,
                classes="view-tab -summary",
                id="tab-summary",
            )

    def update_active_tab(self, active_view: str) -> None:
        """Update which tab appears active"""
        self.current_view = active_view

        # Remove active class from all tabs
        for tab_id in ["tab-status", "tab-entries", "tab-summary"]:
            try:
                tab = self.query_one(f"#{tab_id}")
                tab.remove_class("-active")
            except:
                pass

        # Add active class to current tab
        try:
            if active_view == "status":
                self.query_one("#tab-status").add_class("-active")
            elif active_view == "entries":
                self.query_one("#tab-entries").add_class("-active")
            elif active_view == "summary":
                self.query_one("#tab-summary").add_class("-active")
        except:
            pass


class StatusWidget(Static):
    """Widget showing current tracking status"""

    def __init__(self, tracker: TimeTracker):
        super().__init__()
        self.tracker = tracker
        self.timer: Optional[Timer] = None

    def on_mount(self) -> None:
        self.update_status()
        self.timer = self.set_interval(1.0, self.update_status)

    def update_status(self) -> None:
        active_entry = self.tracker.get_active_entry()

        if active_entry:
            duration = active_entry.duration()
            duration_str = self.tracker.format_duration(duration)
            tags_str = f"[{', '.join(active_entry.tags)}]" if active_entry.tags else ""
            desc_str = (
                f" - {active_entry.description}" if active_entry.description else ""
            )

            status_text = Text()
            status_text.append("⏱️  TRACKING: ", style="bold green")
            status_text.append(f"{duration_str}", style="bold yellow")
            status_text.append(f" {tags_str}", style="bold magenta")
            status_text.append(desc_str, style="cyan")

            self.update(status_text)
        else:
            status_text = Text()
            status_text.append("⏸️  NOT TRACKING", style="bold #6c7086")
            self.update(status_text)


class EntryTable(DataTable):
    """Table widget for displaying time entries"""

    BINDINGS = [
        Binding("d", "delete_entry", "Delete Entry"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, tracker: TimeTracker):
        super().__init__()
        self.tracker = tracker
        self.cursor_type = "row"

    def on_mount(self) -> None:
        self.add_columns("Start", "End", "Duration", "Tags", "Description")
        self.refresh_data()

    def refresh_data(self) -> None:
        self.clear()
        entries = sorted(self.tracker.entries, key=lambda x: x.start_time, reverse=True)

        for entry in entries:
            start_str = self.tracker.format_time(entry.start_time)
            end_str = (
                self.tracker.format_time(entry.end_time) if entry.end_time else "Active"
            )
            duration_str = self.tracker.format_duration(entry.duration())
            tags_str = ", ".join(entry.tags) if entry.tags else ""

            # Style active entries
            if entry.is_active():
                end_str = Text("Active", style="bold #a6e3a1")
                duration_str = Text(duration_str, style="bold #f9e2af")

            self.add_row(
                start_str,
                end_str,
                duration_str,
                tags_str,
                entry.description,
                key=str(entry.id),
            )

    def action_delete_entry(self) -> None:
        row_key = self.cursor_row
        if row_key is not None:
            entry_id = int(self.get_row_key_from_index(row_key))
            self.tracker.delete_entry(entry_id)
            self.refresh_data()

    def action_refresh(self) -> None:
        self.refresh_data()


class SummaryWidget(Static):
    """Widget showing time tracking summary"""

    def __init__(self, tracker: TimeTracker, days: int = 7):
        super().__init__()
        self.tracker = tracker
        self.days = days

    def on_mount(self) -> None:
        self.update_summary()

    def update_summary(self) -> None:
        now = datetime.now()
        start_date = now - timedelta(days=self.days)

        # Filter entries within date range
        period_entries = [
            entry
            for entry in self.tracker.entries
            if entry.start_time >= start_date and entry.end_time is not None
        ]

        if not period_entries:
            self.update(f"No completed entries in the last {self.days} days")
            return

        # Calculate total time and group by tags
        total_duration = sum(
            (entry.duration() for entry in period_entries), timedelta()
        )
        tag_durations = {}

        for entry in period_entries:
            duration = entry.duration()
            if not entry.tags:
                tag_durations.setdefault("(no tags)", timedelta())
                tag_durations["(no tags)"] += duration
            else:
                for tag in entry.tags:
                    tag_durations.setdefault(tag, timedelta())
                    tag_durations[tag] += duration

        # Create summary text
        summary_text = Text()
        summary_text.append(
            f"Summary - Last {self.days} Days\n\n", style="bold #cba6f7"
        )

        sorted_tags = sorted(tag_durations.items(), key=lambda x: x[1], reverse=True)

        for tag, duration in sorted_tags:
            percentage = (
                duration.total_seconds() / total_duration.total_seconds()
            ) * 100
            duration_str = self.tracker.format_duration(duration)
            summary_text.append(f"{tag:<20} ", style="#94e2d5")
            summary_text.append(f"{duration_str:>10} ", style="#f9e2af")
            summary_text.append(f"({percentage:5.1f}%)\n", style="#a6e3a1")

        summary_text.append(f"\n{'Total':<20} ", style="bold #cdd6f4")
        summary_text.append(
            f"{self.tracker.format_duration(total_duration):>10}\n",
            style="bold #f9e2af",
        )

        self.update(summary_text)


class TimeTrackerApp(App):
    """Main TUI application"""

    CSS = CATPPUCCIN_CSS

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+c", "quit", "Quit"),
        Binding("s", "start_tracking", "Start Tracking"),
        Binding("t", "stop_tracking", "Stop Tracking"),
        Binding("1", "show_status", "Status"),
        Binding("2", "show_entries", "Entries"),
        Binding("3", "show_summary", "Summary"),
        Binding("r", "refresh", "Refresh"),
        Binding("j", "focus_next", "Focus Next", show=False),
        Binding("k", "focus_previous", "Focus Previous", show=False),
        Binding("g,g", "focus_first", "Focus First", show=False),
        Binding("shift+g", "focus_last", "Focus Last", show=False),
    ]

    MODES = {
        "status": "Status View",
        "entries": "Entries View",
        "summary": "Summary View",
    }

    current_mode = reactive("status")

    def __init__(self):
        super().__init__()
        self.tracker = TimeTracker()
        self.status_widget = None
        self.entry_table = None
        self.summary_widget = None
        self.view_bar = None

    def compose(self) -> ComposeResult:
        yield Header()
        self.view_bar = ViewBar(self)
        yield self.view_bar
        with Container(id="main-container"):
            yield Container(id="content")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Time Tracker"
        self.sub_title = "Vim-style TUI"
        self.switch_mode("status")

    def action_start_tracking(self) -> None:
        def check_result(started: bool) -> None:
            if started:
                self.refresh_all()

        self.push_screen(StartTrackingModal(self.tracker), check_result)

    def action_stop_tracking(self) -> None:
        stopped_entry = self.tracker.stop_tracking()
        if stopped_entry:
            self.notify(f"Stopped tracking: {stopped_entry.description or 'Untitled'}")
        else:
            self.notify("No active tracking session")
        self.refresh_all()

    def action_show_status(self) -> None:
        self.switch_mode("status")

    def action_show_entries(self) -> None:
        self.switch_mode("entries")

    def action_show_summary(self) -> None:
        self.switch_mode("summary")

    def action_refresh(self) -> None:
        self.tracker.load_data()
        self.refresh_all()
        self.notify("Refreshed data")

    def action_focus_next(self) -> None:
        self.screen.focus_next()

    def action_focus_previous(self) -> None:
        self.screen.focus_previous()

    def action_focus_first(self) -> None:
        if self.entry_table and self.current_mode == "entries":
            self.entry_table.cursor_row = 0

    def action_focus_last(self) -> None:
        if self.entry_table and self.current_mode == "entries":
            self.entry_table.cursor_row = self.entry_table.row_count - 1

    def switch_mode(self, mode: str) -> None:
        self.current_mode = mode

        # Update view bar to highlight active tab
        if self.view_bar:
            self.view_bar.update_active_tab(mode)

        content_container = self.query_one("#content")
        content_container.remove_children()

        if mode == "status":
            self.status_widget = StatusWidget(self.tracker)
            content_container.mount(self.status_widget)
        elif mode == "entries":
            self.entry_table = EntryTable(self.tracker)
            content_container.mount(self.entry_table)
        elif mode == "summary":
            self.summary_widget = SummaryWidget(self.tracker)
            content_container.mount(self.summary_widget)

    def refresh_all(self) -> None:
        if self.status_widget:
            self.status_widget.update_status()
        if self.entry_table:
            self.entry_table.refresh_data()
        if self.summary_widget:
            self.summary_widget.update_summary()


def main():
    app = TimeTrackerApp()
    app.run()


if __name__ == "__main__":
    main()
