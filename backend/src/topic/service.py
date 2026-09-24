
from dataclasses import dataclass
from uuid import UUID
from src.topic.repository import TopicRepository
from src.attachment.repository import AttachmentRepository
from src.core.providers.llm import LLMClient
from src.topic.model import Topic
from src.utils.cursor import Cursor
from src.core.providers.llm.schemas import TopicGen
from src.core.providers.storage import BaseStorage
from src.attachment.model import Attachment
from src.utils.cursor import decode, encode
@dataclass
class PaginatedTopics:
    topics: list[Topic]
    cursor: str 

class TopicService:
    def __init__(self, topic_repo: TopicRepository, llm: LLMClient, bucket:BaseStorage, attachment_repo: AttachmentRepository):
        self.topic_repo = topic_repo
        self.llm = llm 
        self.attachment_repo = attachment_repo
        self.bucket = bucket

    def create_topic(self, name: str, summary: str, session_id: UUID) -> Topic:
        """
        manually create a topic based on your notes
        """
        print(f'session_id: {session_id}')
        new_topic = Topic(name=name, summary=summary, session_id=session_id)
        res = self.topic_repo.create_topic(new_topic)
        return res


    def generate_topics(self, session_id: UUID, user_id: UUID) -> list[Topic]:
        # get the storage path 
        notes: list['Attachment'] = self.attachment_repo.get_all_attachments(session_id=session_id, type='notes')

        notes_ref_list = []
        for note in notes:
            # get the notes bytes from the object store 
            content = self.bucket.download_file(note.storage_loc)
            # upload to the llm 
            note_file = self.llm.upload_file(bytes=content, mime_type=note.mime_type)
            notes_ref_list.append(note_file)

        
        # use the notes to generate a topic 
        generated_topics: list['TopicGen'] = self.llm.generate_topics(notes_ref_list)
        topic_list = [
            Topic(name=topic.name, summary=topic.summary, session_id=session_id) for topic in generated_topics
        ]
        return self.topic_repo.create_all_topics(topic_list)

    def get_topic(self, topic_id: UUID) -> Topic:
        return self.topic_repo.get_topic_by_id(topic_id)
            
    def get_all_topics(self, session_id: UUID, cursor: str = None, limit: int = 10) -> PaginatedTopics:
        cursor_created_at, cursor_topic_id = None, None

        if cursor:
            decoded_cursor = decode(cursor)
            cursor_created_at = decoded_cursor.cursor_created_at
            cursor_topic_id = decoded_cursor.cursor_id

        topic_list = self.topic_repo.get_topics_by_session_id(
            session_id=session_id,
            cursor_date_created=cursor_created_at,
            cursor_topic_id=cursor_topic_id,
            limit=limit
        )

        

        

        encoded_cursor = ""
        if topic_list:
            new_cursor = Cursor(
                cursor_created_at=topic_list[-1].created_at,
                cursor_id = topic_list[-1].topic_id
            )
            encoded_cursor = encode(new_cursor)

        print(f'new cursor: {encoded_cursor}')
        return PaginatedTopics(topics=topic_list,cursor=encoded_cursor)

    def update_topic(self,topic_id: UUID, name: str | None, summary: str) -> Topic:
        return self.topic_repo.update_topic(topic_id=topic_id, summary=summary, name=name)

    def delete_topic(self, topic_id: UUID):
        return self.topic_repo.delete_topic(topic_id=topic_id)
    
    