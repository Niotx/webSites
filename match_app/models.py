from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    university = db.Column(db.String(150))
    city = db.Column(db.String(150))
    interests = db.Column(db.String(500))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reported_user_id = db.Column(db.Integer)
    reason = db.Column(db.String(500))
