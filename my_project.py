import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import datetime
import os
import numexpr as ne
import math
import webbrowser
import speech_recognition as sr
import pywhatkit
import wikipedia
import pyautogui
from pynput.keyboard import Key,Controller
from time import sleep

class VoiceAssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("GENESIS")
        master.configure(bg="#f0f0f0")  # Set background color for the entire window

        self.engine = pyttsx3.init()
        self.rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 150)  # Adjust the value as needed (default is usually 200)

        self.create_widgets()

    def create_widgets(self):
        self.chat_display = scrolledtext.ScrolledText(self.master, width=50, height=20, bg="black", fg="white")  # Set background color for the chat display
        self.chat_display.pack(expand=True, fill="both")

        self.input_label = tk.Label(self.master, text="Enter your command:", bg="white", fg="black")  # Set background color for the label
        self.input_label.pack()

        self.input_entry = tk.Entry(self.master, width=50)
        self.input_entry.pack()

        self.send_button = tk.Button(self.master, text="Send", command=self.handle_send, bg="grey", fg="white")  # Set background and foreground color for the button
        self.send_button.pack()

        #self.listen_button = tk.Button(self.master, text="Listen", command=self.handle_listen, bg="grey", fg="white")  # Add a button to listen to voice commands
        #self.listen_button.pack()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.chat_display.insert(tk.END, f"Assistant: {text}\n")
        self.chat_display.see(tk.END)

    def perform_task(self, command):
        websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com"
        }
        if "hello" in command:
            self.greetme()
        elif "i am fine" in command:
            self.speak("that's great")
        elif "how are you" in command:
            self.speak("Perfect")
        elif "thank you" in command:
            self.speak("you are welcome, sir")
        elif "what is the date" in command:
            date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today's date is {date}")
        elif "what is the time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {time}")
        elif "tell me something about you" in command:
            self.speak("""HEllo I am GENESIS your personal voice assistant. 
        Let me tell you a bit about what I can do. First off, I'm equipped with advanced speech recognition technology, so you can simply speak to me, and I'll understand. Just say          something like, 'What's the weather today?' or 'Open YouTube,' and I'll take care of it. If you prefer, you can also type your commands in the text box. I can search web for you, I can control your media playback too, When it comes to calculations, I've got you covered. By engaging with you in this friendly and informative way, I aims to create a more personal and helpful experience.
                    
        so, LET'S GET STARTED! WHAT CAN I DO FOR YOU TODAY?    """)
        elif "open" in command:
            app_name = command.split("open ")[-1]
            if app_name in websites:
                url = websites[app_name]
                webbrowser.open(url)
                self.speak(f"Opening {app_name}")
            else:
                os.system(f"start {app_name}")
                self.speak(f"Opening {app_name}")
        elif "calculate" in command:
            try:
                expression = command.split("calculate ")[-1]
                # Mapping trigonometric functions to math module for NumExpr evaluation
                result = ne.evaluate(expression, {'sin': math.sin, 'cos': math.cos, 'tan': math.tan})
                self.speak(f"The result is {result}")
            except Exception as e:
                self.speak("Sorry, I couldn't calculate that.")
        elif "google" in command:
            self.searchGoogle(command)
        elif "youtube" in command:
            self.searchYoutube(command)
        elif "wikipedia" in command:
            self.searchWikipedia(command)
        elif "pause" in command:
            pyautogui.press("k")
            self.speak("Video paused")
        elif "play" in command:
            pyautogui.press("k")
            self.speak("Video played")
        elif "mute" in command:
            pyautogui.press("m")
            self.speak("Video muted")
        elif "volume up" in command:
            self.volumeup()
            self.speak("Turning volume up")
        elif "volume down" in command:
            self.volumedown()
            self.speak("Turning volume down")
        elif command == "exit":
            self.master.quit()
        else:
            self.speak("I'm sorry, I didn't understand that.")

    def handle_send(self):
        command = self.input_entry.get().lower()
        if command:
            self.chat_display.insert(tk.END, f"User: {command}\n")
            self.input_entry.delete(0, tk.END)
            self.perform_task(command)
        else:
            self.chat_display.insert(tk.END, "User: (empty command)\n")

    def handle_listen(self):
        command = self.takeCommand().lower()
        if command:
            self.chat_display.insert(tk.END, f"User: {command}\n")
            self.perform_task(command)

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source, 0, 4)
        try:
            self.speak("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            self.speak(f"You said: {query}")
        except Exception as e:
            self.speak("Say that again, please.")
            return "None"
        return query

    def searchGoogle(self, query):
        if "google" in query:
            query = query.replace("google search", "").replace("google", "").strip()
            self.speak("This is what I found on Google.")
            try:
                pywhatkit.search(query)
                result = wikipedia.summary(query, sentences=1)
                self.speak(result)
            except:
                self.speak("No speakable output available.")

    def searchYoutube(self, query):
        if "youtube" in query:
            self.speak("This is what I found for your search!")
            query = query.replace("youtube search", "").replace("youtube", "").strip()
            web = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(web)
            pywhatkit.playonyt(query)
            self.speak("Done, Sir.")

    def searchWikipedia(self, query):
        if "wikipedia" in query:
            self.speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").replace("search wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia...")
            self.speak(results)
            self.chat_display.insert(tk.END, f"Wikipedia: {results}\n")
            self.chat_display.see(tk.END)
            

    def greetme(self):
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.speak("Good Morning")
        elif hour >= 12 and hour < 18:
            self.speak("Good Afternoon")
        else:
            self.speak("Good Evening")
        self.speak("Please tell me, how can I help you?")

    def volumeup(self):
        keyboard = Controller()
        for _ in range(5):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
            sleep(0.1)

    def volumedown(self):
        keyboard = Controller()
        for _ in range(5):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)
            sleep(0.1)
    

root = tk.Tk()
app = VoiceAssistantGUI(root)
root.mainloop()
