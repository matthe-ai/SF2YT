from youtubesearchpython import VideosSearch
from spotify_songs import get_name_track,get_names_playlist

#Using httpx<0.26

def get_link(track_id:str)->str:
    """
    Receives the track_id of a track and returns its link from YouTube
    Args:
        track_id (str): The id from the track
    Returns:
        Link (str): The link from YouTube
    """
    data = get_name_track(track_id)
    if not data:
        return "Dados inexistentes"
    text:str = data[0]+" "+data[1]
    try:
        search = VideosSearch(query=text,limit=3)
        result_all = search.result()
        for track in result_all['result']:
            title = track['title']
            link = track['link']
            if not ("remix" in text.lower() and "remix" in title.lower()):
                if not ("clipe" in text.lower() and "clipe" in title.lower()):
                    return link
    except Exception as e:
        print(f"Não foi possivel conseguir o link/titulo \nErro: {e}")
    return "Resultados inconclusivos/não foi possivel baixar a mesma música"

def get_links(playlist_id:str)->list:
    """
    Receives the playlist_id of a playlist and returns the links from YouTube
    Args:
        playlist_id (str): The id from the playlist
    Returns:
        Links (list): The links from YouTube
    """
    all_data = get_names_playlist(playlist_id)
    all_links = []
    for item in all_data:
        text = item[0]+" "+item[1]
        try:
            search = VideosSearch(query=text,limit=3)
            result_all = search.result()
            for track in result_all['result']:
                title = track['title']
                link = track['link']
                if not ("remix" in text.lower() and "remix" in title.lower()):
                    if not ("clipe" in text.lower() and "clipe" in title.lower()):
                        all_links.append(link)
                        print(f"title: {title} \n link: {link}")
                        break
        except Exception as e:
            print(f"Não foi possivel conseguir o link/titulo \nErro: {e}")
    return all_links
