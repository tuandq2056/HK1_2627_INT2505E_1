import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_404_problem_json(client):
    response = client.get('/resources/999')
    assert response.status_code == 404
    assert response.content_type == 'application/problem+json'
    
    data = response.get_json()
    assert 'type' in data
    assert 'title' in data
    assert 'detail' in data
    assert 'status' in data
    assert data['status'] == 404
    assert 'instance' in data
    assert data['instance'] == '/resources/999'
    assert 'stack' not in data

def test_missing_accept_header(client):
    response = client.get('/resources/999')
    assert response.status_code == 404
    assert response.content_type == 'application/problem+json'

def test_accept_json_header(client):
    response = client.get('/resources/999', headers={'Accept': 'application/json'})
    assert response.status_code == 404
    assert response.content_type == 'application/problem+json'

def test_uncaught_exception(client, caplog):
    # Patch a route service to raise an exception
    with patch('services.book_service.get_books_list', side_effect=Exception("This is a random bug")):
        response = client.get('/books')
    
    assert response.status_code == 500
    assert response.content_type == 'application/problem+json'
    
    data = response.get_json()
    assert data['title'] == 'Internal Server Error'
    assert data['status'] == 500
    
    # Ensure error is logged server-side
    assert "An uncaught exception occurred" in caplog.text

