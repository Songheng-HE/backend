from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    membership_duration = db.Column(db.Integer, nullable=False)  # 会员时长（月）

    def __repr__(self):
        return f'<User {self.username}>'
