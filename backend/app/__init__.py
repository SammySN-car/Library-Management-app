from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db, User
from werkzeug.security import generate_password_hash

from .resources.auth import SignupResource, LoginResource
from .resources.book import BookListResource, BookResource
from .resources.borrow import BorrowListResource, BorrowResource, UserBorrowResource
from .resources.member import MemberListResource, MemberResource
from .resources.report import ReportResource

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    api = Api(app)
    # Auth
    api.add_resource(SignupResource, '/api/signup')
    api.add_resource(LoginResource, '/api/login')
    
    # Books
    api.add_resource(BookListResource, '/api/books')
    api.add_resource(BookResource, '/api/books/<int:book_id>')
    
    # Borrows
    api.add_resource(BorrowListResource, '/api/borrow')
    api.add_resource(BorrowResource, '/api/borrow/<int:record_id>')
    api.add_resource(UserBorrowResource, '/api/my-books')
    
    # Members (Admin)
    api.add_resource(MemberListResource, '/api/members')
    api.add_resource(MemberResource, '/api/members/<int:user_id>')
    
    # Reports (Admin)
    api.add_resource(ReportResource, '/api/reports')

    with app.app_context():
        db.create_all()
        # Pre-seed Admin if not exists
        if not User.query.filter_by(email='admin@library.com').first():
            admin = User(name='Admin', email='admin@library.com', password_hash=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()

    return app
