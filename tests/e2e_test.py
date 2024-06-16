def test_end_to_end(test_client, auth_header):
  # Create a new client
  client_response = test_client.post('/clients', json={'name': 'E2E Client'}, headers=auth_header)
  assert client_response.status_code == 201
  client_id = client_response.json['id']

  # Create a vehicle for the client
  vehicle_response = test_client.post('/vehicles', json={
    'color': 'GRAY',
    'model': 'CONVERTIBLE',
    'client_id': client_id
  }, headers=auth_header)
  assert vehicle_response.status_code == 201
  vehicle_id = vehicle_response.json['id']

  # Get the client
  get_client_response = test_client.get(f'/clients/{client_id}', headers=auth_header)
  assert get_client_response.status_code == 200
  assert get_client_response.json['name'] == 'E2E Client'
  assert len(get_client_response.json['vehicles']) == 1

  # Update the client
  update_client_response = test_client.put(f'/clients/{client_id}', json={'name': 'Updated E2E Client'}, headers=auth_header)
  assert update_client_response.status_code == 200
  assert update_client_response.json['name'] == 'Updated E2E Client'

  # Get the vehicle
  get_vehicle_response = test_client.get(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert get_vehicle_response.status_code == 200
  assert get_vehicle_response.json['color'] == 'GRAY'

  # Update the vehicle
  update_vehicle_response = test_client.put(f'/vehicles/{vehicle_id}', json={
    'color': 'BLUE',
    'model': 'SEDAN',
    'client_id': client_id
  }, headers=auth_header)
  assert update_vehicle_response.status_code == 200
  assert update_vehicle_response.json['color'] == 'BLUE'

  # Delete the vehicle
  delete_vehicle_response = test_client.delete(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert delete_vehicle_response.status_code == 204

  # Delete the client
  delete_client_response = test_client.delete(f'/clients/{client_id}', headers=auth_header)
  assert delete_client_response.status_code == 204

  # Verify the client has been deleted
  get_client_after_delete_response = test_client.get(f'/clients/{client_id}', headers=auth_header)
  assert get_client_after_delete_response.status_code == 404

  # Verify the vehicle has been deleted
  get_vehicle_after_delete_response = test_client.get(f'/vehicles/{vehicle_id}', headers=auth_header)
  assert get_vehicle_after_delete_response.status_code == 404
