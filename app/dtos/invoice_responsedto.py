from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.dtos.invoice_dto import InvoiceItemDTO


class InvoiceResponseDTO(BaseModel):
    invoice_number: str
    customer_id: int
    invoice_date: date
    due_date: date
    notes: str | None = None
    tax_rate: Decimal
    items: list[InvoiceItemDTO]