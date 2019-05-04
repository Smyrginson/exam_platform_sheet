from db import db
from models.exam import ExamModel
from models.answer import AnswerModel


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(30), nullable=True)
    password = db.Column('password', db.String(30), nullable=True)
    exam = db.relationship('ExamModel', backref='owner', lazy='dynamic')
    answer = db.relationship('AnswerModel', backref='user', lazy='dynamic')
    points = db.Column('points', db.Integer, default=0)

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def take_score(cls):
        return cls.query.order_by(cls.points.desc()).all()

    @classmethod
    def find_by_name(cls, _username: str):
        return cls.query.filter_by(username=_username).first()

    def find_others_courses(self):
        exam_list = UserModel.query.filter(UserModel.id != self.id)
        return exam_list.exam

    def get_exams(self):
        return self.exam



    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

