from fastapi import FastAPI
from app.routers import invoices
from app.middleware.error_handler import error_handler_middleware


app = FastAPI(
    title="Invoice Portal API",
    version="1.0.0"
)

app.middleware("http")(error_handler_middleware)
app.include_router(invoices.router)