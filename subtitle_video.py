import ffmpeg
import subprocess

def burn_subtitules(video, srt, title_original):
    print(' conversion started', video, srt, title_original)
    inputVideo = ffmpeg.input(video)
    audio = inputVideo.audio    
    ffmpeg.concat(inputVideo.filter("subtitles", srt), audio, v=1, a=1).output(title_original+'_sub.mp4').run()
    print('conversion completed ', video, srt)

def convert_video_to_audio(video_file_path, audio_file_path):
    print(' conversion started')
    command = "ffmpeg -i {} -vn -acodec libmp3lame -ar 48000 -b:a 64k {}".format(video_file_path, audio_file_path)
    subprocess.call(command, shell=True)
    print('conversion completed')

