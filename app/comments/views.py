from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.schemas import comment_schema, comments_schema
from app.models import Post
from app.utils import is_valid_uuid

bp = Blueprint('comments', __name__)

class CommentAPI(MethodView):

    def get(self, post_id, comment_id=None):
        if comment_id is None:
            # Return list of comments for a specific post
            return jsonify(message=f'List of Comments for Post {post_id}')
        else:
            # Return a single comment
            if not is_valid_uuid(post_id):
                return jsonify(error=f'Invalid Post UUID {post_id}'), 400

            if not is_valid_uuid(comment_id):
                return jsonify(error=f'Invalid Comment UUID {comment_id}'), 400

            return jsonify(message=f'Get Comment {comment_id} for Post {post_id}')

    @jwt_required()
    def post(self, post_id):
        ''' Create a new comment for a specific post '''
        if not is_valid_uuid(post_id):
            return jsonify(error=f'Invalid Post UUID {post_id}'), 400

        comment_data = request.json
        if not comment_data:
            return jsonify(error=f'Not input data provided.'), 404

        # Check if post found
        post_found = Post.query.get(post_id)
        if not post_found:
            return jsonify(error=f'Post {post_id} not found.'), 404

        try:
            new_comment = comment_schema.load(comment_data)
            new_comment.post_id = post_id
            new_comment.user_id = current_user.id
            db.session.add(new_comment)
            db.session.commit()
            return comment_schema.dump(new_comment), 201 # 201 Created 
        except ValidationError as err:
            return jsonify(err.messages), 400
        except IntegrityError:
            db.session.rollback()  # Rollback en caso de error
            return jsonify(error=f'Error creating comment'), 40

    @jwt_required()
    def delete(self, post_id, comment_id):
        # Delete a single comment
        return jsonify(message=f'Delete Comment {comment_id} for Post {post_id}')

    @jwt_required()
    def put(self, post_id, comment_id):
        # Update a single comment
        return jsonify(message=f'Update Comment {comment_id} for Post {post_id}')


comment_view = CommentAPI.as_view('comment_api')
bp.add_url_rule('/<string:post_id>/comments/', defaults={'comment_id': None}, view_func=comment_view, methods=['GET',])
bp.add_url_rule('/<string:post_id>/comments/', view_func=comment_view, methods=['POST',])
bp.add_url_rule('/<string:post_id>/comments/<string:comment_id>/', view_func=comment_view, methods=['GET', 'PUT', 'DELETE'])
