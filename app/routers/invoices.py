from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database import get_db
from app.dtos import InvoiceDTO
from app.models import Invoice, InvoiceItem


router = APIRouter()


@router.post("/create_invoice")
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
        total=total
    )

    # Add invoice to database
    try:
        db.add(invoice_model)
        # Generate invoice ID
        db.flush()
        # Map InvoiceItemDTO → InvoiceItem model
        for item in invoice.items:
            item_model = InvoiceItem(
                invoice_id=invoice_model.id,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.quantity * item.unit_price
            )

            db.add(item_model)
        db.commit()
        db.refresh(invoice_model)

    except Exception:
        db.rollback()
        raise
   

    return {
        "message": "Invoice created successfully.",
        "result": {
            "id": invoice_model.id,
            "invoice_number": invoice_model.invoice_number,
            "customer_id": invoice_model.customer_id,
            "invoice_date": invoice_model.invoice_date,
            "due_date": invoice_model.due_date,
            "status": invoice_model.status,
            "notes": invoice_model.notes,
            "sub_total": invoice_model.sub_total,
            "tax_rate": invoice_model.tax_rate,
            "tax_amount": invoice_model.tax_amount,
            "total": invoice_model.total,
            "created_at": invoice_model.created_at
            }
    }



# from fastapi import APIRouter ,Depends
# from sqlalchemy.orm import Session
# from src.utils.db import get_db
# from decimal import Decimal

# from app.dtos import InvoiceDTO
# from app.models import Invoice, InvoiceItem


# router = APIRouter()


# @router.post("/create_invoice")
# def create_invoice(invoice: InvoiceDTO, db: Session = Depends(get_db)):
#     #calculations
#     sub_total = Decimal("0")

#     for item in invoice.items:
#         line_total = item.quantity * item.unit_price
#         sub_total += line_total

#     tax_amount = sub_total * invoice.tax_rate / Decimal("100")
#     total = sub_total + tax_amount

#     #Map InvoiceDTO → Invoice

#     invoice_model = Invoice(
#     invoice_number=invoice.invoice_number,
#     customer_id=invoice.customer_id,
#     invoice_date=invoice.invoice_date,
#     due_date=invoice.due_date,
#     notes=invoice.notes,
#     tax_rate=invoice.tax_rate,
#     sub_total=sub_total,
#     tax_amount=tax_amount,
#     total=total
# )

#     for item in invoice.items:
#     item_model = InvoiceItem(
#         invoice_id=invoice_model.id,
#         description=item.description,
#         quantity=item.quantity,
#         unit_price=item.unit_price,
#         line_total=item.quantity * item.unit_price
#     )

#     db.add(item_model)
#     return {"message": "Invoice created successfully.",
#             "result":invoice }