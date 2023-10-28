from flask import request, jsonify, Blueprint, current_app
from flask.views import MethodView

bp = Blueprint('auth', __name__)

class LoginAPI(MethodView):
    def get(self):
        return jsonify(message='Hello World Auth Mdl')

bp.add_url_rule('/login', view_func=LoginAPI.as_view('login_api'), methods=['GET'])