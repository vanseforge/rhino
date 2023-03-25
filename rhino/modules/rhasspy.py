import requests
import logging


import yaml
with open('./rhino/settings.yml', 'r') as file:
    settings = yaml.safe_load(file)

rhasspy_url = settings['rhasspy']['http_url']

def speak(text, siteId):

    if text is None or text == "":
        return
    if siteId is None:
        siteId = ""

    if text == "":
        return

    logging.info(f"Text: {text}, siteId: {siteId}")
    try:
         requests.post( rhasspy_url+"/api/text-to-speech?siteId=" +siteId , data = text.encode('utf-8'))
    except requests.exceptions.RequestException as e: 
        logging.exception(f"speak() - Exception: {e}")

def playWAV(wavfile, siteId):
    headers = {'accept': 'text/plain', 'content-type': 'audio/wav'}
    try:
          requests.post(rhasspy_url +"/api/play-wav?siteId=" + siteId, data=wavfile, headers=headers)
    except requests.exceptions.RequestException as e: 
        logging.exception(f"playWAV() - Exception: {e}")
   