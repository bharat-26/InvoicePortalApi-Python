
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models import User, EmailOTP
from app.schemas import LoginRequest, VerifyOTPRequest
from app.security import verify_password, create_access_token, generate_otp
from app.email_service import send_otp_email
from app.config import get_settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    settings = get_settings()

    user = db.query(User).filter(User.email == data.email).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expiry_minutes)

    new_otp = EmailOTP(
        email=user.email,
        otp=otp,
        expires_at=expires_at
    )

    db.add(new_otp)
    db.commit()

    send_otp_email(user.email, otp)

    return {
        "message": "OTP sent successfully"
    }


@router.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):

    otp_record = db.query(EmailOTP).filter(
        EmailOTP.email == data.email
    ).order_by(EmailOTP.id.desc()).first()

    if otp_record is None:
        raise HTTPException(
            status_code=400,
            detail="OTP not found"
        )

    if otp_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="OTP has expired"
        )

    if otp_record.otp != data.otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    user = db.query(User).filter(User.email == data.email).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    token = create_access_token(user.id, user.email)

    return {
        "message": "Login successful",
        "access_token": token,
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }