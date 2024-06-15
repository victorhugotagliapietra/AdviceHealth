from app import db

def update_sales_opportunity(client):
  if client.vehicles:
    client.sales_opportunity = False
  else:
    client.sales_opportunity = True
  db.session.commit() 