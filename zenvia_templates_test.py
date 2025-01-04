import requests
import json
from time import sleep
import re

# Function to validate phone numbers
def is_valid_phone_number(number):
    return re.fullmatch(r'\+?[1-9]\d{10,14}$', number) is not None

# Receiving and validating user inputs
while True:
    token = input("Enter the API token: ")
    if token:
        break
    print("Token cannot be empty.")

while True:
    from_number = input("Enter the sender's phone number: ")
    if is_valid_phone_number(from_number):
        break
    print("Invalid sender number. Use a valid international format.")

while True:
    to_number = input("Enter the recipient's phone number: ")
    if is_valid_phone_number(to_number):
        break
    print("Invalid recipient number. Use a valid international format.")

while True:
    try:
        sleep_time = int(input("Enter the sleep time between messages (in seconds): "))
        if sleep_time > 0:
            break
        print("Sleep time must be a positive integer.")
    except ValueError:
        print("Please enter a valid number.")

# URL to fetch approved templates
url_templates = 'https://api.zenvia.com/v2/templates'
headers = {
    'X-API-TOKEN': token,
    'Content-Type': 'application/json',
}
payload_templates = {'channel': 'WHATSAPP', 'status': 'APPROVED'}

# Fetching approved templates
response_templates = requests.get(url_templates, headers=headers, params=payload_templates)

# Checking request success
if response_templates.status_code != 200:
    print("Error fetching templates:", response_templates.text)
    exit()

# Processing templates
templates = response_templates.json()

# URL to send messages
url_send = 'https://api.zenvia.com/v1/channels/whatsapp/messages'

for template in templates:
    # Creating custom fields
    fields = {}
    for field in template['fields']:
        fields[field] = field

    # Constructing the message payload
    payload_send = {
        'from': from_number,
        'to': to_number,
        'contents': [
            {
                'type': 'template',
                'templateId': template['id'],
                'fields': fields,
            }
        ]
    }

    # Sending the message
    response_send = requests.post(url=url_send, headers=headers, json=payload_send)

    # Displaying the API response
    if response_send.status_code != 200:
        print("Error sending message:", response_send.text)
    else:
        print(f"Message sent successfully! TemplateId = {template['id']}")

    sleep(sleep_time)
