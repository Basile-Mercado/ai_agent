import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from var import system_prompt
from functions.function_declaration import *

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
    else:
        generate_content(client, messages)

def generate_content(client, messages, verbose=False):    
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
        ]
    )    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        call_result = call_function(response.function_calls[0], verbose)
        if call_result.parts[0] and verbose:
            print(f"-> {call_result.parts[0].function_response.response}")
            pass
        else:
            print(f"Function call: {response.function_calls[0].name}{response.function_calls[0].args}")
            raise Exception("Function call failed or returned no response.")

if __name__ == "__main__":
    main()
