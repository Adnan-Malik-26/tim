import pytest
from datetime import datetime
from time_tracker import TimeTracker, TimeEntry

def test_start_stop_tracking(tmp_path):
    tracker = TimeTracker(data_file=tmp_path / "test.json")

    # Start
    entry = tracker.start_tracking(tags=["test"], description="unit test")
    assert entry.is_active()

    # Stop
    stopped = tracker.stop_tracking()
    assert stopped.end_time is not None
    assert not stopped.is_active()
