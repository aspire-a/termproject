from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "User"

    user_id = db.Column("User ID", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("Email", db.String(100), unique=True, nullable=False)
    name = db.Column("Name", db.String(60), nullable=False)
    surname = db.Column("Surname", db.String(60), nullable=False)
    phone = db.Column("Phone", db.String(20))
    address = db.Column("Adress", db.Text)
    password = db.Column("Password", db.String, nullable=False)
    verify_time = db.Column("Verify Time", db.DateTime)
    national_id = db.Column("National ID", db.String(20))
    kyc_status = db.Column("KYC Status", db.String(30))

    def __init__(self, email, name, surname, password, phone=None, address=None, national_id=None):
        self.email = email
        self.name = name
        self.surname = surname
        self.phone = phone
        self.address = address
        self.national_id = national_id
        self.set_password(password)

    def set_password(self, plain: str) -> None:
        self.password = generate_password_hash(plain, method="pbkdf2:sha256")

    def check_password(self, plain: str) -> bool:
        return check_password_hash(self.password, plain)

    def get_id(self) -> str:
        return str(self.user_id)
