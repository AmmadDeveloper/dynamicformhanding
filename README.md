# Django Contact Forms with Token Authentication

This project implements a Django REST Framework API with token-based authentication for handling dynamic contact forms.

## Features

- Dynamic form handling API that accepts any form fields
- Token-based authentication for API security
- Simple GET and POST endpoints for form submission

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install django djangorestframework
   ```
3. Apply migrations:
   ```
   python manage.py migrate
   ```
4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## Authentication

This API uses token-based authentication. To use the API:

1. Obtain a token by sending a POST request to `/api-token-auth/` with your username and password:
   ```
   POST /api-token-auth/
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. The response will contain your token:
   ```
   {
     "token": "your_auth_token"
   }
   ```

3. Include this token in the Authorization header for all API requests:
   ```
   Authorization: Token your_auth_token
   ```

## API Endpoints

### GET /api/dynamic-form/

Returns a simple success message to verify the API is working.

**Authentication required**: Yes

**Response**:
```json
{
  "message": "GET endpoint is working",
  "status": "success"
}
```

### POST /api/dynamic-form/

Accepts any form data and returns it as confirmation.

**Authentication required**: Yes

**Request Body**: Any JSON object

**Response**:
```json
{
  "message": "Data received successfully",
  "received_data": {
    "field1": "value1",
    "field2": "value2",
    ...
  }
}
```

## Example Usage

See the `token_auth_example.py` script for a complete example of how to:
1. Obtain an authentication token
2. Make authenticated requests to the API
3. Handle the API responses

## Implementation Details

The token authentication is implemented using Django REST Framework's built-in TokenAuthentication class. The key components are:

1. Added `rest_framework` and `rest_framework.authtoken` to INSTALLED_APPS
2. Configured REST_FRAMEWORK settings with TokenAuthentication
3. Added authentication_classes and permission_classes to the API views
4. Created an endpoint for obtaining tokens
5. Applied migrations to create the necessary database tables