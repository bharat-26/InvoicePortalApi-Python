
from sqlalchemy.orm import Session
from app.models import AuditLog


def create_audit_log(
    db: Session,
    event_type: str,
    status: str,
    email: str = None,
    user_id: int = None,
    ip_address: str = None,
    details: str = None
) -> AuditLog:
    
    audit_log = AuditLog(
        event_type=event_type,
        status=status,
        email=email,
        user_id=user_id,
        ip_address=ip_address,
        details=details,
    )

    db.add(audit_log)
    db.commit()

    return audit_log