# Microservices Architecture Project

This project is built using a microservices architecture. It consists of various services such as User Service, Auth Service, and Discussions Service, each running in its own container. 

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Docker
- Docker Compose

## Getting Started

### Step 1: Create a .env File

Create a `.env` file in the root directory of your project with the following content:

```dotenv
SECRET_KEY="YOUR_SECRET_KEY"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="YOUR_TIME_IN_HOURS"
USER_SERVICE_URL="http://0.0.0.0:8080/api/v1/users"
AUTH_SERVICE_URL="http://0.0.0.0:8080/api/v1/auth"
MONGODB_URI="YOUR_MONGO_DB_URI"
UPLOADCARE_PUBLIC_KEY="YOUR_PUBLIC_KEY"
UPLOADCARE_SECRET_KEY="YOUR_SECRET_KEY"
```

### Step 2: Build and Run the Services
Use Docker Compose to build and run the services. Open a terminal in the root directory of your project and run the following command:
```bash
docker-compose up --build
```
### Step 3: Access the API Documentation
Once the services are running, you can access the API documentation for each service:

User Service: http://localhost:8080/api/v1/users/docs <br>
Auth Service: http://localhost:8080/api/v1/auth/docs  <br>
Discussions Service: http://localhost:8080/api/v1/discussions/docs  

## Auth Endpoints

### 1. POST /api/v1/auth/token

- **Summary:** Login For Access Token
- **Request Body:**
  - Required, Content Type: `application/x-www-form-urlencoded`
  - JSON Schema: `$ref` to `#/components/schemas/Body_login_for_access_token_api_v1_auth_token_post`
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 2. POST /api/v1/auth/verify-token

- **Summary:** Verify Token
- **Security:**
  - OAuth2 Password Bearer Flow with scopes
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)


## Users Endpoints

### 1. GET /api/v1/users/find-by-identifier

- **Summary:** Find User By Identifier
- **Parameters:**
  - `identifier` (query parameter, required): Identifier (type: string)

### 2. PUT /api/v1/users/follow/{user_id}

- **Summary:** Follow User Api
- **Parameters:**
  - `user_id` (path parameter, required): User Id (type: string)

### 3. PUT /api/v1/users/{user_id}

- **Summary:** Update User Api
- **Parameters:**
  - `user_id` (path parameter, required): User Id (type: string)
- **Request Body:**
  - Required, JSON schema: `$ref` to `#/components/schemas/UserUpdate`
- **Responses:**
  - `200 OK`: Successful Response, JSON schema: `$ref` to `#/components/schemas/UserInDB`
  - `422 Unprocessable Entity`: Validation Error, JSON schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 4. DELETE /api/v1/users/{user_id}

- **Summary:** Delete User Api
- **Parameters:**
  - `user_id` (path parameter, required): User Id (type: string)
- **Responses:**
  - `200 OK`: Successful Response, JSON schema: `{ "type": "object", "title": "Response Delete User Api Api V1 Users  User Id  Delete" }`
  - `422 Unprocessable Entity`: Validation Error, JSON schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 5. GET /api/v1/users/

- **Summary:** List Users
- **Responses:**
  - `200 OK`: Successful Response, JSON schema: Array of `$ref` to `#/components/schemas/UserInDB`

### 6. POST /api/v1/users/

- **Summary:** Create User Api
- **Request Body:**
  - Required, JSON schema: `$ref` to `#/components/schemas/UserCreate`
- **Responses:**
  - `200 OK`: Successful Response

## Discussions Endpoints

### 1. POST /api/v1/discussions/image

- **Summary:** Post Image
- **Request Body:**
  - Required, Content Type: `multipart/form-data`
  - JSON Schema: `$ref` to `#/components/schemas/Body_post_image_api_v1_discussions_image_post`
- **Responses:**
  - `201 Created`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 2. POST /api/v1/discussions/

- **Summary:** Create Discussion Api
- **Request Body:**
  - Required, Content Type: `application/json`
  - JSON Schema: `$ref` to `#/components/schemas/DiscussionCreate`
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/DiscussionInDB`
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 3. PUT /api/v1/discussions/{discussion_id}/like

- **Summary:** Like Discussion
- **Path Parameters:**
  - `discussion_id`: Discussion Id (string, required)
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 4. POST /api/v1/discussions/{discussion_id}/comment

- **Summary:** Create Comment On Discussion
- **Path Parameters:**
  - `discussion_id`: Discussion Id (string, required)
- **Request Body:**
  - Required, Content Type: `application/json`
  - JSON Schema: `$ref` to `#/components/schemas/CommentCreate`
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 5. PUT /api/v1/discussions/comment/{comment_id}/like

- **Summary:** Like Comment On Discussion
- **Path Parameters:**
  - `comment_id`: Comment Id (string, required)
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 6. PUT /api/v1/discussions/comment/{comment_id}/reply

- **Summary:** Reply Comment On Discussion
- **Path Parameters:**
  - `comment_id`: Comment Id (string, required)
- **Request Body:**
  - Required, Content Type: `application/json`
  - JSON Schema: `$ref` to `#/components/schemas/Reply`
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 7. PUT /api/v1/discussions/comment/{comment_id}

- **Summary:** Update Comment On Discussion
- **Path Parameters:**
  - `comment_id`: Comment Id (string, required)
- **Request Body:**
  - Required, Content Type: `application/json`
  - JSON Schema: `$ref` to `#/components/schemas/CommentUpdate`
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 8. DELETE /api/v1/discussions/{discussion_id}/comment/{comment_id}

- **Summary:** Delete Comment On Discussion
- **Path Parameters:**
  - `discussion_id`: Discussion Id (string, required)
  - `comment_id`: Comment Id (string, required)
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 9. PUT /api/v1/discussions/{discussion_id}

- **Summary:** Update Discussion Api
- **Path Parameters:**
  - `discussion_id`: Discussion Id (string, required)
- **Request Body:**
  - Required, Content Type: `application/json`
  - JSON Schema: `$ref` to `#/components/schemas/DiscussionUpdate`
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 10. DELETE /api/v1/discussions/{discussion_id}

- **Summary:** Delete Discussion Api
- **Path Parameters:**
  - `discussion_id`: Discussion Id (string, required)
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 11. GET /api/v1/discussions/{discussion_id}

- **Summary:** Get Discussion By Id Api
- **Path Parameters:**
  - `discussion_id`: Discussion Id (string, required)
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/DiscussionInDB`
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 12. POST /api/v1/discussions/tags/

- **Summary:** Get Discussions By Tags Api
- **Request Body:**
  - Required, Content Type: `application/json`
  - JSON Schema: Array of strings representing tags
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

### 13. GET /api/v1/discussions/search/

- **Summary:** Get Discussions By Text Api
- **Query Parameters:**
  - `search_text`: Text to search (string, required)
- **Responses:**
  - `200 OK`: Successful Response
    - Content Type: `application/json`
    - JSON Schema: (empty)
  - `422 Unprocessable Entity`: Validation Error
    - Content Type: `application/json`
    - JSON Schema: `$ref` to `#/components/schemas/HTTPValidationError`

