import pytest
from app import create_app, db
from app.models.client import Client
from app.models.vehicle import Vehicle

@pytest.fixture(scope='module')
def test_client():
  flask_app = create_app('config.TestingConfig')
  testing_client = flask_app.test_client()

  with flask_app.app_context():
    yield testing_client
    db.session.remove()

def test_create_client(test_client):
  response = test_client.post('/clients', json={'name': 'Test Client'})
  client_id = response.json['id']
  assert response.status_code == 201
  assert response.json['name'] == 'Test Client'

  delete_client(client_id, test_client)

def test_create_vehicle(test_client):
  client_response = test_client.post('/clients', json={'name': 'Test Client for Vehicle'})
  client_id = client_response.json['id']
  
  response = test_client.post('/vehicles', json={
    'color': 'YELLOW',
    'model': 'HATCH',
    'client_id': client_id
  })
  assert response.status_code == 201
  assert response.json['color'] == 'YELLOW'
  assert response.json['model'] == 'HATCH'
  assert response.json['client_id'] == client_id

  delete_client(client_id, test_client)

def delete_client(client_id, test_client):
  response = test_client.delete('/clients/'+client_id)
  assert response.status_code == 204

def test_get_client(test_client):
  client1 = test_client.post('/clients', json={'name': 'Test Client 1'})
  client2 = test_client.post('/clients', json={'name': 'Test Client 2'})
  client1_id = client1.json['id']
  client2_id = client2.json['id']
  check_client1 = test_client.get('/clients/'+client1_id)
  check_client2 = test_client.get('/clients/'+client2_id)

  assert check_client1.status_code == 200
  assert check_client1.json['name'] == 'Test Client 1'
  assert check_client2.status_code == 200
  assert check_client2.json['name'] == 'Test Client 2'

  delete_client(client1_id, test_client)
  delete_client(client2_id, test_client)
  