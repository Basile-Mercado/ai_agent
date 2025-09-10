import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.config import MAX_ITERATIONS, SYSTEM_PROMPT
from functions.function_declaration import *

def main():
    load_dotenv()
    args = sys.argv[1:]
    verbose = "--verbose" in args or "-v" in args
    if not args:
        print("AI Code Assistant")
        print("Usage: python main.py <prompt> --verbose/-v for verbose output")
        print("Example: python main.py 'List files in the working directory'")
        sys.exit(1)
    
    user_prompt = " ".join(args)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    print("Hello from ai-agent!")
    
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERATIONS:
            print("Max iterations reached")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final Response:\n", final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
            break

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
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
    )
    
    if verbose:
        print(f"User prompt: {messages[0].parts[0].text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    if response.candidates:
        for candidate in response.candidates:
            call_content = candidate.content
            messages.append(call_content)
            
    if not response.function_calls:
        return response.text
    
    function_responses = []
    for call in response.function_calls:
        call_result = call_function(call, verbose)
        if call_result.parts[0]:
            function_responses.append(call_result.parts[0])
        else:
            raise Exception("Function call failed or returned no response.:", call_result.parts[0].function_response.name)    
    messages.append(types.Content(role="user", parts=function_responses))

if __name__ == "__main__":
    main()
