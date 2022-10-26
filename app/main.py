from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from . import models
from .database import Engine
from .routers import post, user, auth, like
from fastapi.middleware.cors import CORSMiddleware

# this is the code that generates all the tables, since we're using Alembic, we no longer need to use it
# models.Base.metadata.create_all(bind=Engine)

app = FastAPI()

# CORS
origins = [
    "http://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"], # change it to GET, POST, PUT, DELETE
    allow_headers = ["*"],
)

# binding router with app object
app.include_router(post.router) # /posts 
app.include_router(user.router) # /users 
app.include_router(auth.router) # /login
app.include_router(like.router) # /like

# redirect to docs
@app.get("/", tags=["Document Redirect"])
def home_to_docs():
    return RedirectResponse("/docs")
