import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from models import UserInDB
import httpx
import os
from dotenv import load_dotenv
import logging

import jwt

logging.basicConfig(level=logging.INFO)  # Set level to DEBUG for more detailed output
logger = logging.getLogger(__name__)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user_by_identifier(identifier):
    url = f"{USER_SERVICE_URL}/find-by-identifier"
    try:
        async with httpx.AsyncClient() as client:
            params = {"identifier": identifier}
            response = await client.get(url, params=params)

            if response.status_code == 200:
                return response.json()  # Assuming the response returns JSON data for the user
            elif response.status_code == 404:
                return None  # User not found
            else:
                # Handle other status codes (e.g., 500 for internal server error)
                raise HTTPException(status_code=response.status_code, detail="Failed to retrieve user")
    
    except httpx.HTTPError as http_err:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(err)}")


async def authenticate_user(identifier: str, password: str) -> UserInDB:
    
    user = await get_user_by_identifier(identifier)
    logger.debug(f"this is the user data {user}")
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user