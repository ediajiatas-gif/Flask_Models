# from ...blueprints.user import customers_bp
from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db



# Create our Create Customer Route
@customers_bp.route('', methods=['POST']) #post method to create data 
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
# We need to create a Customer Object from our Customer data
    new_customer = Customers(**data)
    
# Next add Customer to session
    db.session.add(new_customer)
    
# Last commit to session
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201 