import os

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