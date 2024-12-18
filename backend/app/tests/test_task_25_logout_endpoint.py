from tests.utils import create_random_auth_user, get_session, get_client
from crud.user import deauthenticate

def test_deauthenticate():
    db = get_session()
    
    # Random user
    user = create_random_auth_user(db)

    # Check token is not None
    assert user.token is not None

    # Deauthenticate user
    deauthenticate(db, user)

    # Refresh user data
    db.refresh(user)

    # Check token is None
    assert user.token is None

    # Clean up
    db.delete(user)
    db.commit()
    
def test_logout():
    db = get_session()
    client = get_client()

    # Random user
    user = create_random_auth_user(db)

    # Authorization header with correct JWT
    h = {"Authorization": f"Bearer {user.token}"}

    # Check response is successful
    r = client.post("login/logout", headers=h)
    assert r.status_code == 200

    # Try to logout again
    r = client.post("login/logout", headers=h)
    assert r.status_code == 401
    assert r.json() == {"detail": "Invalid token"}

    # Delete data created
    db.delete(user)
    db.commit()
