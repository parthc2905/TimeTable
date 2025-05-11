import json
import os
from datetime import datetime
from typing import Dict, Generator, List
from openai import OpenAI

class StudentChatbot:
    def __init__(self, api_key: str, storage_dir: str = "chatbot_sessions"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        
        self.API_CONFIG = {
            "model": "shisa-ai/shisa-v2-llama3.3-70b:free",
            "headers": {
                "HTTP-Referer": "https://your-student-app.com",
                "X-Title": "Student Schedule Assistant"
            }
        }

    def _get_system_prompt(self) -> Dict:
        return {
            "role": "system",
            "content": (
                "You are a Student Schedule Assistant. ALWAYS format responses using Markdown:\n"
                "1. Use ## for section headers\n"
                "2. Use - for bullet points\n"
                "3. **bold** for important items\n"
                "4. Separate sections with \\n\\n\n"
                "5. Never use HTML tags\n\n"
                "Example format:\n"
                "## Schedule Analysis\\n\\n"
                "- **Priority**: Math exam\\n"
                "- **Time Needed**: 2 hours\\n\\n"
                "## Recommended Plan\\n\\n"
                "- Monday: 1hr lecture review\\n"
                "- Tuesday: 2hr problem solving\\n"
                f"Current date: {datetime.now().strftime('%Y-%m-%d')}"
            )
        }

    def get_new_session_id(self) -> str:
        return f"stu_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def process_message(self, session_id: str, user_input: str) -> Generator[str, None, None]:
        messages = [
            self._get_system_prompt(),
            {"role": "user", "content": user_input}
        ]
        
        stream = self.client.chat.completions.create(
            model=self.API_CONFIG["model"],
            messages=messages,
            stream=True,
            temperature=0.3,
            extra_headers=self.API_CONFIG["headers"]
        )   
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content