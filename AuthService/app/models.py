from pydantic import BaseModel

class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
