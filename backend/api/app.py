from fastapi import FastAPI
from api.controllers import auth_router, session_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(session_router)