from app.models.client import Client
from app import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ClientSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Client
    include_relationships = True
    load_instance = True
    sqla_session = db.session

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
