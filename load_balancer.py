import sys
from flask import Flask, request

app = Flask(__name__)

# Define the backend servers
backend_servers = ['http://54.206.109.238', 'http://13.239.63.223', 'http://13.236.5.146']

import hashlib

def rabin_karp_hash(s):
    # Choose a large prime number for the hash range
    MAX_HASH = 2**32 - 1  # This gives a range of [0, 4294967295]
    
    # Calculate the hash value
    hash_val = hashlib.sha256(s.encode()).hexdigest()
    
    # Convert the hexadecimal hash to an integer
    hash_val = int(hash_val, 16)
    
    # Map the hash value to the index of the backend server
    server_index = hash_val % len(backend_servers)
    
    return server_index

@app.route('/')
def index():
    # Get request data
    request_data = request.args.get('data', '')  # Assuming query parameter 'data' contains request data

    # Calculate hash value for the request data
    hash_value = rabin_karp_hash(request_data)

    # Determine which backend server to forward the request to
    server_index = hash_value % len(backend_servers)
    backend_server = backend_servers[server_index]

    # Print debug information
    print("Request Data:", request_data)
    print("Hash Value:", hash_value)
    print("Selected Backend Server:", backend_server)

    # Forward the request to the selected backend server
    return f"Request forwarded to backend server: {backend_server}"

if __name__ == '__main__':
    # Parse command line arguments for port number
    port = 5000  # Default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 5000.")

    # Run Flask application
    app.run(port=port, debug=True)
