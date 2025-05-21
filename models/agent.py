from sqlalchemy.orm import relationship
from user.model import db, User


class CustomerServiceAgent(db.Model):
    __tablename__ = "customer_service_agent"

    agent_id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name            = db.Column(db.String(60),  nullable=False)
    email           = db.Column(db.String(100), nullable=False, unique=True)
    phone           = db.Column(db.String(20))
    employment_time = db.Column(db.DateTime,    nullable=False)

    issues       = relationship("Issue",       back_populates="agent")
    transactions = relationship("Transaction", back_populates="agent")


class Issue(db.Model):
    __tablename__ = "issue"

    issue_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type          = db.Column(db.String(30))
    creation_time = db.Column(db.DateTime)
    description   = db.Column(db.Text)
    resolve_time  = db.Column(db.DateTime)
    status        = db.Column(db.String(20))

    user_id  = db.Column(db.Integer,
                         db.ForeignKey("user.user_id"), nullable=False)
    agent_id = db.Column(db.Integer,
                         db.ForeignKey("customer_service_agent.agent_id"),
                         nullable=False)

    user  = relationship(User, backref="issues")
    agent = relationship(CustomerServiceAgent, back_populates="issues")


class Transaction(db.Model):
    __tablename__ = "transaction"

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type           = db.Column(db.String(20))
    currency       = db.Column(db.String(10))
    amount         = db.Column(db.Float)
    status         = db.Column(db.String(20))
    request_time   = db.Column(db.DateTime)
    approve_time   = db.Column(db.DateTime)

    user_id  = db.Column(db.Integer,
                         db.ForeignKey("user.user_id"), nullable=False)
    agent_id = db.Column(db.Integer,
                         db.ForeignKey("customer_service_agent.agent_id"),
                         nullable=False)

    user  = relationship(User, backref="transactions")
    agent = relationship(CustomerServiceAgent, back_populates="transactions")
