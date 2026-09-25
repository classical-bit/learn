import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("OPENROUTER_API_KEY is None!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def main():
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ],
    )

    if response.usage == None:
        raise RuntimeError("OpenRouter response usage is None!")


    print(f"User Prompt: {args.user_prompt}")
    print(f"Prompt Tokens: {response.usage.prompt_tokens}")
    print(f"Response Tokens: {response.usage.completion_tokens}")
    print(f"Response: \n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
