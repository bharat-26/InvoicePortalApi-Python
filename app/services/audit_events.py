
from fastapi import Request


def audit_event(
    request: Request,
    event_type: str,
    status: str,
    email: str = None,
    user_id: int = None,
    details: str = None,
):
    request.state.audit_event = {
        "event_type": event_type,
        "status": status,
        "email": email,
        "user_id": user_id,
        "details": details,
    }