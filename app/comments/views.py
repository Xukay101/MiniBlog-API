from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, current_user

from app import db
from app.schemas import comment_schema, comments_schema

bp = Blueprint('comments', __name__)

class CommentAPI(MethodView):

    def get(self, post_id, comment_id=None):
        if comment_id is None:
            # Return list of comments for a specific post
            return jsonify(message=f'List of Comments for Post {post_id}')
        else:
            # Return a single comment
            return jsonify(message=f'Get Comment {comment_id} for Post {post_id}')

    @jwt_required
    def post(self, post_id):
        # Create a new comment for a specific post
        return jsonify(message=f'Create new Comment for Post {post_id}')

    @jwt_required
    def delete(self, post_id, comment_id):
        # Delete a single comment
        return jsonify(message=f'Delete Comment {comment_id} for Post {post_id}')

    @jwt_required
    def put(self, post_id, comment_id):
        # Update a single comment
        return jsonify(message=f'Update Comment {comment_id} for Post {post_id}')


comment_view = CommentAPI.as_view('comment_api')
bp.add_url_rule('/<int:post_id>/comments/', defaults={'comment_id': None}, view_func=comment_view, methods=['GET',])
bp.add_url_rule('/<int:post_id>/comments/', view_func=comment_view, methods=['POST',])
bp.add_url_rule('/<int:post_id>/comments/<int:comment_id>/', view_func=comment_view, methods=['GET', 'PUT', 'DELETE'])
