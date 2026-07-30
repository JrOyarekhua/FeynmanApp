from fastapi import FastAPI
from controllers.auth_controller import auth_router

app = FastAPI()

app.include_router(auth_router)