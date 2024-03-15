import urllib.request, json

api = '' # your api key from https://developer.riotgames.com/
puuid = '' # fill in with a player puuid

with urllib.request.urlopen(
        'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/' + puuid) as url:
    matchList = json.loads(url.read().decode())

print(matchList)

i = 1

for match in matchList:
    with urllib.request.urlopen(
            'https://europe.api.riotgames.com/lol/match/v5/matches/' + match + '/timeline?api_key=' + api) as url:
        data = json.loads(url.read().decode())
        jsonString = json.dumps(data, indent=4)
        jsonFile = open("Match" + str(i) + ".json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        print("Match" + str(i) + "data fetched!")
    i = i + 1

i = 1

for match in matchList:
    with urllib.request.urlopen(
            'https://europe.api.riotgames.com/lol/match/v5/matches/' + match + '?api_key=' + api) as url:

        # https://europe.api.riotgames.com/lol/match/v5/matches/EUN1_3151592547?api_key=RGAPI-bd7e0ddf-fefa-4be8-9cad-ce8c8c4fe9c1

        data = json.loads(url.read().decode())
        jsonString = json.dumps(data, indent=4)
        jsonFile = open("Match" + str(i) + "Info.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        print("Match" + str(i) + "data fetched!")
    i = i + 1