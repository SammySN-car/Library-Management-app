from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime, timedelta
from ..models import db, Book, BorrowRecord, User

def is_admin():
    claims = get_jwt()
    return claims.get('role') == 'admin'

class BorrowListResource(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
            
        records = BorrowRecord.query.all()
        result = []
        for r in records:
            result.append({
                'id': r.id,
                'user_id': r.user_id,
                'user_name': r.user.name,
                'book_id': r.book_id,
                'book_title': r.book.title,
                'issue_date': r.issue_date.isoformat() if r.issue_date else None,
                'due_date': r.due_date.isoformat() if r.due_date else None,
                'return_date': r.return_date.isoformat() if r.return_date else None,
                'status': r.status,
                'fine_amount': r.fine_amount
            })
        return {'message': 'Records retrieved', 'data': result}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        book_id = data.get('book_id')
        
        # If admin is issuing, they provide user_id. If user is borrowing, use their JWT identity.
        user_id = data.get('user_id') if is_admin() else get_jwt_identity()

        if not book_id or not user_id:
            return {'message': 'book_id and user_id are required'}, 400

        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
            
        if book.available_copies <= 0:
            return {'message': 'Book is not available'}, 409

        # User shouldn't borrow the same book twice if they haven't returned it
        existing = BorrowRecord.query.filter_by(user_id=user_id, book_id=book_id, status='issued').first()
        if existing:
            return {'message': 'User already has this book issued'}, 409

        # 14 days borrow period
        due_date = datetime.utcnow() + timedelta(days=14)

        record = BorrowRecord(
            user_id=user_id,
            book_id=book_id,
            due_date=due_date,
            status='issued'
        )
        book.available_copies -= 1

        db.session.add(record)
        db.session.commit()
        return {'message': 'Book issued successfully', 'data': {'id': record.id}}, 201


class BorrowResource(Resource):
    @jwt_required()
    def put(self, record_id):
        # Admin or the user themselves can return
        record = BorrowRecord.query.get(record_id)
        if not record:
            return {'message': 'Record not found'}, 404

        current_user_id = get_jwt_identity()
        if not is_admin() and record.user_id != current_user_id:
            return {'message': 'Unauthorized to return this book'}, 403

        if record.status == 'returned':
            return {'message': 'Book already returned'}, 409

        record.status = 'returned'
        record.return_date = datetime.utcnow()
        
        # Free up the book
        book = Book.query.get(record.book_id)
        if book:
            book.available_copies += 1

        db.session.commit()
        return {'message': 'Book returned successfully'}, 200


class UserBorrowResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        records = BorrowRecord.query.filter_by(user_id=user_id).all()
        result = []
        for r in records:
            result.append({
                'id': r.id,
                'book_id': r.book_id,
                'book_title': r.book.title,
                'issue_date': r.issue_date.isoformat() if r.issue_date else None,
                'due_date': r.due_date.isoformat() if r.due_date else None,
                'return_date': r.return_date.isoformat() if r.return_date else None,
                'status': r.status,
                'fine_amount': r.fine_amount
            })
        return {'message': 'My books retrieved', 'data': result}, 200
