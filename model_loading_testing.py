#!/usr/bin/env python3
from ModelLoader import Language_Model
import argparse
import speech_recognition as sr
import subprocess
import pyttsx3
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

engine = pyttsx3.init("nsss")

r = sr.Recognizer()

model = Language_Model()

context = f'Context/{arg}.txt'
questions = f'Questions/questions_{arg}.txt'
init_file = f'Init_Files/{arg}.txt'

model_roberta = "deepset/roberta-large-squad2"
model_name = "distilbert-base-cased-distilled-squad"
#model_name = "deepset/roberta-base-squad2"

model.load_model(model_roberta)
lst_question = []

while True:
    print('Please Ask a Question')
    engine.say('Please Ask a Question')
    engine.runAndWait()

    with sr.Microphone() as source:
        try:
            audio_text = r.listen(source, timeout=10)
            audio_text = r.recognize_google(audio_text)
            print(audio_text)
        except sr.WaitTimeoutError:
            print("No audio detected. Please type your question:")
            audio_text = input()

    model.load_context(context_file=context)

    try:
        model.predict(question=[audio_text])
    except Exception as error:
        print(f"Error Occurred: {error}")
