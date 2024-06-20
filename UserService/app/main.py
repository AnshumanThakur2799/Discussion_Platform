from fastapi import FastAPI, HTTPException, Depends, status, Request , APIRouter
from database.db_actions import create_user, update_user, delete_user, get_users, get_user_by_id, get_user_by_identifier , get_user_by_name , follow_user
from schema.models import UserInDB, UserCreate, UserUpdate
import httpx
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set level to DEBUG for more detailed output
logger = logging.getLogger(__name__)

app = FastAPI(openapi_url="/api/v1/users/openapi.json", docs_url="/api/v1/users/docs")


load_dotenv()

user_router = APIRouter()
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    logger.debug(f"headers : {auth_header}")
    if auth_header:
        token = auth_header.split(" ")[1]
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{AUTH_SERVICE_URL}/verify-token", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            return response.json()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")


@user_router.get("/find-by-identifier")
async def find_user_by_identifier(identifier: str):

    user = await get_user_by_identifier(identifier)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.put("/follow/{user_id}")
async def follow_user_api(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    follower_id = current_user.get("sub") 
    followed_user = await get_user_by_id(user_id)
    
    if not followed_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to follow not found")
    

    await follow_user(followed_user["_id"], follower_id)

    return {"message": f"User {follower_id} is now following user {user_id}"}

@user_router.put("/{user_id}", response_model=UserInDB)
async def update_user_api(user_id: str, user: UserUpdate, current_user = Depends(get_current_user)):
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")
    return await update_user(user_id, user)

@user_router.delete("/{user_id}", response_model=dict)
async def delete_user_api(user_id: str, current_user = Depends(get_current_user)):
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    return await delete_user(user_id)

async def find_user_by_name(name: str):
    return await get_user_by_name(name)

@user_router.get("/", response_model=list[UserInDB])
async def list_users():
    return await get_users()

@user_router.get("/{user_id}", response_model=UserInDB)
async def read_user(user_id: str):
    user = await get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") 
    
@user_router.post("/")
async def create_user_api(user: UserCreate):
    return await create_user(user)


app.include_router(user_router, prefix="/api/v1/users")
