import json
import copy
from PIL import Image

import pprint

# load the replay file
f = open('Match3.json')
data = json.load(f)

usePlateau = True
# useMode 0 - simple, 1 - Simple(7), 2 - Complex
useMode = 1

death_offset = 2500
respawn_offset = 1000

# mapping  of colors to areas
colorToArea = None
areaImage = None

if useMode == 0:
    areaImage = Image.open('LoLBaseMap2.png')
    colorToArea = {(0, 51, 153): 'BlueBase',
               (153, 255, 255): 'BottomLane',
               (255, 255, 255): 'MidLane',
               (102, 102, 255): 'Jungle',
               (0, 255, 0): 'TopLane',
               (255, 153, 204): 'PurpleBase',
               }
elif useMode == 1:
    areaImage = Image.open('LoLBaseMap3.png')
    colorToArea = {(0, 51, 153): 'BlueBase',
                   (153, 255, 255): 'BottomLane',
                   (255, 255, 255): 'MidLane',
                   (71, 121, 234): 'TopJungle',
                   (102, 102, 255): 'BottomJungle',
                   (101, 101, 254): 'BottomJungle',
                   (0, 255, 0): 'TopLane',
                   (255, 153, 204): 'PurpleBase',
                   }
else:
    areaImage = Image.open('LoLBaseMap1.png')
    colorToArea = {(0, 51, 153): 'BlueBase',
               (204, 204, 255): 'BlueTopLane',
               (102, 102, 255): 'TopBlueJungle',
               (255, 255, 255): 'BlueMiddleLane',
               (51, 102, 153): 'BottomRedJungle',
               (153, 255, 255): 'BlueBottomLane',
               (0, 0, 255): 'ContestedTop',
               (102, 153, 255): 'TopRiver',
               (128, 128, 128): 'ContestedMiddle',
               (0, 255, 255): 'BottomRiver',
               (51, 153, 102): 'ContestedBottom',
               (0, 255, 0): 'PurpleTopLane',
               (153, 153, 255): 'TopRedJungle',
               (220, 121, 0): 'PurpleMiddleLane',
               (255, 255, 0): 'BottomBlueJungle',
               (153, 0, 204): 'PurpleBottomLane',
               (255, 153, 204): 'PurpleBase',
               }


# returns the name of the area at position (x,y)
# x, y are between 0...1
def getAreaName(x, y):
    width, height = areaImage.size
    x = (int)(x * width)
    y = (int)(height - y * height)
    if useMode == 0 or useMode == 1:
        r, g, b = areaImage.getpixel((x, y))
    else:
        r, g, b, a = areaImage.getpixel((x, y))

    area = colorToArea[(r, g, b)]

    return area

# delete events whose timestamp is between time1 and time2
def deleteEventsInTimeSpan(events, time1, time2):
    indicesToDelete = []
    for i in range(len(events)):
        if events[i]['timestamp'] > time1 and events[i]['timestamp'] < time2:
            indicesToDelete.append(i)

    for i in indicesToDelete:
        del events[i]


# extract the frames (representing ~1min intervalls)
info = data['info']
frames = data["info"]["frames"]


# adds position and timestamp information to the current player
def add_Info():
    PlayerPosTime.append(eventsWithPos[i]['position'])
    PlayerTime.append(eventsWithPos[i]['timestamp'])


currentPlayerID = 0

