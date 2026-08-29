from pydantic import BaseModel  
from datetime import date
from decimal import Decimal




class InvoiceItemDTO(BaseModel):
    description: str
    quantity: Decimal
    unit_price: Decimal

class InvoiceDTO(BaseModel):
    invoice_number: str
    customer_id: int
    invoice_date: date
    due_date: date
    notes: str | None = None
    tax_rate: Decimal
    items: list[InvoiceItemDTO]

    

