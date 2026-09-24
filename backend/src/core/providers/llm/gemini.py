
from io import BytesIO

from pydantic import TypeAdapter
from src.core.providers.llm import LLMClient
from google.genai import Client
from google.genai.types import File,GenerateContentConfig

from src.core.providers.llm.schemas import EvalGen, TopicGen


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
    
    def transcribe(self, audio: bytes) -> str:
        res = self.client.models.generate_content(
            model=self._MODEL,
            contents=["Transcribe this audio exactly as spoken. Return only the transcript text with no additional commentary, formatting, or explanation. If you are unable to return an empty string",audio]
        )
        
        return res.text

    
    def generate_topics(self, notes_list: list[File]) -> list[TopicGen]:
        with open("prompts/topic_gen.md", 'r') as prompt:
            res = self.client.models.generate_content(
                model=self._MODEL,
                contents=notes_list,
                config=GenerateContentConfig(
                    system_instruction=prompt,
                    response_mime_type="application/json",
                    response_schema=list[TopicGen],
                    temperature=0
                )
            )

            adapter = TypeAdapter(list[TopicGen])
            topics = adapter.validate_json(res.text)
            return topics

    def generate_evaluation(self, explanation, topics, prompt: str, notes_links: list[str,str]) -> EvalGen:
        # serialize topics 
        adapter = TypeAdapter(list[TopicGen])
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
                response_schema=EvalGen,
                temperature=0
            )
        )

        evals = EvalGen.model_validate_json(res.text)
        return evals