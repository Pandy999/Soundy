import requests
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()

voices = []
r = requests.get('https://api.elevenlabs.io/v1/voices').json()
for voice in r['voices']:
    voices.append(voice['name'])
print(voices)