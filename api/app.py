from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from models import CreateSessionReturn, DeleteSessionReturn, Evaluation, GetSessionReturn, Session, Topic, SessionBody, TopicReturn, TranscriptReturn, EvaluationReturn
from uuid import UUID
from dependencies import get_service
from service.feynman import FeynmanService
from exceptions import SessionNotFoundError, InvalidFileError

app = FastAPI()


# session handling 
@app.post("/api/session")
async def create_session(notes: UploadFile, audio: UploadFile, service: FeynmanService=Depends(get_service)) -> CreateSessionReturn:
    note_bytes,audio_bytes = await notes.read(), await audio.read()
    try:
        session_id: UUID = service.create_session(note_bytes=note_bytes, audio_bytes=audio_bytes, 
                                      notes_mime_type=notes.content_type, audio_mime_type=audio.content_type)
        return CreateSessionReturn(session_id=session_id)
    except SessionNotFoundError as e :
        raise HTTPException(404,detail=str(e))
    except InvalidFileError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.delete("/api/session")
async def delete_session(session_id: UUID, service: FeynmanService=Depends(get_service)) -> DeleteSessionReturn:
    try:
        session_id = service.delete_session(session_id)
        return DeleteSessionReturn(session_id=session_id)
    except SessionNotFoundError as e:
        raise HTTPException(404,detail=str(e))
    except Exception as e:
        raise HTTPException(500,detail=str(e))

@app.get("/api/session")
async def get_session(session_id: UUID, service: FeynmanService=Depends(get_service)) -> GetSessionReturn:
    try:
        session: Session = service.get_session(session_id)
        return GetSessionReturn(session=session)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    

# topic routes
@app.post("/api/topics")
async def generate_topics(req: SessionBody, service: FeynmanService = Depends(get_service)) -> TopicReturn:
    try:
        topic_prompt = ''
        with open('prompts/topic_gen.md','r') as file:
            topic_prompt = file.read()
        topics: list[Topic] = service.generate_topics(topic_prompt,req.session_id)

        return TopicReturn(topics=topics)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/topic")
async def get_topics(session_id: UUID, service: FeynmanService = Depends(get_service)) -> TopicReturn:
    try:
        topics: list[Topic] = service.get_topics(session_id)
        return TopicReturn(topics=topics)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# transcript routes
@app.post("/api/transcript")
async def generate_transcript(req:SessionBody , service: FeynmanService = Depends(get_service)) -> TranscriptReturn:
    try:
        transcript: str = service.generate_transcript(req.session_id)
        return TranscriptReturn(transcript=transcript)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))

@app.get("/api/transcript")
async def get_transcript(session_id: UUID, service: FeynmanService=Depends(get_service)) -> TranscriptReturn:
    try:
        transcript: str = service.get_transcript(session_id) 
        return TranscriptReturn(transcript=transcript)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))
    
# evaluation routes
@app.post("/api/evaluation")
async def generate_evaluation(req: SessionBody, service: FeynmanService=Depends(get_service)) -> EvaluationReturn:
    try:
        prompt = ''
        with open('prompts/student_performance.md','r') as file:
            prompt = file.read()
        evaluation: Evaluation = service.generate_evaluation(req.session_id, prompt)
        return EvaluationReturn(evaluation=evaluation)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))

@app.get("/api/evaluation")
async def get_evaluation(req: SessionBody, service: FeynmanService=Depends(get_service)) -> EvaluationReturn:
    try:
        evaluation: Evaluation = service.get_evaluation(req.session_id)
        return EvaluationReturn(evaluation=evaluation)
    except SessionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))