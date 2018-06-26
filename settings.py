import json

def setupConfig(develop=False, prod=False):
    #This func take config from config.json and add them to the application
    try:
        with open("config.json", 'r') as c:
            conf = json.load(c)
            if develop:
                return conf['DEVELOP']
            return conf['PROD']
    except Exception as e:
        print(f"Setup config error: {e}")