#!/usr/bin/env python3
from ModelLoader import Language_Model
import argparse
import speech_recognition as sr
import subprocess
import pyttsx3

parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Loading a model')
args = parser.parse_args()
arg = args.model
arg = arg.lower()

engine = pyttsx3.init("nsss")

r = sr.Recognizer()

model = Language_Model()

context = f'Context/{arg}.txt'
questions = f'Questions/questions_{arg}.txt'
init_file = f'Init_Files/{arg}.txt'

#model_name = "deepset/roberta-large-squad2"
model_name = "distilbert-base-cased-distilled-squad"
#model_name = "deepset/roberta-base-squad2"

model.load_model(model_name)
lst_question = []
with open(init_file, "r") as file:
    intro_speech = file.read()

engine.say(intro_speech)

while True:
    engine.say('Please Ask a Question')
    engine.runAndWait()
    with sr.Microphone() as source:
        audio_text = r.listen(source)
    model.load_context(context_file=context)
    try:
        audio_text = r.recognize_google(audio_text)
    except Exception as error:
        print(f"Error Occured: {error}")
    print(audio_text)
    model.predict(question=[audio_text])
