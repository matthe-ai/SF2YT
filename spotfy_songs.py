from os import getenv
from base64 import b64encode
from dotenv import load_dotenv
from requests import post,get
load_dotenv()

def get_token(client_id:str=getenv("client_id"),client_secret:str=getenv("client_secret"))->tuple:
    """
    Get the required token to make requests
    Args:
        client_id (str): It's already in the .env file, if not, provide yours
        client_secret (str): It's already in the .env file, if not, provide yours
    Returns:
        data (tuple): token,token_type
    """
    token,token_type = "",""
    base64_auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    auth_options = {
        'url':'https://accounts.spotify.com/api/token',
        'headers':{
            'Authorization':'Basic ' + base64_auth,
            'Content-type':'application/x-www-form-urlencoded'
        },
        'form':{
            'grant_type': 'client_credentials'
        }
    }
    response = post(auth_options['url'],headers=auth_options['headers'],data=auth_options['form'],timeout=15)
    if response.status_code == 200:
        r = response.json()
        token = r['access_token']
        token_type = r['token_type']
    else:
        return 'Não foi possível obter o token de acesso'
    data = (token,token_type)
    return data

def api_call_playlist(playlist_id:str,off_set:int=0)->dict:
    """
    Get the info from a full playlist
    Args:
        playlist_id (str):  The ID from the playlist
        off_set (int): Where the playlist starts (default:0)
    Returns:
        api_response (dict): all the data from the playlist
    """
    acess_token,token_type = get_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset={off_set}"
    response = get(url,headers={'Authorization':token_type+' '+acess_token},timeout=15)
    api_response = response.json()
    return api_response

def api_call_track(track_id:str)->dict:
    """
    Get the info from a single track
    Args:
        track_id (str): the ID from the music
    Returns:
        api_response (dict): all the data from the music
    """
    acess_token,token_type = get_token()
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = get(url,headers={'Authorization':token_type+' '+acess_token},timeout=15)
    api_response = response.json()
    return api_response

def get_name_track(track_id:str)->list:
    """
    With the data from the api_call, it gets the name of the music and the name of the artist
    Args:
        track_id (str): the ID from the music
    Returns:
        music_data (dict): [name_music,name_artist]
    """
    data = api_call_track(track_id)
    name_music = data['name']
    name_artist = data['artists'][0]['name']
    music_data = [name_music,name_artist]
    return music_data

def get_names_playlist(playlist_id:str)->list:
    """
    With the data from the api_call, it gets the names of the musics and the names of the artists
    Args:
        playlist_id (str): the ID from the playlist
    Returns:
        music_data (list): [[music_data_name,music_track_artist_name]]
    """
    musics_data = []
    data = api_call_playlist(playlist_id) # Todos os dados
    music_total = data['total']
    for i in range(0,music_total//50+1):
        if i == 0:
            data = api_call_playlist(playlist_id) # Todos os dados
        else:
            data = api_call_playlist(playlist_id,(50*i)+1) # Todos os dados
        data_itens:list[dict] = data['items'] # Recorte de apenas os itens
        for music in data_itens:
            try:
                music_track_data = music['track']
                music_track_artists = music_track_data['artists'][0]
                music_track_artist_name = music_track_artists['name']
                music_data_name = music_track_data['name']
                musics_data.append([music_data_name,music_track_artist_name])
            except Exception as e:
                print(f"Error {e} while downloading music: {music_data_name}")
    return musics_data
