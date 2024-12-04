from os import environ as env
from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from routes.user import userRouter
from routes.holidayRequests import holidayRouter
from routes.team import teamRouter
from routes.role import roleRouter
from routes.auth import authRouter

# Set up OpenAPI
description = """
The Team Holiday Manager API is a RESTful API that allows you to manage your team's holiday requests. 

## Roles
You can:
* **Create Roles**.
* **Read Roles**.

## Teams
You can:
* **Create Teams**.
* **Read Teams**.
* **Delete Teams**.

## Users
You can:
* **Create Users**.
* **Read Users**.
* **Update Users**.
* **Delete Users**.
* **Update User Password**.

## Holiday Requests
You can:
* **Create Holiday Requests**.
* **Read Holiday Requests**.
* **Update Holiday Requests**.
* **Delete Holiday Requests**.

## Authentication
You can:
* **Login for token**.
"""

# Set up OpenAPI tags
tags_metadata = [
    {
        "name": "Roles",
        "description": "Operations with Roles.",
    },
    {
        "name": "Teams",
        "description": "Operations with Teams.",
    },
    {
        "name": "Users",
        "description": "Operations with users.",
    },
    {
        "name": "Holiday Requests",
        "description": "Operations with Holiday Requests.",
    },
    {
        "name": "Authentication",
        "description": "Gain access to the APIs.",
    },
]

stage = env.get("AWS_STAGE_NAME", None)
root_path = f"/{stage}" if stage else "/"

# Set up FastAPI
app = FastAPI(
    title="Phoebus Software Shared Calendar API",
    openapi_tags=tags_metadata,
    description=description,
    root_path=root_path,
)

# Set up CORS
origins = ["*"]  # Allow requests from any origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up routes
app.include_router(roleRouter, prefix="/roles", tags=["Roles"])
app.include_router(teamRouter, prefix="/teams", tags=["Teams"])
app.include_router(userRouter, prefix="/users", tags=["Users"])
app.include_router(authRouter, prefix="/auth", tags=["Auth"])
app.include_router(holidayRouter, prefix="/holiday-request", tags=["Holiday Requests"])

# Test route to check the API is working
@app.get("/")
async def root():
    return {"message": "Welcome to the Team Holiday Manager API!"}

# Set up Mangum for AWS Lambda
handler = Mangum(app=app)


# LOCAL TESTING - Run the main.py locally
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="", port=8000)
