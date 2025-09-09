import os
from functions.config import *

def get_files_info(working_directory, directory="."):    
    try:
        full_path = os.path.join(working_directory, directory)
        list_of_files = os.listdir(full_path)
        if working_directory in os.path.abspath(full_path):
            to_return_str = ""
            for i in list_of_files:
                to_return_str += f"- {i}: file_size={os.path.getsize(f'{full_path}/{i}')} bytes, is_dir={os.path.isdir(os.path.join(full_path, i))}\n"            
            return to_return_str
        elif os.path.isdir(directory) == False:
            return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {str(e)}'
    
def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if working_directory in os.path.abspath(full_path):
            content = ""
            with open(full_path, 'r') as file:
                content = file.read()
                if len(content) > MAX_FILE_SIZE:
                    content = content[:MAX_FILE_SIZE] + f"[...File \"{full_path}\" truncated at {MAX_FILE_SIZE} characters]"
            return f"- {file_path}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}\n{content}"
        elif os.path.isfile(full_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {str(e)}'
    
def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        if working_directory in os.path.abspath(full_path):
            with open(full_path, 'w') as file:
                file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        elif os.path.isfile(full_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {str(e)}'