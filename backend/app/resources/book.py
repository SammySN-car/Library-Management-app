from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from backend.utils.db import db
from backend.models.models import Book,BorrowRecord
from backend.utils.jwt_utils import admin_required
from sqlalchemy import text

class AddBook(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data=request.get_json()
        title=data.get('title')
        author=data.get('author')
        isbn=data.get('isbn')
        genre=data.get('genre')
        total_copies=data.get('total_copies')
        price=data.get('price')

        if not all([title,author,isbn,genre,total_copies]):
            return {'message':'require all details'},400
        
        existing=Book.query.filter_by(isbn=isbn).first()
        if existing:
            return {'message':'Book with this ISBN already exists'},409

        book=Book(
            title=title,
            author=author,
            isbn=isbn,
            genre=genre,
            total_copies=total_copies,
            available_copies=total_copies,
            price=price or 0
        )
        db.session.add(book)
        db.session.commit()

        return {'message':'book added successfully'},201

class EditBook(Resource):
    @jwt_required()
    @admin_required
    def put(self,book_id):
        data=request.get_json()
        title=data.get('title')
        author=data.get('author')
        isbn=data.get('isbn')
        genre=data.get('genre')
        total_copies=data.get('total_copies')
        price=data.get('price')

        if not all([title,author,isbn,genre,total_copies]):
            return {'message':'require all details'},400

        book=Book.query.get(book_id)
        if not book:
            return {'message':'book not found'},404

        old_total=book.total_copies
        issued=old_total - book.available_copies

        if total_copies<issued:
            return {'message':'Cannot reduce below currently issued count'},409

        book.title=title
        book.author=author
        book.isbn=isbn
        book.genre=genre
        book.total_copies=total_copies
        book.available_copies=total_copies - issued
        book.price=price or 0

        db.session.commit()
        return {'message':'book updated successfully'},200

    @jwt_required()
    @admin_required
    def get(self,book_id):
        book=Book.query.get(book_id)
        if not book:
            return {'message':'book not found'},404
        book_details={'id':book.id,'title':book.title,'author':book.author,'isbn':book.isbn,'genre':book.genre,'total_copies':book.total_copies,'available_copies':book.available_copies,'price':book.price}
        return {'message':'here are the details','book_details':book_details},200

class DeleteBook(Resource):
    @jwt_required()
    @admin_required
    def delete(self,book_id):
        count=BorrowRecord.query.filter_by(book_id=book_id,status='issued').count()
        if count>0:
            return {'message':'Cannot delete because book has active borrows'},409
        obj=Book.query.filter_by(id=book_id).first()
        if not obj:
            return {'message':'book not found'},404
        db.session.delete(obj)
        db.session.commit()
        return {'message':'book deleted successfully'},200

class ViewBooks(Resource):
    @jwt_required()
    def get(self):
        sql=text("""
            SELECT b.*,
                (SELECT COUNT(*) FROM BORROW_RECORD br WHERE br.book_id = b.id AND br.status = 'issued') AS currently_issued
            FROM BOOK b
        """)
        result=db.session.execute(sql)
        books=[dict(row._mapping) for row in result]
        return {'message':'here are the details','all_books':books},200
