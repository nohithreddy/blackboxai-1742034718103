from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
import os
from auth import verify_credentials, enforce_permissions
from notebook_integration import execute_code
from ai_integration import generate_code, ai_chat

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Configure session
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')  # Change in production
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not all([username, password, role]):
        return jsonify({'error': 'Missing credentials'}), 400

    user = verify_credentials(username, password, role)
    if user:
        session['user'] = {
            'username': username,
            'role': role
        }
        return jsonify({
            'message': 'Login successful',
            'user': {
                'username': username,
                'role': role
            }
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'})

@app.route('/api/run', methods=['POST'])
def run_model():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Check if user has permission to run models
    if not enforce_permissions(session['user']['role'], 'run_model'):
        return jsonify({'error': 'Permission denied'}), 403

    try:
        # Get file and parameters from request
        file = request.files.get('file')
        model_type = request.form.get('model')
        run_mode = request.form.get('mode')

        if not all([file, model_type, run_mode]):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Generate code using AI
        generated_code = generate_code({
            'filename': file.filename,
            'content': file.read().decode('utf-8')
        }, model_type, run_mode)

        # Execute the generated code
        timestamp = datetime.now().isoformat()
        result = execute_code(generated_code)

        return jsonify({
            'timestamp': timestamp,
            'output': result,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    message = data.get('message')
    username = data.get('username')

    if not message or not username:
        return jsonify({'error': 'Missing message or username'}), 400

    try:
        response = ai_chat(message, username)
        return jsonify({
            'response': response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/admin/install-package', methods=['POST'])
def install_package():
    if 'user' not in session or session['user']['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    package_name = request.json.get('package')
    if not package_name:
        return jsonify({'error': 'Missing package name'}), 400

    try:
        # TODO: Implement secure package installation
        return jsonify({
            'message': f'Package {package_name} installed successfully',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
