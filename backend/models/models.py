from backend.utils.db import db

class Users(db.Model):
    __tablename__='USERS'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    full_name=db.Column(db.String,nullable=False)
    email_id=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    role=db.Column(db.String,db.CheckConstraint("role in ('admin','user')"),nullable=False,default='user')

    borrow_records=db.relationship('BorrowRecord',backref='user',cascade='all,delete')

class Book(db.Model):
    __tablename__='BOOK'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    isbn=db.Column(db.String,unique=True,nullable=False)
    genre=db.Column(db.String,nullable=False)
    total_copies=db.Column(db.Integer,nullable=False)
    available_copies=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Integer,nullable=False,default=0)

    borrow_records=db.relationship('BorrowRecord',backref='book',cascade='all,delete')

class BorrowRecord(db.Model):
    __tablename__='BORROW_RECORD'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    book_id=db.Column(db.Integer,db.ForeignKey('BOOK.id',ondelete='CASCADE'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('USERS.id',ondelete='CASCADE'),nullable=False)
    issue_date=db.Column(db.String,nullable=False)
    due_date=db.Column(db.String,nullable=False)
    return_date=db.Column(db.String)
    fine_amount=db.Column(db.Integer,default=0)
    status=db.Column(db.String,db.CheckConstraint("status in ('issued','returned','overdue')"),nullable=False,default='issued')
