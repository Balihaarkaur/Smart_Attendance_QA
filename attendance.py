from __future__ import annotations

import csv
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class AttendanceTracker:
    """Handles attendance record creation and summary generation.
    
    Manages employee attendance records with validation, filtering, and export capabilities.
    Supports multiple status types (Present, Absent, Leave) and provides comprehensive
    reporting features including attendance rates and date-based filtering.
    """
    VALID_STATUSES = ("Present", "Absent", "Leave")

    def __init__(self) -> None:
        self.records: Dict[int, Dict[str, str]] = {}

    def add_record(self, emp_id: int, date: str, status: str) -> None:
        self._validate_emp_id(emp_id)
        normalized_date = self._validate_date(date)
        self._validate_status(status)
        self.records.setdefault(emp_id, {})[normalized_date] = status

    def get_summary(self, emp_id: int) -> Optional[Dict[str, int]]:
        if emp_id not in self.records:
            return None
        return self._summarize(self.records[emp_id])

    def get_all_summaries(self) -> Dict[int, Dict[str, int]]:
        return {emp_id: self._summarize(records) for emp_id, records in self.records.items()}

    def get_records(self, emp_id: int) -> Optional[Dict[str, str]]:
        return self.records.get(emp_id)

    def get_all_records(self) -> Dict[int, Dict[str, str]]:
        return self.records.copy()

    def delete_record(self, emp_id: int, date: str) -> bool:
        normalized_date = self._validate_date(date)
        if emp_id in self.records and normalized_date in self.records[emp_id]:
            del self.records[emp_id][normalized_date]
            if not self.records[emp_id]:
                del self.records[emp_id]
            return True
        return False

    def get_attendance_rate(self, emp_id: int) -> Optional[float]:
        if emp_id not in self.records:
            return None
        summary = self._summarize(self.records[emp_id])
        total = sum(summary.values())
        if total == 0:
            return 0.0
        return (summary["Present"] / total) * 100

    def filter_by_date_range(self, start_date: str, end_date: str) -> Dict[int, Dict[str, str]]:
        start = self._validate_date(start_date)
        end = self._validate_date(end_date)
        filtered = {}
        for emp_id, records in self.records.items():
            filtered_records = {date: status for date, status in records.items() if start <= date <= end}
            if filtered_records:
                filtered[emp_id] = filtered_records
        return filtered

    def export_to_csv(self, filepath: str) -> None:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Employee_ID", "Date", "Status"])
            for emp_id, records in sorted(self.records.items()):
                for date, status in sorted(records.items()):
                    writer.writerow([emp_id, date, status])

    def export_to_json(self, filepath: str) -> None:
        data = {
            str(emp_id): records
            for emp_id, records in self.records.items()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def import_from_csv(self, filepath: str) -> int:
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.add_record(
                        int(row["Employee_ID"]),
                        row["Date"],
                        row["Status"]
                    )
                    count += 1
                except (ValueError, KeyError):
                    continue
        return count

    def _validate_emp_id(self, emp_id: int) -> None:
        if not isinstance(emp_id, int) or emp_id <= 0:
            raise ValueError("Invalid employee ID")

    def _validate_status(self, status: str) -> None:
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {', '.join(self.VALID_STATUSES)}")

    def _validate_date(self, date: str) -> str:
        try:
            return datetime.strptime(date, "%Y-%m-%d").date().isoformat()
        except (TypeError, ValueError) as exc:
            raise ValueError("Date must be in YYYY-MM-DD format") from exc

    def _summarize(self, records: Dict[str, str]) -> Dict[str, int]:
        summary = {status: 0 for status in self.VALID_STATUSES}
        for status in records.values():
            summary[status] += 1
        return summary
