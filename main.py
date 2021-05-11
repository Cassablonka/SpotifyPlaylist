# Importing the required packages
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setting up the variables
client_id = "Your Client Id"
client_secret = "Your Screct Id"
redirect_uri = "http://example.com"
scope = "playlist-modify-private"

# Authenticating through Spotify
authorise = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope= scope,
        redirect_uri= redirect_uri,
        client_id= client_id,
        client_secret= client_secret,
        show_dialog= True,
        cache_path= "token.txt"
    )
)

user_id = authorise.current_user()['id']

# Taking user input for the date of which he wants to make playlist
date = input('Hello, which year do you want to travel to ? \nEnter the date in YYYY-MM-DD format : ')

# Setting up URL
URL = f"https://www.billboard.com/charts/hot-100/{date}"
# URL = "https://www.billboard.com/articles/list/6792625/top-50-love-songs-of-all-time/" ## For different list - Love Songs

# Getting the data from URL
response = requests.get(URL)
contents = response.text


# Intialising the scrapping
soup = BeautifulSoup(contents, 'html.parser')

songs = soup.find_all(name='h3', class_='chart-element__information__song')
# songs = soup.find_all(name='h3', class_='article__list__title') ## For Love Songs

# top_100 = [song.getText().split('"')[1] for song in songs ] ## For Love Songs
top_100 = [ song.getText() for song in songs ]

song_uris = []
year = date.split("-")[0]

# Creating the list of track id after scrapping of songs from website
for song in top_100[::-1]:
    result = authorise.search(q=f"track: {song} year: {year}", type="track")
    print(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesnt exist in Spotify. Skipped.")

# Setting the playlist
playlist = authorise.user_playlist_create(user=user_id, name=f'{date} Billboard 100', public=False)
# playlist = authorise.user_playlist_create(user=user_id, name=f'Top 50 Love Songs Ever', public=False)

# Creating the playlist
authorise.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
