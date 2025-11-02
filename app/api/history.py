from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Weather
ns_history = Namespace('History', description='User weather query history operations', path='/api/v1/history')

@ns_history.route('/')
class WeatherHistoryResource(Resource):
    decorators = [jwt_required()]
    @ns_history.doc('Get weather query history for the user logged in')
    def dispatch_request(self, *args, **kwargs):
        self.user_id = get_jwt_identity()
        user = User.query.get(self.user_id)
        if not user:
            ns_history.abort(404,'User not found')
        return super().dispatch_request(*args, **kwargs)

    @ns_history.doc('Get weather query history for the user logged in')
    @ns_history.param('page', 'Page number for pagination', required=False, default=1)
    def get(self):
        page = request.args.get('page', 1, type=int)
        history = Weather.query.filter_by(user_id=self.user_id).order_by(Weather.timestamp.desc())
        pagination = history.paginate(page=page, per_page=10, error_out=False)

        items = pagination.items
        calls = [{'data': item.data, 'timestamp': str(item.timestamp)} for item in items]

        return {
            'calls': calls,
            'page': pagination.page,
            'pages': pagination.pages,
            'total':pagination.total
        }