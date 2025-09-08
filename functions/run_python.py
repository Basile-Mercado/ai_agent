import os
import subprocess
        
def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        if full_path.endswith('.py') == False:
            print(f'Error: "{file_path}" is not a Python file.')
        elif os.path.isfile(full_path) == False:
            print(f'Error: File "{file_path}" not found.')
        elif working_directory not in os.path.abspath(full_path):
            print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        else:
            print("Executing Python file...")
            completed_process = subprocess.run(
                ['python', os.path.abspath(full_path)] + args, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                timeout=30, 
                cwd=working_directory,
            )
            if completed_process.stdout != "":
                print(
                    f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}\n" 
                    if completed_process.returncode < 0 else f"Process Exited with code {completed_process.returncode}"
                    )
            else :
                print("STDOUT: No output produced.\nSTDERR: " + completed_process.stderr)
    except Exception as e:
        print(f"Error: executing Python file: {e}")