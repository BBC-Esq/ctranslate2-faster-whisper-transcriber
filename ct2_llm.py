import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class LLMFormatter:
    def __init__(self, model_name="gpt-4o-mini"):
        self.model_name = model_name
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def format_transcription(self, transcription):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an AI assistant that reviews speech-to-text transcriptions and corrects them for natural line breaks (i.e. paragraphs) during natural pauses. You only responsd with the corrected transcription."},
                    {"role": "user", "content":  "Give me the corrected version of this transcription:\n\n" + transcription}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error formatting transcription: {e}")
            return transcription

