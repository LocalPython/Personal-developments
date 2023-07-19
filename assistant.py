#Импорты
import sys #Работа со скриптом
import os #Работа с операционкой
import time #Работа со временем
import pyttsx3 #Преобразование текста в речь
import speech_recognition as sr #Распознование голоса
from fuzzywuzzy import fuzz #Неточное сравнение
import datetime #Работа с датой
import keyboard #Работа с клавиаттурой
import webbrowser #Чтобы открывать ссылки

import requests #Доступ к сайтам
from bs4 import BeautifulSoup #Упрощение кода сайта

import getpass                                   #НОВОЕ НОВОЕ НОВОЕ Автозагрузка
USER_NAME = getpass.getuser()

def add_to_startup(file_path="D:\\Python\\assistant.exe"):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "assistant.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)

add_to_startup()        






#Присваиваение переменным их значений
ass = pyttsx3.init()  #Переменная для работы с Преобразованием текста
voices = ass.getProperty("voices") #Получаем список стандартных голосов Windows
ass.setProperty("voice", "ren") #Установка атрибута


file = 0 #Bool переменная
google = 0 #Bool переменная

ins = 0   #НОВОЕ НОВОЕ НОВОЕ Переменная, чтобы приостанавливать прослушку

r = sr.Recognizer() #Переменная для работы с Распознованием речи

#Настройка голоса
for voice in voices:                                                    
	if voice.name == "Microsoft Irina Desktop - Russian":     #Здесь мы проходимся по списку всех голосов и устанавливаем Ирину
		ass.setProperty("voice", voice.id)


#Мозги
opts = {      #Словарь
    "name": ('лена','ленка','ленок','ленчик','леня', 'лен', 'елена', 'елана',
     'леночка', 'ленушка', 'линушка', 'алена', 'алёна', 'яна', 'ена', 'алёнушка','ира'), #Имена на которые откликнется бот
    "what": {
        "time": ('текущее время','сейчас времени','который час', 'сколько времени'),   #Примеры вопроса времени
        "repeat": ('повтори','воспроизведи радио','включи радио'),   #Примеры запроса радио
        "funny": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты','скажи смешное' ,'скучно' ,'развесели меня'), #Примеры запроса анекдотов
        "stop": ('остановись','прекрати работу','выключись','хватит слушать','уйди','пока', 'закройся'),
        "open": ('запусти','открой'),
        "close": ('закрой','выключи'),
        "can":('что ты умеешь', 'как тобой пользоваться', 'что умеешь', 'какие у тебя есть функции', 'твои функции'),
        "kill":('выключи компьютер', 'выруби комп', 'заверши работу компьютера', 'выключай комп'),
        "restart":('перезагрузи компьютер', 'перезагрузка компа', 'перезагружай комп', 'рестарт компьютера'),
        "hi": ('привет','здарова','ку','салам','hello','здравствуй'),
        "how": ('как ты','че как','как дела','че нового','что нового','как у тебя дела','как твои дела','че как ты','что как ты вообще',),
        "thank": ('спасибо','от души','благодарю','спасибо тебе'),
        "kurs": ('какой курс доллара','курс доллара','сколько доллар','доллар к рублю','сколько рублей доллар','сколько доллар в рублях','курс рубля к доллару','сколько стоит доллар','сколько сейчас доллар',),
        "google": ('загугли','найди','найди в браузере','загугли в браузере'),
    }
}

files = {
    "яндекс браузер",                              #Список возможных файлов для открытия
    "google chrome",
    "диспетчер задач",
    "редактор реестра",
    "диспетчер устройств",
    "проводник",
    "блокнот",
    "paint",
    "командную строку",
    "вконтакте",
    "вк",
    "онтакте",
    "vk"
}
#Функция "Скажи"
def speak(what):   
    print( what )
    ass.say( what )     #Чтобы можно было вызвать функцию и указать что сказать роботу
    ass.runAndWait()
    ass.stop()


keyboard.wait('ins')      #НОВОЕ НОВОЕ НОВОЕ Не работает пока не нажали первый раз инсерт

