import json

def setupConfig(develop=False, prod=False):
    try:
        with open("config.json", 'r') as c:
            conf = json.load(c)
            if develop:
                return conf['DEVELOP']
            return conf['PROD']
    except Exception as e:
        print(f"Setup config error: {e}")