# Project Name: Oracle Robotics 
# Cozmo Detective model used as base from whatrocks GitHub
# Additional functions added as needed
# DRAFT FILE BEFORE I MAKE THE CHANGES IN THE FINAL CODE

from flask import Flask
import sys
import os
import shutil
import requests
import json
import time
import asyncio
import datetime
import subprocess


app = Flask(__name__)

isProcessing = False
isTakingPicture = False
targetObject = 'alienoid'
discoveredObject = False


@app.route('/<object>')
def index(object):
    subprocess.call('pipenv run python3 findObject.py ' + object, shell=True)
    return "Cozmo is doing its things!"