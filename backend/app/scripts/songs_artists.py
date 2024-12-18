import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unicodedata
import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Spotify API credentials
client_id = '53d2b2391f6640cdbff8277ec6485fb7'
client_secret = '7e9d7db9565c4b598194cc75cc5535e0'

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def clean_name(name):
    # Normalize the string to decompose accents into base characters
    normalized = unicodedata.normalize('NFD', name)
    # Filter out combining characters (accents, tildes, etc.)
    without_accents = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    # Replace spaces with underscores and remove special characters
    cleaned = ''.join(c for c in without_accents if c.isalnum() or c == ' ').replace(' ', '_')
    return cleaned[:16]




def search_youtube_link(song_name, artist_name):
    """Search for the first YouTube link for the song using Bing."""
    
    # Construct the search query
    query = f"{song_name} {artist_name} site:youtube.com"
    encoded_query = urllib.parse.quote(query)

    # Bing search URL
    url = f"https://www.bing.com/search?q={encoded_query}"

    # Send a request to Bing
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load page")

    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first YouTube link in the search results
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "youtube.com/watch" in href:
            return href

    return None





# Get the top 10 artists globally
def get_top_artists():
    # Spotify does not have a direct "top artists" endpoint, so we use the search API
    # Here, we search for popular artists globally
    results = sp.search(q='genre:pop', type='artist', limit=10)  # Adjust query as needed
    top_artists = []
    
    for artist in results['artists']['items']:
        # Fetch detailed artist information using the artist's URI
        artist_details = sp.artist(artist['uri'])
        top_tracks = sp.artist_top_tracks(artist['uri'], country='US')  # Adjust country as needed
        songs = []

        for track in top_tracks['tracks'][:5]:  # Get the top 5 songs
            if len(track['name']) > 30:
                continue
            # Search for YouTube link
            youtube_link = search_youtube_link(track['name'], artist_details['name'])

            # Add song information
            song_info = {
                'name': track['name'],
                'release_date': track['album']['release_date'],  # Get release date
                'album': track['album']['name'],  # Get album name
                'genre': artist_details['genres'][0] if artist_details['genres'] else None,  # Get genre
                'sources': [ track['external_urls']['spotify'],  youtube_link  ] if youtube_link else [ track['external_urls']['spotify']]
            }

            print(song_info)
            songs.append(song_info)
        
        # Create a dictionary with the required information
        artist_dict = {
            'name': clean_name(artist_details['name']),
            'email': clean_name(artist_details['name']) + '@spotify.com',
            'password': 'password',
            'genres': artist_details['genres'][0] if artist_details['genres'] else None,
            'image_url': artist_details['images'][0]['url'] if artist_details['images'] else None,
            'songs': songs,
            'spotify_uri': artist_details['uri'],
            'description': f"{artist_details['name']} is a popular artist known for genres like {', '.join(artist_details['genres']) if artist_details['genres'] else 'various genres'}."
        }

        top_artists.append(artist_dict)
    
    return top_artists

# Fetch and print the top 10 artists
top_artists = get_top_artists()

def save_artists_to_json(top_artists, filename='backend/app/data/top_artists.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(top_artists, f, ensure_ascii=False, indent=4)

save_artists_to_json(top_artists)