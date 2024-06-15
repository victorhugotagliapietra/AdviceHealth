from app.models.vehicle import Vehicle
from app import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class VehicleSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Vehicle
    include_fk = True
    load_instance = True
    sqla_session = db.session
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)
