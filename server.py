from flask import Flask, jsonify
import random
import time
import logging

class VideoTranslationServer:
    # Simulates a video translation backend with status tracking
    def __init__(self, delay):
        self.delay = delay
        self.start_time = time.time()
        self.status = "pending"

    def check_status(self):
        # Checks the current status of the video translation process
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.delay:
            if self.status == "pending":
                self.status = random.choice(["completed", "error"])
        logging.info(f"Status changed to: {self.status}") 
        return self.status

class VideoTranslationApp:
    # Flask app for the video translation server
    def __init__(self, delay):
        self.server = VideoTranslationServer(delay)
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        # Sets up the API routes
        self.app.add_url_rule('/status', view_func=self.get_status, methods=['GET'])

    def get_status(self):
        # API endpoint to get the current status
        status = self.server.check_status()
        logging.info(f"Status checked: {status}")
        return jsonify({"result": status})

    def run(self):
        # Runs the Flask app
        logging.info("Starting Flask server...")
        self.app.run(port=5000, debug=False, use_reloader=False)

def start_server(delay):
    # Starts the server in a separate thread
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    app_instance = VideoTranslationApp(delay)
    app_instance.run()
