from flask import jsonify, request
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid JSON body"}), 400

    # Check if username and password match hardcoded values
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_password = os.getenv('ADMIN_PASSWORD')
    if data['username'] == admin_username and data['password'] == admin_password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
