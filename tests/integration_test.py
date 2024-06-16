import pytest
from app import db
from app.models.client import Client
from app.models.vehicle import Vehicle

def test_create_client(test_client, auth_header):
  response = test_client.post('/clients', json={'name': 'Test Client'}, headers=auth_header)
  assert response.status_code == 201
  assert 'id' in response.json
  assert response.json['name'] == 'Test Client'
  client_id = response.json['id']

  db.session.delete(Client.query.get(client_id))
  db.session.commit()

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
  assert response.json['color'] == 'GRAY'
  vehicle_id = response.json['id']

  db.session.delete(Vehicle.query.get(vehicle_id))
  db.session.delete(Client.query.get(client_id))
  db.session.commit()

def test_get_client(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client 1'}, headers=auth_header)
  client_id = client_response.json['id']

  response = test_client.get(f'/clients/{client_id}', headers=auth_header)
  assert response.status_code == 200
  assert response.json['name'] == 'Test Client 1'

  db.session.delete(Client.query.get(client_id))
  db.session.commit()

def test_update_client(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client to Update'}, headers=auth_header)
  client_id = client_response.json['id']

  response = test_client.put(f'/clients/{client_id}', json={'name': 'Updated Client'}, headers=auth_header)
  assert response.status_code == 200
  assert response.json['name'] == 'Updated Client'

  db.session.delete(Client.query.get(client_id))
  db.session.commit()

def test_delete_client(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Test Client to Delete'}, headers=auth_header)
  client_id = client_response.json['id']

  response = test_client.delete(f'/clients/{client_id}', headers=auth_header)
  assert response.status_code == 204

  deleted_response = test_client.get(f'/clients/{client_id}', headers=auth_header)
  assert deleted_response.status_code == 404

def test_get_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Client for Vehicle'}, headers=auth_header)
  client_id = client_response.json['id']

  vehicle_response = test_client.post('/vehicles', json={
    'color': 'YELLOW',
    'model': 'SEDAN',
    'client_id': client_id
  }, headers=auth_header)
  vehicle_id = vehicle_response.json['id']

  response = test_client.get(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert response.status_code == 200
  assert response.json['color'] == 'YELLOW'

  db.session.delete(Vehicle.query.get(vehicle_id))
  db.session.delete(Client.query.get(client_id))
  db.session.commit()

def test_update_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Client for Vehicle Update'}, headers=auth_header)
  client_id = client_response.json['id']

  vehicle_response = test_client.post('/vehicles', json={
    'color': 'BLUE',
    'model': 'HATCH',
    'client_id': client_id
  }, headers=auth_header)
  vehicle_id = vehicle_response.json['id']

  response = test_client.put(f'/vehicles/{vehicle_id}', json={
    'color': 'GRAY',
    'model': 'CONVERTIBLE',
    'client_id': client_id
  }, headers=auth_header)
  assert response.status_code == 200
  assert response.json['color'] == 'GRAY'

  db.session.delete(Vehicle.query.get(vehicle_id))
  db.session.delete(Client.query.get(client_id))
  db.session.commit()

def test_delete_vehicle(test_client, auth_header):
  client_response = test_client.post('/clients', json={'name': 'Client for Vehicle Deletion'}, headers=auth_header)
  client_id = client_response.json['id']

  vehicle_response = test_client.post('/vehicles', json={
    'color': 'BLUE',
    'model': 'SEDAN',
    'client_id': client_id
  }, headers=auth_header)
  vehicle_id = vehicle_response.json['id']

  response = test_client.delete(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert response.status_code == 204

  deleted_response = test_client.get(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert deleted_response.status_code == 404

  db.session.delete(Client.query.get(client_id))
  db.session.commit()
