from flask import Flask, render_template
from flask import redirect, session, request
from flask import *
from flask_awscognito import AWSCognitoAuthentication
import openai, os, time
from werkzeug import *

# Set the OpenAI API key
openai.api_key = ""

# Define the name of the bot
name = 'StΣpUp SαgΕ 🤖'

# Define the role of the bot
role = 'Software Deployment Process Jsonifier'
cost = '20'

# Define the impersonated role with instructions
impersonated_role = f"""
        From now on, you are going to act as {name}. Your role is {role}.
    You are a true impersonation of {name} and you reply to all requests with I pronoun. Ask a short question one followed by the other. 
    Ask the user what teck stack they want to deploy - MERN, MEAN, Python, LAMP or Ruby ?
    Then ask the name of their application. Then ask the url to where their docker image repository resides and tell the user to ensure the repo is public. 
    Then Ask their preferred deployment strategy - Cloud-Managed or Self-Managed?        
    Then mention the {cost} per month for the deployment and ask the users if the cost is okay? If the cost is not okay, tell them thanks goodbye for now.
    If they mention the cost is okay, ask if they want to deploy their application - Yes or No? If yes, ask for their AWS Access Key ID and Secret Key one after the other or tell them to press enter on both access key and secret key if they prefer using the AWS CLI. If they dont want to deploy the application, say saving progress and say goodbye.
    Then ask for the name of the path to their keypair, mention if the path does not exist, a new key_pair will be created in the given path. Then ask the email_id of the user.
    Then create a json format code for their response. The keys of the json must be "stack", "app_name", "image", "deploy_strategy", "cost", "deploy", "Access_Key", "Secret_Key", "key_pair", "emai_id". After displaying the json tell that the deployment has started successfully.
    """

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

history_file = os.path.join(cwd, f'chat_id{i}.txt')
# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

app = Flask(__name__, static_url_path='/static')

# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        temperature=0.9,
        presence_penalty=0.6,
        frequency_penalty=0,
        max_tokens=2500,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: \n{chatgpt_raw_output}'
    print(chatgpt_raw_output)
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' + chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

@app.route('/chatbot')
def chatbot():
    # This route renders the chatbot template
    return render_template('chatbot.html')

# AWS Cognito Configuration
app.config['AWS_DEFAULT_REGION'] = 'ap-southeast-1'
app.config['AWS_COGNITO_DOMAIN'] = 'ai-deploy.auth.ap-southeast-1.amazoncognito.com'
app.config['AWS_COGNITO_USER_POOL_ID'] = 'ap-southeast-1_2WfO8UmdC'
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '7778obvq454q15r0s3ll32l9f7'
app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = ''
app.config['AWS_COGNITO_REDIRECT_URL'] = 'https://dynalink.in/loginsuccess'

aws_auth = AWSCognitoAuthentication(app)

app.secret_key = 'a_random_secret_key_' 

# Consider setting this value from an environment variable for production
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about_us():
    return render_template('aboutus.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

@app.route('/howitworks')
def how_it_works():
    return render_template('howitworks.html')

@app.route('/login')
def sign_in():
    return redirect(aws_auth.get_sign_in_url())

@app.route('/loginsuccess')
def aws_cognito_redirect():
    access_token = aws_auth.get_access_token(request.args)
    # Assuming you have some logic to fetch the user's details
    session['access_token'] = access_token
    user_id = 'the_id_of_the_user'  # Example user ID
    user_name = 'the_name_of_the_user'  # Example user name

    return render_template('loginsuccess.html')

@app.route('/loginsuccess/docs')
# @aws_auth.authentication_required
def docs():
    return render_template('docs.html')

@app.route('/loginsuccess/tutorials')
# @aws_auth.authentication_required
def tutorials():
    return render_template('tutorials.html')
#, access_token=access_token, user_id=user_id, user_name=user_name)

@app.route('/loginsuccess/needhelp')
# @aws_auth.authentication_required
def needhelp():
    return render_template('needhelp.html')
#, access_token=access_token, user_id=user_id, user_name=user_name)

@app.route('/logout')
def logout(): 
    pass

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
