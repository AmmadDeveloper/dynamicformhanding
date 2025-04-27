import hashlib
import base64
from django.core.exceptions import ObjectDoesNotExist

def hash_id(id):
    """
    Hash an ID to create a secure but reproducible identifier.

    Args:
        id: The ID to hash (typically an integer)

    Returns:
        A base64-encoded string representing the hashed ID
    """
    # Convert ID to string and encode to bytes
    id_bytes = str(id).encode('utf-8')

    # Create a hash of the ID
    hash_obj = hashlib.sha256(id_bytes)
    hash_digest = hash_obj.digest()

    # Encode the hash digest to base64 for URL-friendly format
    # and remove padding characters (=) which are not URL-friendly
    encoded = base64.urlsafe_b64encode(hash_digest).decode('utf-8').rstrip('=')

    # Return a portion of the hash to keep it reasonably sized
    return encoded[:16]  # Return first 16 characters

def find_form_by_hash(hashed_id):
    """
    Find a form by its hashed ID.

    Args:
        hashed_id: The hashed ID of the form

    Returns:
        The Form object if found, None otherwise
    """
    # Import here to avoid circular imports
    from .models import Form

    # Since we can't decode the hash, we need to check all forms
    # This is inefficient for large datasets but works for our purpose
    for form in Form.objects.all():
        if hash_id(form.id) == hashed_id:
            return form

    return None
