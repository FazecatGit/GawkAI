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

    MAX_ITERATIONS = 20

    try:

        for i in range(MAX_ITERATIONS):
            response = generate_content(client1, messages1)

            # If model gave a natural language text answer:
            if response.text and response.text.strip():
                # Add model's response to messages
                for candidate in response.candidates:
                    messages1.append(candidate.content)
                    
                # Only stop if this response also has no function calls (i.e., it's really final)
                if not response.function_calls:
                    print(f"\nFinal answer:\n{response.text}")
                    break

            # If model wants to call a tool:
            if response.function_calls:
                # Add model's tool call proposals into messages FIRST
                for candidate in response.candidates:
                    messages1.append(candidate.content)
                    
                print(f"DEBUG: Number of function calls: {len(response.function_calls)}")
                
                tool_parts = []
                for j, call in enumerate(response.function_calls):  # Changed i to j to avoid conflict
                    print(f"DEBUG: Processing function call {j+1}: {call.name}")
                    
                    tool_response_content = call_function(call, verbose)
                    
                    if verbose:
                        print(f"-> {tool_response_content.parts[0].function_response.response}")

                    result_dict = tool_response_content.parts[0].function_response.response
                    print(f"Function returned:\n{result_dict.get('result') or result_dict.get('error')}")
                    
                    tool_parts.append(tool_response_content.parts[0])
                
                print(f"DEBUG: Number of tool_parts collected: {len(tool_parts)}")
                
                # Send all function responses in ONE message
                messages1.append(types.Content(role="tool", parts=tool_parts))
            else:
                print("No function call requested; stopping.")
                break
    except Exception as e:
        print(f"Error during execution: {e}")

    # Verbose output
    if verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()


    