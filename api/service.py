
"""
contains the api functions as well as helper functions for the api logic
"""
 
from io import BytesIO
from google.genai.types import File
from google.genai.client import Client
from models import *
from uuid import UUID, uuid4
 
 
ALLOWED_NOTE_TYPES = ["application/pdf"]
ALLOWED_AUDIO_TYPES = ["audio/m4a", "audio/mpeg", "audio/wav", "audio/mp4"]
 
MAX_NOTE_BYTES = 20 * 1024 * 1024 # 20 MB
MAX_AUDIO_BYTES = 20 * 1024 * 1024 # 20 mb

 
def create_new_session(client: Client, sessions: dict[UUID,Session], note_bytes: bytes, audio_bytes: bytes, notes_mime_type: str, audio_mime_type:str) -> SessionReturn:
    """
    takes in request informatio and creates the session, returning the session id 
 
    Paremeters:
        - client: Google genai client
        - sessions: session container holding sessions
        - note_bytes: notes in bytes
        - audio_bytes: audio in bytes
        - note_mime_type: specified mime type descriptor for notes 
        _ audio_mime_type: specified mime type descriptor for audio
    
    Return:
        - returns the associated session id with the session
    """
 
    
    # chaeck if the file is valid 
    if not is_valid_file(notes_mime_type, note_bytes,ALLOWED_NOTE_TYPES,MAX_NOTE_BYTES):
        raise  ValueError('Invalid note type. Please ensure that it is a PDF file and no more than 20MBs')
    if not is_valid_file(content_type=audio_mime_type, content=audio_bytes, allowed_types=ALLOWED_AUDIO_TYPES, max_bytes=MAX_AUDIO_BYTES):
        raise ValueError(f'Invalid note type. Please ensure that it is one of the following: {','.join(ALLOWED_AUDIO_TYPES)}')
    # upload to gemini
    note_file, audio_file = get_gemini_file(note_bytes,notes_mime_type, client), get_gemini_file(audio_bytes, audio_mime_type, client)
 
    # create and store session
    session_id = uuid4()
 
    # create sessionObject 
    new_session = Session(session_id=session_id, audio=audio_file, notes=note_file)
    sessions[new_session.session_id] = new_session
 
    # return session
    return SessionReturn(session_id=new_session.session_id)
 
def is_valid_file(content_type: str, content: bytes, allowed_types: list[str], max_bytes: int) -> bool:
    """
    Takes in file information and determines if the file is valid 
 
    Parameters
        - content_type: mime type of the file
        - content: the actual bytes in the file 
        - allowed_types: list of allowed types 
        - max_bytes: the maximum number of bytes allowed in a file
 
    Returns: boolean determining weather a file is valid
    """
    return content_type in allowed_types and 0 < len(content) <= max_bytes
 
from pathlib import Path
from google.genai.types import GenerateContentConfig
from pydantic import TypeAdapter
from models import Topic
 
 
def generate_session_topics(client: Client, session: Session, topic_prompt: str) -> list[Topic]:
    """
    Generates topics from a session's notes via Gemini and stores them on the session.
 
    Parameters:
        - client: Google genai client
        - session: session to get the topics from
        - topic_prompt: prompt to pass into the llm 
 
    Returns:
        - list of generated Topic objects
 
    Raises:
        - ValueError if the session or its notes are missing
    """
 
    if not session:
        raise ValueError("session is null")
    if not session.notes:
        raise ValueError("Invalid notes. Please ensure notes are not null")
    
    res = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=session.notes,
        config=GenerateContentConfig(
            system_instruction=topic_prompt,
            response_mime_type="application/json",
            response_schema=list[Topic],
            temperature=0,
        ),
    )
 
    adapter = TypeAdapter(list[Topic])
    topics = adapter.validate_json(res.text)
    session.topics = topics
    return topics
 
 
def get_gemini_file(content: bytes, mime_type: str, client: Client) -> File:
    """
    upload a file to gemini and returns the file
 
    Parameters:
        - bytes: the contents of the file in byte form
        - mime_type: the associated mime type of the file 
    Returns: 
         - Gemini Api file object 
    """
    content = BytesIO(content)
 
    return client.files.upload( file=content,
        config={
            "mime_type":mime_type
        }
    )
 
 
def fetch_session_topics(sessions: dict[UUID,Session], session_id: UUID) -> list[Topic]:
    """
    Retrieves previously generated topics for a session.
 
    Parameters:
        - sessions: session container holding sessions
        - session_id: UUID of the target session
 
    Returns:
        - list of Topic objects stored on the session
 
    Raises:
        - ValueError if the session or its topics are missing
    """
    session = sessions.get(session_id)
    if not session:
        raise ValueError("Session does not exist. Please create a session.")
    if not session.topics:
        raise ValueError("Topics not found. Ensure that you have generated topics from the notes provided.")
    return session.topics
 