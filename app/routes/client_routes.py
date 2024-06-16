from flask import Blueprint, request, jsonify
from app import db
from app.models.client import Client
from app.schemas.client_schema import client_schema, clients_schema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

bp = Blueprint('client_routes', __name__, url_prefix='/clients')

@bp.route('', methods=['POST'])
@jwt_required()
def create_client():
  try:
    data = request.json
    new_client = Client(name=data['name'])
    db.session.add(new_client)
    db.session.commit()
    return jsonify(client_schema.dump(new_client)), 201
  except ValidationError as err:
    return jsonify(err.messages), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while creating the client.", "message": str(e)}), 500

@bp.route('', methods=['GET'])
@jwt_required()
def get_clients():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 10, type=int)
  pagination = Client.query.paginate(page=page, per_page=per_page, error_out=False)
  
  clients = pagination.items
  total_pages = pagination.pages
  total_items = pagination.total

  return jsonify({
    'clients': clients_schema.dump(clients),
    'page': page,
    'per_page': per_page,
    'total_pages': total_pages,
    'total_items': total_items
  })

@bp.route('/<uuid:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
  client = db.session.get(Client, client_id)
  if client is None:
    return jsonify({'error': 'Client not found'}), 404
  return jsonify(client_schema.dump(client))

@bp.route('/<uuid:client_id>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
def delete_client(client_id):
  try:
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return '', 204
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while deleting the client.", "message": str(e)}), 500
