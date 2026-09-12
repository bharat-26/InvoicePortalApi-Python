from pydantic import BaseModel  
from decimal import Decimal
from datetime import date




class InvoiceItemDTO(BaseModel):
    description: str
    quantity: Decimal=1
    unit_price: Decimal

class InvoiceDTO(BaseModel): 
    invoice_number: str
    customer_id: int
    invoice_date: date
    due_date: date
    notes: str | None = None
    tax_rate: Decimal
    items: list[InvoiceItemDTO]


