Spotify Song to Hex Color (SignalRGB Support)
=============================================
How to use: (no SignalRGB)
-----------
`SpotifyColor-no_signal.py`  
If you want automatic hex color values based on the song you're listening to on your Spotify account, 
create an application at [Spotify](https://developer.spotify.com/dashboard). Set the following settings:  
* Redirect URIs - http://localhost/:8080  
* APIs used - Web Playback SDK, Web API  

After creating the app copy the Client ID, Client secret, and Redirect URI and replace 
`your_client_id`, `your_client_secret`, and `your_redirect_uri` in the script respectively. 
After running the script, you should be redirected to an authentication page. After accepting, copy 
the "http://localhost..." link and paste it in the command line where asked. You should not be asked 
to do this again (on the same device and account). Once you're done, play a song and see the hex codes 
show up!

For SignalRGB:
--------------
`SpotifyColor.py`  
**This script is currently only for the "Pump Up Beats" effect.**  
If you want to use this for another effect, refer to the SignalRGB command line [documentation](https://docs.signalrgb.com/application-url-s/using-command-line) 
and replace the `command` variable under `def update_signalrgb_effect(hex_value)` with your new command. 
Simply do the same steps for this script as for the script without SignalRGB.

The color detection is very simple and may not always be accurate, but it works really well.
