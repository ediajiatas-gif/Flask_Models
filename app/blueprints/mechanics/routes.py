# from ...blueprints.user import mechanics_bp
from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.util import encode_token, token_required

@mechanics_bp.route("/login", methods=['POST'])
@limiter.limit("5 per 10 minute")
def login():
    try:
        data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic = db.session.query(Mechanics).where(Mechanics.email==data['email']).first()
    
    if mechanic and check_password_hash(mechanic.password, data['password']):
        token = encode_token(mechanic.id)
        return jsonify({
            "message": f"Welcome {mechanic.first_name}",
            "token": token,
        }), 200
    
    return jsonify({"Error": "Invalid email or password"}), 401

# Next we create our Mechanic Route
@mechanics_bp.route('', methods=['POST']) #post method to create data
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #resets password key's value to the hash of current value
    data["password"] = generate_password_hash(data["password"])
    
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
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200
    '''converts/returns object/data into json'''

# READ INDIVIDUAL MECHANIC
@mechanics_bp.route('/profile', methods=['GET'])
@token_required
@limiter.limit("15 per hour")
def read_mechanic():
    mechanic_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    return mechanic_schema.jsonify(mechanic), 200

    
# UPDATE A MECHANIC
@mechanics_bp.route('', methods=['PUT'])
@token_required
def update_mechanic():
    mechanic_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    mechanic_data["password"] = generate_password_hash(mechanic_data["password"])
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200    
    
    
# DELETE MECHANIC
@mechanics_bp.route('', methods=['DELETE'])
@token_required
def delete_mechanic():
    token_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, token_id)

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted mechanic: {token_id}"}), 200

