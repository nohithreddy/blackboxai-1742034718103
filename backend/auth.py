# Simple in-memory user store (replace with database in production)
USERS = {
    'admin': {
        'password': 'admin123',
        'role': 'admin'
    },
    'student': {
        'password': 'student123',
        'role': 'student'
    },
    'alpha': {
        'password': 'alpha123',
        'role': 'alpha'
    }
}

# Role-based permissions
PERMISSIONS = {
    'admin': ['run_model', 'install_package', 'chat'],
    'student': ['run_model', 'chat'],
    'alpha': ['run_model', 'chat']
}

def verify_credentials(username, password, role):
    """Verify user credentials and role"""
    user = USERS.get(username)
    if user and user['password'] == password and user['role'] == role:
        return True
    return False

def enforce_permissions(role, action):
    """Check if role has permission to perform action"""
    return action in PERMISSIONS.get(role, [])
