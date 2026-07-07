from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from .resources.auth import SignupResource, LoginResource

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    api = Api(app)
    api.add_resource(SignupResource, '/api/signup')
    api.add_resource(LoginResource, '/api/login')

    with app.app_context():
        db.create_all()

    return app
