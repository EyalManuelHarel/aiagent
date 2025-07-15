import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from agent_config import SYSTEM_PROMPT

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) == 1:
        print("ERROR: Not giving an argument")
        sys.exit(1)
    prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
    print(response.text)
    
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(f"User prompt: {prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
if __name__ == "__main__":
    main()
