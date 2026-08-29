from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Date,
    Numeric,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.sql import func
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    invoice_number = Column(
        String(30),
        nullable=False,
        unique=True
    )

    customer_id = Column(
        BigInteger,
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False
    )

    invoice_date = Column(
        Date,
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="Draft"
    )

    notes = Column(
        String(1000),
        nullable=True
    )

    sub_total = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    tax_rate = Column(
        Numeric(5, 2),
        nullable=False,
        default=0
    )

    tax_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    total = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('Draft', 'Sent', 'Paid', 'Cancelled')",
            name="ck_invoices_status"
        ),
        CheckConstraint(
            "due_date >= invoice_date",
            name="ck_invoices_due_date"
        ),
    )

class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    invoice_id = Column(
        BigInteger,
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False
    )

    description = Column(
        String(300),
        nullable=False
    )

    quantity = Column(
        Numeric(12, 2),
        nullable=False,
        default=1
    )

    unit_price = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    line_total = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_invoice_items_quantity"
        ),
    )


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(200),
        nullable=True
    )

    phone = Column(
        String(50),
        nullable=True
    )

    address = Column(
        String(300),
        nullable=True
    )

    city = Column(
        String(100),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )