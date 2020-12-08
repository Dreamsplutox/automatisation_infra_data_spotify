#imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import datetime

#credentials
clientId= "66a487c61a4f49e58fc0cdbf5c301e74"
clientSecret="5f96618372f44485a23f4e832c7045a9"
client_credentials_manager = SpotifyClientCredentials(clientId, clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ### Get all artist ids
df = pd.read_csv('spotify_famous_artists.csv')
artist_ids = df["artist_id"].tolist()
artist_names = df["artist"].tolist()

# ### Get tracks of an artist + check if one of the release dates == today (purpose pack ?)
# #### If it's the case, add data to a dict and save to csv in the hand

def track_release_today_or_not(artist_id):
    release_today = False
    
    tracks = sp.artist_top_tracks(artist_id)
    
    for track in tracks['tracks']:
        # if song released today, need to purpose a pack to the artist
        if track['album']['release_date'] == str(datetime.date.today()):
            release_today = True
            return release_today
    
    return release_today

#init dict pack_artists ==> will contain a column to know if we should purpose the pack
pack_artists = []

for i in range(0, len(artist_ids)):
    purpose_pack = track_release_today_or_not(artist_ids[i])
    pack_artists.append([artist_ids[i], artist_names[i], purpose_pack])
    


# ### Create the dataset
df = pd.DataFrame(pack_artists, columns = ['artist_id', "artist_name", 'purpose_premium_pack'])
df.to_csv("purpose_premium_pack_"+str(datetime.date.today())+".csv", sep = ',', encoding="utf-8-sig", index=False)