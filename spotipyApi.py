import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import fileinput
import re
from pprint import pprint
# from jsonmerge import Merger

cid ="758b9e90346649409515e5705043464f"
secret = "4130541e7efd4a1c912ac4571909484b"

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

track_id = track_name = popularity = artist_name = []

#premier échantillion de données récupéré qui va nous donner la structure JSON
track_results_A = sp.search(q='year:2018', type='track', limit=50,offset=0)

#var avec tous les items, ici on récup les x premiers items et à chaque itération
#on va merge, on aura aiinsi un json complet à la fin
all_items = track_results_A['tracks']['items']

#parcours des données et récupération à chaque fois des items
for i in range(50,10000, 50):
    print('=============== Generate data  iterat num %s / 10000 ==============='%(i+1))
    track_results = sp.search(q='year:2018', type='track', limit=50,offset=i)
    all_items.append(track_results['tracks']['items'])




    for j, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
        print(len(popularity))
    #break
        #print('{} - {} - {} - {}'.format(t['artists'][0]['name'], t['name'], t['id'], t['popularity']))

#ecrire flux dans fichier
# with open('output_data.json', 'w') as f:
#     json.dump(track_results_A, f)


print('\nLen of artist_name = {} \nLen of track_name = {} \nLen of popularity = {} \nLen of track_id = {} '.format(len(artist_name), len(track_name), len(popularity), len(track_id)))

#json_track_id = json.loads(track_id)
#print(json_track_id)

# for idx in range(len(track_id)):
#
#     print('{} - {} - {} - {}'.format(track_id[idx], track_name[idx], popularity[idx], artist_name[idx]))
