from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# OAuth2PasswordRequestForm returns dict {'username' : 'asdasd', 'password' : 'asdasdasd'}
# When you make the change, it will no longer accept the JSON HTTP request, you need to send credentials in parameters
from sqlalchemy.orm import Session
from ..database import get_db
from .. import utils, models, schemas, oauth2


router = APIRouter(tags = ["Authentication"])

@router.post("/login", response_model=schemas.Token)
def authenticateUser(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == userCredentials.username).first()

    # is such a user doesn't exist and password that has been specified is false, raise HTTPException
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # if user does exist try to access password of the user otherwise we got an error
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # JWT
    accessToken = oauth2.createAccessToken(data= {"uid" : user.id})

    return {"access_token" : accessToken, "token_type" : "bearer"}

