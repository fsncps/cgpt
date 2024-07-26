import openai
import os
import json

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize conversation history
def initialize_conversation():
    return [{"role": "system", "content": "You are a helpful assistant."}]

# Function to add messages to the conversation and get a response with streaming
def add_message_and_get_response(conversation, user_message):
    conversation.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=conversation,
        stream=True
    )
    assistant_message = ""
    print("Assistant: ", end="", flush=True)
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta'].get('content', '')
        print(chunk_message, end="", flush=True)
        assistant_message += chunk_message
    print()  # Newline after complete message
    conversation.append({"role": "assistant", "content": assistant_message})
    return assistant_message

# Function to save the conversation to a JSON file
def save_conversation(conversation, filename="conversation.json"):
    with open(filename, "w") as f:
        json.dump(conversation, f, indent=2)

# Function to load the conversation from a JSON file
def load_conversation(filename="conversation.json"):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as f:
            return json.load(f)
    else:
        return initialize_conversation()

if __name__ == "__main__":
    # Load previous conversation if exists, otherwise initialize a new one
    conversation = load_conversation("conversation.json")

    while True:
        user_input = input("You: ")
        assistant_response = add_message_and_get_response(conversation, user_input)

        save_conversation(conversation)

