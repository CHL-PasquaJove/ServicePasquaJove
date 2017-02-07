# Pending to implement security
import hashlib


def digest(user, password):
    return hashlib.sha224(password).hexdigest()
