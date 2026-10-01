import os
import json
import time

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing in .env file"
    )


# Gemini client
client = genai.Client(
    api_key=api_key
)


# Model
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)


def create_fallback_story(
    story_prompt,
    character,
    setting,
    tone,
    art_style
):
    """
    Creates a local demo story when Gemini
    is temporarily unavailable.
    """

    return {
        "title": f"{character} and the Mystery of {setting}",

        "panels": [

            {
                "panel": 1,
                "title": "The Beginning",

                "narration": (
                    f"{character} enters {setting} "
                    f"after receiving a mysterious message."
                ),

                "dialogue": (
                    f"{character}: What could be waiting for me here?"
                ),

                "image_prompt": (
                    f"{character} entering {setting}, "
                    f"{art_style} style, {tone} atmosphere."
                )
            },

            {
                "panel": 2,
                "title": "The Discovery",

                "narration": (
                    f"{character} discovers a strange object "
                    f"hidden inside the {setting}."
                ),

                "dialogue": (
                    f"{character}: I've never seen anything like this!"
                ),

                "image_prompt": (
                    f"{character} discovering a mysterious object "
                    f"in {setting}, {art_style} style."
                )
            },

            {
                "panel": 3,
                "title": "The Challenge",

                "narration": (
                    f"The mysterious object reveals a challenge "
                    f"that {character} must solve."
                ),

                "dialogue": (
                    f"{character}: I won't give up. "
                    f"I'll solve this mystery!"
                ),

                "image_prompt": (
                    f"{character} facing a mysterious challenge "
                    f"in {setting}, {art_style} style, "
                    f"dramatic scene."
                )
            },

            {
                "panel": 4,
                "title": "The Ending",

                "narration": (
                    f"With courage and creativity, {character} "
                    f"solves the mystery and discovers the truth."
                ),

                "dialogue": (
                    f"{character}: Every adventure teaches us something new."
                ),

                "image_prompt": (
                    f"{character} successfully solving the mystery "
                    f"in {setting}, {art_style} style, "
                    f"happy ending."
                )
            }

        ]
    }


def generate_comic_story(
    story_prompt,
    character,
    setting,
    tone,
    art_style
):

    prompt = f"""
You are an expert comic book writer.

Create a short and interesting comic story.

User information:

Story Prompt:
{story_prompt}

Main Character:
{character}

Setting:
{setting}

Tone:
{tone}

Art Style:
{art_style}

Create exactly 4 comic panels.

Each panel must contain:

1. Panel number
2. Panel title
3. Narration
4. Dialogue
5. Image prompt

The story must continue logically from Panel 1 to Panel 4.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "Comic title",
    "panels": [
        {{
            "panel": 1,
            "title": "Panel title",
            "narration": "Narration",
            "dialogue": "Dialogue",
            "image_prompt": "Detailed visual description"
        }},
        {{
            "panel": 2,
            "title": "Panel title",
            "narration": "Narration",
            "dialogue": "Dialogue",
            "image_prompt": "Detailed visual description"
        }},
        {{
            "panel": 3,
            "title": "Panel title",
            "narration": "Narration",
            "dialogue": "Dialogue",
            "image_prompt": "Detailed visual description"
        }},
        {{
            "panel": 4,
            "title": "Panel title",
            "narration": "Narration",
            "dialogue": "Dialogue",
            "image_prompt": "Detailed visual description"
        }}
    ]
}}
"""

    try:

        max_retries = 3

        for attempt in range(max_retries):

            try:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )

                result = response.text.strip()

                break

            except Exception as error:

                error_message = str(error)

                if (
                    "503" in error_message
                    and attempt < max_retries - 1
                ):

                    wait_time = 5 * (2 ** attempt)

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    raise

        # Remove Markdown code blocks
        if result.startswith("```json"):
            result = result[7:]

        elif result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        # Convert JSON to Python dictionary
        story = json.loads(result)

        return story

    except Exception as error:

        print(
            "Gemini unavailable. "
            "Using local fallback story."
        )

        print(
            "Gemini error:",
            error
        )

        return create_fallback_story(
            story_prompt=story_prompt,
            character=character,
            setting=setting,
            tone=tone,
            art_style=art_style
        )