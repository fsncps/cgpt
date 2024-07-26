
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize OpenAI client

class OpenAIAssistant:
    def __init__(self):
        self.model = "gpt-4"
        self.temperature = 0.7
        self.max_tokens = 550
        self.top_p = 1.0
        self.presence_penalty = 0.5
        self.frequency_penalty = 0.5
        self.user_name = "Claire"
        self.assistant_name = "Carl-Gustav"
        self.greeting_message = "Hello Claire! How can I assist you today?"
        self.conversation_file = "data/prompts.json"
        self.conversation = self.load_conversation()
        self.add_message("assistant", self.greeting_message)

    def add_message(self, role, content):
        self.conversation.append({"role": role, "content": content})

    def get_response(self):
        try:
            response = client.chat.completions.create(model=self.model,
            messages=self.conversation,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            stream=True)
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end='', flush=True)
                    full_response += content
            print()  # For newline after the stream
            return full_response
        except Exception as e:
            print("Error occurred:", e)
            return "There was an error processing your request."

    def save_conversation(self):
        try:
            with open(self.conversation_file, 'w') as file:
                json.dump(self.conversation, file, indent=4)
        except Exception as e:
            print(f"Error saving conversation: {e}")

    def load_conversation(self):
        if os.path.exists(self.conversation_file):
            try:
                with open(self.conversation_file, 'r') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error loading conversation: {e}")
        return [{"role": "system", "content": "You are a cat by the name of Carl-Gustav and a computer expert and your task is to assist Claire with all computer stuff, LinkedIn and writing application letters and CVs."}]

    def chat(self):
        print(self.greeting_message)
        while True:
            user_input = input(f"{self.user_name}: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if user_input.lower() in ['help', 'assist']:
                help_messages = [
                    "If you need any help, feel free to ask!",
                    "How can I assist you today?",
                    "Need some help? I'm here for you."
                ]
                help_message = random.choice(help_messages)
                print(help_message)
                continue

            # Add user message to conversation
            self.add_message("user", user_input)

            # Get and print assistant's response
            response = self.get_response()
            if response:
                self.add_message("assistant", response)
                self.save_conversation()
            else:
                print(f"{self.assistant_name}: Sorry, I couldn't process your request.")

if __name__ == "__main__":
    assistant = OpenAIAssistant()
    assistant.chat()