# loop through the 10 players
for p in range(1,11):
    currentPlayerID = p

    events = []         # list of events
    timelineInfo = []   # This list will include objects with x position, y position, timestamp

    # TRAJECTORY
    # Get Player's position and timestamps from the frames
    for i in range(len(frames)):
        timelineInfo.append(frames[i]["participantFrames"][str(currentPlayerID)]["position"])
        timelineInfo[i]['timestamp'] = frames[i]["timestamp"]

        # Loop and Save the event list
        events.append(frames[i]['events'])

    eventsWithPos = []

    # EVENTS
    # Looping through events, find position, timestamp etc.
    for i in range(len(events)):
        for j in range(len(events[i])):

            # CODE UPDATE BELOW // we need also to add the player's position as a killer
            if events[i][j]['type'] == "CHAMPION_KILL" and events[i][j]['killerId'] == currentPlayerID:
                eventsWithPos.append(events[i][j])
            # CODE UPDATE ABOVE

            # if events[i][j]['type'] == "BUILDING_KILL" and events[i][j]['killerId'] == currentPlayerID:
            #     eventsWithPos.append(events[i][j])
            elif events[i][j]['type'] == "ELITE_MONSTER_KILL" and events[i][j]['killerId'] == currentPlayerID:
                eventsWithPos.append(events[i][j])
            elif events[i][j]['type'] == "TURRET_PLATE_DESTROYED" and events[i][j]['killerId'] == currentPlayerID:
                eventsWithPos.append(events[i][j])

            # CHAMPION_SPECIAL_KILL                                 ignored because of being only extra information about CHAMPION_KILL
            # ITEM_SOLD, ITEM_PURCHASED, ITEM_UNDO, ITEM_DESTROYED  ignored because of no position
            # PAUSE_END, GAME_END                                   ignored because of no position
            # SKILL_LEVEL_UP, LEVEL_UP                              ignored because of no position
            # WARD_PLACED, WARD_KILL                                ignored because of no position

    PlayerPosTime = []                  # list of coordinates
    PlayerTime = []                     # list of timestamps

    for i in range(len(events)):
        for j in range(len(events[i])):
            if events[i][j]['type'] == "CHAMPION_KILL" and events[i][j]['victimId'] == currentPlayerID:
                if not usePlateau:
                    PlayerPosTime.append({'x': events[i][j]['position']['x'], 'y': events[i][j]['position']['y']})
                    time1 = events[i][j]['timestamp']
                    PlayerTime.append(time1)
                    print("playerID = " + str(currentPlayerID) + " time = " + str(events[i][j]['timestamp']))
                else:
                    time = events[i][j]['timestamp']
                    time1 = time - death_offset
                    time2 = time + death_offset
                    copy1 = copy.copy(events[i][j])
                    copy2 = copy.copy(events[i][j])
                    copy1['timestamp'] = time1
                    copy2['timestamp'] = time2

                    # delete events within the plateau
                    deleteEventsInTimeSpan(eventsWithPos, time1, time2)     # eventWithPos does not include CHAMPION_KILL events
                    deleteEventsInTimeSpan(timelineInfo, time1, time2)      # timelineInfo at this point only contains trajectory

                    # add plateau
                    PlayerPosTime.append({'x': events[i][j]['position']['x'], 'y': events[i][j]['position']['y']})
                    PlayerTime.append(time1)

                    PlayerPosTime.append({'x': events[i][j]['position']['x'], 'y': events[i][j]['position']['y']})
                    PlayerTime.append(time2)

                    # go back to base (respawn)
                    if currentPlayerID <= 5:
                        PlayerPosTime.append({'x': 5, 'y': 5})            # blue team
                    else:
                        PlayerPosTime.append({'x': 14900, 'y': 14900})    # red team

                    newtime = time2 + respawn_offset
                    PlayerTime.append(newtime)

                    # debug output
                    victimID = events[i][j]['victimId']
                    x = events[i][j]['position']['x']
                    y = events[i][j]['position']['y']
                    area = getAreaName(x / 15000, y / 15000)

                    print("playerID = " + str(victimID) + " area = " + area + " time = " + str(time1) + "- D")
                    print("playerID = " + str(victimID) + " area = " + area + " time = " + str(time) + "< D")
                    print("playerID = " + str(victimID) + " area = " + area + " time = " + str(time2) + "+ D")
            if events[i][j]['type'] == "BUILDING_KILL" and events[i][j]['killerId'] == currentPlayerID:
                if not usePlateau:
                    PlayerPosTime.append({'x': events[i][j]['position']['x'], 'y': events[i][j]['position']['y']})
                    time = events[i][j]['timestamp']
                    PlayerTime.append(time1)
                    print("playerID = " + str(currentPlayerID) + " time = " + str(events[i][j]['timestamp']))
                else:
                    time = events[i][j]['timestamp']
                    time1 = time - death_offset
                    time2 = time + death_offset
                    copy1 = copy.copy(events[i][j])
                    copy2 = copy.copy(events[i][j])
                    copy1['timestamp'] = time1
                    copy2['timestamp'] = time2

                    # delete events within the plateau
                    deleteEventsInTimeSpan(eventsWithPos, time1, time2)     # eventWithPos does not include CHAMPION_KILL events
                    deleteEventsInTimeSpan(timelineInfo, time1, time2)      # timelineInfo at this point only contains trajectory

                    # add plateau
                    PlayerPosTime.append({'x': events[i][j]['position']['x'], 'y': events[i][j]['position']['y']})
                    PlayerTime.append(time1)

                    PlayerPosTime.append({'x': events[i][j]['position']['x'], 'y': events[i][j]['position']['y']})
                    PlayerTime.append(time2)

                    # debug output
                    killerId = events[i][j]['killerId']
                    x = events[i][j]['position']['x']
                    y = events[i][j]['position']['y']
                    area = getAreaName(x / 15000, y / 15000)

                    print("playerID = " + str(killerId) + " area = " + area + " time = " + str(time1) + "- D")
                    print("playerID = " + str(killerId) + " area = " + area + " time = " + str(time) + "< D")
                    print("playerID = " + str(killerId) + " area = " + area + " time = " + str(time2) + "+ D")

    # Find out the timestamp and position info when any events happened to the player
    for i in range(len(eventsWithPos)):
        try:
            # BUILDING_KILL, ELITE_MONSTER_KILL, TURRET_PLATE_DESTROYED events
            if eventsWithPos[i]['killerId'] == currentPlayerID:
                add_Info()
                continue

            # CHAMPION_KILL events are handled directly above
        except KeyError:
            pass

    # Cleaning the data
    for i in range(len(PlayerPosTime)):
        PlayerPosTime[i]['timestamp'] = PlayerTime[i]

    # Insert the players position and time into timelineInfo
    for i in range(len(PlayerPosTime)):
        timelineInfo.append(PlayerPosTime[i])

    print(timelineInfo)

    # Ordering it based on the timestamp
    timelineInfo.sort(key=lambda x: x['timestamp'])

    print(timelineInfo)

    # export of player data to JSON file
    jsonString = json.dumps(timelineInfo)
    jsonFile = open("Results/Player" + str(currentPlayerID) + ".json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
