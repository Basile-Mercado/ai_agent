import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    args = sys.argv[1:]
    if not args:
        print("Usage: python main.py <prompt>")
        sys.exit(1)
    
    user_prompt = " ".join(args)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    print("Hello from ai-agent!")
    
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    if any([arg == '-v' or arg== '--verbose' for arg in args]):
        generate_content(client, messages, verbose=True)
    generate_content(client, messages)

def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    if verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
