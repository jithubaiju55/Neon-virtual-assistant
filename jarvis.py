
import pyttsx3
import speech_recognition as sr
import datetime as dt
import os
import cv2
from requests import get
import time
import json
import string
import re
import webbrowser
import pywhatkit as kit
import sys
from word2number import w2n
import pyjokes
from contacts import contacts
import vobject
import pyautogui
import requests
import instadownloader
import instaloader
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Neonui import Ui_NeonGUI
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voices',voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50) 

with open('what.json', 'r') as file:
    what = json.load(file)

with open('tellabout.json','r') as file:
    tellabt=json.load(file)

with open('who.json','r') as file:
    who=json.load(file)

with open('why.json','r') as file:
    why=json.load(file)
#text for speaking
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def clean_text(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))



def wish():
    hour=int(dt.datetime.now().hour)
    tt=time.strftime("%I:%M %p")

    if hour>=0 and hour<=12:
        speak(f"good Morning ,its {tt}")
    elif hour>12 and hour<18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")
    speak("i am Neon,your personal assistant, sir please tell me how i can help you")

import datetime as dt
import time
import os

def parse_time_manual(time_str):
    try:
        # Normalize input: remove extra spaces, correct AM/PM notation, and handle missing colons
        time_str = time_str.lower().replace('.', '').strip()

        # Add colon if missing between hours and minutes
        if len(time_str) > 2 and time_str[-2:] in ("am", "pm") and ':' not in time_str:
            time_str = time_str[:-2].zfill(4) + time_str[-2:]
            time_str = time_str[:2] + ":" + time_str[2:]

        # Parse time based on AM/PM or 24-hour format
        if "am" in time_str or "pm" in time_str:
            alarm_time = dt.datetime.strptime(time_str, "%I:%M %p")
        else:
            alarm_time = dt.datetime.strptime(time_str, "%H:%M")
        
        now = dt.datetime.now()
        # Set the alarm for the current day or the next day if time has passed
        alarm_time = alarm_time.replace(year=now.year, month=now.month, day=now.day)
        if alarm_time < now:
            alarm_time += dt.timedelta(days=1)
        
        return alarm_time
    except Exception as e:
        speak(f"Invalid time format. Please enter time in HH:MM AM/PM or 24-hour format. Error: {e}")
        return None

def set_alarm_with_voice():
    speak("Please tell the time for the alarm in the format HH:MM AM or PM.")
    time_query = MainThread().takecommand().lower()  # Capture the spoken input

    try:
        # Parse the time
        alarm_time = parse_time_manual(time_query)
        if not alarm_time:
            speak("Unable to set the alarm. Please provide a valid time.")
            return

        # Confirm the alarm time to the user
        speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}. Waiting until the alarm time.")
        
        while True:
            now = dt.datetime.now()
            if now >= alarm_time:
                # Play music or perform an action
                music_dir = 'D:\\music'
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                speak("Your alarm is ringing!")
                break
            time.sleep(1)  # Sleep for a second to reduce CPU usage
    except Exception as e:
        speak(f"Error setting the alarm: {e}")


  
def clean_text(text):
    text = text.lower()  # Convert to lowercase for case-insensitive comparison
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

def match_query(query, data):
    found = False
    query_clean = clean_text(query)  # Clean and normalize the query
    
    # Loop through the questions in the "tell_about" section
    for qa in data["tell_about"]:
        if isinstance(qa, dict):  # Ensure the item is a dictionary
            question_clean = clean_text(qa["question"])  # Clean and normalize the question
            
            # Check if the cleaned query exactly matches the cleaned question
            if query_clean == question_clean:
                speak(qa['answer'])
                found = True
                break
    
    return found


def parse_vcf(file_path):
    contacts = {}
    with open(file_path, "r") as file:
        vcf = vobject.readComponents(file)
        for contact in vcf:
            if hasattr(contact, "fn") and hasattr(contact, "tel"):
                name = contact.fn.value
                phone = contact.tel.value
                contacts[name.lower()] = phone
    return contacts



def send_message_via_voice(contacts,self):
    speak("Please say the name of the contact you want to send a message to.")
    contact_name = startExection.takecommand()
    
    if contact_name in contacts:
        phone_number = contacts[contact_name]
        speak(f"Found contact {contact_name} with number {phone_number}. Should I send the message?")
        
        confirmation = startExection.takecommand()
        if "yes" in confirmation:
            speak("Please say the message you want to send.")
            message = startExection.takecommand()
            
            speak("At what hour should I send the message? Say in 24-hour format.")
            hour = startExection.takecommand()
            
            # Ensure hour is valid
            try:
                hour = int(hour)
            except ValueError:
                speak("Sorry, I didn't catch the hour. Let's try again.")
                return send_message_via_voice(contacts)

            speak("At what minute should I send the message?")
            minute = startExection.takecommand()
            
            # Ensure minute is valid
            try:
                minute = int(minute)
            except ValueError:
                speak("Sorry, I didn't catch the minute. Let's try again.")
                return send_message_via_voice(contacts)
            
            # Send the WhatsApp message
            speak(f"Sending your message to {contact_name} at {hour}:{minute}.")
            kit.sendwhatmsg(phone_number, message, hour, minute)
            speak("Message sent!")
        else:
            speak("Message not sent.")
    else:
        speak("Sorry, I couldn't find that contact. Please try again.")

