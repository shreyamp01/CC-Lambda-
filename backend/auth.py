from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "super-secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
