#!/usr/bin/env python3
from ModelLoader import Language_Model
import argparse
import speech_recognition as sr
import subprocess
import pyttsx3
from sys import platform
import time

parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Loading a model')
args = parser.parse_args()
try:
    arg = args.model
    arg = arg.lower()
except Exception as error:
    arg = 'eiffel'
    print(error)
if platform == "win32":
    engine = pyttsx3.init("sapi5")
    print("Windows detected, Opinion Rejected")
elif platform == "darwin":
    engine = pyttsx3.init("nsss")
    print("MacOS, CoolOS")
else:
    raise Exception("Unsupported Platform")

r = sr.Recognizer()

model = Language_Model()

context = f'Context/{arg}.txt'
questions = f'Questions/questions_{arg}.txt'
init_file = f'Init_Files/{arg}.txt'

model_roberta = "deepset/roberta-large-squad2"
model_name = "distilbert-base-cased-distilled-squad"
model_name = "deepset/roberta-base-squad2"
model_custom = "Models/discovery"
model.load_model(model_name)
lst_question = []

engine.say("Discovery Start")
while True:
    engine.runAndWait()
    check = 0
    with sr.Microphone() as source:
        print("Listening for 'hey discovery'...")
        audio_text = r.listen(source)
        try:
            audio_text = r.recognize_google(audio_text)
            print(audio_text)
        except sr.UnknownValueError:
            engine.say("No audio detected. Please Enter your Question")
            audio_text = input().lower()
            check = 1
    model.load_context(context_file=context)
    print("Saving model: ")
    model.save_model("discovery")
    if "hey discovery" in audio_text.lower() or (check == 1):
        with sr.Microphone() as source:
            try:
                engine.say("Please ask your question:")
                audio_text = r.listen(source)
                audio_text = r.recognize_google(audio_text)
                model.predict(question=[audio_text])
            except sr.UnknownValueError:
                print("No audio detected. Please try again.")
            except Exception as error:
                print(f"Error Occurred: {error}")
