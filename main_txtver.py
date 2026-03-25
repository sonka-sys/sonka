#библиотеки
import queue, sys, string, wave, subprocess, requests
import sounddevice as sd
#from vosk import Model, KaldiRecognizer
from ollama import chat
from pygame import mixer
from piper import PiperVoice
from pytube import Search
from emoji import replace_emoji

#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#инициализация переменных
#q = queue.Queue()
mixer.init()
#model = Model(lang="ru")
table = str.maketrans('', '', string.punctuation)
voice = PiperVoice.load("./ru_RU-irina-medium.onnx")

#-----------функции------------
# локальная ии модель
# локальная ии модель
def ai(question,_):
    stream = chat(
        model='gemma3:1b',
        messages=[{'role': 'user', 'content': (question+" Ответь кратко")}],
        stream=True,
    )
    
    counter=0
    lentext=0
    fulltext=""
    mixer.music.load("00.wav")
    mixer.music.play()
    for chunk in stream:
        fulltext+=chunk['message']['content'].replace('\n','').replace('*','')
        newtext = fulltext[lentext:]
        for sym in newtext:
            if sym == '.':
                with wave.open(f"{counter}.wav", "wb") as wav_file:
                    voice.synthesize_wav(newtext, wav_file)
                if counter >1:
                    mixer.music.queue(f"{counter-1}.wav")
                elif counter==1:
                    mixer.music.load("0.wav")
                    mixer.music.play()
                counter+=1
                lentext+=len(newtext)
    while mixer.music.get_busy(): None

#  преобразование одного предложения в текст

# стриминг с ютуб

