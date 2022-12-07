from random import randrange
from fastapi import FastAPI, status, HTTPException, Response

# for schemas part
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
temp_db = [
    {
        "title": "How to change your life",
        "content": "Be positive, be motivated",
        "published": False,
        "rating": 4,
        "id": 1
    },
    {
        "title": "How to change your skills",
        "content": "Be positive, be motivated",
        "published": False,
        "rating": 4,
        "id": 2
    },
    {
        "title": "How to change your working",
        "content": "Be positive, be motivated",
        "published": False,
        "rating": 4,
        "id": 3
    }
]


class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class UpdatePostSchema(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    print(temp_db)
    return {
        "message": "Posts fetched successfully!",
        "payload": temp_db
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(data: PostSchema):
    data = data.dict()
    data['id'] = randrange(0, 100000)
    temp_db.append(data)
    print(temp_db)
    return {
        "message": "Post created successfully!",
        "payload": data
    }


@app.get("/posts/{uid}")
async def get_post(uid: int):
    print(uid)
    ans = [post for post in temp_db if post["id"] == uid]
    if not ans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found!")
    return {
        "message": "Post fetched successfully!",
        "payload": ans[0]
    }


@app.delete("/posts/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(uid: int):
    index, ans = -1, 0
    for post in temp_db:
        index = index + 1
        if post["id"] == uid:
            ans = 1
            del temp_db[index]
            break
    if not ans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{uid}")
async def update_user(uid: int, data: UpdatePostSchema):
    index, ans = 0, 0
    for post in temp_db:
        if post["id"] == uid:
            temp_db[index] = data
            ans = temp_db[index]
            break
        index += 1
    if not ans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found!")
    return {
        "message": "Post updated successfully!",
        "payload": ans
    }
