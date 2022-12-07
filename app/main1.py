import time
from fastapi import FastAPI, HTTPException, status, Response
import psycopg2
from psycopg2.extras import RealDictCursor

# for schemas part
from pydantic import BaseModel
from typing import Optional

while True:
    try:
        connection = psycopg2.connect(host='localhost', database='FastAPI_database', user='postgres',
                                      password='sns123456', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("connection to database.py Successful!")
        break
    except Exception as e:
        print("connection to database.py failed!")
        print("Error: ", e)
        time.sleep(3)

app = FastAPI()


class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True


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
    cursor.execute(""" SELECT * FROM posts """)
    result = cursor.fetchall()
    return {
        "message": "Posts fetched successfully!",
        "payload": result
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(data: PostSchema):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) returning *""", (data.title, data.content, data.published))
    result = cursor.fetchone()
    connection.commit()
    return {
        "message": "Post created successfully!",
        "payload": result
    }


@app.get("/posts/{uid}")
async def get_post(uid: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(uid))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found!")
    return {
        "message": "Post fetched successfully!",
        "payload": result
    }


@app.delete("/posts/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(uid: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", str(uid))
    result = cursor.fetchone()
    connection.commit()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{uid}")
async def update_user(uid: int, data: UpdatePostSchema):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (data.title, data.content, data.published, str(uid)))
    result = cursor.fetchone()
    connection.commit()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found!")
    return {
        "message": "Post updated successfully!",
        "payload": result
    }
