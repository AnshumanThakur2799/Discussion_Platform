from fastapi import HTTPException , status , Request , File
import httpx
from pyuploadcare import Uploadcare
from pyuploadcare.resources.file import UploadProgress
from pyuploadcare.exceptions import UploadcareException
import os
from pathlib import Path
import logging
from typing import Tuple
import time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")

UPLOADCARE_PUBLIC_KEY = os.getenv("UPLOADCARE_PUBLIC_KEY")
UPLOADCARE_SECRET_KEY = os.getenv("UPLOADCARE_SECRET_KEY")

def is_file_size_acceptable(contents: str):
    print("checking file size")
    MB = 1024 * 1024
    if contents:
        size = len(contents)
        if size > int(5* MB):
            return False
        return True
    else:
        raise FileExistsError

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


async def upload_picture_to_uploadcare(contents: bytes, name: str) -> Tuple[str, str]:
    logger.info(f"Calling function to upload picture to Uploadcare with name: {name}")
    logger.debug(f"Uploading picture of size {len(contents)} bytes")
    
    directory = "temporary"

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        if len(contents) > 10 * 1024 * 1024:  # 10 MB
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="File size exceeds 10 MB limit.",
            )

        # Write contents to a temporary file
        temp_file_path = f"temporary/{name}"
        with open(temp_file_path, "wb") as f:
            f.write(contents)

        # Upload the file to Uploadcare
        uploadcare = Uploadcare(public_key=UPLOADCARE_PUBLIC_KEY, secret_key=UPLOADCARE_SECRET_KEY)
        with open(temp_file_path, "rb") as created_picture:
            uploaded_picture: File = uploadcare.upload(created_picture)

        logger.debug(f"Picture {name} uploaded successfully")
        return (
            f'https://ucarecdn.com/{uploaded_picture.uuid}/',
            uploaded_picture.uuid,
        )

    except HTTPException as e:
        logger.error(e.detail)
        raise e

    except UploadcareException as e:
        logger.error(f"Uploadcare Exception: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    finally:
        # Clean up: delete the temporary file
        try:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.debug(f"Temporary file {temp_file_path} deleted")
        except Exception as e:
            logger.error(f"Error while deleting temporary file {temp_file_path}: {e}")


#TODO just added this retry logic because DNS resolution from uploadcare

async def retry_upload_picture(contents: bytes, name: str, max_retries: int = 3) -> Tuple[str, str]:
    retry_count = 0
    while retry_count < max_retries:
        try:
            return await upload_picture_to_uploadcare(contents, name)
        except Exception as e:
            logger.warning(f"Attempt {retry_count + 1} failed: {e}")
            retry_count += 1
            if retry_count >= max_retries:
                logger.error(f"Failed to upload picture after {max_retries} attempts.")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload picture after {max_retries} attempts."
                )

            logger.info(f"Retrying upload attempt {retry_count}...")
            # Introduce a small delay before retrying
            time.sleep(1)  # Adjust the delay time as needed


async def delete_pictures_from_uploadcare(picturesList: list):
    logger.info(f"Callling Function for deleting pictures to uploadcare")
    try:
        uploadcare = Uploadcare(public_key=UPLOADCARE_PUBLIC_KEY, secret_key=UPLOADCARE_SECRET_KEY)
        uploadcare.delete_files(picturesList)
        logger.debug(f"Picture deleted succesfully")
        return "Deleted"
    except UploadcareException as e:
        logger.error(f"uploadcare Exception : {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail= "error in deleting picture from uploadcare")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail= "error in deleting picture from uploadcare")
