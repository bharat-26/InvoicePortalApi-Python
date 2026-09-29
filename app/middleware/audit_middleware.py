
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.database import SessionLocal
from app.services.audit_service import create_audit_log


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception:
            self._save_audit_event(request, status_code=500)
            raise

        self._save_audit_event(request, status_code=response.status_code)
        return response

    @staticmethod
    def _save_audit_event(request: Request, status_code: int):
        event = getattr(request.state, "audit_event", None)

        if not event:
            return

        db = SessionLocal()

        try:
            create_audit_log(
                db=db,
                event_type=event["event_type"],
                status=event["status"],
                email=event.get("email"),
                user_id=event.get("user_id"),
                ip_address=(
                    request.client.host if request.client else None
                ),
                details=event.get("details"),
            )
        except Exception:
            db.rollback()
            # Don't let audit logging break the API request
        finally:
            db.close()