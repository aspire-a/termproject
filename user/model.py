from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "user"

    user_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email       = db.Column(db.String(100), unique=True, nullable=False)
    name        = db.Column(db.String(60),  nullable=False)
    surname     = db.Column(db.String(60),  nullable=False)
    phone       = db.Column(db.String(20))
    address     = db.Column(db.Text)
    password    = db.Column(db.String,     nullable=False)
    verify_time = db.Column(db.DateTime)
    national_id = db.Column(db.String(20))
    kyc_status  = db.Column(db.String(30))

    # inverse relationships arrive via back_populates/backref elsewhere

    def __init__(self, email, name, surname, password,
                 phone=None, address=None, national_id=None):
        self.email       = email
        self.name        = name
        self.surname     = surname
        self.phone       = phone
        self.address     = address
        self.national_id = national_id
        self.set_password(password)

    def set_password(self, plain: str) -> None:
        self.password = generate_password_hash(plain, method="pbkdf2:sha256")

    def check_password(self, plain: str) -> bool:
        return check_password_hash(self.password, plain)

    def get_id(self) -> str:
        return str(self.user_id)
