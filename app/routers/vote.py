from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, authjwt
from app.database import get_db_connection as get_db

api_router = APIRouter(
    prefix="/vote",
    tags=['vote']
)


@api_router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(data: schemas.Vote, db: Session = Depends(get_db), ut_data=Depends(authjwt.get_current_user)):
    result = db.query(models.Post).filter(models.Post.id == data.post_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found!")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == data.post_id, models.Vote.user_id == ut_data.id)
    got_vote = vote_query.first()
    print(got_vote)
    if data.dir == 1:
        if got_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {ut_data.id} has already voted on post {data.post_id}")
        new_vote = models.Vote(user_id=ut_data.id, post_id=data.post_id)
        db.add(new_vote)
        db.commit()
        return {
            "message": "successfully added vote"
        }
    else:
        if not got_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {
            "message": "successfully deleted vote"
        }
