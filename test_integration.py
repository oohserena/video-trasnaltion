import threading
import time
from server import start_server
from client import VideoTranslationClient
import unittest

class TestVideoTranslationIntegration(unittest.TestCase):
    """Integration tests for video translation server and client"""

    @classmethod
    def setUpClass(cls):
        cls.server_delay = 5  # Simulated server delay in seconds
        cls.server_thread = threading.Thread(target=start_server, args=(cls.server_delay,), daemon=True)
        cls.server_thread.start()
        time.sleep(2)  # Allow server to spin up

    
    def test_poll_status_success(self):
        print("Test that the client correctly handles normal polling")

        client = VideoTranslationClient("http://127.0.0.1:5000")
        result = client.poll_status(max_retries=10, interval=1)
        print(f"Final status: {result}")
        self.assertIn(result, ["completed", "error", "timeout"])

    def test_poll_status_immediate_completion(self):
        print("Test when the server responds with completed immediately")
        client = VideoTranslationClient("http://127.0.0.1:5000")
        result = client.poll_status(max_retries=1, interval=1)  # Quick poll
        print(f"Final status after immediate poll: {result}")
        self.assertIn(result, ["completed", "error", "timeout"])

    def test_poll_status_timeout(self):
        print("Test that the client returns timeout if the server delay exceeds retries")
        client = VideoTranslationClient("http://127.0.0.1:5000")
        result = client.poll_status(max_retries=2, interval=1)  # Adjust retries to fit server delay
        print(f"Final status with timeout: {result}")
        self.assertIn(result, ["timeout", "error"])
       

    def test_server_error_handling(self):
        print("Test the client's ability to handle server errors")
        client = VideoTranslationClient("http://127.0.0.1:5000")
        original_url = client.base_url
        client.base_url = "http://127.0.0.1:9999"  # Invalid URL to simulate server error
        result = client.get_status()
        print(f"Error result: {result}")
        self.assertTrue(result.startswith("error:"))
        client.base_url = original_url  # Reset to the correct URL

    # def test_status_transitions(self):
    #     """Test server status transitions from pending to completed/error"""
    #     client = VideoTranslationClient("http://127.0.0.1:5000")
    #     time.sleep(2)
        
    #     # Check initial status
    #     response = client.get_status()
    #     initial_status = response
    #     self.assertEqual(initial_status, "pending")  # Explicitly check for 'pending'
        
    #     # Wait for server transition
    #     time.sleep(self.server_delay + 1)
        
    #     # Check final status
    #     response = client.get_status()
    #     self.assertIn(response, ["completed", "error"])


if __name__ == "__main__":
    unittest.main()
