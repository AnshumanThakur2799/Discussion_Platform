from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth_handler import create_access_token, verify_access_token, authenticate_user
import uvicorn

import logging
logging.basicConfig(level=logging.INFO)  # Set level to DEBUG for more detailed output
logger = logging.getLogger(__name__)

app = FastAPI(openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

auth_router = APIRouter()

@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    identifier = form_data.username  # Default to username
    user = await authenticate_user(identifier, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    logger.debug(f"this is the user data receive {user}")
    access_token = await create_access_token(data={"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    payload = await verify_access_token(token)
    return payload

# Include the auth router with the prefix '/auth'
app.include_router(auth_router, prefix="/api/v1/auth")
