import datetime
from db import db
from lm import login_manager
from passlib.hash import pbkdf2_sha256
from flask_login import UserMixin

# Callback function to reload the user object from the active user id in the session
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


class UserModel(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    feedback = db.Column(db.String(1), default="N")
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    feedback_user = db.relationship("FeedbackModel", backref="user")

    def __repr__(self):  # pragma: no cover
        return f"<User({self.id}, {self.name}, {self.email}, {self.feedback}, {self.created})>"

    @classmethod
    def verify_email(cls, email) -> object:
        return cls.query.filter_by(email=email).first()

    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def verify_password(password: str, hash: str) -> bool:
        return pbkdf2_sha256.verify(password, hash)


class FeedbackModel(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, default=5)
    question1 = db.Column(db.Boolean, default=False)
    question2 = db.Column(db.Boolean, default=False)
    question3 = db.Column(db.Boolean, default=False)
    question4 = db.Column(db.Boolean, default=False)
    comments = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self): # pragma: no cover
        return f"<FeedbackModel({self.rating}, {self.question1}, {self.question2}, " \
               f"{self.question3}, {self.question4}, {len(self.comments)})>"

