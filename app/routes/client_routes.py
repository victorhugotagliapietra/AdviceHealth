from flask import Blueprint, request, jsonify
from app import db
from app.models.client import Client
from app.models.vehicle import Vehicle

bp = Blueprint('client_routes', __name__, url_prefix='/clients')

@bp.route('', methods=['POST'])
def create_client():
    data = request.json
    new_client = Client(name=data['name'])
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'id': new_client.id}), 201

@bp.route('', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    response = []
    for client in clients:
        vehicles = [{'id': vehicle.id, 'color': vehicle.color, 'model': vehicle.model} for vehicle in client.vehicles]
        client_data = {
            'id': client.id,
            'name': client.name,
            'sales_opportunity': client.sales_opportunity,
            'vehicles': vehicles
        }
        response.append(client_data)
    return jsonify(response)

@bp.route('/<uuid:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    vehicles = [{'id': vehicle.id, 'color': vehicle.color, 'model': vehicle.model} for vehicle in client.vehicles]
    client_data = {
        'id': client.id,
        'name': client.name,
        'sales_opportunity': client.sales_opportunity,
        'vehicles': vehicles
    }
    return jsonify(client_data)

@bp.route('/<uuid:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.json
    client.name = data.get('name', client.name)
    db.session.commit()
    return jsonify({'id': client.id, 'name': client.name, 'sales_opportunity': client.sales_opportunity})

@bp.route('/<uuid:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return '', 204
