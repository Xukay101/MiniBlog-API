from flask import Blueprint, jsonify, request, url_for
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required 
from marshmallow import ValidationError

from app import db
from app.schemas import post_schema, posts_schema
from app.models import Post, Category
from app.utils import is_valid_uuid

bp = Blueprint('posts', __name__)

class PostAPI(MethodView):

    def get(self, post_id):
        if post_id is None:
            # Return list of posts
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            paginated_posts = Post.query.paginate(page=page, per_page=per_page, error_out=False)
            results = posts_schema.dump(paginated_posts.items)

            meta = {
                'items': results,
                'page': paginated_posts.page,
                'per_page': paginated_posts.per_page,
                'total': paginated_posts.total,
                'pages': paginated_posts.pages,
                'next': url_for('posts.post_api', page=paginated_posts.next_num, per_page=per_page) if paginated_posts.has_next else None,
                'prev': url_for('posts.post_api', page=paginated_posts.prev_num, per_page=per_page) if paginated_posts.has_prev else None,
            }

            return jsonify(**meta)
        else:
            # Return a single post
            if not is_valid_uuid(post_id):
                return jsonify(error=f'Invalid Post UUID {post_id}'), 400

            post = Post.query.get(post_id)
            if not post:
                return jsonify(error=f'Post {post_id} not found.'), 404
            return post_schema.dump(post), 200

    @jwt_required()
    def post(self):
        ''' Create a new post '''
        post_data = request.json
        if not post_data:
            return jsonify(error='Not input data provided.'), 400

        category_ids = post_data.get('categoryIds', [])

        # Check if categories is empty
        if not category_ids:
            return jsonify(error='At least one category is required.'), 400

        # Check if id's are valid
        for category_uuid in category_ids:
            if not is_valid_uuid(category_uuid):
                return jsonify(error='At least one category id is invalid.'), 400

        existing_categories = Category.query.filter(Category.id.in_(category_ids)).all()
        if len(existing_categories) != len(category_ids):
            return jsonify(error='One or more category IDs do not exist.'), 400

        try:
            post = post_schema.load(post_data)
            post.user_id = current_user.id
            post.categories = existing_categories
            db.session.add(post)
            db.session.commit()
            return post_schema.dump(post), 201 # 201 Created 
        except ValidationError as err:
            return jsonify(err.messages), 400

    @jwt_required()
    def delete(self, post_id):
        ''' Delete a single post '''
        if not is_valid_uuid(post_id):
            return jsonify(error=f'Invalid Post UUID {post_id}'), 400

        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404

        # Check if is owner
        if post.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        db.session.delete(post)
        db.session.commit()

        return jsonify(message='Post delete sucesfully.'), 200

    @jwt_required()
    def put(self, post_id):
        ''' Update a single post '''
        if not is_valid_uuid(post_id):
            return jsonify(error=f'Invalid Post UUID {post_id}'), 400

        post_data = request.json
        if not post_data:
            return jsonify(error='No input data provided.'), 400

        post = Post.query.get(post_id)
        if not post:
            return jsonify(error=f'Post {post_id} not found.'), 404

        # Check if is owner
        if post.user_id != current_user.id:
            return jsonify(error='Forbidden'), 403

        try:
            updated_post = post_schema.load(post_data, instance=post, partial=True)
            db.session.commit()
            return post_schema.dump(updated_post), 200
        except ValidationError as err:
            return jsonify(err.messages), 400

post_view = PostAPI.as_view('post_api')
bp.add_url_rule('/', defaults={'post_id': None}, view_func=post_view, methods=['GET',])
bp.add_url_rule('/', view_func=post_view, methods=['POST',])
bp.add_url_rule('/<string:post_id>/', view_func=post_view, methods=['GET', 'PUT', 'DELETE'])