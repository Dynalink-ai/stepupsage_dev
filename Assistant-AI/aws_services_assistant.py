from openai import OpenAI
import json, os, openai
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Initialize OpenAI API
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# retrieve the list of files from the OpenAI Storage
files = client.files.list()

# latest file from the list
lastest_file = files.data[0]

# file ID of the lastest file
lastest_file_id = lastest_file.id

# Create an Assistant
assistant = client.beta.assistants.create(
    name="AWS Services Assistant",
    instructions="You are a deployment planner. Need to ask the user set of questions.Read the file provided in the attachment and ask the question for next stage such as name of the application they want to deploy, then ask the url of their docker image repository and tell the user to ensure the repository is public, then ask the list of aws services he want to use and if he has not idea about the aws services used ask the relevant to questions to determine the list of aws services that would be required to deploy his application and generate a JSON file based on the questionnaire and the user inputs. Questions can change according to the user input.",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-3.5-turbo-0125",
    file_ids=[lastest_file_id]
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
