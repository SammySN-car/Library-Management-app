from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func
from ..models import db, BorrowRecord, Book

def is_admin():
    claims = get_jwt()
    return claims.get('role') == 'admin'

class ReportResource(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {'message': 'Admin access required'}, 403

        # 1. Overdue list
        overdue_records = BorrowRecord.query.filter_by(status='overdue').all()
        overdue_list = [{
            'id': r.id,
            'user_name': r.user.name,
            'book_title': r.book.title,
            'fine_amount': r.fine_amount
        } for r in overdue_records]

        # 2. Total fine collected (status can be returned but fine paid, simplified here by sum of fine_amount)
        total_fines = db.session.query(func.sum(BorrowRecord.fine_amount)).scalar() or 0.0

        # 3. Popular titles (group by book_id, count)
        popular = db.session.query(
            BorrowRecord.book_id, 
            func.count(BorrowRecord.id).label('borrow_count')
        ).group_by(BorrowRecord.book_id).order_by(func.count(BorrowRecord.id).desc()).limit(5).all()

        popular_titles = []
        for p in popular:
            b = Book.query.get(p.book_id)
            if b:
                popular_titles.append({'title': b.title, 'borrows': p.borrow_count})

        return {
            'message': 'Report retrieved successfully',
            'data': {
                'overdue_list': overdue_list,
                'total_fines_collected': total_fines,
                'popular_titles': popular_titles
            }
        }, 200
