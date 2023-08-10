from fastapi import FastAPI
from user.router import userRouter
from holiday_requests.router import holidayRouter
from team.router import teamRouter
from role.router import roleRouter

app = FastAPI(title="Phoebus Software Shared Calendar API")

app.include_router(roleRouter, prefix="/roles")
app.include_router(teamRouter, prefix="/teams")
app.include_router(userRouter, prefix="/users")
app.include_router(holidayRouter, prefix="/holiday-request")

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="", port=8000)
