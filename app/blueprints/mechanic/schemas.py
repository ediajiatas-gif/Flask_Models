# from ...extensions import ma
from app.extensions import ma
from app.models import Mechanics

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics #We create a schema that validates the data as defined by our Mechanics Model
        
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)