from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#middleware config
origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#Path operation (also called Root)
@app.get("/") #decorator with ("/") as path - here it's the root path
def root(): #we could remove the async
    return {"message": "Hello World"}


# "CTRL + C" from the terminal to stop server
# "uvicorn main:app" from the terminal to start it
# "uvicorn main:app --reload" to reload the server each time the code changes

#defining a find post function
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

#defining a find index post function
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i






