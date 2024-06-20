from schemas.models import DiscussionCreate, DiscussionUpdate, DiscussionInDB , CommentInDB
from datetime import datetime
from bson import ObjectId
from typing import List
from fastapi import HTTPException, status
from database.db import client

db = client["spyne"]
discussions_collection = db["discussions"]
comments_collection = db["comments"]

async def create_discussion(discussion: DiscussionCreate) -> DiscussionInDB:
    discussion_dict = discussion.dict()
    discussion_dict["created_on"] = datetime.utcnow()
    result = await discussions_collection.insert_one(discussion_dict)
    created_discussion = await discussions_collection.find_one({"_id": result.inserted_id})
    return DiscussionInDB(**created_discussion, id=str(result.inserted_id))

async def update_discussion(discussion_id: str, discussion: DiscussionUpdate , current_user : str):

    existing_discussion = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not existing_discussion or existing_discussion['owner'] != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this discussion")
    update_data = {k: v for k, v in discussion.dict().items() if v is not None}
    await discussions_collection.update_one({"_id": ObjectId(discussion_id)}, {"$set": update_data})
    updated_discussion = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    updated_discussion["_id"] = str(updated_discussion["_id"])
    return updated_discussion

async def delete_discussion(discussion_id: str , current_user : str):
    existing_discussion = await discussions_collection.find_one({"_id": ObjectId(discussion_id)})
    if not existing_discussion or existing_discussion['owner'] != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this discussion")
    await discussions_collection.delete_one({"_id": ObjectId(discussion_id)})
    return {"message": "Discussion deleted successfully"}

async def get_discussions_by_tags(tags: List[str]):
    cursor = discussions_collection.find({"hashTags": {"$in": tags}})
    discussions = await cursor.to_list(length=None)
    result = [{**discussion, "_id": str(discussion["_id"])} for discussion in discussions]
    return result


async def get_discussions_by_text(search_text: str):
    cursor = discussions_collection.find({"text": {"$regex": search_text, "$options": "i"}})
    discussions = await cursor.to_list(length=None)
    result = [{**discussion, "_id": str(discussion["_id"])} for discussion in discussions]
    return result

async def creating_comment_on_discussion_action(comment , discussion_id) -> CommentInDB:
    comment_dict = comment.dict()
    result = await comments_collection.insert_one(comment_dict)
    comment_id = str(result.inserted_id)
    created_comment = await comments_collection.find_one({"_id": result.inserted_id})
    await discussions_collection.update_one({"_id" : ObjectId(discussion_id)} , {"$addToSet": {"comments" : comment_id}})
    return CommentInDB(**created_comment, id=str(result.inserted_id))

async def updating_comment_on_discussion_action(comment, comment_id , current_user):
    comment_data = await comments_collection.find_one({"_id" : ObjectId(comment_id)})
    if current_user!= comment_data["owner"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")
    
    update_data = {k: v for k, v in comment.dict().items() if v is not None}
    await comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": update_data})
    return { "message": "comment updated successfully"}

async def deleting_comment_on_discussion_action(discussion_id, comment_id, current_user):
    comment_data = await comments_collection.find_one({"_id" : ObjectId(comment_id)})
    if current_user!= comment_data["owner"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
    await discussions_collection.update_one({"_id" : ObjectId(discussion_id)} , {"$pull": {"comments" : comment_id}})
    await comments_collection.delete_one({"_id": ObjectId(comment_id)})
    return {"message": "comment deleted successfully"}

async def liking_comment_on_discussion_action(comment_id, current_user):
    await comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$addToSet": {"likes": current_user}})
    return {"message": "comment liked successfully"}

async def replying_comment_on_discussion_action(reply, comment_id):
    reply_dict = reply.dict()
    await comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$addToSet": {"replies" : reply_dict}})
    return {"message": "replied successfully"}

async def liking_on_discussion_action(discussion_id, current_user):
    await discussions_collection.update_one({"_id": ObjectId(discussion_id)}, {"$addToSet": {"likes": current_user}})
    return {"message": "discussion liked successfully"}

async def  getting_discussion_by_id(discussion_id):
    discussion = await discussions_collection.find_one_and_update({"_id": ObjectId(discussion_id)} , 
                                                                  {"$inc" : {"views" : 1}})
    return DiscussionInDB(**discussion, id=str(discussion["_id"]))