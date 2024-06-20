from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional , List
import re

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_no: Optional[str] = None
    followers: List[str] = Field(default_factory=list)# List of user IDs who follow this user
    following: List[str] = Field(default_factory=list)
    deleted : Optional[bool] = False

class UserCreate(UserBase):
    password: str
    @validator('name')
    def validate_name(cls, v):
        if '@' in v:
            raise ValueError('Name cannot contain "@" symbol')
        if not v.strip():  # Check if name is empty or only whitespace
            raise ValueError('Name cannot be empty')
        if not re.match(r'^[a-zA-Z ]+$', v):  # Check if name contains only letters and spaces
            raise ValueError('Name must contain only letters and spaces')
        return v
    
    @validator('mobile_no')
    def validate_mobile_number(cls, v):
        if not re.match(r'^\d{10}$', v):
            raise ValueError('Mobile number must be 10 digits')
        return v
    
    

class UserUpdate(BaseModel):
    name : Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_no: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: str
