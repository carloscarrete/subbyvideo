from pytube.cli import on_progress
from pytube import YouTube
import os

from ws_sub import get_subtitles, translate_sub

def download_audio(url, output_path, type_sub=''):
  try:
    video = YouTube(url, on_progress_callback=on_progress)
    audio = video.streams.filter(only_audio=True).first()

    out_file = audio.download(output_path=output_path, filename=video.title)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    print(out_file)
    print('----')
    print(new_file)

    os.rename(out_file, new_file)

    print(f"Audio downloaded as {new_file}")
    if type_sub == 'original_sub':
      get_subtitles(new_file)
    elif type_sub == 'english_sub':
      translate_sub(new_file)
    return new_file.replace('.mp3','.srt')
  except Exception as e:
    print("Error:", e)

def download_video(url, output_path):
  try:
    video = YouTube(url, on_progress_callback=on_progress)
    video.streams.get_highest_resolution().download(output_path=output_path, filename=video.title+'.mp4')
    #video.streams.get_by_resolution('480p').download(output_path=output_path)
    print("Video downloaded")
    return video.title
  except Exception as e:
    print("Error:", e)


if __name__ == "__main__":

  url = input("Enter YouTube URL: ")
  #output_path = input("Enter output folder: ")
  output_path = '.'

  # Menu
  download_type = input("Do you want to download audio (a) or video (v)? ")

  if download_type == "a":
    download_audio(url, output_path)
  
  elif download_type == "v":
    download_video(url, output_path)
  
  else:
    print("Invalid input. Please enter a or v.")