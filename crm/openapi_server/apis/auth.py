from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate

public_key_text = Path("micro_public_key.pem").read_text()
public_key = load_pem_x509_certificate(public_key_text.encode()).public_key()


def decode_and_verify_token(token: str) -> dict:
    """
    Validate and decode an access token. If the token is valid, return the payload.
    :param token: The access token to validate and decode.
    :return: The payload of the token.
    """
    return jwt.decode(token, public_key, algorithms=["RS256"],
                      audience=["http://localhost:3000/", "http://127.0.0.1:3000/"])