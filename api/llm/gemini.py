
from io import BytesIO

from pydantic import TypeAdapter
from llm.base import LLMClient
from google.genai import Client
from google.genai.types import File,GenerateContentConfig

from models import Evaluation, Topic


class GeminiClient(LLMClient):
    _MODEL = "gemini-2.0-flash-lite"

    def __init__(self, api_key: str):
        self.client = Client(api_key=api_key)

    def upload_file(self, bytes: bytes, mime_type: str) -> File:
        content = BytesIO(bytes)
        return self.client.files.upload(
            file=content,
            config={
                "mime_type":mime_type
            }
        )

    def transcribe(self, audio) -> str:
        res = self.client.models.generate_content(
            model=self._MODEL,
            contents=["Transcribe this audio exactly as spoken. Return only the transcript text with no additional commentary, formatting, or explanation. If you are unable to return an empty string",audio]
        )
        
        return res.text

    
    def generate_topics(self, notes_ref, prompt: str) -> list[Topic]:
        res = self.client.models.generate_content(
            model=self._MODEL,
            contents=notes_ref,
            config=GenerateContentConfig(
                system_instruction=prompt,
                response_mime_type="application/json",
                response_schema=list[Topic],
                temperature=0
            )
        )

        adapter = TypeAdapter(list[Topic])
        topics = adapter.validate_json(res.text)
        return topics

    def generate_evaluation(self, explanation, topics, prompt: str, notes) -> Evaluation:
        # serialize topics 
        adapter = TypeAdapter(list[Topic])
        formatted_topics = adapter.dump_json(topics).decode()
        user_input = f"""
        Transcription: {explanation}

        Selected Topics: {formatted_topics}
        """

        res = self.client.models.generate_content(
            model=self._MODEL,
            contents=[user_input, notes],
            config=GenerateContentConfig(
                system_instruction=prompt,
                response_mime_type="application/json",
                response_schema=Evaluation,
                temperature=0
            )
        )

        evals = Evaluation.model_validate_json(res.text)
        return evals