from flask import Blueprint, request, jsonify
from app import db
from app.models.vehicle import Vehicle
from app.models.client import Client
from app.schemas.vehicle_schema import vehicle_schema, vehicles_schema
from marshmallow import ValidationError

bp = Blueprint('vehicle_routes', __name__, url_prefix='/vehicles')

@bp.route('', methods=['POST'])
def create_vehicle():
  try:
    data = request.json
    vehicle_data = vehicle_schema.load(data, session=db.session)
    client = Client.query.get_or_404(vehicle_data.client_id)
    if len(client.vehicles) >= 3:
      return jsonify({'error': 'Client can have at most 3 vehicles'}), 400
    new_vehicle = Vehicle(
      color=vehicle_data.color,
      model=vehicle_data.model,
      client_id=vehicle_data.client_id
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(vehicle_schema.dump(new_vehicle)), 201
  except ValidationError as err:
    return jsonify(err.messages), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while creating the vehicle.", "message": str(e)}), 500

@bp.route('', methods=['GET'])
def get_vehicles():
  vehicles = Vehicle.query.all()
  return jsonify(vehicles_schema.dump(vehicles))

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
    return jsonify(err.messages), 400
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while updating the vehicle.", "message": str(e)}), 500

@bp.route('/<uuid:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
  try:
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": "An error occurred while deleting the vehicle.", "message": str(e)}), 500
