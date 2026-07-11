from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.utils.db import db
from backend.models.models import Book,BorrowRecord,Users
from backend.utils.jwt_utils import admin_required
import datetime

class IssueBook(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data=request.get_json()
        book_id=data.get('book_id')
        user_id=data.get('user_id')

        if not all([book_id,user_id]):
            return {'message':'require all details'},400

        book=Book.query.get(book_id)
        if not book:
            return {'message':'book not found'},404
        
        user=Users.query.get(user_id)
        if not user:
            return {'message':'user not found'},404

        if book.available_copies<=0:
            return {'message':'no copies available'},409

        issue_date=datetime.datetime.now().strftime('%Y-%m-%d')
        due_date=(datetime.datetime.now()+datetime.timedelta(days=14)).strftime('%Y-%m-%d')

        record=BorrowRecord(
            book_id=book_id,
            user_id=user_id,
            issue_date=issue_date,
            due_date=due_date
        )
        book.available_copies-=1
        db.session.add(record)
        db.session.commit()

        return {'message':'book issued successfully','record_id':record.id},201

class ReturnBook(Resource):
    @jwt_required()
    def put(self,record_id):
        record=BorrowRecord.query.get(record_id)
        if not record:
            return {'message':'record not found'},404
        
        if record.status=='returned':
            return {'message':'book already returned'},409

        return_date=datetime.datetime.now().strftime('%Y-%m-%d')
        due=datetime.datetime.strptime(record.due_date,'%Y-%m-%d')
        today=datetime.datetime.now()

        fine=0
        if today>due:
            days_late=(today-due).days
            fine=days_late*1

        record.return_date=return_date
        record.fine_amount=fine
        record.status='returned'

        book=Book.query.get(record.book_id)
        book.available_copies+=1

        db.session.commit()

        return {'message':'book returned successfully','fine_amount':fine},200

class ViewBorrows(Resource):
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        user=Users.query.get(int(user_id))

        if user.role=='admin':
            records=BorrowRecord.query.all()
        else:
            records=BorrowRecord.query.filter_by(user_id=int(user_id)).all()
        
        all_records=[]
        for r in records:
            book=Book.query.get(r.book_id)
            all_records.append({
                'id':r.id,'book_id':r.book_id,'book_title':book.title if book else 'Unknown',
                'user_id':r.user_id,'issue_date':r.issue_date,'due_date':r.due_date,
                'return_date':r.return_date,'fine_amount':r.fine_amount,'status':r.status
            })

        return {'message':'here are the details','all_records':all_records},200

class UserBorrowBook(Resource):
    @jwt_required()
    def post(self):
        user_id=get_jwt_identity()
        data=request.get_json()
        book_id=data.get('book_id')

        if not book_id:
            return {'message':'require book_id'},400

        book=Book.query.get(book_id)
        if not book:
            return {'message':'book not found'},404

        if book.available_copies<=0:
            return {'message':'no copies available'},409

        issue_date=datetime.datetime.now().strftime('%Y-%m-%d')
        due_date=(datetime.datetime.now()+datetime.timedelta(days=14)).strftime('%Y-%m-%d')

        record=BorrowRecord(
            book_id=book_id,
            user_id=int(user_id),
            issue_date=issue_date,
            due_date=due_date
        )
        book.available_copies-=1
        db.session.add(record)
        db.session.commit()

        return {'message':'book borrowed successfully','record_id':record.id},201
