from flask import Flask, jsonify, request
from flask_cors import CORS
from attendance import AttendanceTracker
from typing import Dict, Any

app = Flask(__name__)
CORS(app)

# Global tracker instance
tracker = AttendanceTracker()


@app.route('/api/health', methods=['GET'])
def health_check() -> tuple[Dict[str, str], int]:
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Smart Attendance API"}), 200


@app.route('/api/records', methods=['POST'])
def add_record() -> tuple[Dict[str, Any], int]:
    """Add a new attendance record"""
    try:
        data = request.get_json()
        emp_id = int(data['emp_id'])
        date = data['date']
        status = data['status']
        
        tracker.add_record(emp_id, date, status)
        return jsonify({
            "success": True,
            "message": f"Record added for employee {emp_id}"
        }), 201
    except (KeyError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/records/<int:emp_id>', methods=['GET'])
def get_employee_records(emp_id: int) -> tuple[Dict[str, Any], int]:
    """Get all records for a specific employee"""
    records = tracker.get_records(emp_id)
    if records is None:
        return jsonify({"success": False, "error": "Employee not found"}), 404
    return jsonify({"success": True, "emp_id": emp_id, "records": records}), 200


@app.route('/api/records/<int:emp_id>/<string:date>', methods=['DELETE'])
def delete_record(emp_id: int, date: str) -> tuple[Dict[str, Any], int]:
    """Delete a specific attendance record"""
    try:
        success = tracker.delete_record(emp_id, date)
        if success:
            return jsonify({"success": True, "message": "Record deleted"}), 200
        return jsonify({"success": False, "error": "Record not found"}), 404
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/summary/<int:emp_id>', methods=['GET'])
def get_employee_summary(emp_id: int) -> tuple[Dict[str, Any], int]:
    """Get attendance summary for a specific employee"""
    summary = tracker.get_summary(emp_id)
    if summary is None:
        return jsonify({"success": False, "error": "Employee not found"}), 404
    
    rate = tracker.get_attendance_rate(emp_id)
    return jsonify({
        "success": True,
        "emp_id": emp_id,
        "summary": summary,
        "attendance_rate": round(rate, 2) if rate else 0.0
    }), 200


@app.route('/api/summary', methods=['GET'])
def get_all_summaries() -> tuple[Dict[str, Any], int]:
    """Get attendance summaries for all employees"""
    summaries = tracker.get_all_summaries()
    
    result = []
    for emp_id, summary in summaries.items():
        rate = tracker.get_attendance_rate(emp_id)
        result.append({
            "emp_id": emp_id,
            "summary": summary,
            "attendance_rate": round(rate, 2) if rate else 0.0
        })
    
    return jsonify({"success": True, "data": result}), 200


@app.route('/api/records', methods=['GET'])
def get_all_records() -> tuple[Dict[str, Any], int]:
    """Get all attendance records"""
    records = tracker.get_all_records()
    return jsonify({"success": True, "records": records}), 200


@app.route('/api/filter', methods=['GET'])
def filter_records() -> tuple[Dict[str, Any], int]:
    """Filter records by date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({
                "success": False,
                "error": "start_date and end_date are required"
            }), 400
        
        filtered = tracker.filter_by_date_range(start_date, end_date)
        return jsonify({"success": True, "records": filtered}), 200
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.errorhandler(404)
def not_found(error) -> tuple[Dict[str, Any], int]:
    return jsonify({"success": False, "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error) -> tuple[Dict[str, Any], int]:
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
