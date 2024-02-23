#!/usr/bin/env python3
from transformers import pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch
import subprocess
import pyttsx3
from sys import platform
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

    def predict(self, question=[], voice_check: bool=True, generator_check: bool=False) -> None:
        print(f"Len: {len(question)}")
        if len(question) >= 1:
            self.questions = question
        for question in self.questions:
            result = self.model(question=question, context=self.context)
            print(result)
            answer = result['answer']
            if generator_check == True:
                if not answer.isdigit() and not len(answer.split()) == 1: # Ignoring Generation if the answer is a digit (year, etc) or it is a single word (bad generations)
                    if len(answer.split()) < 3:
                        answer = self.generator(answer, max_length=5)
                        answer = answer[0]['generated_text']
            response = f"Question: {question}\nAnswer: {answer}\n"
            print(response)
            #with open(f"Answer_Dump/answer_{self.model_name}{self.place}", "a") as file:
            #    file.write(response)
            #    if voice_check:
            self.voice_generation(answer)
        return None

    def save_model(self, saved_model_name: str) -> None:
        self.model.save_pretrained(f"Models/{saved_model_name}")

    def custom_predict(self, user_input) -> None:

        pass

    def voice_generation(self, text) -> None:

        self.engine.say(text)
        self.engine.runAndWait()
