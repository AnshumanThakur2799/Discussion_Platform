from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DiscussionBase(BaseModel):
    text: str
    image_url: Optional[str] = None
    owner: str
    comments: List[str] = Field(default_factory=list)
    views: Optional[int]
    hashTags: List[str] = Field(default_factory=list)
    likes : List[str] = Field(default_factory=list)

class DiscussionCreate(BaseModel):
    text: str
    owner : Optional[str] = None
    image_url: Optional[str] = None
    hashTags: List[str] = Field(default_factory=list)
    comments: List[str] = Field(default_factory=list)
    views: List[str] = Field(default_factory=list)

class DiscussionUpdate(BaseModel):
    text: Optional[str] = None
    image_url: Optional[str] = None
    hashTags: Optional[List[str]] = None

class DiscussionInDB(DiscussionBase):
    id: str
    created_on: datetime

class Tag(BaseModel):
    tag_name : str
    discussions : List[str] = Field(default_factory=list)

class Reply(BaseModel):
    text: str
    owner: Optional[str] = None

class CommentBase(BaseModel):
    text: str
    owner: Optional[str] = None
    replies: List[Reply] = Field(default_factory=list)
    likes: List[str] = Field(default_factory=list)
class CommentUpdate(BaseModel):
    text: str
class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    id: str

