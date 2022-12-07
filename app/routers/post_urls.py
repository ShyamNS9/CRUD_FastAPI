from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db_connection as get_db
from app import models, schemas, authjwt

api_router = APIRouter(
    prefix="/posts",
    tags=['Posts']  # bifurcates in the swagger UI
)


@api_router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePostSchema)
async def create_post(data: schemas.CreatePostSchema, db: Session = Depends(get_db),
                      ut_data=Depends(authjwt.get_current_user)):
    result = models.Post(owner_id=ut_data.id, **data.dict())
    # result = models.Post(title=data.title, content=data.content, published=data.published)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@api_router.get("/", response_model=List[schemas.ResponsePostSchemaWithVote])
async def get_posts(db: Session = Depends(get_db), ut_data=Depends(authjwt.get_current_user), limit: int = 10,
                    skip: int = 0, search: Optional[str] = ""):
    print(search)
    # result = db.query(models.Post).all()  # to get all posts
    # result = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #  post with filter functionality
    result = db.query(models.Post, func.count(models.Vote.post_id).label("Vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result


@api_router.get("/my", response_model=List[schemas.ResponsePostSchemaWithVote])
async def get_my_posts(db: Session = Depends(get_db), ut_data=Depends(authjwt.get_current_user)):
    # result = db.query(models.Post).filter(models.Post.owner_id == ut_data.id).all()  # without vote count
    result = db.query(models.Post, func.count(models.Vote.post_id).label("Vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.owner_id == ut_data.id).all()
    return result


@api_router.get("/{uid}", response_model=schemas.ResponsePostSchemaWithVote)
async def get_post(uid: int, db: Session = Depends(get_db), ut_data=Depends(authjwt.get_current_user)):
    # result = db.query(models.Post).filter(models.Post.id == uid).first()  # without vote count
    result = db.query(models.Post, func.count(models.Vote.post_id).label("Vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == uid).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    return result


@api_router.get("/my/{uid}", response_model=schemas.ResponsePostSchemaWithVote)
async def get_post(uid: int, db: Session = Depends(get_db), ut_data=Depends(authjwt.get_current_user)):
    # result = db.query(models.Post).filter(models.Post.id == uid).first()  # without vote count
    result = db.query(models.Post, func.count(models.Vote.post_id).label("Vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == uid).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    if result.Post.owner_id != ut_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This post doesn't belongs to you.")
    return result


@api_router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(uid: int, db: Session = Depends(get_db), ut_data=Depends(authjwt.get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == uid)
    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    if result.first().owner_id != ut_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    result.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api_router.put("/{uid}", response_model=schemas.ResponsePostSchema)
async def update_user(uid: int, data: schemas.UpdatePostSchema, db: Session = Depends(get_db),
                      ut_data=Depends(authjwt.get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == uid)
    check = result.first()
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    if result.first().owner_id != ut_data.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # details = data.dict(exclude_unset=True)
    # for key, value in details.items():
    #     setattr(result, key, value)
    # db.add(result)
    result.update(data.dict())
    db.commit()
    return result.first()
