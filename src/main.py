from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import userRouter
from routes.holidayRequests import holidayRouter
from routes.team import teamRouter
from routes.role import roleRouter

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

## Users
You can:
* **Create Users**.
* **Read Users**.
* **Update Users**.
* **Delete Users**.

## Holiday Requests
You can:
* **Create Holiday Requests**.
* **Read Holiday Requests**.
* **Update Holiday Requests**.
* **Delete Holiday Requests**.
"""

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
    }
]



app = FastAPI(title="Phoebus Software Shared Calendar API", openapi_tags=tags_metadata, description=description)

# Set up CORS
origins = ["*"]  # Allow requests from any origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roleRouter, prefix="/roles", tags=["Roles"])
app.include_router(teamRouter, prefix="/teams", tags=["Teams"])
app.include_router(userRouter, prefix="/users", tags=["Users"])
app.include_router(holidayRouter, prefix="/holiday-request", tags=["Holiday Requests"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="", port=8000)
