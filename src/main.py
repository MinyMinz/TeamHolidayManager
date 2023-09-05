from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import userRouter
from routes.holidayRequests import holidayRouter
from routes.team import teamRouter
from routes.role import roleRouter

app = FastAPI(title="Phoebus Software Shared Calendar API")

# Set up CORS
origins = ["*"]  # Allow requests from any origin

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roleRouter, prefix="/roles")
app.include_router(teamRouter, prefix="/teams")
app.include_router(userRouter, prefix="/users")
app.include_router(holidayRouter, prefix="/holiday-request")

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="", port=8000)
