from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from backend.utils.db import db
from backend.models.models import Users,Book,BorrowRecord
from backend.utils.jwt_utils import admin_required
from sqlalchemy import text

class AdminReport(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        genre_sql=text("""
            SELECT genre,COUNT(*) as count FROM BOOK GROUP BY genre
        """)
        genre_result=db.session.execute(genre_sql)
        genre_data=[dict(row._mapping) for row in genre_result]

        overdue_sql=text("""
            SELECT br.*,b.title FROM BORROW_RECORD br
            JOIN BOOK b ON br.book_id=b.id
            WHERE br.status='issued' AND br.due_date<date('now')
        """)
        overdue_result=db.session.execute(overdue_sql)
        overdue_list=[dict(row._mapping) for row in overdue_result]

        fine_sql=text("""
            SELECT SUM(fine_amount) as total_fine FROM BORROW_RECORD WHERE status='returned'
        """)
        fine_result=db.session.execute(fine_sql)
        total_fine=dict(fine_result.fetchone()._mapping)['total_fine'] or 0

        popular_sql=text("""
            SELECT b.title,COUNT(br.id) as borrow_count FROM BORROW_RECORD br
            JOIN BOOK b ON br.book_id=b.id
            GROUP BY br.book_id ORDER BY borrow_count DESC LIMIT 10
        """)
        popular_result=db.session.execute(popular_sql)
        popular_books=[dict(row._mapping) for row in popular_result]

        return {'message':'here are the reports','genre_data':genre_data,'overdue_list':overdue_list,'total_fine':total_fine,'popular_books':popular_books},200

class UserReport(Resource):
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        records=BorrowRecord.query.filter_by(user_id=int(user_id)).all()
        total_borrowed=len(records)
        total_fine=sum(r.fine_amount or 0 for r in records)
        active=len([r for r in records if r.status=='issued'])

        return {'message':'here are the reports','total_borrowed':total_borrowed,'total_fine':total_fine,'active_borrows':active},200

class CSVExport(Resource):
    @jwt_required()
    def get(self):
        import os
        from flask import current_app
        user_id = get_jwt_identity()
        file_name = f"user_{user_id}_export.csv"
        
        # Trigger celery task asynchronously
        try:
            from backend.celery_tasks import export_csv
            task = export_csv.delay(user_id)
            task_id = task.id
        except Exception:
            # Fallback if Celery is not running/configured
            task_id = "dummy_task_id"
            
        return {'message': 'CSV export task started', 'task_id': task_id, 'file_name': file_name}, 202

class CSVDownload(Resource):
    @jwt_required()
    def get(self, file_name):
        import os
        from flask import send_file
        user_id = get_jwt_identity()
        expected_file = f"user_{user_id}_export.csv"

        if file_name != expected_file:
            return {"message": "You are not authenticated for this file"}, 403
        
        # Target path for exported csv inside backend
        exports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'exports'))
        file_path = os.path.join(exports_dir, expected_file)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return {"message": "Either file has not been completed yet or you have not exported the file"}, 404

