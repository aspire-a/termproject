from sqlalchemy.exc import IntegrityError
from models import db, User


def create_user(email: str, name: str, surname: str, password: str) -> User:
    user = User(email=email, name=name, surname=surname, password=password)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        raise ValueError(f"E-mail already exists: {err.orig}") from err
    return user


def authenticate(email: str, password: str) -> User | None:
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
