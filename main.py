#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets
import requests
import json
import logging

import i18n
i18n.load_path.append('./rhino/modules/translations')

import rhino

import yaml
with open('./rhino/settings.yml', 'r') as file:
    settings = yaml.safe_load(file)

i18n.set('locale', settings['general']['language'])
i18n.set('fallback', 'en')

rhasspy_websocket = settings['rhasspy']['websocket_url']+'/api/events/intent'


async def websocket_loop():
   
    while True:
        async with websockets.connect(rhasspy_websocket) as websocket:
 
            recv = await websocket.recv()

            jsonstring = json.loads(recv)

            siteId = jsonstring["siteId"]
            intent = jsonstring["intent"]["name"]

            logging.info(f"JSON: {recv}")
            logging.info(f"Intent: |{intent}|")
            print(f"JSON: {recv}")
            print(f"Intent: |{intent}|")

            if intent != "" and rhino.modules.answers.getAnswer(jsonstring) == 0:

                if hasattr(rhino.ext_modules, intent):

                    try:
                        externalFunction = getattr(rhino.ext_modules, intent)
                        externalFunction(jsonstring, siteId)

                    except AttributeError as e:
                        rhino.modules.rhasspy.speak(i18n.t('translations.errors.no_skill'), siteId)
                else:
                    rhino.modules.rhasspy.speak(i18n.t('translations.errors.no_skill'), siteId)

if __name__ == "__main__":
    logging.info("Started")
    print("Started")
    asyncio.run(websocket_loop())


