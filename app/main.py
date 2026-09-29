from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import auth, invoices, invoice_actions

from app.middleware.error_handler import error_handler_middleware
from app.middleware.audit_middleware import AuditMiddleware

from app.database import Base, engine

from app.services.invoice_scheduler import (
    start_scheduler,
    stop_scheduler,
)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="Invoice Portal API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(AuditMiddleware)
app.middleware("http")(error_handler_middleware)

app.include_router(auth.router)
app.include_router(invoices.router)
app.include_router(invoice_actions.router)