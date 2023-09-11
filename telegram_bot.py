import telebot
import os
from dotenv import load_dotenv
import urllib.parse

import shutil

from download_video import download_video, download_audio
from subtitle_video import burn_subtitules, convert_video_to_audio
from translate import translate_now
from ws_sub import get_subtitles, translate_sub

load_dotenv() 

TOKEN = os.getenv('API_TELEGRAM')
SERVER = os.getenv('SERVER_IP')
SERVER_CONNECT = os.getenv('IP_PARAMIKO')

bot = telebot.TeleBot(TOKEN)
tg_video = False
tg_video_option = ''
tg_video_yt = ''
tg_type_sub = ''

@bot.message_handler(content_types=['video'])
def handle_video(message):
    global tg_type_sub

    if tg_video:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        print(file_info)
        print(file_info.file_id +file_info.file_path.split(".")[1])
        with open(file_info.file_id +'.mp4', 'wb') as f:
            f.write(downloaded_file)
        video = open(file_info.file_id +'.mp4', 'rb')
        bot.reply_to(message, "Su video será enviado en breve.")
        convert_video_to_audio(file_info.file_id +'.mp4', file_info.file_id +'.mp3')
        if tg_type_sub == 'original_sub':
            get_subtitles(file_info.file_id +'.mp3')
        elif tg_type_sub == 'english_sub':
            translate_sub(file_info.file_id +'.mp3')
        elif tg_type_sub == 'spanish_sub':
            translate_sub(file_info.file_id +'.mp3')
            translate_now(file_info.file_id +'.srt')
        burn_subtitules(file_info.file_id +'.mp4', file_info.file_id +'.srt', file_info.file_id)

        #MOVER VIDEO SUB A LA SIGUIENTE DIRECCION
        shutil.move(file_info.file_id+'_sub.mp4', "/var/www/html/videos/"+file_info.file_id+'.mp4');

        #REMOVER ARCHIVOS VIEJOS, SRT, MP3 y MP4
        os.remove(file_info.file_id +'.mp3')
        os.remove(file_info.file_id +'.srt')
        os.remove(file_info.file_id +'.mp4')

        #bot.send_video(message.chat.id, video, timeout=60)
        bot.reply_to(message, SERVER + '/videos/'+urllib.parse.quote(file_info.file_id) +'.mp4' )
        print( SERVER +  '/videos/'+urllib.parse.quote(file_info.file_id) +'.mp4')
        tg_video = False
    

def send_url_download(message): 
    global tg_video_yt
    global tg_video_option
    try:
        if tg_video_option == '':
            tg_video_yt = message.text
            print(tg_video_yt)
            video_options_sub(message)

    except Exception as e:
        bot.reply_to(message, f"Ocurrió un error: {str(e)}") 


def download_yt_video(message):
    global tg_video_yt
    global tg_video_option
    global tg_video

    if tg_video_option=='sub' or tg_video_option=='original':
        try:

            url = tg_video_yt
            title_video = download_video(url, '.')
            print(title_video)
            bot.reply_to(message, "Su video será enviado en breve.")

            if tg_video_option == 'sub':
                print('...')
                if tg_type_sub == 'original_sub':
                    sub = download_audio(tg_video_yt, '.', 'original_sub')
                elif tg_type_sub == 'english_sub':
                    sub = download_audio(tg_video_yt, '.', 'english_sub')
                elif tg_type_sub == 'spanish_sub':
                    sub = download_audio(tg_video_yt, '.', 'english_sub')
                    #TODO CONVERT FROM DEEPL
                    translate_now(sub)
                print('de mi brilla', sub)
                burn_subtitules(title_video+'.mp4', sub, title_video)

                # TODO, mover video a esa carpeta
                shutil.move(title_video+'_sub.mp4', "/var/www/html/videos/"+title_video+'.mp4')

            elif tg_video_option == 'original':
                print('n')
                # TODO, mover video a esa carpeta
                shutil.move(title_video+'.mp4', "/var/www/html/videos/"+title_video+'.mp4')
            bot.reply_to(message, SERVER + '/videos/'+urllib.parse.quote(title_video) +'.mp4' )
            print( SERVER + '/videos/'+urllib.parse.quote(title_video) +'.mp4')
            tg_video = False
            tg_video_option = ''

        except Exception as e:
            bot.reply_to(message, f"Ocurrió un error: {str(e)}") 

