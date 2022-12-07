from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db_connection as get_db
from app import models, schemas, utils


api_router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@api_router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUsersSchema)
async def create_user(data: schemas.CreateUser, db: Session = Depends(get_db)):
    data.password = utils.hash_create(data.password)
    result = models.User(**data.dict())
    # result = models.Post(title=data.title, content=data.content, published=data.published)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@api_router.get("/", response_model=List[schemas.ResponseUsersSchema])
async def get_users(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    return result


@api_router.get('/{uid}', response_model=schemas.ResponseUsersSchema)
async def get_user_byid(uid: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == uid).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {uid} does not exist!")
    return result
