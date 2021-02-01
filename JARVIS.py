from decimal import Context
from threading import local
from time import strftime, struct_time
from typing import Text
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia # pip install wikipedia
import smtplib
import webbrowser as web
import psutil
import pyjokes
import os
import pyautogui
import random
import json
import requests
import wolframalpha
import time
from urllib.request import urlopen

from wikipedia import exceptions
web.register('chrome', None, web.BackgroundBrowser("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"))

engine = pyttsx3.init()
wolframalpha_app_id = 'write your wolframalpha_app_id '


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    time=datetime.datetime.now().strftime("%I:%M:%S") # for 12 hr clock
    speak('Current time is')
    speak(time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    date = datetime.datetime.now().day
    speak('The current date is')
    speak(date)
    speak(month)
    speak(year)

def wishme():
    speak('Welcome back Aadi!')
    time_()
    date_()

    #greetings

    hour = datetime.datetime.now().hour

    if hour>=6 and hour<12:
        speak('Good morning sir')
    elif hour>=12 and hour<18:
        speak('Good Afternoon sir')
    elif hour>=18 and hour <24:
        speak('Good evening Sir')
    else:
        speak('Good Night sir')

    speak('Jarvis at your service. Please tell me how can i help you ?')


def takeCommand():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio,language='en-US')
        print(query)

    except Exception as e:
        print(e)
        print('Say that again please....')
        speak('Say that again please....')
        return 'None'
    return query





def sendEmail(to,content):
    server =smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    #for this function , you must enable low security in your gmail which you are going to use as sender

    server.login('username@gmail.com', 'password')
    server.sendmail('username@gmail.com', to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save('E:\user\MAK Academy\Full JARVIS\Screenshots JARVIS/screenshot.png')

def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+ usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())


if __name__ == "__main__":

    wishme()

    while True:
        query = takeCommand().lower()

        # All commands will be stored in lower case in query

        if 'time' in query: # tell us time when asked
            time_()

        elif 'date' in query: # tell us date when asked
            date_()

        elif 'wikipedia' in query:
            speak('Searching......')
            query=query.replace('wikipedia', '')
            result=wikipedia.summary(query,sentences=3)
            speak('According to wikipedia')
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak('What should i say?')

                content=takeCommand()
                # provide receiver email address

                speak("Who is the Reciever?")
                receiver=input("Enter Reciever's email :")
                reciever='reciever_is_me@gmail.com'
                to = reciever
                sendEmail(to, content)
                speak('Email has been sent.')

            except Exception as e:
                print(e)
                speak('Unable to send Email.')

        elif 'search in chrome' in query:
            speak('What would you like to search?')
            search = takeCommand().lower()
            web.get('chrome').open_new_tab(search + '.com')

        elif 'search youtube' in query:
            speak('What should I search?')
            search_Term = takeCommand().lower()
            speak('Here we go to YouTube!')
            web.open('https://www.youtube.com/results?search_query='+search_Term)

        elif 'search google' in query:
            speak('What should i search')
            search_Term = takeCommand().lower()
            speak('searching...')
            web.open('https://www.google.com/search?q='+search_Term)


        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'go offline' in query:
            speak('Going offline Sir!')
            quit()

        elif 'word' in query:
            speak('Opening MS Word......')
            ms_word = r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'
            os.startfile(ms_word)

        elif 'write a note' in query:
            speak('What should i write, Sir?')
            notes = takeCommand()
            file = open('notes.txt','w')
            speak("Sir should i include data and time?")
            ans = takeCommand()
            if 'yes' in ans or 'sure' in ans:
                strftime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(':-')
                file.write(notes)
                speak('Done Talking Notes, Sir!')
            else:
                file.write(notes)

        elif 'show note' in query:
            speak('Showing notes')
            file = open('notes.txt', 'r')
            print(file.read())
            speak(file.read())

        elif 'screenshot' in query:
            screenshot()
            speak('Screenshot taken')

        elif 'play music' in query:
            songs_dir = 'E:\songs'
            music = os.listdir(songs_dir)
            speak('What should i play?')
            speak('Select a number...')
            ans = takeCommand().lower()
            if 'number' in ans:
                no = int(ans.replace('number',''))
            elif 'random' or 'you choose' in ans:
                no = random.randint(1,100)

                os.startfile(os.path.join(songs_dir,music[no]))

            elif 'remember that' in query:
                speak("What should I remember ?")
                memory = takeCommand()
                speak("You asked me to remember that"+memory)
                remember = open('memory.txt','w')
                remember.write(memory)
                remember.close()

            elif 'do you remember anything' in query:
                remember =open('memory.txt', 'r')
                speak("You asked me to remeber that"+remember.read())

            elif 'where is' in query:
                query = query.replace("Where is","")
                location = query
                speak("User asked to locate"+location)
                web.open_new_tab("https://www.google.com/maps/place/"+location)


        elif 'news' in query:
            try:
                jsonObj = urlopen("Your API Key")
                data = json.load(jsonObj)
                i = 1

                speak('here are some top news from the times of india')
                print('''========================= TOP HEADLINES====================='''+ '\n')

                for item in data['articles']:

                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1

            except Exception as e:
                print(str(e))

        elif 'calculate' in query:
            Client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split() [indx + 1:]
            res = Client.query(''.join(query))
            answer = next(res.results).Text
            print('The answer is : '+answer)

            try:
                print(next(res.results).Text)
                speak(next(res.results).Text)
            except StopIteration:
                print("No results")

        elif 'remember that' in query:
                speak("What should I remember ?")
                memory = takeCommand()
                speak("You asked me to remember that"+memory)
                remember = open('memory.txt','w')
                remember.write(memory)
                remember.close()

        #sleep-time
        elif "don't listen" in query or "stop listening" in query:
            speak("for how much seconds you want me to stop listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
