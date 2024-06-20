from typing import List
from database.db_actions import (create_discussion,
                                 update_discussion,
                                 delete_discussion,
                                 get_discussions_by_tags,
                                 get_discussions_by_text,
                                 creating_comment_on_discussion_action,
                                 updating_comment_on_discussion_action,
                                 deleting_comment_on_discussion_action,
                                 liking_comment_on_discussion_action,
                                 replying_comment_on_discussion_action,
                                 liking_on_discussion_action,
                                 getting_discussion_by_id,
)
from schemas.models import DiscussionCreate, DiscussionUpdate, DiscussionInDB
from utils import retry_upload_picture

import logging
logging.basicConfig(level=logging.INFO)  # Set level to DEBUG for more detailed output
logger = logging.getLogger(__name__)


async def create_discussion_action(discussion: DiscussionCreate) -> DiscussionInDB:
    return await create_discussion(discussion)

async def update_discussion_action(discussion_id: str, discussion: DiscussionUpdate, current_user: str):
    return await update_discussion(discussion_id, discussion , current_user)

async def delete_discussion_action(discussion_id: str, current_user: str):
    return await delete_discussion(discussion_id,current_user)

async def get_discussions_by_tags_action(tags: List[str]):
    return await get_discussions_by_tags(tags)

async def get_discussions_by_text_action(search_text: str):
    return await get_discussions_by_text(search_text)

async def uploading_image(content , image_name):
    return await retry_upload_picture(content, image_name)

async def create_comment_on_discussion_action(comment , discussion_id):
    return await creating_comment_on_discussion_action(comment, discussion_id)

async def update_comment_on_discussion_action(comment, comment_id,current_user):
    return await updating_comment_on_discussion_action(comment, comment_id,current_user)

async def delete_comment_on_discussion_action(discussion_id, comment_id,current_user):
    return await deleting_comment_on_discussion_action(discussion_id, comment_id,current_user)

async def like_comment_on_discussion_action(comment_id, current_user):
    return await liking_comment_on_discussion_action(comment_id, current_user)

async def reply_comment_on_discussion_action(reply, comment_id):
    return await replying_comment_on_discussion_action(reply, comment_id)

async def like_on_discussion_action(discussion_id, current_user):
    return await liking_on_discussion_action(discussion_id, current_user)

async def get_discussion_by_id(discussion_id):
    return await getting_discussion_by_id(discussion_id)