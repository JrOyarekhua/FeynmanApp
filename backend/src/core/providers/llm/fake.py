
from src.core.providers.llm import LLMClient
from src.core.providers.llm.schemas import EvalGen, TopicGen, Confidencelevel, EvalResult
from uuid import uuid4

class FakeLLM(LLMClient):
    def __init__(self):
        self.files = {}

    def upload_file(self, bytes, mime_type):
        file_id = f'file{uuid4()}' 

        self.files[file_id] = mime_type
        return file_id

    def transcribe(self, audio) -> str:
        return 'fake audio'

    def generate_topics(self, notes_list) -> list[TopicGen]:
        return [
            TopicGen(
            name='fake topic 1 ',
            summary='fake summary'
        ), TopicGen(
            name='fake topic 2', 
            summary='fake summary 2'
        )]

    def generate_evaluation(self, explanation, topics, prompt, notes) -> EvalGen:
        return EvalGen(
            confidenceLevel=Confidencelevel('needs_improvement'),
            coverage=EvalResult(
                score=75.5,
                passed=['fake passed'],
                failed=['fake failed']
            )
        )