from fastapi import APIRouter, UploadFile, HTTPException, Depends
from models import User, Session
from api.dependencies import authorize_user, get_session_service
from service import SessionService
from uuid import UUID
from schemas import SessionResponseDetailed, SessionResponse, AllSessionsResponse, Cursor
from utils.cursor import decode

session_router = APIRouter(
    prefix="/api/sessions",
    tags=["Sessions"],
)

@session_router.post("/", response_model=SessionResponse)
def create_session(user:User=Depends(authorize_user), 
                   service: SessionService = Depends(get_session_service)):
    return service.create_session(user.user_id)

@session_router.get("/")
def get_all_sessions(cursor: str | None = None,
                    limit: int = 10,
                    user:User=Depends(authorize_user), 
                    service: SessionService = Depends(get_session_service),
                   ) -> AllSessionsResponse:
    
    print(f'cursor: {cursor}')
    last_created_at, last_session_id = None, None 
    if cursor:
        decoded_cursor: Cursor = decode(cursor)
        last_created_at, last_session_id = (
            decoded_cursor.cursor_created_at,
            decoded_cursor.cursor_id
        )
    
    res = service.get_all_sessions(user.user_id, last_created_at, 
                                   last_session_id,limit)    
    
    
    return AllSessionsResponse(sessions=res.sessions, cursor=res.next_cursor)

@session_router.get('/{session_id}', response_model=SessionResponseDetailed)
def get_session(session_id: UUID, service: SessionService = Depends(get_session_service)):
    return service.get_session(session_id)


@session_router.delete('/{session_id}')
def delete_session(session_id: UUID ,service: SessionService = Depends(get_session_service)):
    deleted_id = service.delete_session(session_id)
    return {'message':f'user {deleted_id} sucessfuly deleted!'}