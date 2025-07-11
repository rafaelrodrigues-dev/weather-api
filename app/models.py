from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(255),nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    feels_like = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    generated_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id',name='fk_weather_user_id'),
        nullable=False
    )

    user = db.relationship('User',backref=db.backref('history', lazy='dynamic'))

    def create(self):
        db.session.add(self)
        db.session.commit()