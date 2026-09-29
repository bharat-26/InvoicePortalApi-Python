
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.models import Invoice, Customer
from app.email_service import send_invoice_status_email


def get_customer_email(db, customer_id):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    return customer.email if customer else None

def process_invoices():
    db = SessionLocal()

    try:
        invoices = (
            db.query(Invoice)
            .filter(Invoice.status == "Processing")
            .all()
        )

        for invoice in invoices:
            invoice_id = invoice.id
            invoice_number = invoice.invoice_number
            customer_id = invoice.customer_id

            try:
                customer_email = get_customer_email(db, customer_id)

                if not customer_email:
                    raise ValueError("Customer email is missing")

                if not invoice.items:
                    raise ValueError("Invoice has no items")

                # Mark invoice as successfully processed
                invoice.status = "Sent"
                db.commit()

            except Exception as e:
                db.rollback()

                # Reload invoice after rollback
                invoice = (
                    db.query(Invoice)
                    .filter(Invoice.id == invoice_id)
                    .first()
                )

                if invoice is None:
                    continue

                invoice.status = "Failed"
                db.commit()

                # Try to notify the customer about failure
                customer_email = get_customer_email(
                    db,
                    customer_id
                )

                if customer_email:
                    try:
                        send_invoice_status_email(
                            to_email=customer_email,
                            invoice_number=invoice_number,
                            status="Failed",
                            message_text=(
                                "We couldn't process your invoice.\n"
                                "You can choose to retry processing "
                                "the invoice or reject it."
                            ),
                        )
                    except Exception as email_error:
                        print(
                            f"Failure email could not be sent for "
                            f"{invoice_number}: {email_error}"
                        )

                print(f"Invoice {invoice_number} failed: {e}")
                continue

            # Email failure should not change invoice status
            try:
                send_invoice_status_email(
                    to_email=customer_email,
                    invoice_number=invoice_number,
                    status="Sent",
                    message_text=(
                        "Your invoice has been processed successfully."
                    ),
                )
            except Exception as email_error:
                print(
                    f"Success email could not be sent for "
                    f"{invoice_number}: {email_error}"
                )

    finally:
        db.close()

scheduler = BackgroundScheduler()

def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        process_invoices,
        trigger="interval",
        minutes=1,
        id="invoice_processing_job",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()