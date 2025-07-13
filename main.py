import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        )
    # Call the model
    response = generate_content(client1, messages1)

    # Verbose output
    if verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
        print(response.text)


if __name__ == "__main__":
    main()






    