from flask import request, jsonify
from . import registration_login_bp
from .registration_login_api_service import user_registration_insert, user_login

# Route: Register User (Create new user)
@registration_login_bp.route('/signup', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields: username, email, or password"}), 400

    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({"error": "Invalid email format"}), 400

    # password_hash = hash_password(password)
    password_hash= password
    return user_registration_insert(username, email, password_hash)

# Route: Login User (Authenticate and log user in)
@registration_login_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    return user_login(email, password)
