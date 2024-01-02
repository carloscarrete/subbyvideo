import os
import subprocess
import zipfile
import yt_dlp as yt
import re
import random
import string


from ws_sub import get_subtitles, translate_sub

videos_example = [
    'https://www.youtube.com/watch?v=Qg3tTCEnfxw',
    'https://www.youtube.com/watch?v=xFyEo2_MPvA',
    'https://www.youtube.com/watch?v=UtfNsGJkKgU'
]

downloaded_videos = []

def generateRandomId():
    characters = string.ascii_letters + string.digits  
    random_id = ''.join(random.choice(characters) for _ in range(10))
    return random_id

def download_audio(url, output_path, type_sub=''):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'video')
            ydl.download([url])

        mp3_file = os.path.join(output_path, f"{video_title}.mp3")

        print(f"Audio downloaded as {mp3_file}")
        
        if type_sub == 'original_sub':
            get_subtitles(mp3_file)
        elif type_sub == 'english_sub':
            translate_sub(mp3_file)

        return mp3_file.replace('.mp3', '.srt')

    except Exception as e:
        print("Error:", e)

def download_video(url, output_path='.'):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        }

        with yt.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'video')
            video_id = info_dict.get('id', 'unknown_id')
            ydl.download([url])

        #mp4_file = os.path.join(output_path, f"{video_title}")
        mp4_file = os.path.join(output_path, f"{video_id}")

        print(f"Video downloaded as {mp4_file}")
        print('Id:', video_id)
        print('mp4 file:', mp4_file)
        return mp4_file

    except Exception as e:
        print("Error:", e)

def download_videos(videos):
    downloaded_videos = []
    for url in videos:
        video_file = download_video(url) + '.mp4'
        downloaded_videos.append(video_file)
    return compress_videos(downloaded_videos)


def getArraryVideos(videos):
    text = videos 
    urls = re.findall(r'https://\S+', text)
    return urls

def compress_videos(video_list, output_path='.', archive_format='.zip'):
    random_id = generateRandomId()
    try:
        archive_name = os.path.join(output_path, random_id + '_video' + archive_format)
        with zipfile.ZipFile(archive_name, 'w') as zip_file:
            for video_file in video_list:
                zip_file.write(video_file)
                os.remove(video_file)  # Delete video added in zip file
        print('Compressed')
        return random_id + '.zip'
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    output_path = '.'  # Carpeta de salida, puedes cambiarla si lo deseas.

    # Menú
    download_type = input("Do you want to download audio (a) or video (v)? ")

    if download_type == "a":
        download_audio(url, output_path)
    elif download_type == "v":
        download_video(url, output_path)
    elif download_type == 'm':
        download_videos()
    else:
        print("Invalid input. Please enter a or v.")