#Send video to server
@bot.message_handler(content_types=['video'])
def handle_video(message):
    global tg_video
    if tg_video:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_info.file_id+file_info.file_path.split(".")[1], 'wb') as f:
            f.write(downloaded_file)
        tg_video = True
    else:
        bot.reply_to(message, "Comando no válido.")


@bot.message_handler(commands=['start'])
def handle_menu(message):
    menu_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    button1 = telebot.types.InlineKeyboardButton(text='Descargar YouTube', callback_data='option1')
    button2 = telebot.types.InlineKeyboardButton(text='Subtitular Video', callback_data='option2')
    menu_markup.add(button1, button2)
    bot.send_message(message.chat.id, '¿Qué desea hacer?', reply_markup=menu_markup)

def video_options_sub(message):
    download_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    original_button = telebot.types.InlineKeyboardButton(text='Original sin subtítulos', callback_data='original')
    download_with_subs_button = telebot.types.InlineKeyboardButton(text='Con subtítulos', callback_data='download_subs')
    download_markup.add(original_button, download_with_subs_button)
    bot.send_message(message.chat.id, '¿Cómo quieres el video?', reply_markup=download_markup)
        
def sub_options(message):
    subs_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    original_button = telebot.types.InlineKeyboardButton(text='Original', callback_data='original_sub')
    spanish_button = telebot.types.InlineKeyboardButton(text='Español', callback_data='spanish_sub')
    english_buton = telebot.types.InlineKeyboardButton(text='Inglés', callback_data='english_sub')
    subs_markup.add(original_button, spanish_button, english_buton)
    bot.send_message(message.chat.id, 'Selecciona una opción:', reply_markup=subs_markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global tg_video
    global tg_video_yt
    global tg_video_option
    global tg_type_sub
    if call.data == 'option1':
        bot.send_message(call.message.chat.id, 'Por favor, envia el link del video de YouTube')
        tg_video_yt = True
        bot.register_next_step_handler(call.message, send_url_download)
    elif call.data == 'option2':
        bot.send_message(call.message.chat.id, 'De acuerdo. Ahora, ¿En que idioma quiere sus subtítulos?')
        tg_video = True
        sub_options(call.message)
    elif call.data ==  'original':
        tg_video_option="original"
        print('original')
        bot.send_message(call.message.chat.id, 'Se descargará el video original. Por favor espere, esto puede tardar unos minutos')
        download_yt_video(call.message)
        #bot.register_next_step_handler(call.message, send_url_download)
    elif call.data ==  'download_subs':
        tg_video_option="sub"
        print('sub', tg_video_yt)
        print(tg_video_option)
        #bot.send_message(call.message.chat.id, 'Se descargará el video con subtítulos. Por favor espere, esto puede tardar unos minutos')
        #download_yt_video(call.message)
        sub_options(call.message)
    elif call.data ==  'original_sub':
        tg_type_sub="original_sub"
        bot.send_message(call.message.chat.id, 'Se descargará el video con subtítulos en su idioma original. Por favor espere, esto puede tardar unos minutos')
        download_yt_video(call.message)
        print('ORIGINAL')
    elif call.data ==  'spanish_sub':
        tg_type_sub="spanish_sub"
        bot.send_message(call.message.chat.id, 'Se descargará el video con subtítulos en Español. Por favor espere, esto puede tardar unos minutos')
        download_yt_video(call.message)
        print('SPANISH')
    elif call.data ==  'english_sub':
        tg_type_sub="english_sub"
        bot.send_message(call.message.chat.id, 'Se descargará el video con subtítulos en Inglés. Por favor espere, esto puede tardar unos minutos')
        download_yt_video(call.message)
        print('ENGLISH')
    

        #bot.register_next_step_handler(call.message, send_url_download)
        #send_url_download(call.message)

bot.polling()