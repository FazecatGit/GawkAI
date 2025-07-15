import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.functiondeclaration import available_functions
from functions.get_files_info import *
from system_prompt import system_prompt
from functions.dispatcher import call_function, WORKING_DIRECTORY
from functions.run_python import run_python_file

def main():
    load_dotenv()
    
    # Parse CLI arguments FIRST
    parser = argparse.ArgumentParser(description="Ask Gemini something")
    parser.add_argument("prompt", help="The prompt to send")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = args.prompt
    verbose = args.verbose

    # gemini client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in environment variables.")
        sys.exit(1)

    client1 = genai.Client(api_key=api_key)
    

    messages1 = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    # calling the model
    def generate_content(client, messages):
        return client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
        )
    # Call the model
    response = generate_content(client1, messages1)

    # Verbose output
    if verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')


    if not response.function_calls:
        print(response.text)
        return

    for call in response.function_calls:
        function_call_result = call_function(call, verbose)

        if not function_call_result.parts or not function_call_result.parts[0].function_response.response:
            raise Exception("Function call did not return proper response")

        result_dict = function_call_result.parts[0].function_response.response

        if verbose:
            print(f"-> {result_dict}")


        print(f"Function returned:\n{result_dict.get('result') or result_dict.get('error')}")

if __name__ == "__main__":
    main()






    