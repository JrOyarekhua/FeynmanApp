from fastapi import APIRouter
from fastapi import Depends
from src.api.dependencies.auth import authorize_user 
from src.api.dependencies.services import get_topic_service    
from src.topic.schema import AllTopicsResponse, TopicCreate, TopicResponse, TopicUpdate
from src.topic.service import TopicService, PaginatedTopics
from src.utils.cursor import Cursor
from src.user.model import User
from uuid import UUID


topic_router = APIRouter(
    prefix="/api/sessions/{session_id}/topics",
    tags=["Topics"],
    
)

@topic_router.post("/", response_model=TopicResponse)
def create_topic(session_id: UUID, topic: TopicCreate, topic_service: TopicService = Depends(get_topic_service) ,user: User = Depends(authorize_user)):
    return topic_service.create_topic(name=topic.name, 
                                      summary=topic.summary, 
                                      session_id=session_id)

@topic_router.post("/generate", response_model= list[TopicResponse])
def generate_topic(session_id: str, topic_service: TopicService = Depends(get_topic_service), user: User = Depends(authorize_user)):
    return topic_service.generate_topics(session_id, user.auth_id)

@topic_router.get("/", response_model=AllTopicsResponse)
def get_all_topics(session_id: UUID, cursor: str = None, topic_service: TopicService = Depends(get_topic_service), user: User = Depends(authorize_user)) -> PaginatedTopics:
    return topic_service.get_all_topics(session_id=session_id, cursor=cursor)

@topic_router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: UUID, topic_service: TopicService = Depends(get_topic_service), user: User = Depends(authorize_user)):
    return topic_service.get_topic(topic_id)

@topic_router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: str, data: TopicUpdate, topic_service: TopicService = Depends(get_topic_service), user: User = Depends(authorize_user)):
    return topic_service.update_topic(topic_id=topic_id, name=data.name, summary=data.summary)

@topic_router.delete("/{topic_id}")
def delete_topic(topic_id: UUID, topic_service: TopicService = Depends(get_topic_service), user: User = Depends(authorize_user)):
    deleted_id = topic_service.delete_topic(topic_id)
    return {"message":f"topic {deleted_id} was succesfully deleted !"}
