from functions.get_files_info import get_file_content, get_files_info, write_file
from functions.run_python import run_python_file
import google.genai.types as types
from functions.config import WORKING_DIR

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")
    function_dictionary = {
        "get_files_info": lambda: get_files_info(WORKING_DIR, function_call_part.args.get("directory", ".")),
        "get_file_content": lambda: get_file_content(WORKING_DIR, function_call_part.args.get("file_path")),
        "write_file": lambda: write_file(WORKING_DIR, function_call_part.args.get("file_path"), function_call_part.args.get("content", "")),
        "run_python_file": lambda: run_python_file(WORKING_DIR, function_call_part.args.get("file_path"), function_call_part.args.get("args", []))
    }
    for function in function_dictionary:
        if function_call_part.name == function:
            function_result = function_dictionary[function]()
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": function_result},
                    )
                ],
            )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)