import argparse
from typing import Optional

from attendance import AttendanceTracker


def _build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Smart Attendance CLI")
	subparsers = parser.add_subparsers(dest="command", required=True)

	add_parser = subparsers.add_parser("add", help="Add an attendance record")
	add_parser.add_argument("emp_id", type=int, help="Employee ID")
	add_parser.add_argument("date", type=str, help="Date in YYYY-MM-DD format")
	add_parser.add_argument("status", type=str, choices=AttendanceTracker.VALID_STATUSES)

	summary_parser = subparsers.add_parser("summary", help="Show summary for an employee")
	summary_parser.add_argument("emp_id", type=int, help="Employee ID")

	subparsers.add_parser("list", help="List summaries for all employees")

	return parser


def main(argv: Optional[list[str]] = None) -> int:
	parser = _build_parser()
	args = parser.parse_args(argv)

	tracker = AttendanceTracker()

	if args.command == "add":
		tracker.add_record(args.emp_id, args.date, args.status)
		print("Record added.")
		return 0

	if args.command == "summary":
		summary = tracker.get_summary(args.emp_id)
		if summary is None:
			print("No records found for this employee.")
		else:
			print(summary)
		return 0

	if args.command == "list":
		summaries = tracker.get_all_summaries()
		if not summaries:
			print("No attendance records yet.")
		else:
			for emp_id, summary in sorted(summaries.items()):
				print(emp_id, summary)
		return 0

	return 1


if __name__ == "__main__":
	raise SystemExit(main())
