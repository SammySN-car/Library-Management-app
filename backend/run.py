from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from backend.utils.db import db
import os
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Mail config (unused/stubs)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# JWT config
app.config['JWT_SECRET_KEY'] = 'this-is-my-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
jwt = JWTManager(app)

# Database config
db_path = os.path.join(os.path.dirname(__file__), 'data', 'library.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)  # ensure the folder exists
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)

from backend.models.models import Users, Book, BorrowRecord

with app.app_context():
    db.create_all()
    print("✅ DB created")
    if not Users.query.filter_by(role='admin').first():
        password_val = 'admin'
        adm = Users(
            full_name='ADMIN',
            email_id="ADMIN@gmail.com",
            password=generate_password_hash(password_val),
            address="ADMINS HOME",
            pincode=110001,
            role='admin'
        )
        db.session.add(adm)
        db.session.commit()
        print("✅ Admin user created")

# Resources
from backend.app.resources.auth import Register, Login
from backend.app.resources.book import AddBook, EditBook, DeleteBook, ViewBooks
from backend.app.resources.borrow import IssueBook, ReturnBook, ViewBorrows, UserBorrowBook
from backend.app.resources.member import ViewMembers
from backend.app.resources.report import AdminReport, UserReport, CSVExport, CSVDownload

api = Api(app)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(AddBook, '/admin/book')
api.add_resource(EditBook, '/admin/book/<int:book_id>')
api.add_resource(DeleteBook, '/admin/book/<int:book_id>')
api.add_resource(ViewBooks, '/books')
api.add_resource(IssueBook, '/admin/issue')
api.add_resource(ReturnBook, '/admin/return/<int:record_id>')
api.add_resource(ViewBorrows, '/borrows')
api.add_resource(UserBorrowBook, '/borrow')
api.add_resource(ViewMembers, '/admin/members')
api.add_resource(AdminReport, '/admin/reports')
api.add_resource(UserReport, '/user/reports')
api.add_resource(CSVExport, '/user/export_csv')
api.add_resource(CSVDownload, '/user/export_csv/<string:file_name>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
