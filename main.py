from os import mkdir,path,getcwd
import yt_download_music
from tqdm import tqdm
import acquire_links

keep = "s"

while keep == "s":
    folder_name = input("Coloque o nome da pasta que deseja salvar as músicas: ")
    music_folder = getcwd() #current directory
    if not path.exists(path.join(music_folder,folder_name)):
        mkdir(path.join(music_folder,folder_name))
    music_folder = path.join(music_folder,folder_name)
    link = input("Coloque o link do YT ou Spotify:\nPode ser de musica ou playlist\nR: ")
    if 'youtube' in link:
        if 'playlist' in link:
            yt_download_music.download_playlist(link,music_folder)
        else:
            yt_download_music.download_audio(link,music_folder)
    elif 'spotify' in link:
        if 'playlist' in link:
            playlist_id = link.rsplit('/',4)[4]
            if '?' in playlist_id:
                playlist_id = playlist_id.rsplit('?',2)[0]
            links = acquire_links.get_links(playlist_id)
            for link in tqdm(links,desc="Baixando..."):
                yt_download_music.download_audio(link,music_folder)
        else:
            track_id = link.rsplit('/',5)[5]
            if '?' in track_id:
                track_id = track_id.rsplit('?',2)[0]
            link = acquire_links.get_link(track_id)
            yt_download_music.download_audio(link,music_folder)
    else:
        print("link inválido")
    keep = input("Continuar ? (s/n)\nR: ").lower() 
