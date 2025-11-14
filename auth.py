"""
Authentication module for MediAI Guardian 3.0
Handles user login and role-based access control
"""

def authenticate_user(username, password):
    """
    Authenticate user credentials and return role
    
    Args:
        username (str): User's username
        password (str): User's password
    
    Returns:
        str: User role ('patient' or 'doctor') if valid, None if invalid
    """
    # Demo credentials
    valid_credentials = {
        "patient": {"password": "123", "role": "patient"},
        "doctor": {"password": "123", "role": "doctor"}
    }
    
    if username in valid_credentials:
        if valid_credentials[username]["password"] == password:
            return valid_credentials[username]["role"]
    
    return None

def check_role_access(required_role, user_role):
    """
    Check if user has access to a specific role-based feature
    
    Args:
        required_role (str): Required role for access
        user_role (str): Current user's role
    
    Returns:
        bool: True if access granted, False otherwise
    """
    if required_role == "any":
        return True
    
    if required_role == "doctor" and user_role == "doctor":
        return True
    
    if required_role == "patient" and user_role == "patient":
        return True
    
    return False

def get_user_permissions(role):
    """
    Get user permissions based on role
    
    Args:
        role (str): User role
    
    Returns:
        dict: Dictionary of permissions
    """
    permissions = {
        "patient": {
            "view_dashboard": True,
            "view_vitals": True,
            "simulate_medicine": True,
            "view_digital_twin": True,
            "access_emergency": True,
            "generate_reports": False,
            "view_all_patients": False
        },
        "doctor": {
            "view_dashboard": True,
            "view_vitals": True,
            "simulate_medicine": True,
            "view_digital_twin": True,
            "access_emergency": True,
            "generate_reports": True,
            "view_all_patients": True
        }
    }
    
    return permissions.get(role, {})
