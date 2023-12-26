import os
import subprocess
import yt_dlp as yt

from ws_sub import get_subtitles, translate_sub

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

def download_video(url, output_path):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        }

        with yt.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'video')
            ydl.download([url])

        mp4_file = os.path.join(output_path, f"{video_title}")

        print(f"Video downloaded as {mp4_file}")
        return mp4_file

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
    else:
        print("Invalid input. Please enter a or v.")
