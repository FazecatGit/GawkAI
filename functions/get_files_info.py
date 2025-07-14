import os
from functions.config import*

def get_files_info(working_directory, directory=None):
    try:
         
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory = os.path.abspath(working_directory)

        if not full_path.startswith(working_directory):
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(full_path):
            return (f'Error: "{directory}" is not a directory')
        
    
        files = os.listdir(full_path)
        result_lines = []    
        for file in files:
            file_path = os.path.join(full_path, file)
            is_dir = os.path.isdir(file_path)
            size = os.path.getsize(file_path)
            result_lines.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")
        
        if directory == ".":
            header = "Result for current directory:"
        else:
            header = f"Result for '{directory}' directory:"
        return f"{header}\n" + "\n".join(result_lines)
    
    except Exception as e:
        return f"Error: {e}"
    
    
def get_file_content(working_directory, file_path):
    try:

        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        if not full_path.startswith(working_directory):
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(full_path):
            return (f'Error: File not found or is not a regular file: "{file_path}"')
        
        with open(full_path, "r") as f:
            file_content_string = f.read()

        if len(file_content_string) > MAX_CHAR_LIMIT:
            truncated_message = (f'...File "{file_path}" truncated at 10000 characters')
            return file_content_string[:MAX_CHAR_LIMIT] + truncated_message
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
    
def write_file(working_directory, file_path, content):
    try:

        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_directory = os.path.abspath(working_directory)

        if not full_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            chars_written = f.write(content)
        return f'Successfully wrote to "{file_path}" ({chars_written} characters written)'

    except Exception as e:
        return f"Error: {e}"


#    os.path.abspath(): Get an absolute path from a relative path 
#    os.path.join(): Join two paths together safely (handles slashes) \
#    .startswith(): Check if a string starts with a substring \
#     os.path.isdir(): Check if a path is a directory \
#     os.listdir(): List the contents of a directory
#     os.path.getsize(): Get the size of a file \
#     os.path.isfile(): Check if a path is a file 
#     .join(): Join a list of strings together with a separator \
