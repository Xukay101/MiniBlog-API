# Global Schemas
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import ma
from app.models import User

# User Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(load_only=True)  # Este campo se usa solo para cargar datos

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
