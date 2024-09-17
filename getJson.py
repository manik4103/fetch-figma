from flask import Flask, request, jsonify, render_template
import requests
import os

# Initialize Flask app
app = Flask(__name__)

def get_figma_file(file_key, api_token):
    headers = {
        'X-Figma-Token': api_token
    }
    url = f'https://api.figma.com/v1/files/{file_key}'
    response = requests.get(url, headers=headers)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-figma', methods=['POST'])
def fetch_figma_data():
    try:
        # Debugging to print the received data
        print("Received JSON:", request.json)

        # Extract file_key and api_token from the request payload
        data = request.json
        file_key = data.get('file_key')
        api_token = data.get('api_token')

        if not file_key or not api_token:
            return jsonify({"error": "file_key and api_token are required"}), 400

        # Fetch the Figma file data using the provided file_key and api_token
        figma_data = get_figma_file(file_key, api_token)

        # Return the Figma data as a JSON response
        return jsonify(figma_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
