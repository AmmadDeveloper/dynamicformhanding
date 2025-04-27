"""
This script demonstrates how to create a form with form fields in a single request and submit data to it.

To use this script:
1. Make sure the Django server is running
2. Run this script with Python: python form_post_example.py
3. The script will show how to obtain a token and create a form with fields
4. It will display the submission URL for the created form
5. It will submit sample data to the form and show the response

The script demonstrates the complete workflow:
- Creating a form with fields
- Getting the form details
- Testing the submission URL
- Submitting data to the form

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
    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.post(url, data=data, verify=False)

    if response.status_code == 200:
        token = response.json().get('token')
        print(f"Successfully obtained token: {token}")
        return token
    else:
        print(f"Failed to obtain token. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_form_with_fields(token, form_data):
    """Create a form with fields in a single request."""
    url = f"{BASE_URL}/api/forms/"
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }

    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.post(url, headers=headers, json=form_data, verify=False)

    print(f"\nCreating form with fields...")
    print(f"Status code: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Response: {response.text}")
        return None

def get_form_with_fields(token, form_id):
    """Get a form with its fields."""
    url = f"{BASE_URL}/api/forms/{form_id}/"
    headers = {
        'Authorization': f'Token {token}'
    }

    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.get(url, headers=headers, verify=False)

    print(f"\nGetting form with fields...")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Response: {response.text}")
        return None

def test_submission_url(token, submission_url):
    """Test the submission URL by making a GET request to it."""
    headers = {
        'Authorization': f'Token {token}'
    }

    print(f"\nTesting submission URL: {submission_url}")
    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.get(submission_url, headers=headers, verify=False)

    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Response: {response.text}")
        return None

def submit_form_data(token, submission_url, form_data):
    """Submit data to a form."""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }

    print(f"\nSubmitting data to form: {submission_url}")
    print(f"Data: {json.dumps(form_data, indent=2)}")

    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.post(submission_url, headers=headers, json=form_data, verify=False)

    print(f"Status code: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Response: {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace with your actual username and password
    username = "admin"
    password = "your_password_here"

    # Get a token
    token = get_token(username, password)

    if token:
        # Example form data with fields
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

        # Create the form with fields
        created_form = create_form_with_fields(token, form_data)

        # If form was created successfully, get it to verify fields were created
        if created_form and 'id' in created_form:
            form_details = get_form_with_fields(token, created_form['id'])

            # Test the submission URL if it's in the response
            if form_details and 'submission_url' in form_details:
                submission_url = form_details['submission_url']
                print(f"\nForm submission URL: {submission_url}")

                # Test the submission URL
                test_submission_url(token, submission_url)

                # Example of how to submit data to the form
                print("\nExample of how to submit data to the form:")
                print(f"""
                import requests

                url = "{submission_url}"
                headers = {{
                    'Authorization': 'Token YOUR_TOKEN',
                    'Content-Type': 'application/json'
                }}
                data = {{
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "phone": "123-456-7890",
                    "message": "Hello, this is a test submission!"
                }}

                response = requests.post(url, headers=headers, json=data)
                print(response.json())
                """)

                # Actually submit data to the form
                form_submission_data = {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "phone": "123-456-7890",
                    "message": "Hello, this is a test submission!"
                }

                submit_form_data(token, submission_url, form_submission_data)
