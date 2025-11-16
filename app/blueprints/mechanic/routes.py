# from ...blueprints.user import mechanics_bp
from app.blueprints.mechanic import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, db

# Next we create our Mechanic Route
@mechanics_bp.route('', methods=['POST']) #post method to create data 
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
# We need to create a Mechanic Object from our Customer data
    new_mechanic = Mechanics(**data)
    
# Next add Mechanic to session
    db.session.add(new_mechanic)
    
# Last commit to session
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201 #We always want to return

# READ Mechanics
@mechanics_bp.route("", methods=['GET'])
def read_mechanics():
    mechanics = db.session.get(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200
    '''converts/returns object/data into json'''

# READ INDIVIDUAL MECHANIC
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def read_mechanic(mechanic_id):
    '''takes an ID from the url, finds that user in db, and returns their info as json'''
    mechanic = db.session.get(Mechanics, mechanic_id)
    '''goes to db and gets mechanic with this id from Mechanics Model '''
    return mechanic_schema.jsonify(mechanic), 200
    '''converts object/data into json'''
    
# DELETE MECHANIC
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"Error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({
        "message": f"Successfully deleted mechanic: {mechanic.name}"}), 200

# UPDATE A MECHANIC
@mechanics_bp.route('/<int:mechanic>', methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message: Mechanic not found"}), 404
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200