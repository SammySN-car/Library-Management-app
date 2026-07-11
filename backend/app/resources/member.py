from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.models.models import Users
from backend.utils.jwt_utils import admin_required

class ViewMembers(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        users=Users.query.filter_by(role='user').all()
        all_users=[]
        for u in users:
            all_users.append({
                'id':u.id,'full_name':u.full_name,'email_id':u.email_id,
                'address':u.address,'pincode':u.pincode
            })
        return {'message':'here are the details','all_users':all_users},200
