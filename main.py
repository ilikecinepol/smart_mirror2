import speech_recognition as sr
import pyttsx3
from settings import *
from weather import *
import datetime
from fuzzywuzzy import fuzz
import time
from random import randint

r = sr.Recognizer()
m = sr.Microphone(device_index=1)
speak_engine = pyttsx3.init()
name = ''
# настройки
opts = {
    "alias": ('Наташа', 'Наташенька', 'Ната', '',),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        'weather': ('Погода', "температура", "градусов", "одеться", "что одеть"),
        "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты'),
        'thanks': ('спасибо','ты лучший','благодарю','признателен','благодарен')

    }
}
with m as source:
    print('Скажи что-нибудь: ')
    audio = r.listen(source)


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def speach_recognition():
    with m as source:
        print('Скажи что-нибудь: ')
        audio = r.listen(source)

    query = r.recognize_google(audio, language='ru-RU')
    # print('Вы сказали ' + query.lower())
    callback(r, audio)
    return query.lower()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak(f"Сейчас {str(now.hour)} часов {str(now.minute)} минут")

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("D:\\Jarvis\\res\\radio_record.m3u")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

    elif cmd == 'weather':
        speak(weather_coords())

    elif cmd == 'thanks':
        welcome = ['Не стоит благодарностей',"Это моя работа","Всегда рада помочь", f"Пожалуйста, {name}"]
        speak(welcome[randint(0, len(welcome)-1)])

    else:
        print('Команда не распознана, повторите!')


def voice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def test_microfone():
    with m as source:
        r.adjust_for_ambient_noise(source)


def first_meeting():
    speak('Здравствуйте. Как вас зовут?')
    global name
    name = speach_recognition()


if __name__ == '__main__':
    test_microfone
    while True:
        try:
            text = speach_recognition()
        except:
            pass
        time.sleep(0.1)
