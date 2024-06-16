import pytest
from app import db
from app.models.client import Client

def test_create_client(test_client):
  response = test_client.post('/clients', json={'name': 'Unit Test Client'})
  assert response.status_code == 201
  assert response.json['name'] == 'Unit Test Client'

def test_get_client(test_client):
  client = Client.query.first()
  response = test_client.get(f'/clients/{client.id}')
  assert response.status_code == 200
  assert response.json['name'] == client.name

def test_update_client(test_client):
  client = Client.query.first()
  response = test_client.put(f'/clients/{client.id}', json={'name': 'Unit Updated Client Name'})
  assert response.status_code == 200
  assert response.json['name'] == 'Unit Updated Client Name'

def test_delete_client(test_client):
  client = Client.query.first()
  response = test_client.delete(f'/clients/{client.id}')
  assert response.status_code == 204
  assert Client.query.get(client.id) is None
