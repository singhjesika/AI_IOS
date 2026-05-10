import os
from groq import Groq
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AIService:
    def __init__(self):
        self.model = "llama3-70b-8192"

    async def chat(self, message: str, agent: str = "General", system_prompt: str = None, history: list = None):
        try:
            if not system_prompt:
                system_prompt = f"""You are a friendly, smart {agent} AI assistant inside an app called AI_IOS, designed for students.
Always reply in simple, easy-to-understand language.
Always give REAL examples with specific details.
Use emojis to make responses friendly.
Be specific and helpful like a good teacher."""

            messages = [{"role": "system", "content": system_prompt}]

            # Add history if provided
            if history:
                for h in history[:-1]:  # exclude last since we add message below
                    messages.append({"role": h["role"], "content": h["content"]})

            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            reply = response.choices[0].message.content
            logger.info(f"AI response generated for agent: {agent}")
            return {"response": reply}

        except Exception as e:
            logger.error(f"AI service error: {e}")
            return {"response": f"Sorry, I encountered an error: {str(e)}"}


ai_service = AIService()