import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
         
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        if not full_path.startswith(working_directory):
            return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.exists(full_path):
            return (f'Error: File "{file_path}" not found.')
        if not file_path.endswith(".py"):
            return (f'Error: "{file_path}" is not a Python file.')

        result = subprocess.run(["python3", file_path],
                                stderr=subprocess.PIPE, 
                                stdout=subprocess.PIPE,
                                cwd=working_directory, 
                                timeout = 30
                                )
        output = ""
        if result.stdout.decode().strip():
            output += "STDOUT:" + result.stdout.decode()
        if result.stderr.decode().strip():
            output += "STDERR: " +result.stderr.decode()
        if result.returncode != 0:
            output += f"Process exited code {result.returncode}"
        if not output.strip():
            output = "No output produced."
        return output
    

    except Exception as e:
        return f"Error: executing Python file: {e}"

