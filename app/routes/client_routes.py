from flask import Blueprint, request, jsonify
from app import db
from app.models.client import Client
from app.schemas.client_schema import client_schema, clients_schema
from marshmallow import ValidationError

bp = Blueprint('client_routes', __name__, url_prefix='/clients')

@bp.route('', methods=['POST'])
def create_client():
  try:
    data = request.json
    client_data = client_schema.load(data, session=db.session)
    new_client = Client(name=client_data.name)
    db.session.add(new_client)
    db.session.commit()
    return jsonify(client_schema.dump(new_client)), 201
  except ValidationError as err:
    return jsonify(err.messages), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while creating the client.", "message": str(e)}), 500

@bp.route('', methods=['GET'])
def get_clients():
  clients = Client.query.all()
  return jsonify(clients_schema.dump(clients))

@bp.route('/<uuid:client_id>', methods=['GET'])
def get_client(client_id):
  client = Client.query.get_or_404(client_id)
  return jsonify(client_schema.dump(client))

@bp.route('/<uuid:client_id>', methods=['PUT'])
def update_client(client_id):
  try:
    client = Client.query.get_or_404(client_id)
    data = request.json
    client_data = client_schema.load(data, partial=True, session=db.session)
    client.name = client_data.name
    db.session.commit()
    return jsonify(client_schema.dump(client))
  except ValidationError as err:
    return jsonify(err.messages), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while updating the client.", "message": str(e)}), 500

@bp.route('/<uuid:client_id>', methods=['DELETE'])
def delete_client(client_id):
  try:
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return '', 204
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while deleting the client.", "message": str(e)}), 500
