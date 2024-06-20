from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from schema.models import UserInDB, UserCreate, UserUpdate
import bcrypt
from passlib.context import CryptContext
import logging
from database.db import client
# Configure logging
logging.basicConfig(level=logging.INFO)  # Set level to DEBUG for more detailed output
logger = logging.getLogger(__name__)
from pymongo import ReturnDocument
data_base = client["spyne"]
users_collection = data_base["users"]
users_collection.create_index([("email", 1)], unique=True)
users_collection.create_index([("mobile_no", 1)], unique=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user: UserCreate):
    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password.decode('utf-8')

    # Remove the password field from the dictionary to avoid storing it
    user_dict.pop("password")

    # Insert the user data into the database
    try:
        result = users_collection.insert_one(user_dict)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Retrieve the inserted user from the database to return it
    created_user = users_collection.find_one({"_id": result.inserted_id})
    return {
        "user_id" : str(result.inserted_id),
    }

async def update_user(user_id: str, user: UserUpdate) -> UserInDB:
    try:
        obj_id = ObjectId(user_id)
        update_fields = {k: v for k, v in user.dict(exclude_unset=True).items()}

        if "password" in update_fields:
            # Hash the new password
            update_fields["hashed_password"] = pwd_context.hash(update_fields["password"])
            del update_fields["password"]  # Remove plain text password from update fields

        # Update user in database
        result = users_collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": update_fields},
            return_document=ReturnDocument.AFTER
        )

        return UserInDB(**result, id = str(obj_id))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")



async def delete_user(user_id: str) -> dict:
    #TODO we usually do cron jobs for these taks by setting deleted = true
    user = users_collection.update_one({"_id" : ObjectId(user_id)} , {"$set": {"deleted": True}})
    return {"message": "User deleted"}

async def get_users() -> list[UserInDB]:
    cursor = users_collection.find()
    users = list(cursor)
    return [UserInDB(**user, id=str(user["_id"])) for user in users]


async def get_user_by_id(user_id: str) -> UserInDB:
    user = users_collection.find_one({"_id" : ObjectId(user_id)})
    if(not user): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(**user , id = str(user["_id"]))

async def get_user_by_name(name: str) -> UserInDB:
    user =  users_collection.find_one({"name" : name})
    if(not user): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInDB(**user)

async def get_user_by_identifier(identifier: str):
    logger.debug(f"Searching for identifier: {identifier}")

    user = None
    user =  users_collection.find_one({"name" : identifier}) or users_collection.find_one({"email" : identifier}) or users_collection.find_one({"mobile_no" : identifier})
    #TODO this is not a good practice this call should be mamde only once or maybe it doesnt look good
    logger.debug(f"Searching for user: {user}")
    user["_id"] = str(user["_id"])
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

async def follow_user(user_id_to_follow: str, follower_id: str):
    user_id_obj = ObjectId(user_id_to_follow)
    follower_id_obj = ObjectId(follower_id)

    result_followed = users_collection.update_one(
        {"_id": user_id_obj},
        {"$addToSet": {"followers": str(follower_id_obj)}}
    )

    if result_followed.modified_count != 1:
        raise HTTPException(status_code=404, detail="User to follow not found")

    result_follower = users_collection.update_one(
        {"_id": follower_id_obj},
        {"$addToSet": {"following": str(user_id_obj)}}
    )

    if result_follower.modified_count != 1:
        raise HTTPException(status_code=404, detail="Follower not found")