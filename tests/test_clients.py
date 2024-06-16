import pytest
from app.models.client import Client

def test_create_client(test_client, auth_header):
  response = test_client.post('/clients', json={'name': 'Test Client'}, headers=auth_header)
  assert response.status_code == 201
  assert 'id' in response.json

def test_get_clients(test_client, auth_header):
  response = test_client.get('/clients', headers=auth_header)
  assert response.status_code == 200

def test_get_client(test_client, auth_header):
  create_response = test_client.post('/clients', json={'name': 'Test Client'}, headers=auth_header)
  client_id = create_response.json['id']

  response = test_client.get(f'/clients/{client_id}', headers=auth_header)
  assert response.status_code == 200
  assert response.json['name'] == 'Test Client'

def test_update_client(test_client, auth_header):
  create_response = test_client.post('/clients', json={'name': 'Test Client'}, headers=auth_header)
  client_id = create_response.json['id']

  response = test_client.put(f'/clients/{client_id}', json={'name': 'Updated Client'}, headers=auth_header)
  assert response.status_code == 200
  assert response.json['name'] == 'Updated Client'

def test_delete_client(test_client, auth_header):
  create_response = test_client.post('/clients', json={'name': 'Test Client'}, headers=auth_header)
  client_id = create_response.json['id']

  response = test_client.delete(f'/clients/{client_id}', headers=auth_header)
  assert response.status_code == 204
  assert Client.query.get(client_id) is None
