from flask import Blueprint, request, jsonify
from app import db
from app.exceptions import ClientError
from app.models.vehicle import Vehicle
from app.models.client import Client
from app.schemas.vehicle_schema import vehicle_schema, vehicles_schema
from marshmallow import ValidationError

from app.services.update_sales_opportunity import update_sales_opportunity

bp = Blueprint('vehicle_routes', __name__, url_prefix='/vehicles')

@bp.route('', methods=['POST'])
def create_vehicle():
  try:
    data = request.json
    vehicle_data = vehicle_schema.load(data, session=db.session)
    client_id = str(vehicle_data.client_id)
    client = Client.query.get(client_id)
    if not client:
      raise ClientError('Client not found', 404, 'This Client does not exist!')
    if len(client.vehicles) >= 3:
      return jsonify({'error': 'Client can have at most 3 vehicles'}), 400
    new_vehicle = Vehicle(
      color=vehicle_data.color,
      model=vehicle_data.model,
      client_id=vehicle_data.client_id
    )
    db.session.add(new_vehicle)
    db.session.commit()
    update_sales_opportunity(client)
    return jsonify(vehicle_schema.dump(new_vehicle)), 201
  except ValidationError as err:
    db.session.rollback()
    return jsonify(err.messages), 400
  except ClientError as e:
    db.session.rollback()
    return jsonify(e.to_dict()), e.status
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while creating the vehicle.", "message": str(e)}), 500

@bp.route('', methods=['GET'])
def get_vehicles():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 10, type=int)
  pagination = Vehicle.query.paginate(page=page, per_page=per_page, error_out=False)
  
  vehicles = pagination.items
  total_pages = pagination.pages
  total_items = pagination.total

  return jsonify({
    'vehicles': vehicles_schema.dump(vehicles),
    'page': page,
    'per_page': per_page,
    'total_pages': total_pages,
    'total_items': total_items
  })

@bp.route('/<uuid:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
  vehicle = Vehicle.query.get_or_404(vehicle_id)
  return jsonify(vehicle_schema.dump(vehicle))

@bp.route('/<uuid:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
  try:
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    data = request.json
    vehicle_data = vehicle_schema.load(data, partial=True, session=db.session)
    vehicle.color = vehicle_data.color
    vehicle.model = vehicle_data.model
    db.session.commit()
    return jsonify(vehicle_schema.dump(vehicle))
  except ValidationError as err:
    db.session.rollback()
    return jsonify(err.messages), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while updating the vehicle.", "message": str(e)}), 500

@bp.route('/<uuid:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
  try:
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    client_id = vehicle.client_id
    db.session.delete(vehicle)
    db.session.commit()
    client = Client.query.get_or_404(client_id)
    update_sales_opportunity(client)
    return '', 204
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while deleting the vehicle.", "message": str(e)}), 500
