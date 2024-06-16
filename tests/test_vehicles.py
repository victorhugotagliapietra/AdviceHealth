import pytest
from app.models.vehicle import Vehicle

def test_create_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client for Vehicle'}, headers=auth_header)
  client_id = client_response.json['id']

  response = test_client.post('/vehicles', json={
    'color': 'GRAY',
    'model': 'CONVERTIBLE',
    'client_id': client_id
  }, headers=auth_header)
  assert response.status_code == 201
  assert 'id' in response.json

def test_get_vehicles(test_client, auth_header):
  response = test_client.get('/vehicles', headers=auth_header)
  assert response.status_code == 200

def test_get_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client for Vehicle'}, headers=auth_header)
  client_id = client_response.json['id']

  vehicle_response = test_client.post('/vehicles', json={
    'color': 'GRAY',
    'model': 'CONVERTIBLE',
    'client_id': client_id
  }, headers=auth_header)
  vehicle_id = vehicle_response.json['id']

  response = test_client.get(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert response.status_code == 200
  assert response.json['color'] == 'GRAY'

def test_update_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client for Vehicle'}, headers=auth_header)
  client_id = client_response.json['id']

  vehicle_response = test_client.post('/vehicles', json={
    'color': 'GRAY',
    'model': 'CONVERTIBLE',
    'client_id': client_id
  }, headers=auth_header)
  vehicle_id = vehicle_response.json['id']

  response = test_client.put(f'/vehicles/{vehicle_id}', json={
    'color': 'BLUE',
    'model': 'SEDAN',
    'client_id': client_id
  }, headers=auth_header)
  assert response.status_code == 200
  assert response.json['color'] == 'BLUE'

def test_delete_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client for Vehicle'}, headers=auth_header)
  client_id = client_response.json['id']

  vehicle_response = test_client.post('/vehicles', json={
    'color': 'GRAY',
    'model': 'CONVERTIBLE',
    'client_id': client_id
  }, headers=auth_header)
  vehicle_id = vehicle_response.json['id']

  response = test_client.delete(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert response.status_code == 204
  assert Vehicle.query.get(vehicle_id) is None
