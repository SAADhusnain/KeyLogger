# KeyLogger

A Python-based keylogger that records keystrokes and periodically sends them to a remote server. The keystrokes are also saved locally in a file for backup.

## Features
- **Keystroke Logging**: Captures each key press with a timestamp.
- **Remote Transmission**: Sends collected keystrokes to a configured server endpoint.
- **Local Storage**: Stores keystrokes in a local log file.
- **Buffered Sending**: Keystrokes are sent in batches when a buffer size is reached or after a time interval.
- **Multithreading**: Utilizes separate threads to handle logging, sending, and file operations for efficient performance.

## Requirements

- Python 3.x
- The following Python libraries:
  - `pynput` for capturing keyboard input
  - `requests` for sending HTTP POST requests

Install the required libraries using:

```bash
pip install pynput requests
```
## Configuration
Open the script file and adjust the following settings:

 - **log_file_path**: The path to the local log file where keystrokes will be stored.
 - **server_url**: The URL of the remote server where keystrokes will be sent.
 - **buffer_size**: The number of keystrokes to collect before sending them to the server.
 - **send_interval**: The time interval (in seconds) to send collected keystrokes, even if the buffer is not full.

## Usage
To run the keylogger:

 1. Ensure you have Python 3.x installed.

 2. Install the required Python libraries using the command mentioned above.

 3. Run the script using:

```bash
python keylogger.py  ##(Replace keylogger.py with the name of the script if it's different.)
```


 4. The keylogger will start capturing keystrokes. Press Esc to stop the listener.

## Server Setup
Make sure the server you are sending the keystrokes to is properly set up to handle POST requests. The server should be listening on the specified server_url endpoint and be able to accept text/plain data.

Example using a simple Python HTTP server (with Flask):

```bash
from flask import Flask, request

app = Flask(__name__)

@app.route('/receive_keystrokes', methods=['POST'])
def receive_keystrokes():
    data = request.data.decode('utf-8')
    print(f"Received data:\n{data}")
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```
## Warnings
 - **Legal Notice**: This software is intended for educational and authorized use only. Unauthorized use of this software is illegal and unethical. Ensure you have permission to monitor or log keystrokes on any system before deploying this software.
 - **Privacy**: Do not use this software to capture sensitive information without consent.
 - **Security**: Ensure your server is secured if you are sending keystrokes over a network. Consider encrypting the data if necessary.

## Disclaimer
I am not responsible for any misuse of this software. Use responsibly and ethically.

## Contributing
If you'd like to contribute, feel free to submit a pull request. For any issues, please open an issue on the GitHub repository.

## Author
Mohammad Saad Husnain

saaddi456@gmail.com

Github: SAADhusnain

## Notice
Im still working on this so ive yet to update the readme file so yeah  


