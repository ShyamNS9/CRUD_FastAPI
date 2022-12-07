from fastapi import HTTPException, status, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db_connection as get_db
from app import models, schemas, utils, authjwt

api_router = APIRouter(
    tags=['Authentication']
)


@api_router.post("/login", response_model=schemas.Token)
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.email == data.username).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify_pass(data.password, result.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = authjwt.create_access_token(details={"user_id": result.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
