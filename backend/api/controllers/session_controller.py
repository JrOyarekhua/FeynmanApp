from fastapi import APIRouter, UploadFile, HTTPException, Depends
from models import User, Session
from api.dependencies import authorize_user, get_session_service
from service import SessionService
from uuid import UUID
from schemas import SessionResponseDetailed, SessionResponse, AllSessionsResponse, SessionCursor

session_router = APIRouter(
    prefix="/api/sessions",
    tags=["Sessions"],
)

@session_router.post("/", response_model=SessionResponse)
def create_session(user:User=Depends(authorize_user), 
                   service: SessionService = Depends(get_session_service)):
    return service.create_session(user.user_id)

@session_router.get("/")
def get_all_sessions(cursor: SessionCursor = None,
                    limit: int = 10,
                    user:User=Depends(authorize_user), 
                    service: SessionService = Depends(get_session_service),
                   ) -> AllSessionsResponse:
    
    cursor_created_at, cursor_id = None, None

    if cursor:
        cursor_created_at, cursor_id = cursor.created_at, 
        cursor.session_id

    res = service.get_all_sessions(user.user_id, cursor_created_at, cursor_id,limit)
    
    return AllSessionsResponse(res.sessions, SessionCursor(res.next_cursor[0], res.next_cursor[1]))

@session_router.get('/{session_id}', response_class=Session)
def get_session(session_id: UUID, service: SessionService = Depends(get_session_service)):
    return service.get_session(session_id)


@session_router.delete('/{session_id}')
def delete_session(session_id: UUID ,service: SessionService = Depends(get_session_service)):
    return service.delete_session(session_id)