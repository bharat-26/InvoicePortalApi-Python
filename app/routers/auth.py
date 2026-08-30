# email, password, status 401 unauthorized - login api, audit logging also

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest
from app.security import verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

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

    token = create_access_token(user.id, user.email) #write a better message

    return {
        "message": "Login successful",
        "access_token": token,
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name
    }


# login pr otp email pr jaega
# email + password, use smtp provider 
# otp has been sent successfully, otp wala page dikhega