import gradio as gr
import asyncio
import tempfile
import logging
import requests
from VOCALIS import Agent, ContentGenerator
from edgeTTsLang import languages


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_the_content(content_type, language,output_style,content_length, theme, expectations):
    try:
        temperature_map = {
            "Precise (Deterministic)": 0.1,
            "Very Focused (Low Randomness)": 0.3,
            "Moderately Focused (Slight Randomness)": 0.4,
            "Balanced (Moderate Creativity)": 0.5,
            "Slightly Creative (Moderate Randomness)": 0.6,
            "Creative (High Randomness)": 0.7,
            "Highly Creative (Very High Randomness)": 0.8,
            "Experimental (Maximum Randomness)": 0.95,
        }
        temperature = temperature_map.get(output_style, 0.6)
        agent = Agent(model="gemini-2.0-flash", temperature=temperature)
        generator = ContentGenerator(agent, content_type, language, content_length, theme, expectations)
        output = generator.generate_content()

        return output

    except ValueError as ve:
        return f"Input Error: {ve}"
    except requests.exceptions.ConnectionError:
        return "Network Error: Could not connect to API. Please check your internet connection."
    except Exception as e:
        return f"General Error: {e}"

async def text_to_speech(text, voice, rate, pitch):
    import edge_tts
    if not text.strip():
        return None, "Please enter text to convert."
    if not voice:
        return None, "Please select a voice."
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    return tmp_path, None

async def tts_interface(content_type, language, voice, output_style, content_length, theme, Customization, rate, pitch):
    text_output = generate_the_content(content_type, language, output_style, content_length, theme, Customization)
    if text_output.startswith("Error:"):
        return None, None, gr.Markdown(text_output)

    audio_file, warning = await text_to_speech(text_output, languages[language][voice], rate, pitch)

    if warning:
        return text_output, gr.Markdown(warning)

    return text_output, audio_file, None

def create_demo():
    language_choices = list(languages.keys())

    custom_theme = gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="blue",
        neutral_hue="slate",
        radius_size=gr.themes.sizes.radius_sm,
        font=[gr.themes.GoogleFont("Montserrat"), "Arial", "sans-serif"],
    )

    demo = gr.Interface(
        fn=tts_interface,
        theme=custom_theme,
        inputs=[
            gr.Dropdown(label="Content Type", choices=[
                "story", "social", "news", "motivational", "explainer", "advertisement", "interview", "podcast",
                "testimonial", "comedy", "audiobook", "documentary", "meditation", "education", "poem", "recipe",
                "script", "summary", "email", "blog"
            ], value="story"),
            gr.Dropdown(label="Language", choices=language_choices, value=language_choices[0] if language_choices else ""),
            gr.Dropdown(label="Voice", choices=["Female", "Male"], value="Female"),
            gr.Dropdown(label="Output Style", choices=[
                "Precise (Deterministic)", "Very Focused (Low Randomness)", "Moderately Focused (Slight Randomness)",
                "Balanced (Moderate Creativity)", "Slightly Creative (Moderate Randomness)",
                "Creative (High Randomness)", "Highly Creative (Very High Randomness)",
                "Experimental (Maximum Randomness)"
            ], value="Balanced (Moderate Creativity)"),
            gr.Slider(label="Content Length (Words)", minimum=100, maximum=1000, value=200, step=10),
            gr.Dropdown(label="Theme/Nature (Optional)", choices=[
                "General/None", "Narrative/Storytelling", "Informative/Educational", "Descriptive/Atmospheric",
                "Persuasive/Argumentative", "Humorous/Comedic", "Emotional/Inspirational", "Technical/Scientific",
                "Historical/Cultural", "Modern/Contemporary", "Futuristic/Sci-Fi", "Fantasy/Mythical",
                "Mystery/Suspense", "Adventure/Exploration", "Realistic/Documentary", "Philosophical/Reflective",
                "Social/Relational", "Environmental/Nature", "Personal/Anecdotal"
            ], value="General/None"),
            gr.Textbox(label="Customization", placeholder="Add any extra information to help customize the generated content"),
            gr.Slider(minimum=-50, maximum=50, value=0, label="Speech Rate Adjustment (%)", step=1),
            gr.Slider(minimum=-20, maximum=20, value=0, label="Pitch Adjustment (Hz)", step=1)
        ],
        outputs=[
            gr.Textbox(label="Generated Text"),
            gr.Audio(label="Generated Audio", type="filepath"),
            gr.Markdown(label="Error/Warning", visible=True)
        ],
        title="✨ AI VoiceCraft: Text-to-Speech Studio 🎙️",
        description="""  
        🚀 Transform your text into captivating audio! 🚀  

        This tool generates AI-powered content and converts it into lifelike speech using Microsoft Edge TTS.  

        🔹 **Features at a Glance:**  
        🌍 Supports multiple languages and voices  
        🎚️ Adjust speech rate and pitch for natural delivery  
        📝 Generate dynamic content: stories, news, podcasts & more  
        🎭 Customize tone, length, and style to fit your needs  

        """,
        article="""  
        # 🌟 Welcome to AI VoiceCraft! 🌟  

        **Unleash the power of AI-driven text-to-speech.**  

        This advanced application blends **cutting-edge AI content generation** with high-quality speech synthesis to create immersive audio experiences.  

        ## 🎤 Key Highlights:  
        🔊 Natural and expressive voice output  
        📖 AI-powered script generation tailored for speech  
        ⚙️ Fine-tune pitch, rate, and delivery style  

        🔗 [Discover more AI tools@MusabbirKM](https://www.example.com/ai-tools)  
        """,

        allow_flagging="never",
        api_name=None,
    )
    return demo

async def main():
    demo = create_demo()
    demo.queue(default_concurrency_limit=5)
    demo.launch(show_api=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(main())
