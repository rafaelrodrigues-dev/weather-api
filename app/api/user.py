from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.models import User
from app.validators import validate_email, validate_password

ns_user = Namespace('User', description='User related operations', path='/api/v1/me')

update_user_model = ns_user.model('UpdateUser', {
    'name': fields.String(required=False, description='The name of the user'),
    'email': fields.String(required=False, description='The email of the user'),
    'password': fields.String(required=False, description='The password of the user')
})

user_info_model = ns_user.model('UserInfo', {
    'id': fields.Integer(description='The user identifier'),
    'name': fields.String(description='The name of the user'),
    'email': fields.String(description='The email of the user')
})

user_model = ns_user.model('User', {
    'user': fields.Nested(user_info_model)
})

@ns_user.route('/')
@ns_user.response(404, 'User not found')
@ns_user.response(401, 'Unauthorized')
class MeResource(Resource):
    decorators = [jwt_required()]

    def dispatch_request(self, *args, **kwargs):
        current_user_id = get_jwt_identity()
        self.user = User.query.filter_by(id=current_user_id).first()

        if not self.user:
            ns_user.abort(404,'User not found')
    
        return super().dispatch_request(*args, **kwargs)

    @ns_user.doc('Get the information of the user logged in')
    @ns_user.marshal_with(user_model)
    def get(self):
        data = {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email
        }

        return {'user': data}, 200
    
    @ns_user.doc('Update the information of the user logged in') 
    @ns_user.expect(update_user_model)
    @ns_user.response(201, 'User updated')
    @ns_user.response(400, 'Invalid input')
    def patch(self):
        data = ns_user.payload
        if not data:
            return {'msg': 'No data provided to update'}, 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        updated = False

        if name:
            self.user.name = name
            updated = True
        if email:
            if not validate_email(email):
                return {'msg': 'Invalid email format'}, 400
            self.user.email = email
            updated = True
        if password:
            if not validate_password(password):
                return {
                'msg':'Password is too weak',
                'obs':'Password must be alphanumeric, one uppercase and one lowercase.'
            }, 400

            self.user.password = generate_password_hash(password)
            updated = True

        if not updated:
            return {'msg': 'No valid data provided to update'}, 400

        self.user.update()

        return {'msg': 'User updated'}, 201

    @ns_user.doc('Delete the user logged in')
    @ns_user.response(204, 'User deleted')
    def delete(self):
        self.user.delete()
        return '', 204