if not ins == 1:
    def callback(recognizer, audio):   #Выполняется если что то произнесли в микрофон

        try:
            voice = recognizer.recognize_google(audio, language = "ru-RU").lower() #Сюда передаётся то, что сказали в микрофон
            print("[log] Распознано: " + voice) #Выводим то, что распознали
        
            if voice.startswith(opts["name"]):  #Если услышали Лена, тогда действуем

                cmd = voice #То, что сказали

     
                for x in opts['name']:
                    cmd = cmd.replace(x, "").strip()   #Удаляем имя бота и пробелы из конечной фразы и передаем ее дальше

                if "загугли" in cmd or "загугли в браузере" in cmd or "найди" in cmd or "загугли в браузере" in cmd:
                    cmd = cmd.replace("загугли", "").strip() 
                    cmd = cmd.replace("в браузере", "").strip() 
                    cmd = cmd.replace("найди", "").strip() 
                    google = cmd 
                    cmd = "загугли"
                else:
                    google = 0    

                for y in files:
                    file = y                  #Файл который нужно будет открыть
                    dlina = len(cmd)            #Кол-во символов строки
                    cmd = cmd.replace(y, "").strip()               #Если нашел слово из списка файлов, тогда запоминаем его, вырезаем и идем дальше                     
                    if dlina > len(cmd):
                        break
               
                # распознаем и выполняем команду
                cmd = recognize_cmd(cmd)   #Возвращает из какой ячейки брать действие и сколько процентов совпадение
                print(cmd)
                print(google)
                if cmd["percent"] > 75:  #Если сповпало больше чем на 75%, то выполняем команду
                	execute_cmd(cmd['what'], file, google) #Выполнение команды из нужной ячейки
                file = 0
                

     
        except sr.UnknownValueError:  #Исключение, если не расслышал голос
            print("[log] Голос не распознан!")
        except sr.RequestError as e:    #Исключение, если что то не так с подключением к сети
            print("[log] Неизвестная ошибка, проверьте интернет!")  




