from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import status, Response, Depends, HTTPException, APIRouter
from typing import List

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"] # creates a lable named Users in documentation and add all path operations under the label
)

# --- POSTS --- #
# READ POSTS
@router.get("/", response_model=List[schemas.GetPostResponse])
def getPosts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ""):
    # cursor.execute("""select * from posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
############

# READ POST
@router.get("/{id}", response_model=schemas.GetPostResponse)
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
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    # SQLi prevention, sanitazition for SQLi is handled by the library itself 
    # cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * ;""", 
    # (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    newPost = models.Post(user_id=currentUser.id, **post.dict())
    # instead of **post.dict(), we could use following
    #title = post.title, content = post.content, published = post.published
    db.add(newPost)
    db.commit()
    # same as returning * in SQL
    db.refresh(newPost)
    return newPost
#############

# DELETE POST
@router.delete("/{id}")
def deletePost(id: int, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id) # returns SQL query .first() .all() .delete() executes the query
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Couldn't find post with the id of {id}")

    if post.first().user_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete someone else's post")
        
    post.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#############

# UPDATE POST
@router.put("/{id}", response_model=schemas.PostResponse)
def updatePost(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    # cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *;""", (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    query_post = db.query(models.Post).filter(models.Post.id == id)

    if not query_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})

    if query_post.first().user_id != currentUser.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can delete someone else's post")
    
    query_post.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    return query_post.first()
#############

# --- END POSTS --- #