import pytest
from src.auth.jwt_handler import create_access_token, decode_access_token
from src.auth.auth_service import verify_password, get_password_hash
from datetime import timedelta

def test_jwt_encoding_decoding():
    data = {"username": "test_user", "role": "admin"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["username"] == "test_user"
    assert decoded["role"] == "admin"
    assert "exp" in decoded

def test_password_hashing():
    plain_password = "secure_password_123"
    hashed = get_password_hash(plain_password)
    
    assert hashed != plain_password
    assert verify_password(plain_password, hashed) is True
    assert verify_password("wrong_password", hashed) is False
