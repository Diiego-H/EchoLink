from tests.utils import random_lower_string
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import jwt
from core.security import create_access_token

def test_create_jwt():
    subject = random_lower_string()

    # Load environment variables from .env file
    load_dotenv()

    # Data from .env file
    key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    delta = timedelta(days=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")))

    # Check data from .env file is loaded
    assert key is not None
    assert algorithm is not None
    assert delta is not None

    # Wanted JWT token
    expire = datetime.utcnow() + delta
    to_encode = {"exp": expire, "sub": str(subject)}
    expected_token = jwt.encode(to_encode, key, algorithm=algorithm)
    
    # Check token
    token = create_access_token(subject)
    assert token is not None
    assert token == expected_token
