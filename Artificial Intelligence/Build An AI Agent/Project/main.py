import os
from openai import OpenAI
from dotenv import load_dotenv
import argparse
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from typing_extensions import Iterable


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("OPENROUTER_API_KEY is None!")

def main():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    messages: Iterable[ChatCompletionMessageParam] = [
        {"role": "user", "content": args.user_prompt},
    ]

    response = generate_content(client, messages)

    if response.usage == None:
        raise RuntimeError("OpenRouter response usage is None!")


    print(f"User Prompt: {args.user_prompt}")
    print(f"Prompt Tokens: {response.usage.prompt_tokens}")
    print(f"Response Tokens: {response.usage.completion_tokens}")
    print(f"Response: \n{response.choices[0].message.content}")


def generate_content(client: OpenAI, messages: Iterable[ChatCompletionMessageParam]) -> ChatCompletion:
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

if __name__ == "__main__":
    main()
