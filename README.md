# Storyline Visualisation for League of Legends (LoL) Matches JSON Fetch

![storylines](https://i.postimg.cc/pL21zGDM/Legend.jpg)

The Python project is a prerequisite for fetching and generating
relevant storyline JSON file to feed the iStoryline Visualisation
Web App.

## Python Pipeline of Fetching Data

1. Get your RIOT API key from [here](https://developer.riotgames.com/).
2. Open the `main.py` file and replace the `api` variable with your RIOT API key.
3. Find out a player's puuid and fill in the `puuid` variable in `main.py`.
4. Run `python main.py` to get the most recent matches from the player.
5. Run `python analyze_G.python` to get each player's geo-time data.
6. Run `python trajectory_G.py` to aggregate the above 10 players' data and generate the storyline JSON file.
7. Run `python battle-extractor2.py` to get the DBSCAN data and generate the DBSCAN JSON file.
8. Run `python count1.py` to get the killing events information and generate the killingInfo JSON file.

## Notes

LoLBaseMap png files are different divisions of LoL Map.

Match and Match info Json files are some examples which you could get from the API. Match json file contains the timestamp events etc. the match INFO json contains its match ID and the player info for that match.

In this project, we used ST_DBCSCAN to cluster the killing events and generate the DBSCAN JSON file.

As such, to display a complete visualization, you will need:
- a match base information (directly fetched from Riot, this contains participants info for that match, screenshot 1)
- timeline json (generated by python) info here such as timestamp, position, killtype, etc. were from different Match json file
- ST-DBSCAN results

## Example of JSON file

The JSON examples below are app-readable. This python project aims to generate such JSON files.

There are three types of information to generate:

1. The Storyline Layout

The Json file is a dictionary with two keys: Locations and Characters.
Locations is a dictionary with keys as the location names and values as the location IDs.
Characters is a dictionary with keys as the character names (in our case, the player) and values as a list of dictionaries.
Each dictionary in the list contains the start and end timestamp of the character's appearance in the storyline.
The session number is used to distinguish the different locations of the same character.

```JSON
{
  "Story": {
    "Locations": {
      "BlueBase": [1],
      "MidLane": [2],
      "RedBase": [3]
    },
    "Characters": {
      "Player1": [
        {
          "Start": 1,
          "End": 5,
          "Session": 1
        },
        {
          "Start": 5,
          "End": 6,
          "Session": 2
        }
      ],
      "Player2/3/4/5/6...": [
        {
          "Start": 1,
          "End": 5,
          "Session": 1
        }
      ]
    }
  }
}
```

2. Killing Events Information
   The JSON file below is a list of dictionaries.
   Each dictionary contains the timestamp, killer ID, killer name, victim ID, victim name, position, and kill type.

```JSON
[
  {
    "timestamp": 119026,
    "killerID": 4,
    "killerName": "Gangplank",
    "victimID": 7,
    "victimName": "Diana",
    "position": {
      "x": 6774,
      "y": 7281
    },
    "killType": "CHAMPION_KILL"
  },
  {
    "timestamp": 147897,
    "killerID": 8,
    "killerName": "Seraphine",
    "victimID": 4,
    "victimName": "Gangplank",
    "position": {
      "x": 6108,
      "y": 6264
    },
    "killType": "CHAMPION_KILL"
  }
]
```

3. The DBSCAN Result
   The JSON file below is a list of dictionaries.
   Each dictionary contains the label, timestamp, and player.
   Labels were clustered by player killing events at the adjacent timestamp and location.

```JSON
[
  {
    "label": 0,
    "timestamp": 214564,
    "player": "Player5"
  },
  {
    "label": 0,
    "timestamp": 217801,
    "player": "Player2"
  }
]
```

## Import the Output File to the Storyline Visualisation

Now we already have the storyline JSON file. We can then import the file to the storyline visualisation.

Please check details from the GitHub repo: [Storyline Visualisation for LoL Matches](https://github.com/tiange997/iStoryline.js).
