from flask import Blueprint, request, jsonify
from app import db
from app.models.vehicle import Vehicle
from app.models.client import Client

bp = Blueprint('vehicle_routes', __name__, url_prefix='/vehicles')

@bp.route('', methods=['POST'])
def create_vehicle():
  data = request.json
  client = Client.query.get_or_404(data['client_id'])
  if len(client.vehicles) >= 3:
    return jsonify({'error': 'Client can have at most 3 vehicles'}), 400
  new_vehicle = Vehicle(color=data['color'], model=data['model'], client_id=data['client_id'])
  db.session.add(new_vehicle)
  db.session.commit()
  return jsonify({'id': new_vehicle.id}), 201

@bp.route('', methods=['GET'])
def get_vehicles():
  vehicles = Vehicle.query.all()
  return jsonify([{'id': vehicle.id, 'color': vehicle.color, 'model': vehicle.model, 'client_id': vehicle.client_id} for vehicle in vehicles])

@bp.route('/<uuid:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
  vehicle = Vehicle.query.get_or_404(vehicle_id)
  return jsonify({'id': vehicle.id, 'color': vehicle.color, 'model': vehicle.model, 'client_id': vehicle.client_id})

@bp.route('/<uuid:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
  vehicle = Vehicle.query.get_or_404(vehicle_id)
  data = request.json
  vehicle.color = data.get('color', vehicle.color)
  vehicle.model = data.get('model', vehicle.model)
  db.session.commit()
  return jsonify({'id': vehicle.id, 'color': vehicle.color, 'model': vehicle.model, 'client_id': vehicle.client_id})

@bp.route('/<uuid:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
  vehicle = Vehicle.query.get_or_404(vehicle_id)
  db.session.delete(vehicle)
  db.session.commit()
  return '', 204
