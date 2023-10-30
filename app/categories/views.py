from flask import Blueprint, jsonify, request, url_for
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
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            paginated_categories = Category.query.paginate(page=page, per_page=per_page, error_out=False)
            results = categories_schema.dump(paginated_categories.items)

            meta = {
                'items': results,
                'page': paginated_categories.page,
                'per_page': paginated_categories.per_page,
                'total': paginated_categories.total,
                'pages': paginated_categories.pages,
                'next': url_for('categories.category_api', page=paginated_categories.next_num, per_page=per_page) if paginated_categories.has_next else None,
                'prev': url_for('categories.category_api', page=paginated_categories.prev_num, per_page=per_page) if paginated_categories.has_prev else None,
            }

            return jsonify(**meta)
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