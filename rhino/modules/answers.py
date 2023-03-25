# -*- coding: utf-8 -*-
from rhino.modules.rhasspy import speak, playWAV
from openhab import OpenHAB

import requests
from os import path
from pydub import AudioSegment
import urllib.request
import xmltodict
import logging

import random
import datetime
from zoneinfo import ZoneInfo

import time
import threading

import locale


import i18n
i18n.load_path.append('./rhino/modules/translations')


import yaml
with open('./rhino/settings.yml', 'r') as file:
    settings = yaml.safe_load(file)

i18n.set('locale', settings['general']['language'])
i18n.set('fallback', 'en')

locale.setlocale(locale.LC_ALL, settings['general']['locale'])

openhab_url = settings['openHAB']['http_url'] +'/rest'
openhab = OpenHAB(openhab_url)

# files                                                                         
src = "tagesschau100s.mp3"
dst = "tagesschau100s.wav"

class MyTimer(threading.Timer):
    started_at = None
    started_timer = None
    def start(self):
        self.started_at = time.time()
        self.started_timer = threading.Timer.start(self)
    def elapsed(self):
        return time.time() - self.started_at
    def remaining(self):
        return self.interval - self.elapsed()

def TimerEnds(siteId):
    files = open(f"./rhino/sounds/{settings['general']['alarm_sound']}", 'rb')
    playWAV(files, siteId)
    

