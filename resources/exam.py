from models.user import UserModel
from models.exam import ExamModel


class CreateExam:
    @classmethod
    def create(cls, username):
        creator = UserModel.find_by_name(username)
        exam = ExamModel()
        exam.owner = creator
        exam.save_to_db()
        return exam



