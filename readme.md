# **RH**ASSPY **I**TENT HA**N**DLER FOR **O**PENHAB (RHINO)
## Introduction
RHINO (**RH**ASSPY **I**TENT HA**N**DLER FOR **O**PENHAB) is a simple intent handler for rhasspy with a connection to openHAB.
Some skills are built-in and is also possible to write own skills (folder "ext_modules").
Available skills:
* Switch on/off lights
* Tell a joke
* Activate gaming mode
* Play "Tagesschau in 100 s" (german only, sorry)
* Get outside temperature
* Get weather
* Get time/day
* Roll a dice
* Say hello, good morning, good night, thanks
* Start a timer

## Installation & Configuration

### Installation
Clone this reporsitory:
```
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```
Navigate to the cloned reporsitory where the dockerfile is.

Docker command line:
```
docker image build -t rhino .
docker run -d -v your_folder/settings.yml:/usr/app/rhino/rhino/settings.yml,your_folder/ext_modules:/usr/app/rhino/rhino/ext_modules --name rhino rhino
```

The settings.yml should point to your own settings file.
The ext_modules folder should point to a folder with your own skills (optional).

In rhasspy you need to write your sentences for the used intents. An example is in the folder rhasspy_sentences. The translation from the light names to the openhab items needs to be done in the sentence file in rhasspy.

### Configuration
Adjust the settings in settings.yml file

Example of settings.yml:
```
general:
  timezone: 'Europe/Berlin'
  locale: 'de_DE.UTF-8'
  language: 'de'
  alarm_sound: 'alarm.wav'
openHAB:
  http_url: 'http://10.0.0.3:8080'
  items:
    outside_temperature: 'HeatPump_Temperature_1'
    weather_condition: 'Weather_OWM_Condition'
    gaming: 'Gaming'
rhasspy:
  http_url: 'http://10.0.0.2:12101'
  websocket_url: 'ws://10.0.0.2:12101'
  ```

## How to write an own skill
You just need to create a function which is namend like your intent and has two parameter (data from rhasspy and the site id). The data from rhasspy is the JSON string from rhasspy and the site id is id from the rhasspy satellite.
Example
```
def Test(data, siteId):
    text = "I am a test function for a user module"
    print("TEST!")
    speak(text, siteId)
```

## Donate
If you would like to support the developer with a cup of coffee you can do that via [Buy Me A Coffee](https://www.buymeacoffee.com/vanseforge).

## Todo
* Function to stop the timer

## Contributing
Community contributions are welcomed!

