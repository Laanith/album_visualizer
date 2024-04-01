import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st


spotify_scopes = " ".join([
    "ugc-image-upload",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
    "streaming",
    "playlist-modify-public",
    "playlist-modify-private",
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-library-modify",
    "user-library-read",
    "user-read-email",
    "user-read-private",
    "user-read-recently-played",
    "user-top-read",
    "user-read-playback-position",
    "user-read-playback-position",
    "user-read-playback-position",
    "user-follow-modify",
    "user-follow-read"
])

spot = spotipy.Spotify()


CLIENTID = '330df97ad32746e7bce5bcecc5f62a39'
CLIENTSECRET = '7bf2127ff8d047308ffc4b0ba631f31e'
REDIRECTURI = 'http://localhost:8888/callback'


auth = SpotifyOAuth(
    client_id=CLIENTID,
    client_secret=CLIENTSECRET,
    redirect_uri=REDIRECTURI,
    open_browser=True,
    scope=spotify_scopes,
)

sp = spotipy.Spotify(auth_manager=auth)


def LogUserData():
    my_details = sp.me()
    st.write(f"Hello ! { my_details['display_name'] }")
    st.image(my_details['images'][1]['url'])


def DisplaySearchBar():
    with st.form("Visualize the album"):
        url_input = st.text_input("Enter the album url here")
        button = st.form_submit_button("Fetch !")
        if button:
            album_id = url_input[url_input.find(
                'album/')+len('album/'): url_input.find('?')]
            album = sp.album(album_id)
            st.header(album['name'])
            st.image(album['images'][1]['url'])
            st.write(f"Album id : {album_id}")
            st.write(f"Album url : {album['external_urls']['spotify']}")
            st.subheader('Tracks :')
            album_tracks = sp.album_tracks(album_id)
            track_ids = [item['id'] for item in album_tracks['items']]
            tracks = sp.tracks(track_ids)['tracks']
            tracks = sorted(
                tracks, key=lambda x: x['popularity'], reverse=True)
            for track in tracks:
                st.subheader(track['name'])
                st.write(f"Popularity : {track['popularity']}")
                if track['preview_url'] is not None:
                    st.audio(track['preview_url'])

            #     track_details = sp.track(item['id'])
            #     st.write(track_details['name'])
            #     st.write(f"Popularity : {track_details['popularity']}")
            #     st.write(track_details['preview_url'])
            #     if track_details['preview_url'] is not None:
            #         st.audio(track_details['preview_url'])


if __name__ == '__main__':
    LogUserData()
    DisplaySearchBar()
