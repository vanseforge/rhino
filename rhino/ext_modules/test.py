from rhino.modules.rhasspy import speak

def Test(data, siteId):
    text = "I am a test function for a user module"
    print("TEST!")
    speak(text, siteId)