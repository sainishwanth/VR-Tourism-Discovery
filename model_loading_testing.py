#!/usr/bin/env python3
from ModelLoader import Language_Model
import argparse
import speech_recognition as sr
import subprocess
from sys import platform
import time
def say_samantha(text):
    subprocess.run(["say", "-v", "Samantha", text])

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
    # No need for pyttsx3 on macOS
    print("Windows detected, Opinion Rejected")
elif platform == "darwin":
    print("MacOS, CoolOS")
else:
    raise Exception("Unsupported Platform")

r = sr.Recognizer()

model = Language_Model()
context = f'Context/{arg}.txt'
questions = f'Questions/questions_{arg}.txt'
init_file = f'Init_Files/{arg}.txt'
model.load_context(context)
model_roberta = "deepset/roberta-large-squad2"
model_name = "distilbert-base-cased-distilled-squad"
model_name = "deepset/roberta-base-squad2"
model_custom = "Models/discovery"
model.load_model(model_name)
lst_question = []

say_samantha("Discovery Start")

while True:
    with sr.Microphone() as source:
        try:
            print("Please ask your question:")
            say_samantha("Please ask your question:")
            audio_text = r.listen(source)
            audio_text = r.recognize_google(audio_text)
            print(audio_text)
            answer = model.predict(question=str(audio_text))
            say_samantha(answer)
        except sr.UnknownValueError as err:
            print(f"No audio detected. Please try again.{err}")
