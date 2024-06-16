import pytest
from app import create_app, db
from app.models.client import Client
from app.models.vehicle import Vehicle

@pytest.fixture(scope='module')
def test_client():
  flask_app = create_app('config.TestingConfig')
  testing_client = flask_app.test_client()

  with flask_app.app_context():
    db.create_all()
    yield testing_client
    db.session.remove()


def test_end_to_end(test_client):
  # Create a new client
  client_response = test_client.post('/clients', json={'name': 'e2e Client'})
  client_id = client_response.json['id']
  assert client_response.status_code == 201

  # Create a new vehicle for the client
  vehicle_response = test_client.post('/vehicles', json={
    'color': 'GRAY',
    'model': 'SEDAN',
    'client_id': client_id
  })
  assert vehicle_response.status_code == 201

  # Get the client and check the sales_opportunity status
  get_client_response = test_client.get(f'/clients/{client_id}')
  assert get_client_response.status_code == 200
  assert get_client_response.json['sales_opportunity'] == False

  # Delete the vehicle
  vehicle_id = vehicle_response.json['id']
  delete_vehicle_response = test_client.delete(f'/vehicles/{vehicle_id}')
  assert delete_vehicle_response.status_code == 204

  # Check the client again
  get_client_response = test_client.get(f'/clients/{client_id}')
  assert get_client_response.status_code == 200
  assert get_client_response.json['sales_opportunity'] == True
