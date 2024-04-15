from openai import OpenAI
import os, openai, json
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

# Read the JSON file content generated
content = client.files.content(file_id=lastest_file_id).read()

# Parse the content as JSON
data = json.loads(content)

# Write the data to the JSON file
with open("stepUpSage_deployment_planner.json", "w") as f:
    json.dump(data, f, indent=4)

print("The content has been successfully stored in 'deployment_planner.json'.")
