from db import db


class AnswerModel(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))

    @classmethod
    def find_answer(cls, user, exam, question):
        return cls.query.filter(db.and_(cls.user_id == user.id,
                                        cls.exam_id == exam.id,
                                        cls.question_id == question.id)
                                ).first()

    @classmethod
    def count_correct_answers(cls, user, exam):
        result = cls.query.filter(db.and_(cls.user_id == user.id, cls.exam_id == exam.id))
        return result.query.filter(cls.is_correct).count()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


