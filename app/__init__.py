from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from app.config import Settings

app = Flask(__name__)
app.config.from_object(Settings)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# Root Endpoint
@app.route('/')
def root():
    return jsonify(message=f'Welcome to {app.config["APP_NAME"]}')

# Registro de Blueprints
from app.auth.views import bp as auth_bp
# from app.users.views import blueprint as users_bp 
# from app.posts.views import blueprint as posts_bp 
# from app.comments.views import blueprint as comments_bp
# from app.categories.views import blueprint as categories_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(users_bp, url_prefix='/users')
# app.register_blueprint(posts_bp, url_prefix='/posts')
# app.register_blueprint(comments_bp, url_prefix='/comments')
# app.register_blueprint(categories_bp, url_prefix='/categories')


# Inicializaciones

