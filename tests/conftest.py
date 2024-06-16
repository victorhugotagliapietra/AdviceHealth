import pytest
from app import create_app, db
from app.models.user import User
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def test_client():
  flask_app = create_app('config.TestingConfig')
  testing_client = flask_app.test_client()

  with flask_app.app_context():
    db.create_all()
    user = User(username='testuser')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()
    yield testing_client
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='module')
def auth_header(test_client):
  with test_client.application.app_context():
    user = User.query.filter_by(username='testuser').first()
    access_token = create_access_token(identity=str(user.id))
    return {'Authorization': f'Bearer {access_token}'}
