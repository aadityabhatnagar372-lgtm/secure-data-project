import os

from cryptography.fernet import Fernet


ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    raise RuntimeError("ENCRYPTION_KEY environment variable is not set")


_fernet = Fernet(ENCRYPTION_KEY)


def encrypt_data(data: str) -> str:
    """Encrypt text and return a token string."""
    return _fernet.encrypt(data.encode("utf-8")).decode("utf-8")


def decrypt_data(token: str) -> str:
    """Decrypt a token and return the original text."""
    return _fernet.decrypt(token.encode("utf-8")).decode("utf-8")