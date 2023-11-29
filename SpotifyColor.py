import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorthief import ColorThief
import requests
from io import BytesIO
import time
import subprocess

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'your_redirect_uri'

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
    #'yellow': (255, 255, 0),
    #'orange': (255, 165, 0),
    #'purple': (128, 0, 128),
    #'pink': (255, 192, 203),
}

def update_signalrgb_effect(hex_value):
    # Execute SignalRGB command to apply the effect with the new hex value
    command = f'start signalrgb://effect/apply/Pump%20Up%20Beats?staticCol1=%23{hex_value}^&staticCol2=%23{hex_value}'
    subprocess.run(command, shell=True)

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
        dominant_color_hex = "{:02x}{:02x}{:02x}".format(*dominant_color)

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

def poll_for_track_change():
    current_track_id = None

    while True:
        try:
            current_track = sp.current_playback()
            if current_track and 'item' in current_track:
                track_id = current_track['item']['id']
                if track_id != current_track_id:
                    current_track_id = track_id
                    album_cover_url = get_current_track_info()

                    if album_cover_url:
                        dominant_color = get_dominant_color_similar_to_common(album_cover_url)

                        if dominant_color:
                            print(f"The dominant color similar to a common color of the album cover is: {dominant_color}")

                            # Update SignalRGB with the new hex value
                            update_signalrgb_effect(dominant_color)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)  # Adjust the delay (in seconds) as needed

if __name__ == "__main__":
    # Start polling for track changes and update SignalRGB
    poll_for_track_change()
