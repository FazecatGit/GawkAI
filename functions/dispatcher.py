from google.genai import types
from functions.get_files_info import get_files_info, get_file_content, write_file
from functions.run_python import run_python_file

# adjust this to your actual working directory, or pass it in as an arg
WORKING_DIRECTORY = "calculator"


FUNCTION_MAP = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
    }

def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    target_function= FUNCTION_MAP.get(function_name)

    if target_function is None:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )   
    
    args["working_directory"] = WORKING_DIRECTORY

    try:
        function_result = target_function(**args)
    except Exception as e:
        function_result = f"Error while calling {function_name}: {e}"

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )
        ],
    )