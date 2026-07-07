from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from ..models import db, Book

def is_admin():
    claims = get_jwt()
    return claims.get('role') == 'admin'

class BookListResource(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.all()
        result = []
        for b in books:
            result.append({
                'id': b.id,
                'title': b.title,
                'author': b.author,
                'isbn': b.isbn,
                'genre': b.genre,
                'total_copies': b.total_copies,
                'available_copies': b.available_copies
            })
        return {'message': 'Books retrieved successfully', 'data': result}, 200

    @jwt_required()
    def post(self):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
            
        data = request.get_json()
        
        # Check if ISBN exists
        if Book.query.filter_by(isbn=data.get('isbn')).first():
            return {'message': 'Book with this ISBN already exists'}, 409

        book = Book(
            title=data.get('title'),
            author=data.get('author'),
            isbn=data.get('isbn'),
            genre=data.get('genre'),
            total_copies=data.get('total_copies', 1),
            available_copies=data.get('total_copies', 1)
        )
        db.session.add(book)
        db.session.commit()
        return {'message': 'Book added successfully', 'data': {'id': book.id}}, 201


class BookResource(Resource):
    @jwt_required()
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
            
        return {
            'message': 'Book retrieved successfully',
            'data': {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isbn': book.isbn,
                'genre': book.genre,
                'total_copies': book.total_copies,
                'available_copies': book.available_copies
            }
        }, 200

    @jwt_required()
    def put(self, book_id):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
            
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        data = request.get_json()
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.isbn = data.get('isbn', book.isbn)
        book.genre = data.get('genre', book.genre)
        
        # Adjust available copies if total copies changed
        new_total = data.get('total_copies', book.total_copies)
        diff = new_total - book.total_copies
        book.total_copies = new_total
        book.available_copies = book.available_copies + diff

        db.session.commit()
        return {'message': 'Book updated successfully'}, 200

    @jwt_required()
    def delete(self, book_id):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
            
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
            
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}, 200
