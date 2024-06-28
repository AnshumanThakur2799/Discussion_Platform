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
