from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.models import User
from app.validators import validate_email, validate_password

ns_user = Namespace('User', description='User related operations')

update_user_model = ns_user.model('UpdateUser', {
    'name': fields.String(required=False, description='The name of the user'),
    'email': fields.String(required=False, description='The email of the user'),
    'password': fields.String(required=False, description='The password of the user')
})

@ns_user.route('/')
class MeResource(Resource):
    method_decorators = [jwt_required()]

    @ns_user.doc('Get the information of the user logged in')
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        data = {
            'id': user.id,
            'name':user.name,
            'email':user.email
        }

        return {'user': data}, 200
    
    @ns_user.doc('Update the information of the user logged in') 
    @ns_user.expect(update_user_model)
    @ns_user.response(200, 'User updated')
    @ns_user.response(400, 'Invalid input')
    def patch(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        data = user.payload
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if name:
            user.name = name
        if email:
            if not validate_email(email):
                return {'msg': 'Invalid email format'}, 400
            user.email = email
        if password:
            if not validate_password(password):
                return {
                'msg':'Password is too weak',
                'obs':'Password must be alphanumeric, one uppercase and one lowercase.'
            }, 400

            user.password = generate_password_hash(password)
        else:
            return {'msg': 'No data provided to update'}, 400

        user.update()

        return {'msg': 'User updated'}, 200

    @ns_user.doc('Delete the user logged in')
    @ns_user.response(204, 'User deleted')
    def delete(self):
        current_user_id = get_jwt_identity()
        User.query.filter_by(id=current_user_id).delete()

        return {'msg': 'User deleted'}, 204