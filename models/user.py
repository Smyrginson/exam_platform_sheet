from app import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), nullable=False)
    password = db.Column('password', db.String(20), nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, _username: str) -> "UserModel":
        return cls.query.filter_by(username=_username).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()