def main_msg():
    contacts = parse_vcf("contacts.vcf")
    speak("Contacts loaded successfully!")

    # Start sending a message via voice
    send_message_via_voice(contacts)


def news():
    main_url='https://newsapi.org/v2/everything?q=tesla&from=2024-11-06&sortBy=publishedAt&apiKey=690a2e28fb1b452c8ad791b1e667400f'
    main_page=requests.get(main_url).json()
    articles=main_page['articles']
    head=[]
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar['title'])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("listeninig.....")
            r.pause_threshold=2
            audio=r.listen(source,timeout=3,phrase_time_limit=10)
        try:
            print("Recoginising....")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said :{query}")
        except Exception as e:
            print("say that again.....")
            return "none"
        return query
    

    def TaskExecution(self):
            wish()
            while True:  # Loop to keep the assistant active
                self.query = self.takecommand().lower()

                if 'open notepad' in self.query:
                    speak("opening notepad")
                    npath = "C:\\Windows\\System32\\notepad.exe"
                    os.startfile(npath)

                elif 'open calculator' in self.query:
                    cpath = "C:\\Windows\\System32\\calc.exe"
                    os.startfile(cpath)

                elif 'open chrome' in self.query:
                    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                    os.startfile(chrome_path)

                elif 'open paint' in self.query:
                    paint_path = "C:\\Windows\\System32\\mspaint.exe"
                    os.startfile(paint_path)

                elif 'open vs code' in self.query:
                    vpath="D:\\Microsoft VS Code"
                    os.startfile(vpath)
                elif 'open camera' in self.query:
                    cap= cv2.VideoCapture(0)
                    while True:
                        ret,img=cap.read()
                        cv2.imshow('webcam',img)
                        k=cv2.waitKey(50)
                        if k==27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()

                elif 'ip address' in self.query:
                    ip=get('https://api.ipify.org').text
                    speak(f"your ip address is {ip}")

                elif 'what' in self.query:
                    found=False
                    for qa in what:
                        if self.query in qa["question"].lower() :
                            speak(qa['answer'])
                            found=True
                            break
                    if not found:
                        speak("i am sorry i dont have answer for that question")
                elif 'tell about' in self.query:
                    found = match_query(self.query, tellabt)
                    if not found:
                        speak("I'm sorry, I don't have an answer for that question.")
                elif 'who' in self.query:
                    found=False
                    for qa in who:
                        if self.query in qa["question"].lower() :
                            speak(qa['answer'])
                            found=True
                            break
                    if not found:
                        speak("i am sorry i dont have answer for that question")
                elif 'why' in self.query:
                    found=False
                    for qa in why:
                        if self.query in qa["question"].lower() :
                            speak(qa['answer'])
                            found=True
                            break
                    if not found:
                        speak("i am sorry i dont have answer for that question")
                elif 'open youtube' in self.query:
                    webbrowser.open('www.youtube.com')

                elif 'open github' in self.query:
                    webbrowser.open("www.github.com")

                elif 'open instagram' in self.query:
                    webbrowser.open('www.instagram.com')

            #setting alaram

                elif 'set alarm' in self.query or 'set a alarm' in self.query or 'set an alarm' in self.query:
                    set_alarm_with_voice()

        



                elif 'send a message' in self.query:
                    main_msg()

                elif 'play a song on youtube' in self.query or 'play song on yotube'in self.query or 'play on youtube' in self.query:
                    kit.playonyt("unravel")

                elif 'no thanks' in self.query:
                    speak("thank you for using me sir , have a nice day")
                    sys.exit()

                elif 'close notepad' in self.query:
                    speak("closing notepad")
                    os.system('taskkill /f /im notepad.exe')
                elif 'tell me a joke' in self.query:
                    joke=pyjokes.get_joke()
                    speak(joke)
                elif 'shutdown the system' in self.query:
                    os.system("shutdowm /s /t 5")
                elif 'restart the system' in self.query:
                    os.system("shutdown /r /t 5")
                elif "sleep the system" in self.query:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

                elif 'switch the window' in self.query or 'alt tab' in self.query or 'next window' in self.query:
                    pyautogui.keyDown('alt')
                    pyautogui.press('tab')
                    time.sleep(1)
                    pyautogui.keyUp('alt')
                elif 'tell news' in self.query:
                    news()

                elif 'where am i ' in self.query or'where are we' in self.query or 'find my location' in self.query or 'where are you'in self.query:
                    speak('wait sir, let me check')
                    try:
                        ipAdd=requests.get('https://api.ipify.org').text
                        print(ipAdd)
                        url=f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                        geo_request=requests.get(url)
                        geo_data=geo_request.json()
                        city=geo_data['city']
                        country=geo_data['country']
                        speak(f"sir i am not sure ,i think we are in {city} city of {country}  country ")
                    except Exception as e:
                        speak('sorry sir due to network issue iam not able to find where we are ')
                elif 'instagram profile' in self.query or 'profile on instagram' in self.query or 'open my account in instagram'  in self.query or 'open my instagram account' in self.query:
                    speak("sir , please enter the user name correctly")
                    name=input("enter userbame here")
                    webbrowser.open(f"www.instagram.com/{name}")
                    speak(f"here is the profile of user {name}")
                    time.sleep(5)
                    speak("sir would you like to download profile picture of this account")
                    condition=self.takecommand().lower()
                    if 'yes' in condition:
                        mod=instaloader.Instaloader()
                        mod.download_profile(name,profile_pic_only=True)
                        speak("i am done sir ,profile picture is saved in your download folder")
                    else:
                        pass
                elif 'take screenshot' in self.query or 'take a screenshot' in self.query or 'take the screenshot' in self.query:
                    try:
                        speak("Sir, please tell me the name for this screenshot file.")
                        name = self.takecommand().lower()
                        if name == "none" or name.strip() == "":
                            speak("Sorry, I didn't catch the name. Using a default filename.")
                            name = "screenshot"
            
                        speak("Sir, please hold the screen for a few seconds. I am taking the screenshot.")
                        time.sleep(3)
                        img=pyautogui.screenshot()
                        img.save(f"{name}.png")
                        speak("i am done sir the screeshot is saved in the main folder")
                    except Exception as e:
                        speak("Sorry, I was unable to take the screenshot. Please try again.")
                    print(f"Error: {e}")
                elif 'hide all files' in self.query or 'hide folder' in self.query or 'hide data' in self.query:
                    speak('sir please tell me you wnat to hide this folder or make it visible')
                    filecondition=self.takecommand().lower()
                    if "hide" in filecondition:
                        os.system('attrib +h /s /d')
                        speak('sir,all the files in this folder are now hidden')
                    elif 'visible' in filecondition:
                        os.system('attrib -h /s /d')
                        speak('sir,all the files in this folder are now visible')
                    elif 'leave it' in filecondition or 'leave for now' in filecondition:
                        speak('ok sir')

                elif 'do some calculation' in self.query or 'can you calculate' in self.query or 'please calculate'in self.query or 'do this calculation' in self.query:
                        r=sr.Recognizer()
                        with sr.Microphone() as source:
                            speak('say what you want to calculate , example: 3 plus 3')
                            print('listening.....')
                            r.adjust_for_ambient_noise(source)
                            audio=r.listen(source)
                        my_string=r.recognize_google(audio).lower()
                        print(my_string)
                        def get_operator_fu(op):
                            return{
                                '+':operator.add,
                                '-':operator.sub,
                                'x':operator.mul,
                                'divided':operator.truediv


                            }[op]
                        def eval_expr(op1,oper,op2):
                            op1,op2=int(op1),int(op2)
                            return get_operator_fu(oper)(op1,op2)
                        speak("your result is")
                        speak(str(eval_expr(*(my_string.split()))))

                elif 'check the temperature' in self.query or 'check wheather' in self.query:
                    speak('which place temperature do you want to know sir')
                    plc=self.takecommand().lower()
                    print(f"Place received: {plc}")
                    search=f'temperature in {plc}'
                    url=f'https://www.google.com/search?q={search}'
                    r=requests.get(url)
                    data=BeautifulSoup(r.text,'html.parser')
                    temp=data.find('div',class_='BNeawe iBp4i AP7Wnd').text
                    speak(f"current {search} is {temp}")

                elif 'activate how to do mode' in self.query:
                    speak('how to do mode is activated ')
                    while True:
                        speak('please tell me what you want to know')
                        how=self.takecommand().lower()
                        try:
                            if 'exit'in how or 'close how to do mode' in how or 'close'in how:
                                speak('ok sir how to do mode is closed')
                                break
                            else:
                                max_result=1
                                speak("wait sir i am fetching the deatils")
                                how_to=search_wikihow(how,max_result)
                                assert len(how_to)==1
                                how_to[0].print()
                                speak(how_to[0].summary)
                        except Exception as e:
                            speak('sorry sir, i am not able to find this')
                elif 'how much power left' in self.query or 'how much power we have' in self.query or 'battery' in self.query:
                    battery=psutil.sensors_battery()
                    percentage=battery.percent
                    speak(f'sir our system have {percentage} percent battery')
                speak("sir , do you have any other work")

startExection=MainThread()
    
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_NeonGUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
    
    def startTask(self):
        self.ui.movie=QtGui.QMovie("C:/Users/Jithu/Downloads/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie=QtGui.QMovie("C:/Users/Jithu/Downloads/XDZT.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie=QtGui.QMovie("C:/Users/Jithu/Downloads/Jarvis_Loading_Screen.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie=QtGui.QMovie("C:/Users/Jithu/Downloads/D4Ll.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer=QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExection.start()
    
    def showTime(self):
        current_time=QTime.currentTime()
        current_date=QDate.currentDate()
        label_time=current_time.toString('hh:mm:ss')
        label_date=current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app=QApplication(sys.argv)
neon=Main()
neon.show()
exit(app.exec())
