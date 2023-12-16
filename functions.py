import webbrowser
from googlesearch import search
from gtts import gTTS
import os
import pygame
def search_and_open(query):
    try:
        # Perform a Google search and get the first link
        search_results = search(query, num=1, stop=1, pause=2)
        first_link = next(search_results, None)

        if first_link:
            # Open the first link in the default web browser
            webbrowser.open(first_link)
            print(f"Opened: {query}")
        else:
            print(f"No search results found for: {query}")

    except Exception as e:
        print(f"An error occurred: {e}")




def play_mp3(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # Wait for the music to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except pygame.error as e:
        print("Error playing the MP3 file:", e)

    pygame.quit()

def speak(text, language='en'):
    try:
        # Generate the MP3 file
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save("output.mp3")

        # Play the generated MP3 file
        play_mp3("output.mp3")
    except:
        pass