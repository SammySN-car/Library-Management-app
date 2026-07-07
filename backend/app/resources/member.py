from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from ..models import db, User

def is_admin():
    claims = get_jwt()
    return claims.get('role') == 'admin'

class MemberListResource(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
            
        users = User.query.filter_by(role='user').all()
        result = []
        for u in users:
            result.append({
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'is_active': u.is_active,
                'created_at': u.created_at.isoformat() if u.created_at else None
            })
        return {'message': 'Members retrieved', 'data': result}, 200


class MemberResource(Resource):
    @jwt_required()
    def put(self, user_id):
        if not is_admin():
            return {'message': 'Admin access required'}, 403
            
        user = User.query.get(user_id)
        if not user or user.role != 'user':
            return {'message': 'Member not found'}, 404
            
        data = request.get_json()
        if 'is_active' in data:
            user.is_active = data['is_active']
            db.session.commit()
            
        status_msg = 'unblocked' if user.is_active else 'blocked'
        return {'message': f'Member successfully {status_msg}'}, 200
