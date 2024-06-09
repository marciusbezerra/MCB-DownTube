import os
import sys
import googleapiclient.discovery
import pytube
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


def download_video(url):
    try:
        youtube = pytube.YouTube(url)
        video = youtube.streams.get_highest_resolution()
        video.download(max_retries=10)
        print("Download concluído!")
    except Exception as e:
        print(f"Ocorreu um erro ao fazer o download: {e}")


def download_playlist(playlist_id, api_key):
    api_service_name = "youtube"
    api_version = "v3"
    api_key  # Substitua pelo seu próprio API Key do YouTube

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,  # Define o número máximo de vídeos a serem baixados
        playlistId=playlist_id
    )
    response = request.execute()

    for item in response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_title = item['snippet']['title']
        print(f'Downloading {video_title} ({video_id})...')
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        download_video(video_url)


def main():
    playlist_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not playlist_id:
        playlist_id = input("Digite o ID da playlist do YouTube: ")
    api_key = os.getenv("API_KEY")
    download_playlist(playlist_id, api_key)


if __name__ == "__main__":
    main()
