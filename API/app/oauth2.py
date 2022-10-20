from jose import JWTError, jwt
from datetime import datetime, timedelta
from .database import get_db
from sqlalchemy.orm import Session
from . import schemas, models
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

# endpoint of authentication
oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# What we need: 
# 1- SECRET
# 2- Algorithm
# 3- Expire Date

SECRET_KEY = settings.secretKey
ALGORITHM = settings.Algorithm
ACCESS_TOKEN_EXPIRE_IN_MINUTES = settings.AccessTokenExpireMinute

def createAccessToken(data: dict):
    tempData = data.copy()

    expireDate = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_IN_MINUTES)
    tempData.update({"exp" : expireDate})

    return jwt.encode(tempData, SECRET_KEY, algorithm=ALGORITHM)

def verifyAccessToken(token: str, credentialException):
    try:
        # payload of the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("uid")

        if not id:
            raise credentialException
        
        # validating the schema
        tokenData = schemas.TokenData(id=id)
    except JWTError:
        raise credentialException

    return tokenData

# it'll take the id in the JWT in the HTTP Request
def getCurrentUser(token: str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    
    credentialException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verifyAccessToken(token, credentialException)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user