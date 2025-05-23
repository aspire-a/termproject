from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from flask_login import current_user
from models import db, Issue

ALLOWED_TYPES = [
    "KYC", "Withdrawal", "Login", "Deposit", "Trade",
    "API", "Security", "Other"
]


def create_issue(issue_type: str, description: str) -> Issue:
    """
    Insert a new Issue row for the current user.  Returns the Issue.
    Raises ValueError on bad input.
    """
    if issue_type not in ALLOWED_TYPES:
        raise ValueError("Unknown issue type")

    if not description.strip():
        raise ValueError("Description cannot be empty")

    issue = Issue(
        type=issue_type,
        description=description.strip(),
        status="OPEN",
        creation_time=datetime.now(timezone.utc),
        resolve_time=None,
        user_id=current_user.user_id,
        agent_id=1,          # will be assigned by support later
    )

    db.session.add(issue)
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        raise RuntimeError("Database error" + str(err)) from err

    return issue
