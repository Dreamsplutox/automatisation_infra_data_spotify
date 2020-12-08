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


# ### If we are in january, set the year to current year -  1
current_year = datetime.date.today().year
current_month = datetime.date.today().month
if current_month == 1 :
    current_year = current_year - 1


# ### First get as many playlist as possible (let's say, 200)

dictPlayLists = []
for i in range(0,200):
    track_results = sp.search(q='year:'+str(current_year), type='playlist', limit=1,offset=i)
    tmpDict = None
    tmpDict = {
        'idPlayList':track_results['playlists']['items'][0]['id'],
        'playListName':track_results['playlists']['items'][0]['name']
    }
    dictPlayLists.append(tmpDict)


# ### Get only usefull playlists for the current year (current year + "top" in their name) 
def getUsefullPlaylists(dictPlayLists):
    ok_playlists = []
    
    for i in range(0, len(dictPlayLists)): 
        if "Top" in dictPlayLists[i]["playListName"] and str(current_year) in dictPlayLists[i]["playListName"]:
            ok_playlists.append(dictPlayLists[i])
        
    return ok_playlists

dictPlayLists = getUsefullPlaylists(dictPlayLists)

# ### Get all track ids (+ kill dupplicates)
def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

ids = []

for elem in dictPlayLists:
    ids += getTrackIDs(elem["playListName"], elem["idPlayList"])

#ids = getTrackIDs('Top Hits 2020', '53w0lVHBw0m4eEz54yN8FH')


# kill dupplicates
ids = list(dict.fromkeys(ids))

# ### Get usefull data (artists ids and names) in all the tracks + kill dupplicate artist
def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    # meta²
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    artist_id = meta['album']['artists'][0]['id']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features

    track = [name, album, artist, artist_id, release_date, length, popularity]
    return track

# loop over track ids 
tracks = []
all_artist_ids = []

for i in range(len(ids)):
    #time.sleep(.5)
    track = getTrackFeatures(ids[i])
    # check if id of the artist is already here, if that's case don't append the track
    if track[3] not in all_artist_ids:
        # don't add
        all_artist_ids.append(track[3])
        tracks.append(track)    

# ### CREATE / ( maybe MERGE later) CSV with what we have
# create dataset
df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist','artist_id', 'release_date', 'length', 'popularity'])
df.to_csv("spotify_famous_artists.csv", sep = ',', encoding="utf-8-sig", index=False)