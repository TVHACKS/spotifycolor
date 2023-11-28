import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorthief import ColorThief
import requests
from io import BytesIO
import time

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'e68159e422ed41b0878f6d94010b5303'
SPOTIPY_CLIENT_SECRET = '69d40481513c45188be10f885ca44969'
SPOTIPY_REDIRECT_URI = 'http://localhost/:8080'

# Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-currently-playing user-read-playback-state'))

# Common color mapping
COMMON_COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203),
}

def get_dominant_color_similar_to_common(image_url, color_count=10):
    try:
        # Download the image
        response = requests.get(image_url)
        image = BytesIO(response.content)

        # Use ColorThief to get the color palette
        color_thief = ColorThief(image)
        palette = color_thief.get_palette(color_count=color_count, quality=1)

        # Find the dominant color that is most similar to a common color
        dominant_color = min(palette, key=lambda color: min(color_difference(color, common_color) for common_color in COMMON_COLORS.values()))

        # Convert the dominant color to hex
        dominant_color_hex = "#{:02x}{:02x}{:02x}".format(*dominant_color)

        return dominant_color_hex

    except Exception as e:
        print(f"Error: {e}")

    return None

def color_difference(color1, color2):
    # Calculate the color difference between two colors
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

def get_current_track_info():
    try:
        current_track = sp.current_playback()
        if current_track and 'item' in current_track and 'album' in current_track['item']:
            return current_track['item']['album']['images'][0]['url']
    except Exception as e:
        print(f"Error: {e}")
    return None

def main_loop():
    while True:
        album_cover_url = get_current_track_info()

        if album_cover_url:
            dominant_color = get_dominant_color_similar_to_common(album_cover_url)

            if dominant_color:
                print(f"The dominant color similar to a common color of the album cover is: {dominant_color}")

        time.sleep(1)  # Adjust the delay (in seconds) as needed

if __name__ == "__main__":
    main_loop()