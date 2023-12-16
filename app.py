import speech_recognition as sr
from youtubesearchpython import VideosSearch
import os
import pyautogui
import wikipedia
from time import sleep
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import webbrowser
import functions
import threading
name="echo"
# Initialize the recognizer
recognizer = sr.Recognizer()
exit_flag=False
# Configure the microphone as the audio source
microphone = sr.Microphone()
def adjust_system_volume(percent_change):
    devices = AudioUtilities.Getfunctions.speakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    ).QueryInterface(IAudioEndpointVolume)

    current_volume = interface.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, min(1.0, current_volume + percent_change))

    # Set the new volume level
    interface.SetMasterVolumeLevelScalar(new_volume, None)
def search(name):
    try:
        page = wikipedia.page(name)
        p=f"{page.summary}"
        functions.speak(p[:p.find(".")])
    except wikipedia.exceptions.PageError:
        functions.speak("no information found!")
        
def time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")
    functions.speak(formatted_time)
def open(query):
    # Press the Windows key to open the Start menu
    pyautogui.press('win')

    # Wait for the Start menu to open (adjust sleep duration if needed)

    # Type the search query into the search bar
    pyautogui.write(query, interval=0.1)

    # Press Enter to perform the search
    sleep(1)
    pyautogui.press('enter')

    

    
        
def play_song(song_name):
    # Search for the song on YouTube
    videos_search = VideosSearch(song_name, limit = 1)
    results = videos_search.result()

    # Check if there are any search results
    if not results['result']:
        print(f"No results found for '{song_name}'.")
        return

    # Get the URL of the first video in the search results
    video_url = results['result'][0]['link']

    # Open the video in the default web browser
    webbrowser.open(video_url)
    
def tr(a):
    text = recognizer.recognize_google(a).lower()

def main ():
    global exit_flag
    
    print("echo Running!")
    while( exit_flag == True):
        try:
            with microphone as source:
                # Adjust for ambient noise once when the program starts
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source,phrase_time_limit=6)
                program_thread = threading.Thread(check(audio))
                program_thread.start()
                
                
                
     
        except :
            recognizer = sr.Recognizer()
            continue
    print("echo Stopped!")       
        
def check(audio):
    global name
    text = recognizer.recognize_google(audio).lower()
    
    if name in text:
        text=text.replace("echo","")
        print(text)
        if ("hello" in text or "hey" in text or "hi" in text) and (not "play" in text) :
            functions.speak("hello there!")
        elif "what's up" in text or "how are you" in text:
            functions.speak("nothing new im just a robot what about you how are you today")
        elif "song" in text or "play" in text :
            text=text.replace("song","")
            text=text.replace("play","")
            play_song(text)
        elif "open" in text:
            text=text.replace("open","")
            open(text)
        elif "who" in text or "who's" in text or "who is" in text:
            text=text.replace("who","")
            text=text.replace("who's","")
            text=text.replace("who is","")
            search(text)
        elif "say" in text :
            text=text.replace("say","")
            functions.speak(text)
        elif "time" in text :
            text=text.replace("time","")
            functions.speak(time())
        elif "volume" in text:
            if "up" in text :
                adjust_system_volume(0.25)
            elif "down" in text :
                adjust_system_volume(-0.25)
            elif "max" in text :
                adjust_system_volume(1)
            elif "off" in text :
                adjust_system_volume(-1)
        elif "google" in text:
            text=text.replace("google","")
            functions.search_and_open(text)

