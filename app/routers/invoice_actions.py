
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Invoice

router = APIRouter(prefix="/invoices", tags=["Invoice Actions"])

@router.post("/{invoice_number}/retry")
def retry_invoice(
    invoice_number: str,
    db: Session = Depends(get_db),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.invoice_number == invoice_number)
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found",
        )

    if invoice.status != "Failed":
        raise HTTPException(
            status_code=409,
            detail="Only failed invoices can be retried",
        )

    invoice.status = "Processing"
    db.commit()
    db.refresh(invoice)

    return {
        "message": "Invoice queued for retry",
        "invoice_number": invoice.invoice_number,
        "status": invoice.status,
    }

@router.post("/{invoice_number}/reject")
def reject_invoice(
    invoice_number: str,
    db: Session = Depends(get_db),
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.invoice_number == invoice_number)
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found",
        )

    if invoice.status != "Failed":
        raise HTTPException(
            status_code=409,
            detail="Only failed invoices can be rejected",
        )

    invoice.status = "Rejected"
    db.commit()
    db.refresh(invoice)

    return {
        "message": "Invoice rejected",
        "invoice_number": invoice.invoice_number,
        "status": invoice.status,
    }