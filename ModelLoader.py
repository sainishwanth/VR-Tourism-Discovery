#!/usr/bin/env python3
from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch
import subprocess
import pyttsx3
from sys import platform
import os
class Language_Model:

    def __init__(self):
        self.place = None
        self.model_name = None
        self.model = None
        self.context = None
        self.questions = None
        self.generator = None
        self.generator_name = 'distilgpt2'
        if platform == "win32":
            self.engine = pyttsx3.init("sapi5")
            print("Windows detected, Opinion Rejected")
        elif platform == "darwin":
            self.engine = pyttsx3.init("nsss")
            print("MacOS, CoolOS")
        else:
            raise Exception("Unsupported Platform")
        self.engine.setProperty('rate', 170)

    def load_model(self, model_name:str) -> None:

        self.model_name = model_name
        self.model = pipeline('question-answering', model=model_name, tokenizer=model_name)
        #self.generator = pipeline('text-generation', self.generator_name)

    def load_context(self, context_file:str) -> None:

        self.place = context_file
        with open(context_file, "r") as file:
            self.context = file.read()

    def load_question(self, questions_file: str) -> None:

        with open(questions_file, "r") as file:
            self.questions = file.readlines()
            for i in range(len(self.questions)):
               self.questions[i] = self.questions[i].replace("\n", "")
        print(self.questions)

    def predict(self, question, voice_check: bool=True, generator_check: bool=False) -> str:
        result = self.model(question=question, context=self.context)
        answer = result['answer']
        response = f"Question: {question}\nAnswer: {answer}\n"
        print(response)
        return answer

    def save_model(self, saved_model_name: str) -> None:
        if os.path.exists(os.getcwd()+'/'+saved_model_name):
            print("Model Exists")
            return
        print("Saving the model....")
        self.model.save_pretrained(f"Models/{saved_model_name}")
        print("Model Saved")

    def custom_predict(self, user_input) -> None:
        pass

    def voice_generation(self, text) -> None:
        subprocess.run(["say", "-v", "Samantha", text])

