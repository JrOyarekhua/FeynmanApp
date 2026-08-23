from fastapi import FastAPI
import src.core.models
from src.auth.route import auth_router
from src.session.route import session_router
from src.attachment.route import attachment_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(session_router)
app.include_router(attachment_router)