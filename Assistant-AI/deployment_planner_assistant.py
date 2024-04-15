from openai import OpenAI
import json, os, openai
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Initialize OpenAI API
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Create an Assistant
assistant = client.beta.assistants.create(
    name="Deploy-AI Assistant",
    instructions="You are a deployment planner. Need to ask the user set of questions, a minimum of 6 and a maximum of 15 and generate a JSON file based on the questionnaire and the user inputs. Questions can change according to the user input.",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-3.5-turbo-0125",
)

# Create a thread
thread = client.beta.threads.create()

# Add message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Question-1"
)

# Answer for the question from user
user_input = input()

# Add user input as a message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
)

# Run the thread using the assistant
try:
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)

      