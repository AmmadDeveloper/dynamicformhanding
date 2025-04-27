"""
This script demonstrates how to submit data to a specific form using its submission URL.

To use this script:
1. Make sure the Django server is running
2. Run this script with Python: python form_submission_example.py
3. The script will show how to obtain a token and submit data to a specific form

The script demonstrates:
- How to authenticate with the API
- How to submit data to a form with a specific ID
- How to handle the response from the form submission

Requirements:
- requests library: pip install requests
"""

import requests
import json

# Base URL of your Django application
BASE_URL = 'http://127.0.0.1:8000'
# The specific form submission URL with ID
FORM_SUBMISSION_URL = 'http://127.0.0.1:8000/api/dynamic-form/?id=a4ayc_80_OGda4BO'

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

def get_form_details(token, form_url):
    """Get details about the form to understand what fields are required."""
    headers = {
        'Authorization': f'Token {token}'
    }

    print(f"\nGetting form details from: {form_url}")
    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.get(form_url, headers=headers, verify=False)

    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"Response: {response.text}")
        return None

def submit_form_data(token, form_url, form_data):
    """Submit data to the form."""
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }

    print(f"\nSubmitting data to form: {form_url}")
    print(f"Data: {json.dumps(form_data, indent=2)}")

    # Disable SSL certificate verification to fix SSL certificate verification error
    response = requests.post(form_url, headers=headers, json=form_data, verify=False)

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

    print("=== Form Submission Example ===")

    # Get a token
    token = get_token(username, password)

    if token:
        # First, get details about the form to understand what fields are required
        form_details = get_form_details(token, FORM_SUBMISSION_URL)

        if form_details and form_details.get('status') == 'success':
            print("\nPreparing to submit data to the form...")

            # Example form submission data
            # This should match the fields defined in the form
            form_submission_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "message": "This is a test submission from the form_submission_example.py script."
            }

            # Submit the data to the form
            submission_result = submit_form_data(token, FORM_SUBMISSION_URL, form_submission_data)

            if submission_result and submission_result.get('status') == 'success':
                print("\n✅ Form submission was successful!")
            else:
                print("\n❌ Form submission failed.")
        else:
            print("\n❌ Failed to get form details. Please check the form URL.")
    else:
        print("\n❌ Authentication failed. Please check your credentials.")
