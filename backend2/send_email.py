import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the recipient email address
json_file_path = '../backend1/deploy_confirm/chat_id1.json'
with open(json_file_path, 'r') as file:
    data = json.load(file)
recipient_email = data.get('email_id')  # Make sure the JSON contains an 'email' key

# Load the email content from result.txt
with open('result.txt', 'r') as file:
    email_content = file.read()

# Email setup
sender_email = 'easy.ai.deploys@gmail.com'
sender_password = 'fwyuwmbenmxrznhc'
smtp_server = 'smtp.gmail.com'
port = 587  # For starttls

# Create a secure SSL context and send the email
message = MIMEMultipart()
message["Subject"] = "Result Notification"
message["From"] = sender_email
message["To"] = recipient_email

# Add body to email
message.attach(MIMEText(email_content, "plain"))

try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls()  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    server.quit()
