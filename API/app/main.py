from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from . import models
from .database import Engine
from .routers import post, user, auth, like
     
models.Base.metadata.create_all(bind=Engine)

app = FastAPI()

# binding router with app object
app.include_router(post.router) # /posts 
app.include_router(user.router) # /users 
app.include_router(auth.router) # /login
app.include_router(like.router) # /like

# redirect to docs
@app.get("/", tags=["Document Redirect"])
def home_to_docs():
    return RedirectResponse("/docs")
