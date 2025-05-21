from sqlalchemy.orm import relationship
from user.model import db, User


class CustomerServiceAgent(db.Model):
    __tablename__ = "Customer_Service_Agent"

    agent_id        = db.Column("Agent ID", db.Integer,
                                 primary_key=True, autoincrement=True)
    name            = db.Column("Name", db.String(60), nullable=False)
    email           = db.Column("Email", db.String(100), nullable=False, unique=True)
    phone           = db.Column("Phone", db.String(20))
    employment_time = db.Column("Employment Time", db.DateTime, nullable=False)

    issues       = relationship("Issue", back_populates="agent")
    transactions = relationship("Transaction", back_populates="agent")


class Issue(db.Model):
    __tablename__ = "Issue"

    issue_id      = db.Column("Issue ID", db.Integer,
                               primary_key=True, autoincrement=True)
    type          = db.Column("Type", db.String(30))
    creation_time = db.Column("Creation Time", db.DateTime)
    description   = db.Column("Description", db.Text)
    resolve_time  = db.Column("Resolve Time", db.DateTime)
    status        = db.Column("Status", db.String(20))

    user_id  = db.Column("User ID", db.Integer,
                          db.ForeignKey('User."User ID"'), nullable=False)
    agent_id = db.Column("Agent ID", db.Integer,
                          db.ForeignKey('Customer_Service_Agent."Agent ID"'),
                          nullable=False)

    user  = relationship(User, backref="issues")
    agent = relationship(CustomerServiceAgent, back_populates="issues")


class Transaction(db.Model):
    __tablename__ = "Transaction"

    transaction_id = db.Column("Transaction ID", db.Integer,
                                primary_key=True, autoincrement=True)
    type           = db.Column("Type", db.String(20))
    currency       = db.Column("Currency", db.String(10))
    amount         = db.Column("Amount", db.Float)
    status         = db.Column("Status", db.String(20))
    request_time   = db.Column("Request Time", db.DateTime)
    aprove_time    = db.Column("Aprove Time", db.DateTime)

    user_id  = db.Column("User ID", db.Integer,
                          db.ForeignKey('User."User ID"'), nullable=False)
    agent_id = db.Column("Agent ID", db.Integer,
                          db.ForeignKey('Customer_Service_Agent."Agent ID"'),
                          nullable=False)

    user  = relationship(User, backref="transactions")
    agent = relationship(CustomerServiceAgent, back_populates="transactions")