def recognize_cmd(cmd):     #Занимается неточным сравнением того что произнесли
    RC = {'what': '', 'percent': 0, 'text': cmd}
    for c,v in opts['what'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['what'] = c
                RC['percent'] = vrt
          
    return RC  #Оставляет самую похожую фразу и возвращает кол-во процентов и какая это ячейка 
    



def execute_cmd(cmd, file, google):   #Преобразование команды в действие
    if cmd == 'time':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'kurs':   #НОВОЕ НОВОЕ НОВОЕ
        # курс доллара
        DOLLAR_RUB = 'https://www.google.ru/search?q=доллар+к+рублю&newwindow=1&hl=ru&sxsrf=ALiCzsbaaNGlMxNrI2dtKHeBEmjjhrWKdQ%3A1654951246203&source=hp&ei=To2kYo7UCfLrrgTcxYeQBA&iflsig=AJiK0e8AAAAAYqSbXr5wpKDbh-2jErxElyEnXpAPfGbj&ved=0ahUKEwiOs5fptaX4AhXytYsKHdziAUIQ4dUDCAc&uact=5&oq=доллар+к+рублю&gs_lcp=Cgdnd3Mtd2l6EAMyDQgAEIAEELEDEEYQggIyCAgAEIAEELEDMgsIABCABBCxAxCDATIFCAAQgAQyCAgAEIAEELEDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIICAAQgAQQyQM6EQguEIAEELEDEIMBEMcBEKMCOggIABCxAxCDAToICC4QsQMQgwE6CwguEIAEEMcBEK8BOgUILhCABDoLCC4QsQMQgwEQ1AI6CwgAEIAEELEDEMkDOgsILhCABBCxAxCDAToICC4QgAQQsQM6CAguEIAEENQCUIgIWIgXYKsYaAFwAHgAgAFtiAHcCZIBBDEyLjKYAQCgAQGwAQA&sclient=gws-wiz'
        Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 Safari/537.36'}
        full_page = requests.get(DOLLAR_RUB, headers=Headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        ValueDollar = convert[0].text
        speak(ValueDollar + " " + "рублей к доллару")
    
    
    elif cmd == 'funny':
        # рассказать анекдот
        speak("Помню, как то хотел, поступить на филологический, но ихний декан почему то был против")

    elif cmd == 'hi':   #НОВОЕ НОВОЕ НОВОЕ
        # поздароваться
        speak("Привет привет")

    elif cmd == 'how':    #НОВОЕ НОВОЕ НОВОЕ
        # поздароваться
        speak("Всё в порядке, я же программа")

    elif cmd == 'thank':    #НОВОЕ НОВОЕ НОВОЕ
        # поздароваться
        speak("Пожалуйста, обращайтесь")

    elif cmd == 'google':    #НОВОЕ НОВОЕ НОВОЕ
        # загуглить
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' + google)
 

    elif cmd == 'stop':
        speak("Хорошо, я выключаюсь, пока")
        sys.exit()

    elif cmd == 'open':

        if file == 'яндекс браузер':    
            os.system(r'start C:\\Users\\%s\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe' % USER_NAME)

        elif file == 'диспетчер задач':    
            os.system('start taskmgr.exe')

        elif file == 'вк' or file == 'вконтакте' or file == 'онтакте' or file == 'vk':    
            webbrowser.open('https://vk.com', new=2)

        elif file == 'редактор реестра':    
            os.system('start regedit.exe')

        elif file == 'диспетчер устройств':    
            os.system('start devmgmt.msc')

        elif file == 'проводник':    
            os.system('start explorer.exe')

        elif file == 'блокнот':    
            os.system('start notepad.exe')

        elif file == 'paint':    
            os.system('start mspaint.exe')

        elif file == 'командную строку':    
            os.system('start сmd')

        else:
            speak("У меня не получается запустить эту программу")


    elif cmd == 'close':

        if file == 'яндекс браузер':    
            os.system('taskkill -im browser.exe /f')

        elif file == 'диспетчер задач':    
            os.system('taskkill /im taskmgr.exe')

        elif file == 'редактор реестра':    
            os.system('taskkill /im regedit.exe')

        elif file == 'диспетчер устройств':    
            os.system('taskkill /im mmc.exe')

        elif file == 'проводник':    
            os.system('taskkill /im explorer.exe /f')
            os.system('start explorer.exe')

        elif file == 'блокнот':    
            os.system('taskkill /im notepad.exe')

        elif file == 'paint':    
            os.system('taskkill /im mspaint.exe')

        elif file == 'командную строку':    
            os.system('taskkill /im сmd.exe')

        else:
            speak("У меня не получается выключить эту программу")

    elif cmd == 'can':
        print("--------------------------------------------------------------------")  
        print("1.Сколько сейчас времени/Который час??\n\n2.Открой/закрой :\n   1)блокнот\n   2)paint\n   3)командную строку\n   4)проводник\n   5)редактор реестра\n   6)диспетчер устройств\n   7)диспетчер задач\n   8)яндекс браузер\n   9)google chrome\n   10)калькулятор\n\n3.Пока/Выключись/Остановись\n\n4.Рассказать анекдот\n\n5.Выключение/Перезагрузка компьютера\n\n6.Открывать страницу Вконтакте\n\n7.Курс доллара к рублю\n\n8.Загуглить какой-либо запрос")
        print("--------------------------------------------------------------------")  
        ass.say("Вот мой список команд. я умею говорить время, открывать разные приложения, такие как калькулятор, диспетчер устройств, блокнот, пэинт, браузер, а так же могу их закрывать, ещё могу выключить или перезагрузить компьютер, нужно просто попросить об этом")     #Чтобы можно было вызвать функцию и указать что сказать роботу
        ass.say("Так же я могу открыть страницу Вконтакте, найти что нибудь в интернете или рассказать какой сейчас курс доллара к рублю") 
        ass.runAndWait()
        ass.stop()

    elif cmd == 'kill':
        speak("Хорошо, выключаю компьютер")
        os.system('shutdown -s -t 0')
        
    elif cmd == 'restart':
        speak("Хорошо, перезагружаю компьютер")
        os.system('shutdown -r -t 0')

    else:
        print('Команда не распознана, повторите!')



with sr.Microphone() as source:
    speak("Секунду, настраиваюсь...")
    speak("Слушаю")  
    r.adjust_for_ambient_noise(source, duration=0.5)   #Слушает фон чтобы не путать шум с речью     
                    


#stop_listening = r.listen_in_background(sr.Microphone(), callback)


while True:    #Бесконечный цикл для прослушки
    if  ins == 1 and keyboard.is_pressed('ins'):               #НОВОЕ НОВОЕ НОВОЕ Если переменная = 1 и удерживают инсерт, тогда начинает слушать и обнуляет
        speak("Cлушаю")
        ins = 0
    if not ins == 1:                                           #НОВОЕ НОВОЕ НОВОЕ Если переменная = 0, тогда работает, но если нажали енд, то заполняет переменную
        if keyboard.is_pressed('end'):               
            speak("Не слушаю")
            ins = 1
        print("Готова") 
        with sr.Microphone() as source:
            audio = r.listen(source)

        callback(r, audio)
        time.sleep(0.1)

    



######################################################################################################
#Прослушка микрофона

#with sr.Microphone() as source:
#	print("Говори...")
#	audio = r.listen(source)
######################################################################################################





######################################################################################################
#Поиск микрофонов#

#for index, name in enumerate(sr.Microphone.list_microphone_names()):
#    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
######################################################################################################

######################################################################################################
#Распознание и вывод#

#query = r.recognize_google(audio, language="ru-RU")
#print("Вы сказали: " + query.lower())
######################################################################################################

#ass.say(query.lower())
#ass.runAndWait()



#python -m nuitka --mingw64 --onefile --windows-icon-from-ico=kart.png assistant.py
#pyinstaller -w(Если заглушить консоль) -F -i "путь к иконке" assistant.py

