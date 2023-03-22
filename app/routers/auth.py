from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin
from ..models import User
from .. import utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credential: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    # create and return a token
    return {"token": "example token"}
