from fastapi import FastAPI
from user.router import userRouter
app = FastAPI(title="Phoebus Software Shared Calendar API")

app.include_router(userRouter, prefix="/user", tags=["user"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="", port=8000)
