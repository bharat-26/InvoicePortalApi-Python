from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database import get_db
from app.dtos.invoice_dto import InvoiceDTO
from app.models import Invoice, InvoiceItem
from app.dtos.invoice_responsedto import InvoiceResponseDTO
from app.dtos.invoice_status_response import InvoiceStatusResponseDTO



router = APIRouter()

#  invociedto name 
@router.post("/create-invoice",response_model=InvoiceResponseDTO)
def create_invoice(
    invoice: InvoiceDTO,
    db: Session = Depends(get_db)
):
    # Calculate invoice values
    sub_total = Decimal("0")

    for item in invoice.items:
        line_total = item.quantity * item.unit_price
        sub_total += line_total

    tax_amount = sub_total * invoice.tax_rate / Decimal("100")
    total = sub_total + tax_amount

    # Map InvoiceDTO → Invoice model
    invoice_model = Invoice(
        invoice_number=invoice.invoice_number,
        customer_id=invoice.customer_id,
        invoice_date=invoice.invoice_date,
        due_date=invoice.due_date,
        notes=invoice.notes,
        tax_rate=invoice.tax_rate,
        sub_total=sub_total,
        tax_amount=tax_amount,
        total=total,
        items=[
            InvoiceItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.quantity * item.unit_price
            )
            for item in invoice.items
        ]    
    )

    # Add invoice to database
    try:
        db.add(invoice_model)

        db.commit()
        db.refresh(invoice_model)
    except Exception:
        db.rollback()
        raise
   

    return invoice 


@router.get("/invoice-status/{invoice_number}",response_model=InvoiceStatusResponseDTO)
def get_invoice_status(invoice_number: str,db: Session = Depends(get_db)):
    invoice = (db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first())

    if invoice is None:
        raise HTTPException(status_code=404,detail="Invoice not found")

    return {
        "invoice_number": invoice.invoice_number,
        "status": invoice.status
    }