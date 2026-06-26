from sqlalchemy.orm import Session
from .. import models, schemas, hashing, oauth2
from ..database import get_db
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["authorisation"]
)

    

@router.get("/login")
def login(valid: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    valid_email = db.query(models.User).filter(models.User.email == valid.username).first()
    if not valid_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This email is not valid")

    is_password_correct = hashing.verify_password(valid.password, valid_email.password)
    
    if not is_password_correct:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Password is incorrect")
    
    access_token = oauth2.Create_Access_Token(data={"User_Email": valid.username})

    return {"access_token": access_token, "token_type": "bearer"}

    
    
    