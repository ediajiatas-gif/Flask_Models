from flask import Blueprint

service_tickets_bp = Blueprint('services_tickets_bp', __name__)

from . import routes