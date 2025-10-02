# importar bibliotecas
from os import path,rename
from pytubefix import YouTube,Playlist
from tqdm import tqdm

# função de baixar um audio

def download_audio(url:str,path_musics:str):
    """
    Downloads one audio from a youtube video
    Args:
        url (str): The URL from the youtube video
        path_musics (str): The path where the musics are going to be saved on
    Returns:
        Downloaded archives
    """
    try:
        yt = YouTube(url)
        audio = yt.streams.get_audio_only()
        downloaded_file = audio.download(output_path=path_musics)
        base = path.splitext(downloaded_file)[0]
        new_file = base + ".mp3"
        rename(downloaded_file,new_file)
    except Exception as e:
        print("Erro: ",e)

# função de baixar varios audios presentes na playlist

def download_playlist(url:str,path_musics:str):
    """
    Downloads an entire playlist audio from youtube
    Args:
        url (str): The URL from the youtube video
        path_musics (str): The path where the musics are going to be saved on
    Returns:
        Downloaded archives
    """
    videos = Playlist(url)
    for video in tqdm(videos.video_urls,desc="Baixando..."):
        download_audio(video,path_musics)
