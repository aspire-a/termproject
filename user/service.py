from sqlalchemy.exc import IntegrityError
from user.model import db, User


def create_user(email: str, name: str, surname: str, password: str) -> User:
    user = User(email=email, name=name, surname=surname, password=password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise ValueError("E-mail already exists" + str(e))
    return user


def authenticate(email: str, password: str) -> User | None:
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
