import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import fileinput
import re
from pprint import pprint
import pandas as pd
import time
# from jsonmerge import Merger

cid ="758b9e90346649409515e5705043464f"
secret = "4130541e7efd4a1c912ac4571909484b"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#track_id = track_name = popularity = artist_name = []

track_id = []
track_name = []
popularity = []
artist_name = []

month = 1

# premier échantillion de données récupéré qui va nous donner la structure JSON
# track_results = sp.search(q='year:2019', type='track', limit=50,offset=0)

#track_results_A ==> For testing

# var avec tous les items, ici on récup les x premiers items et à chaque itération
#on va merge, on aura ainsi un json complet à la fin
#all_items = track_results_A['tracks']['items']

#parcours des données et récupération à chaque fois des items
for i in range(0,2000, 50):
    print('=============== Generate data for month '+str(month)+' iterat num %s / 2000 ==============='%(i+1))
    track_results = sp.search(q='year:2019', type='track', limit=50,offset=i)
    #all_items.append(track_results['tracks']['items'])

    #sleep to avoid 2000 limit ?
    if i%1000 == 0:
        print("sleep time")
        print("len of track_resu ==> "+str(len(track_results['tracks']['items'])))
        time.sleep(0.0001)
    
    for i, t in enumerate(track_results['tracks']['items']):
        print("hello")
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
        print(len(popularity))
        print("track ids ", len(track_id))
        print("distinct track id ", len(set(track_id)))
    #break
        #print('{} - {} - {} - {}'.format(t['artists'][0]['name'], t['name'], t['id'], t['popularity']))

#Utiliser un dataframe pandas ?
track_dataframe = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'popularity' : popularity})
print(track_dataframe.shape)
print(track_dataframe.head())

print("ARTIST NAME")
for elem in artist_name:
    print("artist : ", elem)

#ecrire flux dans fichier
track_dataframe.to_json(r'D:\\cours\\cinquième_année\\automatisation infrastructure de données\\automatisation_infra_data_spotify\\output_data_from_pandas.json')

# with open('output_data.json', 'w') as f:
#     json.dump(track_results, f)
    # track_results_A for testing

print('\nLen of artist_name = {} \nLen of track_name = {} \nLen of popularity = {} \nLen of track_id = {} '.format(len(artist_name), len(track_name), len(popularity), len(track_id)))

#json_track_id = json.loads(track_id)
#print(json_track_id)

# for idx in range(len(track_id)):
#
#     print('{} - {} - {} - {}'.format(track_id[idx], track_name[idx], popularity[idx], artist_name[idx]))
