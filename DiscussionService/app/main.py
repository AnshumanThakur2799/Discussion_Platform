from fastapi import FastAPI, Depends, UploadFile , APIRouter , Form , File , status
from typing import List , Optional
from schemas.models import DiscussionCreate, DiscussionUpdate, DiscussionInDB , CommentCreate , CommentUpdate , Reply
from utils import get_current_user
from discussion_handler import (create_discussion_action,
                                                      update_discussion_action,
                                                      delete_discussion_action,
                                                      get_discussions_by_tags_action,
                                                      get_discussions_by_text_action,
                                                      uploading_image,
                                                      create_comment_on_discussion_action,
                                                      update_comment_on_discussion_action,
                                                      delete_comment_on_discussion_action,
                                                      like_comment_on_discussion_action,
                                                      reply_comment_on_discussion_action,
                                                      like_on_discussion_action,
                                                      get_discussion_by_id,
)

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set level to DEBUG for more detailed output
logger = logging.getLogger(__name__)

app = FastAPI(openapi_url="/api/v1/discussions/openapi.json", docs_url="/api/v1/discussions/docs")

discussion_router = APIRouter()

@discussion_router.post("/image" , status_code = status.HTTP_201_CREATED)
async def post_image(file : UploadFile):
    contents = file.file.read() 
    imageName = file.filename 
    imageUrl , imageUUID = await uploading_image(contents,imageName)
    return {"imageUrl":imageUrl}    


@discussion_router.post("/", response_model=DiscussionInDB)
async def create_discussion_api(discussion : DiscussionCreate , current_user : str = Depends(get_current_user)):
    logger.info(f"current_user: {current_user}")
    discussion.owner = current_user["sub"]
    discussion.views = 0
    logger.info(f"Discussion data: {discussion}")
    return await create_discussion_action(discussion)

@discussion_router.put("/{discussion_id}/like")
async def like_discussion(discussion_id : str, current_user : str = Depends(get_current_user)) :
    return await like_on_discussion_action(discussion_id, current_user["sub"])

@discussion_router.post("/{discussion_id}/comment")
async def create_comment_on_discussion(discussion_id : str , comment : CommentCreate , current_user : str = Depends(get_current_user)) :
    comment.owner = current_user["sub"]
    return await create_comment_on_discussion_action(comment , discussion_id)

@discussion_router.put("/comment/{comment_id}/like")
async def like_comment_on_discussion(comment_id : str, current_user : str = Depends(get_current_user)) :
    return await like_comment_on_discussion_action(comment_id, current_user["sub"])

@discussion_router.put("/comment/{comment_id}/reply")
async def reply_comment_on_discussion(comment_id : str, reply : Reply , current_user : str = Depends(get_current_user)) :
    reply.owner = current_user["sub"]
    return await reply_comment_on_discussion_action(reply, comment_id)

@discussion_router.put("/comment/{comment_id}")
async def update_comment_on_discussion(comment_id : str, comment : CommentUpdate, current_user : str = Depends(get_current_user)) :
    return await update_comment_on_discussion_action(comment, comment_id , current_user["sub"])

@discussion_router.delete("/{discussion_id}/comment/{comment_id}")
async def delete_comment_on_discussion(discussion_id : str, comment_id : str, current_user : str = Depends(get_current_user)) :
    return await delete_comment_on_discussion_action(discussion_id, comment_id, current_user["sub"])

@discussion_router.put("/{discussion_id}")
async def update_discussion_api(discussion_id: str, discussion: DiscussionUpdate, current_user: str = Depends(get_current_user)):
    return await update_discussion_action(discussion_id, discussion, current_user["sub"])

@discussion_router.delete("/{discussion_id}")
async def delete_discussion_api(discussion_id: str, current_user: str = Depends(get_current_user)):
    return await delete_discussion_action(discussion_id, current_user)


#TODO searchin is brute forced due to lag of time it can be implemented by inddexing the tags and search or better way 
#would be to use elasticsearch

@discussion_router.post("/tags/")
async def get_discussions_by_tags_api(tags: List[str]):
    return await get_discussions_by_tags_action(tags)

@discussion_router.get("/search/")
async def get_discussions_by_text_api(search_text: str):
    return await get_discussions_by_text_action(search_text)

@discussion_router.get("/{discussion_id}", response_model=DiscussionInDB)
async def get_discussion_by_id_api(discussion_id: str):
    return await get_discussion_by_id(discussion_id)


app.include_router(discussion_router, prefix="/api/v1/discussions")