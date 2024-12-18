from time import sleep
from tests.utils import create_random_user_input, create_random_auth_user, get_session, get_client
from models.user import UserLogin
from crud.user import create_user, authenticate
from core.security import create_access_token

def test_token_database():
    db = get_session()

    # Random user
    user_input = create_random_user_input()
    user = create_user(db, user_input)

    # Check no token in database
    assert user.token is None

    # Get JWT
    user = authenticate(db, UserLogin(email=user_input.email, password=user_input.password))
    token = user.token 

    # Check token in database
    assert user.token == token

    # Delete data created
    db.delete(user)
    db.commit()

def test_token_no_format():
    client = get_client()

    # Authorization header with no user token
    h = {"Authorization": "Bearer no_format"}

    # Check no user error
    r = client.get("login/check_token", headers=h)
    assert r.status_code == 403
    assert r.json() == {"detail": "Could not validate credentials"}
    
def test_token_no_user():
    client = get_client()

    # Authorization header with no user token
    h = {"Authorization": f"Bearer {create_access_token(0)}"}

    # Check no user error
    r = client.get("login/check_token", headers=h)
    assert r.status_code == 401
    assert r.json() == {"detail": "User not found"}

def test_token_no_database():
    db = get_session()
    client = get_client()
    
    # Random user
    user = create_random_auth_user(db)

    # Sleep for getting another token based on expiration time
    sleep(1)

    # Authorization header with valid JWT (not in database)
    h = {"Authorization": f"Bearer {create_access_token(user.id)}"}

    # Check invalid token error
    r = client.get("login/check_token", headers=h)
    assert r.status_code == 401
    assert r.json() == {"detail": "Invalid token"}

    # Delete data created
    db.delete(user)
    db.commit()

def test_token_successful():
    db = get_session()
    client = get_client()

    # Random user
    user = create_random_auth_user(db)

    # Authorization header with correct JWT
    h = {"Authorization": f"Bearer {user.token}"}

    # Check response is successful
    r = client.get("login/check_token", headers=h)
    assert r.status_code == 200

    # Delete data created
    db.delete(user)
    db.commit()
