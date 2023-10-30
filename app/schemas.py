# Global Schemas
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import ma
from app.models import User, Post, Category, Comment

# User Schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    id = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    password = fields.String(load_only=True)  # Este campo se usa solo para cargar datos

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at', 'updated_at'] 
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Post Schemas
class PostSchema(ma.SQLAlchemyAutoSchema):
    id = fields.String(dump_only=True)
    comments = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    user_id = fields.String(dump_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user_id', 'categories', 'comments', 'created_at', 'updated_at']
        load_instance = True

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# Category Schemas
class CategorySchema(ma.SQLAlchemyAutoSchema):
    id = fields.String(dump_only=True)
    posts = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'posts', 'created_at', 'updated_at']
        load_instance = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

# Comment Schemas
class CommentSchema(ma.SQLAlchemyAutoSchema):
    id = fields.String(dump_only=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
    user_id = fields.String(dump_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_id', 'post_id', 'created_at', 'updated_at']
        load_instance = True

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
