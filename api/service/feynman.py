
from uuid import UUID
from models import Evaluation, Session, SessionUpdate, Topic
from repository.base import SessionRepository
from llm.base import LLMClient
from exceptions import SessionNotFoundError, InvalidFileError
class FeynmanService():

    ALLOWED_NOTE_TYPES = ["application/pdf"]
    ALLOWED_AUDIO_TYPES = ["audio/m4a", "audio/mpeg", "audio/wav", "audio/mp4"]
        
    MAX_NOTE_BYTES = 20 * 1024 * 1024 # 20 MB
    MAX_AUDIO_BYTES = 20 * 1024 * 1024 # 20 MB

    def __init__(self, client: LLMClient, repository: SessionRepository):
        self.client = client
        self.repository = repository

# session methods        
    def create_session(self, note_bytes: bytes, notes_mime_type: str, audio_bytes:bytes, audio_mime_type: str) -> UUID:


        """
        takes in request informatio and creates the session, returning the session id 
    
        Return:
            - returns the associated session id with the session
        """

        if not LLMClient.is_valid_file(content_type=notes_mime_type,content=note_bytes,allowed_types=self.ALLOWED_NOTE_TYPES,max_bytes=self.MAX_NOTE_BYTES):
            raise InvalidFileError('Invalid note type. Please ensure that it is a PDF file and no more than 20MBs')
        
        if not LLMClient.is_valid_file(content_type=audio_mime_type,content=audio_bytes,allowed_types=self.ALLOWED_AUDIO_TYPES,max_bytes=self.MAX_AUDIO_BYTES):
            raise InvalidFileError(f'Invalid note type. Please ensure that it is one of the following: {','.join(self.ALLOWED_AUDIO_TYPES)}')
        
        # upload notes and audio to llm 
        note_ref = self.client.upload_file(bytes=note_bytes,mime_type=notes_mime_type)
        audio_ref = self.client.upload_file(bytes=audio_bytes, mime_type=audio_mime_type)

        # create new session 
        session_id = self.repository.create_session()

        # add the refrences to the llm 
        updated_session: Session = self.repository.update_session(session_id=session_id, updates=SessionUpdate(
            notes_ref=note_ref,
            audio_ref=audio_ref))

        return session_id
    
    def delete_session(self, session_id: UUID) -> UUID:
            self.repository.delete_session(session_id=session_id)
            return session_id
    
    def update_session(self, session_id: UUID, content: SessionUpdate) -> Session:
        self.repository.update_session(session_id,content)
    
    def get_session(self, session_id: UUID) -> Session:
        return self.repository.get_session(session_id)

# topic methods 
    def generate_topics(self, prompt: str, session_id: UUID) -> list[Topic]:
        session: Session = self.get_session(session_id)
        # get notes 
        notes_ref = session.notes_ref

        # generate topics 
        topics:list[Topic] = self.client.generate_topics(notes_ref=notes_ref,prompt=prompt)
        
        # update the repository with the topics 
        self.repository.update_session(session_id=session_id, updates=SessionUpdate(topics=topics))

        return topics
    
    def get_topics(self, session_id: UUID):
        return self.get_session(session_id).topics


# transcript methods 
    def generate_transcript(self, session_id: UUID) -> str:

        session: Session = self.get_session(session_id)

        # get notes using the session id 
        audio_ref = session.audio_ref

        # call client 
        transcript = self.client.transcribe(audio=audio_ref)

        # store transcription
        self.repository.update_session(session_id=session_id,updates=SessionUpdate(transcript=transcript))

        return transcript

    def get_transcript(self, session_id:UUID):

        session: Session = self.get_session(session_id)

        return session.transcript

# evaluation methods 
    def generate_evaluation(self, session_id:UUID, prompt: str) -> Evaluation:

        session: Session = self.get_session(session_id)

        evaluation = self.client.generate_evaluation(explanation=session.transcript,topics=session.topics,eval_prompt=prompt, notes=session.notes_ref)

        # store evaluation
        self.repository.update_session(session_id=session_id, updates=SessionUpdate(evaluation=evaluation))
        return evaluation
    
    def get_evaluation(self, session_id: UUID) -> Evaluation:

        session: Session = self.get_session(session_id)

        return session.evaluation
