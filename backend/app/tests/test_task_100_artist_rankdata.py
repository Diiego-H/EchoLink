import pytest
from tests.utils import create_random_artist, get_session
from metrics.artists import get_all_artists_with_rank_data


@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test.
    Automatically rolls back transactions after each test.
    """
    db = get_session()  # Assuming `get_session()` sets up a test database session
    try:
        yield db
    finally:
        db.rollback()
        db.close()

# NOTE: There is no test for rank_data logic. Its functionality must be tested manually. QA task.

# Test: Check if all artists are fetched with their rank data
def test_get_all_artists_with_rank_data(db_session):
    # Create random artists
    artist1 = create_random_artist(db_session)
    artist2 = create_random_artist(db_session)

    # Get all artists with rank data
    artists_with_rank_data = get_all_artists_with_rank_data(db_session)

    # Check if the returned list contains the expected artists
    assert len(artists_with_rank_data) >= 2  # At least 2 artists should be present

    # Check if the rank_data is present for each artist
    for artist in artists_with_rank_data:
        assert "rank_data" in artist.model_dump()  # Ensure rank_data is a part of the artist output
        assert isinstance(artist.rank_data, dict)  # rank_data should be a dictionary

    # Check specific artists are in the list
    artist_usernames = [artist.username for artist in artists_with_rank_data]
    assert artist1.user.username in artist_usernames
    assert artist2.user.username in artist_usernames

    # Clean up (delete created artists)
    db_session.delete(artist1.user)
    db_session.delete(artist2.user)
    db_session.commit()

# Test: Ensure rank_data is correctly formatted (optional)
def test_rank_data_format(db_session):
    artist = create_random_artist(db_session)

    # Get artist with rank data
    artists_with_rank_data = get_all_artists_with_rank_data(db_session)
    artist_output = next((a for a in artists_with_rank_data if a.username == artist.user.username), None)

    assert artist_output is not None  # Ensure artist is found
    assert isinstance(artist_output.rank_data, dict)  # rank_data should be a dictionary
    assert "ranking" in artist_output.rank_data  # rank_data should have a 'ranking' field
    assert type(artist_output.rank_data["ranking"]) is int
    assert "tier" in artist_output.rank_data  # rank_data should have a 'tier' field
    assert type(artist_output.rank_data["tier"]) is int
    assert "percentage" in artist_output.rank_data  # rank_data should have a 'percentage' field
    assert type(artist_output.rank_data["percentage"]) is int

    # Clean up (delete created artist)
    db_session.delete(artist.user)
    db_session.commit()