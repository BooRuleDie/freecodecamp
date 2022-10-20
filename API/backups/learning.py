from typing import Optional
from fastapi.params import Body
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Defining the Schema
# Since we defined a schema, fastAPI will make the validiation automatically for us
# It'll check whether data we took as input have fields named (title, content, score) and their values matches with the data type we specified
class Post(BaseModel):
    title: str
    content:str
    score: float
    # optional field, if a field has a default value it's optional
    published: bool = True # default value
    # we can also use Optional from typing
    likeIt: Optional[bool] = True

# GET request example
@app.get("/")
def root():
    return {"message": "Hello World"}

# POST request example
# You don't need to specify an input data to make it work
# But that's against to POST request's purpose
# If you don't need to send a data in the body of the request just use GET
# @app.post("/post-example")
# def postExample(data: dict = Body(...)):
#                 # Take the request's body
#                 # Convert it to dict 
#     return {"message" : f"title: {data['title']}, content: {data['content']}"}

@app.post("/post-example")
def postExample(post: Post):
            
    print(post)
    # And since we're working with pydantic models we can convert these objects into dicts just by using dict() method
    print(post.dict())

    return {"message" : post}  

# API endpoints with best practice
# /posts:id
# /users:id ...
memoryDatabase = [
    {
        "id" : 1,
        "title" : "hebele",
        "content" : "hubele"
    },
    {
        "id" : 2,
        "title" : "hebele2",
        "content" : "hubele2"
    }
]

class PostSchema(BaseModel):
    id: int = 0
    title: str
    content: str

# READ of CRUD
##############
@app.get("/posts")
def getPosts():
    return {"posts" : memoryDatabase}

@app.get("/posts/{id}")
def getPost(id: int, response: Response):

    for post in memoryDatabase:
        if post["id"] == id:
            return {"post" : post}
    
    # better way to manipulate http response status code and the body 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"couldn't find any post with id of {id}"
        )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"error" : f"couldn't find any post with id of {id}"}
##############

# CREATE of CRUD
################
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: PostSchema):
    # it should be done in database normally
    print(post)
    id = randrange(0, 1000000)
    newPost = post.dict()
    newPost["id"] = id
    memoryDatabase.append(newPost)

    return {"newPost" : newPost}
    # raise HTTPException(status_code=status.HTTP_201_CREATED, detail={"newPost" : newPost})
    # It'll also work but specifying a default status code at the beginning is simpler
################

# DELETE of CRUD
################
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # 204 is the default status code for successful delete operations
def deletePost(id: int):
    for index, post in enumerate(memoryDatabase):
        if post["id"] == id:
            memoryDatabase.pop(index)
            # Since we're making a delete operation, we shouldn't return any data
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"couldn't find any post with id of {id}"
        )
################

# UPDATE of CRUD
################
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def updatePost(id: int, post: PostSchema):
    for index, item in enumerate(memoryDatabase):
        if item["id"] == id:
            memoryDatabase[index] = post.dict()
            memoryDatabase[index]["id"] = id
            return {"data" : memoryDatabase[index]}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Couldn't file post with the id of {id}"
    )
################
