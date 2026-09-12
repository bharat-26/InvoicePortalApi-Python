from pydantic import BaseModel


class InvoiceStatusResponseDTO(BaseModel):
    invoice_number: str
    status: str