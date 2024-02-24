#!/usr/bin/env python3

import pyttsx3
import subprocess

engine = pyttsx3.init("nsss")
engine.say("I will speak this text")
engine.runAndWait()
