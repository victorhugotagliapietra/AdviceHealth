import pytest
from app import db
from app.models.client import Client
from app.models.vehicle import Vehicle

def test_create_vehicle(test_client):
  client = Client.query.first()
  response = test_client.post('/vehicles', json={
      'color': 'YELLOW',
      'model': 'HATCH',
      'client_id': client.id
  })
  assert response.status_code == 201
  assert response.json['color'] == 'YELLOW'
  assert response.json['model'] == 'HATCH'
  assert response.json['client_id'] == str(client.id)

def test_get_vehicle(test_client):
  client = Client.query.first()
  vehicle = Vehicle(
    color='BLUE',
    model='SEDAN',
    client_id=client.id
  )
  db.session.add(vehicle)
  db.session.commit()

  response = test_client.get(f'/vehicles/{vehicle.id}')
  assert response.status_code == 200
  assert response.json['color'] == vehicle.color
  assert response.json['model'] == vehicle.model

def test_update_vehicle(test_client):
  client = Client.query.first()
  vehicle = Vehicle(
    color='GRAY',
    model='CONVERTIBLE',
    client_id=client.id
  )
  db.session.add(vehicle)
  db.session.commit()

  response = test_client.put(f'/vehicles/{vehicle.id}', json={'color': 'BLUE', 'model': 'SEDAN'})
  assert response.status_code == 200
  assert response.json['color'] == 'BLUE'
  assert response.json['model'] == 'SEDAN'

def test_delete_vehicle(test_client):
  client = Client.query.first()
  vehicle = Vehicle(
    color='GRAY',
    model='CONVERTIBLE',
    client_id=client.id
  )
  db.session.add(vehicle)
  db.session.commit()

  response = test_client.delete(f'/vehicles/{vehicle.id}')
  assert response.status_code == 204
  assert Vehicle.query.get(vehicle.id) is None
