# from ...extensions import ma
from marshmallow import fields
from app.extensions import ma
from app.models import Customers

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers #We create a schema that validates the data as defined by our Customers Model        
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)