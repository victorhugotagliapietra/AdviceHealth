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

@pytest.fixture(scope='module')
def init_database(test_client):
    with test_client.application.app_context():
      client1 = Client(name='Test Client 1')
      client2 = Client(name='Test Client 2')
      db.session.add(client1)
      db.session.add(client2)
      db.session.commit()

      yield db
      
      db.session.remove()
