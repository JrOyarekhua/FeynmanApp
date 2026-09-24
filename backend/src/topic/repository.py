
from dataclasses import dataclass, fields 
from uuid import UUID

from sqlalchemy.orm import Session
from datetime import datetime
from src.topic.model import Topic
from sqlalchemy import select, update, tuple_, insert


class TopicRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_topic(self, topic: Topic) -> Topic:
        self.db.add(topic)
        self.db.commit()
        self.db.refresh(topic)
        return topic

    def create_all_topics(self, topics: list[Topic]) -> list[Topic]:
        
        query = insert(Topic).values(
            [
                {
                    "session_id": topic.session_id, 
                    "name": topic.name, 
                    "summary":topic.summary
                }
            for topic in topics]
        ).returning(Topic)
        res = self.db.scalars(query).all()

        self.db.commit()
        return res 

    def get_topic_by_id(self, topic_id: UUID) -> Topic | None:
        return self.db.get(Topic, topic_id)

    def get_topics_by_session_id(self, session_id: UUID, 
                                 cursor_topic_id: UUID | None = None,
                                 cursor_date_created: datetime | None = None,
                                 limit: int = 10) -> list[Topic]:
        query = select(Topic).where(Topic.session_id == session_id)

        if cursor_topic_id and cursor_date_created:
            query = query.where(
                tuple_(Topic.created_at, Topic.topic_id) <
                tuple_(cursor_date_created, cursor_topic_id))

        query=query.order_by(Topic.created_at.desc()).limit(limit)
        print(f'query: {query}')
        return self.db.execute(query).scalars().all()

    def update_topic(self, topic_id: UUID,summary: str, name: str | None = None) -> Topic:
        topic = self.get_topic_by_id(topic_id)

        if not topic:
            raise ValueError(f"Topic with id {topic_id} not found")

        if name:
            topic.name = name 

        topic.summary = summary

        self.db.commit()
        self.db.refresh(topic)
        return topic

    def delete_topic(self, topic_id: UUID) -> UUID:
        topic = self.get_topic_by_id(topic_id)

        if not topic:
            raise ValueError(f"Topic with id {topic_id} not found")

        self.db.delete(topic)
        self.db.commit()
        return topic_id