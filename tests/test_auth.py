import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture(scope='module')
def test_client():
  flask_app = create_app('config.TestingConfig')
  testing_client = flask_app.test_client()

  with flask_app.app_context():
    db.create_all()
    yield testing_client
    db.session.remove()
    db.drop_all()

def test_register(test_client):
  response = test_client.post('/auth/register', json={
    'username': 'newuser',
    'password': 'newpassword'
  })
  assert response.status_code == 201

def test_login(test_client):
  test_client.post('/auth/register', json={
    'username': 'loginuser',
    'password': 'loginpassword'
  })
  
  response = test_client.post('/auth/login', json={
    'username': 'loginuser',
    'password': 'loginpassword'
  })
  assert response.status_code == 200
  assert 'access_token' in response.json

def test_protected_route(test_client):
  test_client.post('/auth/register', json={
    'username': 'protecteduser',
    'password': 'protectedpassword'
  })
  login_response = test_client.post('/auth/login', json={
    'username': 'protecteduser',
    'password': 'protectedpassword'
  })
  access_token = login_response.json['access_token']

  headers = {
    'Authorization': f'Bearer {access_token}'
  }
  response = test_client.get('/clients', headers=headers)
  assert response.status_code == 200
