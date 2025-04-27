"""
This script demonstrates how to obtain and use a token for authentication with the API.

To use this script:
1. Make sure the Django server is running
2. Run this script with Python: python token_auth_example.py
3. The script will show how to obtain a token and make authenticated requests
4. It also demonstrates how to create forms with form fields in a single request
5. It also demonstrates how to logout (invalidate the token) and shows that
   authenticated requests fail after logout

Note: The system now generates a new token each time a user logs in, and old tokens are invalidated.
When a user logs out, their token is deleted and can no longer be used for authentication.

The script includes examples of:
- Making authenticated requests to protected endpoints
- Creating a form with form fields in a single request
- Logging out (invalidating the token)

Requirements:
- requests library: pip install requests
"""

import requests
import json

# Base URL of your Django application
BASE_URL = 'http://127.0.0.1:8000'

def get_token(username, password):
    """Obtain an authentication token using username and password."""
    url = f"{BASE_URL}/api-token-auth/"
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json().get('token')
        print(f"Successfully obtained token: {token}")
        return token
    else:
        print(f"Failed to obtain token. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def make_authenticated_request(token, endpoint):
    """Make an authenticated request to the specified endpoint."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers)

    print(f"\nMaking authenticated request to: {url}")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")

def make_unauthenticated_request(endpoint):
    """Make an unauthenticated request to the specified endpoint."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url)

    print(f"\nMaking unauthenticated request to: {url}")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

def logout(token):
    """Logout by invalidating the current token."""
    url = f"{BASE_URL}/api/logout/"
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.post(url, headers=headers)

    print(f"\nLogging out (invalidating token)...")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    else:
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    # Replace with your actual username and password
    username = "admin"
    password = "your_password_here"

    print("=== Token Authentication Example ===")

    # First, try making an unauthenticated request
    make_unauthenticated_request("/api/dynamic-form/")

    # Get a token
    token = get_token(username, password)

    if token:
        # Make an authenticated request
        make_authenticated_request(token, "/api/dynamic-form/")

        # Example of making a POST request with authentication
        print("\nExample of making a POST request with authentication:")
        print("""
        import requests

        url = "http://127.0.0.1:8000/api/dynamic-form/"
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, world!"
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.json())
        """)

        # Example of creating a form with fields in a single request
        print("\nExample of creating a form with fields in a single request:")
        print("""
        import requests
        import json

        url = "http://127.0.0.1:8000/api/forms/"
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        form_data = {
            "name": "Contact Form",
            "description": "A form to collect contact information",
            "form_fields": [
                {
                    "field_name": "First Name",
                    "field_mapping": "first_name"
                },
                {
                    "field_name": "Last Name",
                    "field_mapping": "last_name"
                },
                {
                    "field_name": "Email Address",
                    "field_mapping": "email"
                },
                {
                    "field_name": "Phone Number",
                    "field_mapping": "phone"
                },
                {
                    "field_name": "Your Message",
                    "field_mapping": "message"
                }
            ]
        }

        response = requests.post(url, headers=headers, json=form_data)
        print(json.dumps(response.json(), indent=2))
        """)

        # Demonstrate logout functionality
        print("\n=== Logout Example ===")
        logout_success = logout(token)

        if logout_success:
            print("\nTrying to make an authenticated request after logout...")
            make_authenticated_request(token, "/api/dynamic-form/")
            print("As expected, the request failed because the token was invalidated during logout.")
