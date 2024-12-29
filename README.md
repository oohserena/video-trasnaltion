# Video Translation Server and Client

## Components
### 1. Server
`check_status()`: Returns the current translation status. The status is "pending" initially and after simulated delay, it randomly swiches to either "completed" or "error".

`VideoTranslationApp`(Flask API)
API Endpoint:
`/status`: Returns the current status of the video translation (either "completed", "error", or "pending").

The Flask app runs on port `5000`.

### 2. Client (Flask API)
`get_status()`: Queries the server for the current translation status.
`poll_status()`:  Polls the server at regular intervals with exponential backoff until a status of "completed" or "error" is received, or the maximum retries are reached.

### 3. Integration Tests
`test_poll_status_success()`: Verifies that the client can successfully poll for a completed or errored status.

`test_poll_status_immediate_completion()`: Simulates an immediate response from the server and tests client behavior.

`test_poll_status_timeout()`: Simulates a timeout if the server delay exceeds the retry limit.

`test_server_error_handling()`: Tests the client's error handling when the server is unavailable.

## Usage
### 1. Start the server
Run `server.py` to start the server:
```bash
python server.py
```

### 2. Use the client library
You can use `get_status()` to fetch the current translation status or `poll_status()` to repeatedly check the status until it completes or an error occurs.

### 3. Run the integration test
Run `test_integration.py`:
```bash
python -m unittest test_integration
```

This test starts the server, creates a client, and polls the server status until the job completes or fails

## How It Works
To implement this efficiently and with the customer in mind, the client can use exponential backoff and retry mechanisms to avoid excessive polling and meantime still ensuring that the client gets a result.

### 1. Exponential Backoff
Polling a server too frequently can lead to unnecessary load or delay getting a result. Exponential backoff can adjust the frequency of retries based on the responsetime. For example, the client will retry quickly, but if the server takes longer to respond, the retry interval will increase to reduce the frequency of unnecessary queries.

This ensures that the customer using the client library is not overburdened by excessive requests.

### 2. Timeout and Error Handling
If server is slow to respond or unavailable, our client will set a maximum number of retries and it will stop polling and return a timeout message after.

By providing clear feedback after retries, the client library ensures that the customer knows the outcome instead of leaving them wondering whether the process is still ongoing or stuck.

### 3. Configurable Retries and Intervals
Some customers need quicker results and can tolerate more frequent requests but some may prefer less frequent queries to avoid overloading the server. We  have configuration options for `max_retries`, `interval`, and `backoff_factor` to allow client library customize the behavior to meet customers' needs.

### 4. Logging and Error Messages
If something goes wrong, like a networking issue or a server failure, the client can provide error messages and logging, so that our customers can understand the issume and do troubleshooting.



