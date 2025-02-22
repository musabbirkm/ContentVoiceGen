# 🎙️ AI VoiceCraft: Text-to-Speech Studio 🚀

## Overview

AI VoiceCraft is a powerful web application built with Gradio that leverages cutting-edge AI to generate dynamic text content and transform it into natural-sounding speech. This tool integrates the Gemini AI model for content generation and Microsoft Edge TTS for high-quality audio synthesis.

## Features

-   **Dynamic Content Generation:**
    -      Generate various content types, including stories, news, podcasts, and more.
    -      Customize content length, theme, and style.
    -      Utilize Gemini AI for creative and contextually relevant text output.
-   **High-Quality Text-to-Speech:**
    -      Leverage Microsoft Edge TTS for realistic voice synthesis.
    -      Support for multiple languages and voices.
    -      Fine-tune speech rate and pitch for optimal delivery.
-   **User-Friendly Interface:**
    -      Intuitive Gradio interface for easy navigation and control.
    -      Real-time feedback and error handling.
    -   Attractive theme applied for better user experience.
-   **Customization Options:**
    -      Adjust the creativity level of the AI content generation.
    -   Input custom prompts for fine tuning the AI outputs.
    -   Adjust speech rate and pitch to fit your needs.

## Getting Started

### Prerequisites

-      Python 3.7+
-      Internet connection (for API access and TTS)
-   API Key for Gemini Model.

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Install the required Python packages:

    ```bash
    pip install gradio requests edge-tts google-generativeai nest_asyncio
    ```
3. set your API key in the VOCALIS.py file.
4. Run the application:

    ```bash
    python app.py
    ```


5. Open your web browser and navigate to the local URL provided by Gradio (usually `http://127.0.0.1:7860`).

## Usage

1.  Select the desired content type from the dropdown menu.
2.  Choose the language and voice for the TTS output.
3.  Adjust the output style, content length, and theme as needed.
4.  Enter any custom text or instructions in the customization field.
5.  Adjust the speech rate and pitch using the sliders.
6.  Click the "Submit" button to generate the text and audio.
7.  Review the generated text and listen to the audio output.

## Code Structure

-   `your_script_name.py`: Main application script that integrates Gradio, content generation, and TTS.
-   `VOCALIS.py`: Contains the `Agent` and `ContentGenerator` classes for AI content generation.
-   `edgeTTsLang.py`: Dictionary containing the language and voice codes for Microsoft Edge TTS.

## Dependencies

-   `gradio`: For building the web interface.
-   `requests`: For making HTTP requests to the API.
-   `edge-tts`: For text-to-speech conversion.
-   `google-generativeai`: For interacting with the Gemini AI model.
-   `asyncio`: For asynchronous operations.
-   `nest_asyncio`: For handling nested asyncio events in Jupyter notebooks.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bug fixes, feature requests, or improvements.

## License

This project is licensed under the MIT License.

## Gradio Theme

To enhance the user experience, an attractive theme has been applied to the Gradio interface. You can customize the theme further by modifying the Gradio theme settings in the `create_demo` function.

