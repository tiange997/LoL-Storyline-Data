import json

from PIL import Image

f = open('Match3Info.json')

data = json.load(f)

participantsInfo = data['info']['participants']

heroList = {}
heroInfo = []

print(participantsInfo)

for i in range(len(participantsInfo)):
    elem = {'participantId': participantsInfo[i]['participantId'], 'championId': participantsInfo[i]['championId'],
            'championName': participantsInfo[i]['championName']}
    #print(elem)
    heroInfo.append(elem)

def findName(id):
    for item in participantsInfo:
        if id == item['participantId']:
            # print(item['championName'])
            return item['championName']

def addInfo():
    try:
        for x in heroInfo:
            if x["participantId"] == temp_eventList[j]['killerId']:
                elem = {'timestamp': temp_eventList[j]['timestamp'],
                        'killerID': temp_eventList[j]['killerId'],
                        'killerName': x['championName'],
                        'victimID': temp_eventList[j]['victimId'],
                        'victimName': findName(temp_eventList[j]['victimId']),
                        'position': temp_eventList[j]['position'],
                        # 'placeIndex': getArea(temp_eventList[j]['position']['x']/15000, temp_eventList[j]['position']['y']/15000),
                        'killType': temp_eventList[j]['type']}
                # print(elem)
                CHAMPION_KILL_INFO.append(elem)
    except KeyError:
        for x in heroInfo:
            if x["participantId"] == temp_eventList[j]['killerId']:
                elem = {'timestamp': temp_eventList[j]['timestamp'],
                        'killerID': temp_eventList[j]['killerId'],
                        'killerName': x['championName'],
                        'position': temp_eventList[j]['position'],
                        # 'placeIndex': getArea(temp_eventList[j]['position']['x']/15000, temp_eventList[j]['position']['y']/15000),
                        'killType': temp_eventList[j]['type']}
                # print(elem)
                CHAMPION_KILL_INFO.append(elem)
                print(temp_eventList[j]['position']['x'], temp_eventList[j]['position']['y'])

f.close()

f = open('RichardData/Match3.json')
data = json.load(f)

info = data['info']

frames = data["info"]["frames"]

p_frames = []

# set the counter
CHAMPION_KILL = 0
CHAMPION_SPECIAL_KILL = 0
ELITE_MONSTER_KILL = 0
BUILDING_KILL = 0

CHAMPION_KILL_INFO = []
CHAMPION_SPECIAL_KILL_INFO = []
ELITE_MONSTER_KILL_INFO = []
BUILDING_KILL_INFO = []

for i in range(len(frames)):
    temp_eventList = frames[i]['events']
    # print(len(temp_eventList))
    for j in range(len(temp_eventList)):
        if temp_eventList[j]['type'] == "CHAMPION_KILL":
            CHAMPION_KILL = CHAMPION_KILL + 1
            addInfo()

        # if temp_eventList[j]['type'] == "CHAMPION_SPECIAL_KILL":
        #     CHAMPION_SPECIAL_KILL = CHAMPION_SPECIAL_KILL + 1
        #     addInfo()

        # if temp_eventList[j]['type'] == "ELITE_MONSTER_KILL":
        #     ELITE_MONSTER_KILL = ELITE_MONSTER_KILL + 1
        #     addInfo()
        #
        if temp_eventList[j]['type'] == "BUILDING_KILL":
            BUILDING_KILL = ELITE_MONSTER_KILL + 1
            if 'towerType' in temp_eventList[j]:
                elem = {'timestamp': temp_eventList[j]['timestamp'],
                        'killerId': temp_eventList[j]['killerId'],
                        'towerType': temp_eventList[j]['towerType'],
                        'laneType': temp_eventList[j]['laneType'],
                        'position': temp_eventList[j]['position'],
                        'buildingType': temp_eventList[j]['buildingType'],
                        # 'placeIndex': getArea(temp_eventList[j]['position']['x'] / 15000,
                        #                       temp_eventList[j]['position']['y'] / 15000),
                        'killType': 'BUILDING_KILL'}
                # print(elem)
                CHAMPION_KILL_INFO.append(elem)
            else:
                elem = {'timestamp': temp_eventList[j]['timestamp'],
                        'killerId': temp_eventList[j]['killerId'],
                        'laneType': temp_eventList[j]['laneType'],
                        'position': temp_eventList[j]['position'],
                        'buildingType': temp_eventList[j]['buildingType'],
                        # 'placeIndex': getArea(temp_eventList[j]['position']['x'] / 15000,
                        #                       temp_eventList[j]['position']['y'] / 15000),
                        'killType': 'BUILDING_KILL'}
                # print(elem)
                CHAMPION_KILL_INFO.append(elem)

        # try:
        #     if temp_eventList[j]['towerType']:
        #         BUILDING_KILL_INFO.append(temp_eventList[j]['towerType'])
        #     if temp_eventList[j]['buildingType']:
        #         BUILDING_KILL_INFO.append(temp_eventList[j]['towerType'])
        # except KeyError:
        #     continue

print("CHAMPION_KILL: " + str(CHAMPION_KILL))
# print("CHAMPION_SPECIAL_KILL: " + str(CHAMPION_SPECIAL_KILL))
# print("ELITE_MONSTER_KILL: " + str(ELITE_MONSTER_KILL))
print("BUILDING_KILL: " + str(BUILDING_KILL))
#
# print("CHAMPION_KILL_INFO: ")
# print(CHAMPION_KILL_INFO)
#
# print("CHAMPION_SPECIAL_KILL_INFO: ")
# print(CHAMPION_SPECIAL_KILL_INFO)
#
# print("ELITE_MONSTER_KILL_INFO: ")
# print(ELITE_MONSTER_KILL_INFO)
#
# print("BUILDING_KILL_INFO: ")
# print(BUILDING_KILL_INFO)

CHAMPION_KILL_INFO.sort(key=lambda x: x["timestamp"])

jsonString = json.dumps(CHAMPION_KILL_INFO, indent=4)
jsonFile = open("Results/killingInfo.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

print("CHAMPION_KILL_INFO Json File generated, please check.")