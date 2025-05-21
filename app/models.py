from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