def getAnswer(data):

    intent = data["intent"]["name"]
    slots = data["slots"]
    entities = data["entities"]
    siteId = data["siteId"]

    if intent != "":

        if intent == "ChangeLightState":
            
            try:
                item = openhab.get_item(slots["name"])
                if str(slots["state"]).isnumeric():
                    state = int(slots["state"])
                    speak_text = i18n.t('translations.change_light_state.light_analog', light_name=entities[0]["raw_value"], light_value=slots["state"])
                else:
                    state = slots["state"]
                    if slots["state"] == "ON":
                        speak_text = i18n.t('translations.change_light_state.light_on', light_name=entities[0]["raw_value"])
                    else:
                        speak_text = i18n.t('translations.change_light_state.light_off', light_name=entities[0]["raw_value"])
            
                try:
                    item.command(state)
                except ValueError:
                    pass
            except Exception as e:
                    speak_text = f"{i18n.t('translations.errors.no_connection_openhab')} - {e}"
                    logging.exception(f"ChangeLightState - Exception: {e}")
                    print(speak_text)
                    
            speak(speak_text,siteId)
        
            return 1
                

        elif intent == "GetJoke":
            filename = "./rhino/modules/texts/jokes_"+i18n.get('locale')+".txt"
            with open(filename, encoding="utf-8") as file:
                replies = [line.rstrip() for line in file]
        
            speak(str(random.choice(replies)), siteId)
            return 1
        
        elif intent == "Gamingmode":
            try:
                openhab.get_item(settings['openHAB']['items']['gaming']).command("ON")
                speak_text = i18n.t('translations.gamingmode.feedback')
            except Exception as e:
                    speak_text = f"{i18n.t('translations.errors.no_connection_openhab')} - {e}"
                    logging.exception(f"Gamingmode - Exception: {e}")
                    print(speak_text)
            
            speak(speak_text, siteId)
            return 1
        
        elif intent == "PlayNews":

            try:
                response = requests.get("https://www.tagesschau.de/export/podcast/hi/tagesschau-in-100-sekunden")
            except requests.exceptions.RequestException as e:
                speak(i18n.t('translations.errors.playnews'), siteId)
                logging.exception(f"PlayNews - Exception: {e}")
            
            xmldata = xmltodict.parse(response.content)

            # Download the file from `url` and save it locally under `file_name`:
            with urllib.request.urlopen(xmldata["rss"]["channel"]["item"]["enclosure"]["@url"]) as response, open(src, 'wb') as out_file:
                audiodata = response.read() # a `bytes` object
                out_file.write(audiodata)
        
            # convert wav to mp3                                                            
            sound = AudioSegment.from_mp3(src)
            #t1 = 0 * 1000 #Works in milliseconds
            #t2 = 20 * 1000
            #sound = sound[t1:t2]
            sound = sound.set_channels(1)
            sound.export(dst, format="wav") # parameters=["-ac","1","-ar","8000"])

            #-H  "accept: text/plain" -H  "Content-Type: audio/wav" --data-binary @"/etc/openhab/sounds/$1.wav"

            files = open(dst, 'rb')
            playWAV(files, siteId)
            
            return 1
        
                
        elif intent == "GetTemperature":
            try:
                temperature = openhab.get_item(settings['openHAB']['items']['outside_temperature']).state
                temperature = locale.format_string('%.1f', temperature)
                speak_text = i18n.t('translations.get_temperature.feedback', temperature=str(temperature))
            except Exception as e:
                speak_text = f"{i18n.t('translations.errors.no_connection_openhab')} - {e}"
                logging.exception(f"GetTemperature - Exception: {e}")
                print(speak_text)
                
            speak(speak_text, siteId)
            return 1
                
        elif intent == "GetWeather":
            try:
                temperature = openhab.get_item(settings['openHAB']['items']['outside_temperature']).state
                temperature = locale.format_string('%.1f', temperature)
                weather_condition = openhab.get_item(settings['openHAB']['items']['weather_condition']).state 
                speak_text = i18n.t('translations.get_weather.feedback', condition=str(weather_condition),temperature=str(temperature))
            except Exception as e:
                speak_text = f"{i18n.t('translations.errors.no_connection_openhab')} - {e}"
                logging.exception(f"GetWeather - Exception: {e}")
                print(speak_text)
    
            speak(speak_text, siteId)
            return 1
    
        elif intent == "GetTime":
    
            speak(i18n.t('translations.get_time.feedback', hour=datetime.datetime.now(ZoneInfo(settings['general']['timezone'])).hour, minute=datetime.datetime.now(ZoneInfo(settings['general']['timezone'])).minute), siteId)

            return 1

        elif intent == "GetDay":
            speak(datetime.datetime.now(ZoneInfo(settings['general']['timezone'])).strftime("%A"), siteId)
            return 1

        elif intent == "GetDice":

            randomnumber = random.SystemRandom().randint(1, 6)
            speak(str(randomnumber), siteId)
            return 1        

        elif intent == "Thanks":
            filename = "./rhino/modules/texts/thanks_"+i18n.get('locale')+".txt"
            with open(filename, encoding="utf-8") as file:
                replies = [line.rstrip() for line in file]
        
            speak(str(random.choice(replies)), siteId)
            return 1


        elif intent == "Hello":
            filename = "./rhino/modules/texts/hello_"+i18n.get('locale')+".txt"
            with open(filename, encoding="utf-8") as file:
                replies = [line.rstrip() for line in file]
        
            speak(str(random.choice(replies)), siteId)
            return

        elif intent == "GoodMorning":
            filename = "./rhino/modules/texts/good_morning_"+i18n.get('locale')+".txt"
            with open(filename, encoding="utf-8") as file:
                replies = [line.rstrip() for line in file]
        
            speak(str(random.choice(replies)), siteId)
            return 1


        elif intent == "GoodNight":
            filename = "./rhino/modules/texts/good_night_"+i18n.get('locale')+".txt"
            with open(filename, encoding="utf-8") as file:
                replies = [line.rstrip() for line in file]
        
            speak(str(random.choice(replies)), siteId)
            return 1
        
        elif intent == "Timer:start":
            global timer
            total_seconds = 0
            seconds = int(slots.get("seconds",0))
            minutes = int(slots.get("minutes",0))
            hours = int(slots.get("hours",0))

            total_seconds = seconds + minutes * 60 + hours * 3600
            

            timer = MyTimer(total_seconds, TimerEnds, [siteId])
            timer.start()

            answer_timer = ""
            if hours > 0 and minutes > 0:
                answer_timer = i18n.t('translations.timer.started.hours_minutes_seconds', hours=hours, minutes=minutes, seconds=seconds)
            elif minutes > 0:
                answer_timer = i18n.t('translations.timer.started.minutes_seconds', minutes=minutes, seconds=seconds)
            elif seconds > 0:
                answer_timer = i18n.t('translations.timer.started.seconds', seconds=seconds)

            speak(answer_timer, siteId)
            return 1

        elif intent == "Timer:remaining":
            total_seconds = timer.remaining()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)

            answer_timer = ""
            if hours > 0 and minutes > 0:
                answer_timer = i18n.t('translations.timer.remaining.hours_minutes_seconds', hours=hours, minutes=minutes, seconds=seconds)
            elif minutes > 0:
                answer_timer = i18n.t('translations.timer.remaining.minutes_seconds', minutes=minutes, seconds=seconds)
            elif seconds > 0:
                answer_timer = i18n.t('translations.timer.remaining.seconds', seconds=seconds)

            speak(answer_timer, siteId)
            return 1        

        else:
            return 0

    else:
        return 0