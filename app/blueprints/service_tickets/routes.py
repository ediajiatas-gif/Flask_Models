# from ...blueprints.user import service_tickets_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.models import Mechanics, Service_tickets, db
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError

# POST '/': Pass in all the required information to create the service_ticket.

@service_tickets_bp.route("", methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_tickets(**data)
    
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

# PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: Adds a relationship between a service ticket and the mechanics. (Reminder: use your relationship attributes! They allow you the treat the relationship like a list, able to append a Mechanic to the mechanics list).

@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_tickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not ticket or not mechanic:
        return jsonify({"message": "Mechanic or Service ticket not found"}), 404
    
    if mechanic in ticket.service_ticket_mechanic:
        return jsonify({"message": "Mechanic already assigned to this ticket."}), 400
    
    ticket.service_ticket_mechanic.append(mechanic)
    db.session.commit()
    
    return jsonify({"message": "Mechanic successfully assigned"}), 200


# PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: Removes the relationship from the service ticket and the mechanic.

@service_tickets_bp.route("/<int:ticket_id>/unassign-mechanic/<int:mechanic_id>", methods=['DELETE'])
def unassign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_tickets, ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not ticket or not mechanic:
        return jsonify({"message": "Mechanic or Service Ticket not found"}), 404
    
    if not mechanic in ticket.service_ticket_mechanic:
        return jsonify ({"message": "Mechanic not assigned to this ticket"}), 400
    
    ticket.service_ticket_mechanic.remove(mechanic)
    db.session.commit()
    
    return jsonify({"message": "Mechanic successfully unassigned."}), 200
    
    

# GET '/': Retrieves all service tickets.

@service_tickets_bp.route("", methods=['GET'])
def read_service_tickets():
    service_tickets = db.session.query(Service_tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200