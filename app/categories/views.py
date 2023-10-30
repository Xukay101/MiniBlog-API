from flask import Blueprint, jsonify, request
from flask.views import MethodView

from app import db

bp = Blueprint('categories', __name__)

class CategoryAPI(MethodView):

    def get(self, category_id):
        if category_id is None:
            # Return list of categories 
            return jsonify(message='List of categories')
        else:
            # Return a single category
            return jsonify(message='Get category')

    def post(self):
        # Create a new category
        return jsonify(message='Create new category')

    def delete(self, category_id):
        # Delete a single category
        return jsonify(message='Delete category')

    def put(self, category_id):
        # Update a single category
        return jsonify(message='Update Category')

category_view = CategoryAPI.as_view('category_api')
bp.add_url_rule('/', defaults={'category_id': None}, view_func=category_view, methods=['GET',])
bp.add_url_rule('/', view_func=category_view, methods=['POST',])
bp.add_url_rule('/<int:category_id>/', view_func=category_view, methods=['GET', 'PUT', 'DELETE'])