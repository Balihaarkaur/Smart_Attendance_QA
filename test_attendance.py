import pytest
from attendance import AttendanceTracker

def test_add_record_valid():
    """Verify successful addition of valid attendance record."""
    tracker = AttendanceTracker()
    tracker.add_record(101, '2026-02-01', 'Present')
    summary = tracker.get_summary(101)
    assert summary == {'Present': 1, 'Absent': 0, 'Leave': 0}

def test_add_record_invalid_id():
    """Verify error is raised for invalid employee ID."""
    tracker = AttendanceTracker()
    with pytest.raises(ValueError):
        tracker.add_record(-1, '2026-02-01', 'Present')

def test_add_record_invalid_status():
    """Verify error is raised for invalid attendance status."""
    tracker = AttendanceTracker()
    with pytest.raises(ValueError):
        tracker.add_record(101, '2026-02-01', 'Late')

def test_add_record_invalid_date():
    """Verify error is raised for invalid date format."""
    tracker = AttendanceTracker()
    with pytest.raises(ValueError):
        tracker.add_record(101, '02-01-2026', 'Present')

def test_add_record_boundary_employee_id():
    """Verify attendance record works with minimum valid employee ID."""
    tracker = AttendanceTracker()
    tracker.add_record(1, '2026-02-01', 'Present')
    summary = tracker.get_summary(1)
    assert summary['Present'] == 1

