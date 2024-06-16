from flask import jsonify
from marshmallow import ValidationError
from app import create_app

app = create_app()

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.messages)
    response.status_code = 400
    return response

@app.errorhandler(404)
def resource_not_found(error):
    response = jsonify({"error": "Resource not found"})
    response.status_code = 404
    return response

@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({"error": "Internal server error"})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(debug=True)
