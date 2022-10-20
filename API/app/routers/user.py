from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import status, Response, Depends, HTTPException, APIRouter
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ["Users"] # creates a lable named Users in documentation and add all path operations under the label
)

# --- USERS --- #

# CREATE USER
#############
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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
@router.get("/{id}", response_model=schemas.UserOut)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"Couldn't find user with the id of {id}"})
    
    return user
##########

# --- END USERS --- #