from app import db


class ExamModel(db.Model):
    __tablename__ = ''

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('online', db.Integer, nullable=False)
    owner = db.Column('owner_id', db.Integer)

    def __init__(self):
        self.exam_content = []

    def open_question(self, name):
        self.exam_content.append(db.Column(name, db.String(100)))
        self.exam_content.append(db.Column('answer', db.String(100)))
        self.exam_content.append(db.Column('points', db.Integer))

    def save_exam(self):
        db.create_all()


