from flask import Blueprint, jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db, require_admin_key
from app.schemas import category_schema, categories_schema
from app.models import Category

bp = Blueprint('categories', __name__)

class CategoryAPI(MethodView):

    def get(self, category_id):
        if category_id is None:
            # Return list of categories 
            return jsonify(message='List of categories')
        else:
            # Return a single category
            category = Category.query.get(category_id)
            if not category:
                return jsonify(error=f'Category {category_id} not found.'), 404
            return category_schema.dump(category), 200

    @require_admin_key
    def post(self):
        ''' Create a new category '''
        category_data = request.json
        if not category_data:
            return jsonify(error='Not input data provided.'), 400

        try:
            new_category = category_schema.load(category_data)
            db.session.add(new_category)
            db.session.commit()
            return category_schema.dump(new_category), 201 # 201 Created 
        except ValidationError as err:
            return jsonify(err.messages), 400
        except IntegrityError:
            db.session.rollback()  # Rollback en caso de error
            return jsonify(message=f'Category {category_data["name"]} already exist'), 400

    @require_admin_key
    def delete(self, category_id):
        ''' Delete a single category'''
        category = Category.query.get(category_id)
        if not category:
            return jsonify(error=f'Category {category_id} not found.'), 404

        db.session.delete(category)
        db.session.commit()

        return jsonify(message='Category delete sucesfully.'), 200

    @require_admin_key
    def put(self, category_id):
        ''' Update a single category'''
        category_data = request.json
        if not category_data:
            return jsonify(error='Not input data provided.'), 400

        category = Category.query.get(category_id)
        if not category:
            return jsonify(error=f'Category {category_id} not found.'), 404

        try:
            updated_category = category_schema.load(category_data, instance=category, partial=True)
            db.session.commit()
            return category_schema.dump(updated_category), 200
        except ValidationError as err:
            return jsonify(err.messages), 400

category_view = CategoryAPI.as_view('category_api')
bp.add_url_rule('/', defaults={'category_id': None}, view_func=category_view, methods=['GET',])
bp.add_url_rule('/', view_func=category_view, methods=['POST',])
bp.add_url_rule('/<int:category_id>/', view_func=category_view, methods=['GET', 'PUT', 'DELETE'])