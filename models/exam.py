from db import db
from models.answer import AnswerModel


class ExamModel(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('QuestionModel', backref='exam', lazy='dynamic', cascade="all, delete, delete-orphan")
    answer = db.relationship('AnswerModel', backref='exam', lazy='dynamic')

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def remove_question(cls, question_id):
        question = QuestionModel.find_by_id(question_id)
        exam = cls.query.filter(cls.questions.any(QuestionModel.id == question_id)).first()
        exam.questions.remove(question)
        db.session.commit()
        return exam

    @classmethod
    def find_other_courses(cls, _owner):
        return ExamModel.query.filter(ExamModel.owner_id != _owner.id)

    def count_user_points(self, user):
        variables = self.answer.all()
        counter = 0
        for variable in variables:
            if variable.is_correct:
                if variable.user_id == user.id:
                   counter += 1

        return counter


    def delete_from_db(self):
        for question in self.questions:
            self.questions.remove(question)
            db.session.commit()
        db.session.delete(self)
        db.session.commit()

    def get_questions(self):
        return self.questions

    def count_questions(self):
        return self.questions.count()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(50))
    answer1 = db.Column(db.String(20))
    answer2 = db.Column(db.String(20))
    answer3 = db.Column(db.String(20))
    answer4 = db.Column(db.String(20))
    correct_answer = db.Column(db.Integer)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id', ondelete="CASCADE"))
    answer = db.relationship('AnswerModel', backref='question', lazy='dynamic')

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def delete_from_db(self):
        self.delete()
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

