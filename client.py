import requests
import time
import logging

class VideoTranslationClient:
    # Client library for querying video translation server status
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def get_status(self):
        # Gets the current status from the server
        try:
            response = requests.get(f"{self.base_url}/status", headers=self.headers, timeout=5)
            response.raise_for_status()
            return response.json().get("result", "unknown")
        except requests.RequestException as e:
            logging.error(f"Error during get_status: {e}")
            return f"error: {str(e)}"

    def poll_status(self, max_retries=10, interval=1, backoff_factor=1.5):
        # Polls the server for status with exponential backoff
        retries = 0
        while retries < max_retries:
            status = self.get_status()
            logging.info(f"Attempt {retries + 1}: Received status '{status}'")
            if status in ["completed", "error"]:
                return status
            time.sleep(interval)
            interval *= backoff_factor
            retries += 1
        logging.warning("Polling timed out.")
        return "timeout"
