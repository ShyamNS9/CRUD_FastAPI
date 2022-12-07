from fastapi import FastAPI, APIRouter
from starlette.responses import RedirectResponse
from app.routers import users_urls, post_urls, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.config import setting
from app import models

# models.Base.metadata.create_all(bind=engine)  # not needed as we are using alembic
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_router = APIRouter()
app.include_router(api_router)
app.include_router(users_urls.api_router)
app.include_router(post_urls.api_router)
app.include_router(auth.api_router)
app.include_router(vote.api_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000, log_level="debug")
