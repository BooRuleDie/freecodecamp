from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep

# trying to make a connection to the database
# if successful break the loop 
while(True):
    try:
        conn = psycopg2.connect(host="localhost", dbname="fastAPI", user="postgres", password="6537638Pst.", cursor_factory=RealDictCursor) 
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f"Connection Failed.\nError: {error}")
        sleep(3)

app = FastAPI()

# Schema of the Posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# READ POSTS
@app.get("/posts")
def getPosts():
    cursor.execute("""select * from posts;""")
    posts = cursor.fetchall()

    return {"posts" : posts}
############

# READ POST
@app.get("/posts/{id}")
def getPost(id: int):
    cursor.execute("""select * from posts where id = %s ;""", (str(id),)) # DON'T FORGET TO SPECIFY , in second argument, it's crucial
    post = cursor.fetchone()
    # if not exists return 404
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})
    return {"post" : post}
###########

# CREATE POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    # SQLi prevention, sanitazition for SQLi is handled by the library itself 
    cursor.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * ;""", 
    (post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    return {"post" : newPost}
#############

# DELETE POST
@app.delete("/posts/{id}")
def deletePost(id: int):
    cursor.execute("""delete from posts where id = %s returning *""", (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#############

# UPDATE POST
@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *;""", (post.title, post.content, post.published, str(id)))
    updatedPost = cursor.fetchone()

    if not updatedPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find post with the id of {id}"})
    
    conn.commit()
    return {"post" : updatedPost}
#############