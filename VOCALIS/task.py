from VOCALIS import Agent
import os
import logging
import re
import google.generativeai as genai
from google.generativeai.types import GenerationConfig


# Configure Gemini AI API
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API Key is missing. Set the API_KEY environment variable.")
genai.configure(api_key=api_key)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ContentGenerator:
    def __init__(self, agent: Agent, content_type: str = "story", language: str = "English",content_length: int = 200,
                 theme: str = "General/None", expectations: str = ""):
        self.agent = agent
        self.content_type = content_type.strip().lower()
        self.language = language.strip()
        self.goal = self._get_default_goal()
        self.content_length = content_length  # Added content length
        self.theme = theme.strip()
        self.expectations = expectations.strip()

        # Input validation
        if self.content_type not in [
            "story", "social", "news", "motivational", "explainer", "advertisement", "interview", "podcast",
            "testimonial", "comedy", "audiobook", "documentary", "meditation", "education", "poem", "recipe", "script",
            "summary", "email", "blog"
        ]:
            raise ValueError(f"Invalid content type: {self.content_type}")
        # if self.language not in languages:
        #     raise ValueError(f"Invalid language: {self.language}")

    def _get_default_goal(self) -> str:
        default_goals = {
            "story": "Generate a vivid, engaging, and natural-sounding short story suitable for narration.",
            "social": "Create a casual, engaging, and conversational social media script that sounds authentic.",
            "news": "Write a professional and well-structured news report optimized for audio presentation.",
            "motivational": "Generate an inspiring and natural motivational speech with a strong emotional connection.",
            "explainer": "Break down a complex topic in a clear and engaging way, suitable for an audio explanation.",
            "advertisement": "Write a persuasive and compelling ad script that feels engaging and natural.",
            "interview": "Generate a structured, conversational interview with natural question-answer flow.",
            "podcast": "Write a structured podcast script with natural dialogue and engaging discussions.",
            "testimonial": "Create an authentic-sounding customer testimonial suitable for an audio review.",
            "comedy": "Write a humorous monologue or short sketch with a natural comedic timing.",
            "audiobook": "Generate a structured audiobook chapter with expressive dialogue and immersive narration.",
            "documentary": "Create a professional and informative documentary narration with a storytelling approach.",
            "meditation": "Write a soothing guided meditation script designed for relaxation and mindfulness.",
            "education": "Generate a structured and clear educational script that is easy to follow in an audio format.",
            "poem": "Generate a beautiful and expressive poem with a natural flow.",
            "recipe": "Write a clear and easy-to-follow recipe suitable for audio instructions.",
            "script": "Generate a well-structured script for a short video or audio segment.",
            "summary": "Create a concise and accurate summary of a given topic.",
            "email": "Write a professional and well-formatted email.",
            "blog": "Generate an engaging and informative blog post."
        }
        return default_goals.get(self.content_type,
                                 "Generate a vivid, engaging, and natural-sounding short story suitable for narration.")

    def _build_prompt(self) -> str:
        prompt = (
            f"Role: You are a professional voice-over script writer specializing in {self.content_type} generation for natural speech synthesis.\n"
            f"Task: Create a high-quality, natural-sounding script in {self.language} optimized for text-to-speech (TTS).\n"
            f"Tone: Maintain a conversational and engaging tone, as if speaking directly to a listener.\n"
            f"Structure: Use short, clear sentences. Organize the content into logical paragraphs for easy audio comprehension.\n"
            f"Goal: {self.goal}\n"
            f"Constraints:\n"
            f"- Keep the script under {self.content_length} words.\n"
            f"- Use simple, direct language. Avoid complex jargon or unusual words that may be mispronounced by TTS.\n"
            f"- Do not explicitly state the content type (e.g., 'This is a story', 'Here is a script for voice-over...', etc.).\n"
            f"- Avoid excessive use of abbreviations, as they may not be pronounced correctly by TTS.\n"
            f"- Ensure smooth sentence transitions to maintain a natural flow when spoken aloud.\n"

            f"Instructions for Natural Pacing and Pauses:\n"
            f"- Use punctuation strategically (commas, ellipses, and dashes) to guide pauses in speech.\n"
            f"- Insert line breaks between key ideas to improve speech rhythm and avoid monotony.\n"
            f"- Break down long sentences into shorter, more digestible phrases to improve clarity.\n"

            f"Instructions for Emphasis:\n"
            f"- Use ALL CAPS or spacing between letters for words that should be emphasized.\n"
            f"- Provide phonetic hints for difficult or unusual words if necessary.\n"

            f"Output:\n"
            f"- Return ONLY the generated script. Do not include any introductory phrases like 'Here is a script...' or explanations.\n"
        )

        if self.theme and self.theme != "General/None":
            prompt += f"Theme/Nature: {self.theme}\n"

        if self.expectations:
            prompt += f"User Expectations: {self.expectations}\n"

        return prompt



    def generate_content(self) -> str:
        try:
            model = genai.GenerativeModel(self.agent.model)
            prompt = self._build_prompt()
            contents = [{"parts": [{"text": prompt}]}]
            generation_config = GenerationConfig(temperature=self.agent.temperature, max_output_tokens=1024)

            response = model.generate_content(contents=contents, generation_config=generation_config)
            output = response.text

            output = output.strip()
            output = re.sub(r'\s+', ' ', output)

            return output

        except Exception as e:
            logging.error(f"Error generating content: {e}")
            return f"Generation failed: {e}"


