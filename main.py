import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
from gtts import gTTS
import pygame
import os 
import pyscreenshot as ImageGrab
from PIL import Image



# function taking text as input and converting it to speech
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()


# function using google text to speech 
# pygame is used to convert mp3 to text
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize the mixer
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the mp3 file
    pygame.mixer.music.play()

    # Keep the program running until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# code to take a screenshot of whatever screen the user is on and open that image
def screen_shot():
    im = ImageGrab.grab()
    im.save("fullscreen.png")
    ss = Image.open("fullscreen.png")
    ss.show()

def process_command(c): #processes the command given to it after the wake word is recognized
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "play" in c.lower():
        l = c.lower().split()
        ind = l.index("play")
        song = l[ind+1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "screenshot" in c.lower():
        screen_shot()



if __name__ == "__main__":
    speak("Initializing Jarvis")
    # listen for the wake word 'Jarvis'
    while True:
        r = sr.Recognizer()
        
        try: 
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1) #takes audio for 2 seconds listening for 1 second
            word = r.recognize_google(audio) # converts the audio into text by recognizing it
            if word.lower() == "jarvis": #checks if the audio is saying the word 'jarvis' as its wake word
                speak("How may i help you")
                # listen for further command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source) #takes audio for 2 seconds listening for 1 second
                    command = r.recognize_google(audio)
                    process_command(command)



        except Exception as e: #handles exception in case nothing is spoken
            print("Error;{0}".format(e))
        