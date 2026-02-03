# Smart Attendance System

A comprehensive attendance management system with multiple interfaces and testing frameworks.

## Features

### Core Backend (`attendance.py`)
- Add/delete attendance records
- Employee attendance summaries
- Attendance rate calculation
- Date range filtering
- CSV/JSON export and import
- Input validation (Employee ID, Date, Status)

### Interfaces

#### 1. CLI Interface (`app.py`)
Command-line interface for basic operations:
```bash
python app.py add <emp_id> <date> <status>
python app.py summary <emp_id>
python app.py list
```

#### 2. REST API (`api.py`)
Flask-based REST API with endpoints:
- `POST /api/records` - Add record
- `GET /api/records/<emp_id>` - Get employee records
- `DELETE /api/records/<emp_id>/<date>` - Delete record
- `GET /api/summary/<emp_id>` - Get employee summary
- `GET /api/summary` - Get all summaries
- `GET /api/filter?start_date=X&end_date=Y` - Filter by date range
- `GET /api/health` - Health check

#### 3. Streamlit Web UI (`streamlit_app.py`)
Interactive web interface with:
- Add attendance records
- View individual/all employee summaries
- Generate reports with date filtering
- Export data to CSV/JSON
- Import data from CSV

## Installation

### Requirements
- Python 3.10+ (64-bit for Streamlit)
- Virtual environment recommended

### Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Applications

### CLI
```bash
python app.py add 101 2026-02-01 Present
python app.py summary 101
```

### Flask API
```bash
python api.py
# API runs on http://localhost:5000
```

### Streamlit Web UI
```bash
streamlit run streamlit_app.py
# Opens browser to http://localhost:8501
```

**Note**: Streamlit requires 64-bit Python due to pyarrow dependency.

## Testing

### Run All Tests
```bash
pytest
```

## Selenium Test Execution

Selenium/UI tests are skipped by default to avoid dependency issues.

Run backend tests only:
```bash
pytest
```

Run Selenium tests explicitly:
```bash
pytest --run-selenium
```

### Run Specific Test Suites
```bash
# Backend tests
pytest test_attendance.py -v

# API tests
pytest test_api.py -v

# Selenium tests (requires Chrome/ChromeDriver)
pytest test_selenium.py -v
```

### Test Coverage
- **Backend Tests** (`test_attendance.py`): 5 tests
  - Valid record addition
  - Invalid employee ID
  - Invalid status
  - Invalid date format
  - Boundary conditions

- **API Tests** (`test_api.py`): 15 tests
  - Health check
  - CRUD operations
  - Error handling
  - Date filtering
  - Edge cases

- **Selenium Tests** (`test_selenium.py`): Browser automation tests
  - UI accessibility
  - API endpoint verification
  - End-to-end workflows

## Project Structure
```
Smart_attendance/
├── attendance.py          # Core backend module
├── app.py                 # CLI interface
├── api.py                 # Flask REST API
├── streamlit_app.py       # Streamlit web UI
├── test_attendance.py     # Backend unit tests
├── test_api.py            # API integration tests
├── test_selenium.py       # Selenium browser tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Valid Status Values
- Present
- Absent
- Leave

## Date Format
All dates must be in `YYYY-MM-DD` format (ISO 8601).

## API Usage Examples

### Add Record
```bash
curl -X POST http://localhost:5000/api/records \
  -H "Content-Type: application/json" \
  -d '{"emp_id": 101, "date": "2026-02-01", "status": "Present"}'
```

### Get Summary
```bash
curl http://localhost:5000/api/summary/101
```

### Filter by Date
```bash
curl "http://localhost:5000/api/filter?start_date=2026-02-01&end_date=2026-02-28"
```

## Development

### Running in Development Mode
- API runs with `debug=True` for hot reloading
- Streamlit auto-reloads on file changes

### Adding New Features
1. Update `attendance.py` for backend logic
2. Add API endpoints in `api.py`
3. Create UI components in `streamlit_app.py`
4. Write tests in respective test files
5. Update this README

## Known Limitations
- Streamlit requires 64-bit Python (pyarrow dependency)
- Selenium tests require Chrome and ChromeDriver
- In-memory storage (data lost on restart)
- No authentication/authorization

## Future Enhancements
- Database persistence (SQLite/PostgreSQL)
- User authentication
- Email notifications
- Advanced reporting (charts/graphs)
- Mobile app
- Docker containerization


