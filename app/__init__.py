from functools import wraps

import redis
from flask import Flask, jsonify, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.config import Settings

app = Flask(__name__)
app.config.from_object(Settings)

# Connections
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
redis_conn = redis.StrictRedis.from_url(app.config['REDIS_URL'], decode_responses=True)

# Root Endpoint
@app.route('/')
def root():
    return jsonify(message=f'Welcome to {app.config["APP_NAME"]}')

# Depends 
def require_admin_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('admin-api-key') and request.headers.get('admin-api-key') == app.config['ADMIN_API_KEY']:
            return view_function(*args, **kwargs)
        else:
            return jsonify(message='Unauthorized'), 401
    return decorated_function

# Blueprints
from app.auth.views import bp as auth_bp
from app.posts.views import bp as posts_bp 
from app.categories.views import bp as categories_bp
from app.comments.views import bp as comments_bp
# from app.users.views import bp as users_bp 

app.register_blueprint(auth_bp, url_prefix=f'{app.config["APP_ROOT"]}/auth')
app.register_blueprint(posts_bp, url_prefix=f'{app.config["APP_ROOT"]}/posts')
app.register_blueprint(categories_bp, url_prefix=f'{app.config["APP_ROOT"]}/categories')
app.register_blueprint(comments_bp, url_prefix=f'{app.config["APP_ROOT"]}/posts')
# app.register_blueprint(users_bp, url_prefix=f'{app.config["APP_ROOT"]}/users')