def yt(_, query):
    try:
        links = []
        titles = []
        search = Search(query)
    except: print("error")
    try:
        for video in search.results:
            links.append(video.watch_url)
            titles.append(video.title)
        titlesstr=""
        mixer.music.load("ytintro.wav")
        mixer.music.play()
        while mixer.music.get_busy(): None
        for x in range(3):
            print(titles[x])
            titlesstr+=titles[x]+". "
        with wave.open(f"0.wav", "wb") as wav_file:
            voice.synthesize_wav(replace_emoji(titlesstr, replace=""), wav_file)
        mixer.music.load(f"0.wav")
        mixer.music.play()
        while mixer.music.get_busy(): None

        mixer.music.load("ytoutro.wav")
        mixer.music.play()

        num_of_vid = int(input("какое аудио включить (номер): "))
        subprocess.Popen(['mpv', links[num_of_vid-1], '--no-video'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True)
    except: None
# новости
def stopmpv(*args):
    try:
        p = subprocess.run(["pgrep", "-x", "mpv"], capture_output=True, text=True).stdout.replace("\n","")
        if p!="":subprocess.run(["kill", p])
    except: print("err")

def news():
	None

"""
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
                                u"\U00000000-\U00000009"
                                u"\U0000000B-\U0000001F"
                                u"\U00000080-\U00000400"
                                u"\U00000402-\U0000040F"
                                u"\U00000450-\U00000450"
                                u"\U00000452-\U0010FFFF"
                                "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
"""
# погода

def weather(*args):
    city = 'Кудрово'
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    # получаем данные о температуре и о том, как она ощущается
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    if temperature<0 or temperature_feels<0: 
        weathertext = 'Сейчас в городе '+ city +" минус "+ str(temperature)[1:]+ ' градуса. Ощущается как минус '+ str(temperature_feels)[1:]+ ' градуса'
    else:
        weathertext = 'Сейчас в городе '+ city+" "+ str(temperature)+ ' градуса. Ощущается как '+ str(temperature_feels)+ ' градуса'
    
    with wave.open("0.wav", "wb") as wav_file:
        voice.synthesize_wav(weathertext,wav_file)
    mixer.music.load("0.wav")
    mixer.music.play()
    while mixer.music.get_busy(): None

# будильник
def voicefy(text):
    with wave.open("0.wav", "wb") as wav_file:
        voice.synthesize_wav(text,wav_file)
    mixer.music.load("0.wav")
    mixer.music.play()
    while mixer.music.get_busy(): None

def alarmsound():
    mixer.music.load("alarm.wav")
    mixer.music.play()
    while mixer.music.get_busy(): None
    print("alarm")

def alarm():
    print("asdf")

def timerf(_,text):
    print("asd")
    wordlist= text.split()
    sect=0
    mint=0
    hourt=0
    k=0
    for item in wordlist:
        if "секунд" in item: sect=int(wordlist[k-1])
        if "минут" in item: sect=int(wordlist[k-1])
        if "час" in item: sect=int(wordlist[k-1])
        k+=1
    sect+=mint*60+hourt*3600
    print(sect)
    t=Timer(sect, alarmsound)
    t.start()

# список задач
def whattime(*args):
    voicefy(time.strftime("%H часов %M минут"))

def tasklist():
    """
    функции тасклиста: создать таск лист пометить выполненным, удалить тасклист
    """
    None

# notes

def notes(text,_):
    """
    для начала орпеделить функцию
	функции заметок: создать читать просмотреть список удалить
    """
    None

# wiki поиск

def wiki(_,searchterm):
    search = wikipedia.search(searchterm)
    print(search)
    text = wikipedia.summary(search[0], sentences = 3)
    """
    fs=text.find('(')
    ss=text.find(')')
    if fs!=-1 and ss!=-1:

        text.replace(text[fs:ss+1],"")
    """
    print(text)
    voicefy(text)
# взаимодействие с vosk

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# функция анализа - !!переработать
def analysis(words):
    wordsstr = words
    words = words.split()
    essence = ""
    tokens = []
    maxindex=0
    for word in words:
    	for key, values in dict_of_func.items():
    		for value in values:
    			if value == word:
    				tokens.append(key)
    				if words.index(word)>maxindex:
    					maxindex = words.index(word)

    for x in range(maxindex+1,len(words)):
    	essence = essence + words[x] + " "

    if len(tokens) == 0:
    	None
    elif len(tokens) == 1:
    	for func in func_init.keys():
    		if tokens[0] == func: 
    			func_init[func](userquery, essence)

def fuzzanalysis(words):
    None

def tv(_,query):
    query = query.replace(" ", "")
    for channel, link in channels.items():
        if query==channel:
            print("нашел")
            subprocess.Popen(['mpv', link],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True)

def radio(_,query):
    print(query)
    query = query.replace(" ", "")
    for radio, link in radios.items():
        print(radio)
        if query==radio:
            print("нашел")
            subprocess.Popen(['mpv', link],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True)

#-------------- словари -----------------
controls = {
	'start': ("запусти","выполни","открой","включи"),
    'off': ("выключи", "закрой", "останови", "стоп"),
    'pause': ("поставь на паузу"),
    'resume': ("продолжай", "продолжить", "дальше"),
}
dict_of_func = {
    'off': ("выключи", "закрой", "останови", "стоп"),

    'ai_query': ("подумай", "объясни", "расскажи"),
    'yt_query': ("ютуб", "ютьюб"),
    'news_query': ("новости", "события"),
    'weather_query': ("погода", "температура"),
    'alarm_query': ("будильник","б"),
    'timer_query': ("таймер","n"),
    'tasklist_query': ("задачу", "задач", "задачи"),
    'notes_query': ("записки", "запись"),
    'wiki_query': ("вики", "википедии"),
    'whattime_query': ("время","времени"),
	'tv_query' : ("канал", "телеканал"),
    'radio_query' : ("радио", "радиостанцию"),
}
func_init = {
	'ai_query': ai,
    'yt_query': yt,
    'news_query': news,
    'weather_query': weather,
    'alarm_query': alarm,
    'timer_query': timerf,
    'tasklist_query': tasklist,
    'notes_query': notes,
    'wiki_query': wiki,
    'off': stopmpv,
    'whattime_query': whattime,
	'tv_query': tv,
    'radio_query': radio,
}
channels = {
    "первый канал": 'https://edge1.1internet.tv/dash-live2/streams/1tv-dvr/1tvdash.mpd',
    "россия": 'https://cdn.ntv.ru/unknown_russia/tracks-v1a1/playlist.m3u8',
    "нтв": 'https://cdn.ntv.ru/ntv0/playlist.m3u8',
    "время": 'https://cdn4.skygo.mn/live/disk1/Vremya/HLSv3-FTA/Vremya.m3u8',
}
radios = {
    "максимум": 'http://maximum.hostingradio.ru/maximum96.aacp',
    "рок фм": 'http://nashe1.hostingradio.ru/rock-64.mp3',
    "авторадио": 'http://ic7.101.ru:8000/v3_1',
    "вести фм": 'http://icecast.vgtrk.cdnvideo.ru/vestifm',
}
#------------- рабочий цикл --------------

while True:
    userquery = str(input("запрос: ")).translate(table).lower()
    
    if userquery[:4] == "соня":
    	userquery = userquery[4:]
    	analysis(userquery)
    if userquery == "выход": break


