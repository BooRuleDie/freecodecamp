from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models, schemas, utils
from .database import Engine, get_db
from sqlalchemy.orm import Session
from typing import List


models.Base.metadata.create_all(bind=Engine)

# trying to make a connection to the database
# if successful break the loop 
while(True):
    try:
        conn = psycopg2.connect(host="", dbname="", user="", password="", cursor_factory=RealDictCursor) 
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f"Connection Failed.\nError: {error}")
        sleep(3)

app = FastAPI()

# @app.get("/sqlalchemy")
# def sqlalchemyTest(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
    
#     return {"connection" : posts}

# Schema of the Posts

# --- POSTS --- #
# READ POSTS
@app.get("/posts", response_model=List[schemas.PostResponse])
def getPosts(db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
############

# READ POST
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def getPost(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts where id = %s ;""", (str(id),)) # DON'T FORGET TO SPECIFY , in second argument, it's crucial
    # post = cursor.fetchone()
    # if not exists return 404

    # filter is similar to WHERE in SQL
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})

    return post
###########

# CREATE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # SQLi prevention, sanitazition for SQLi is handled by the library itself 
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * ;""", 
    # (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    newPost = models.Post(**post.dict())
    # instead of **post.dict(), we could use following
    #title = post.title, content = post.content, published = post.published
    db.add(newPost)
    db.commit()
    # same as returning * in SQL
    db.refresh(newPost)
    return newPost
#############

# DELETE POST
@app.delete("/posts/{id}")
def deletePost(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id) # returns SQL query .first() .all() .delete() executes the query
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})
    post.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#############

# UPDATE POST
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *;""", (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    query_post = db.query(models.Post).filter(models.Post.id == id)

    if not query_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})
    
    query_post.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return query_post.first()
#############

# --- END POSTS --- #

# --- USERS --- #

# CREATE USER
#############
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # converting plaintext password into hash
    user.password = utils.hash(user.password)
    
    createdUser = models.Users(**user.dict())
    db.add(createdUser)
    db.commit()
    db.refresh(createdUser)
    
    return createdUser
#############

# GET USER
##########
@app.get("/users/{id}", response_model=schemas.UserOut)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find user with the id of {id}"})
    
    return user
##########

# --- END USERS --- #