import pytest
from api import app
import json


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_add_record_success(client):
    """Test adding a valid attendance record"""
    response = client.post('/api/records',
                          json={'emp_id': 101, 'date': '2026-02-01', 'status': 'Present'},
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True


def test_add_record_invalid_data(client):
    """Test adding an invalid attendance record"""
    response = client.post('/api/records',
                          json={'emp_id': -1, 'date': '2026-02-01', 'status': 'Present'},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_add_record_invalid_status(client):
    """Test adding a record with invalid status"""
    response = client.post('/api/records',
                          json={'emp_id': 101, 'date': '2026-02-01', 'status': 'Late'},
                          content_type='application/json')
    assert response.status_code == 400


def test_add_record_missing_fields(client):
    """Test adding a record with missing fields"""
    response = client.post('/api/records',
                          json={'emp_id': 101},
                          content_type='application/json')
    assert response.status_code == 400


def test_get_employee_records(client):
    """Test retrieving employee records"""
    # First add a record
    client.post('/api/records',
               json={'emp_id': 102, 'date': '2026-02-01', 'status': 'Present'},
               content_type='application/json')
    
    # Then retrieve it
    response = client.get('/api/records/102')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['emp_id'] == 102


def test_get_nonexistent_employee(client):
    """Test retrieving records for non-existent employee"""
    response = client.get('/api/records/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False


def test_get_employee_summary(client):
    """Test getting employee summary"""
    # Add multiple records
    client.post('/api/records',
               json={'emp_id': 103, 'date': '2026-02-01', 'status': 'Present'},
               content_type='application/json')
    client.post('/api/records',
               json={'emp_id': 103, 'date': '2026-02-02', 'status': 'Absent'},
               content_type='application/json')
    
    response = client.get('/api/summary/103')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'summary' in data
    assert 'attendance_rate' in data


def test_get_all_summaries(client):
    """Test getting summaries for all employees"""
    # Add records for multiple employees
    client.post('/api/records',
               json={'emp_id': 104, 'date': '2026-02-01', 'status': 'Present'},
               content_type='application/json')
    client.post('/api/records',
               json={'emp_id': 105, 'date': '2026-02-01', 'status': 'Present'},
               content_type='application/json')
    
    response = client.get('/api/summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert isinstance(data['data'], list)


def test_get_all_records(client):
    """Test getting all records"""
    response = client.get('/api/records')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'records' in data


def test_filter_records_by_date_range(client):
    """Test filtering records by date range"""
    # Add records
    client.post('/api/records',
               json={'emp_id': 106, 'date': '2026-02-01', 'status': 'Present'},
               content_type='application/json')
    client.post('/api/records',
               json={'emp_id': 106, 'date': '2026-02-05', 'status': 'Absent'},
               content_type='application/json')
    
    response = client.get('/api/filter?start_date=2026-02-01&end_date=2026-02-03')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_filter_records_missing_params(client):
    """Test filtering without required parameters"""
    response = client.get('/api/filter?start_date=2026-02-01')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False


def test_delete_record(client):
    """Test deleting a record"""
    # Add a record
    client.post('/api/records',
               json={'emp_id': 107, 'date': '2026-02-01', 'status': 'Present'},
               content_type='application/json')
    
    # Delete it
    response = client.delete('/api/records/107/2026-02-01')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True


def test_delete_nonexistent_record(client):
    """Test deleting a non-existent record"""
    response = client.delete('/api/records/999/2026-02-01')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False


def test_404_endpoint(client):
    """Test accessing a non-existent endpoint"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['success'] is False
