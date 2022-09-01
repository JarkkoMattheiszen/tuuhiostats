#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tuuhiostats downloads PUBG season statistics for a range of 1-10 players, parses and sorts them and
# outputs them to individuals files to be used with Nightbot's urlfetch function. Written for Python 2.7.
#
# Use !commands add !command $(urlfetch https://yourserver/path/file) with Nightbot
#
# Copyright (C) ja sen semmoset 2022 BVK. Terveisiä kotiin!

from __future__ import print_function
import json
import sys
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime

# This is the stuff you need to fill up: your API key, working directory and the players to be included (10 players maximum. This is a PUBG API limitation. )
authorizationKey = ''
workingDirectory = ''
playerNames = ['BaronVonKale', 'MrSys0p', 'Diizzel', 'Dertti', 'Madfexx', 'Wubsi', 'jezpexx', 'mehumi3s', 'Topsu', 'Rikama']
numberOfPlayers = len(playerNames)

# Form the URL to get player ID's from PUBG API
urlNames = ''

x = 0
for i in range(numberOfPlayers):
    if x < (numberOfPlayers - 1):
        urlNames += playerNames[i] + '%2C'
        x += 1
    else:
        urlNames += playerNames[i]
        x += 1

# Get the player ID's from PUBG server and store them to a dictionary
url = 'https://api.pubg.com/shards/steam/players?filter[playerNames]=' + urlNames

headers = CaseInsensitiveDict()
headers['accept'] = 'application/vnd.api+json'
headers['Authorization'] = 'Bearer ' + authorizationKey

resp = requests.get(url, headers=headers)

data = resp.json()

urlIds = ''

# Form the URL to get the player stats from PUBG API
x = 0
for i in range(numberOfPlayers):
    if x < (numberOfPlayers - 1):
        urlIds += data['data'][i]['id'] + '%2C'
        x += 1
    else:
        urlIds += data['data'][i]['id']
        x += 1

# Download the stats as JSON and store them to a dictionary
# Change platform shard, season, gamemode and if needed gamepad filter
url = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-19/gameMode/squad-fpp/players?filter[playerIds]=' + urlIds + '&filter[gamepad]=false'

resp = requests.get(url, headers=headers)

# Debug in case of errors getting the JSON data
# print(resp.status_code)
# print(resp.json())

data = resp.json()

# Create the player database
players = {}

for i in range(numberOfPlayers):
    players[(i+1)] = { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'timeSurvived' : 0, 'matchesPlayed' : 0, 'winsToday' : 0, 'name' : playerNames[i], 'isStreamer' : False, 'lastMatchID' : '' }

# Populate PLAYERS dictionary with the season data
for i in range(0, numberOfPlayers):
    players[i+1]['deaths'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['losses']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['assists'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['assists']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['teamKills'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['teamKills']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['revives'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['revives']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['kills'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['kills']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['wins'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['wins']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['totalDmg'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['damageDealt']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['rounds'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['roundsPlayed']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['dbnos'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['dBNOs']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['top10s'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['top10s']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['matchesPlayed'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['roundsPlayed']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['winsToday'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['dailyWins']
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['timeSurvived'] = 0
    else:
        players[i+1]['timeSurvived'] = round(float(data['data'][i]['attributes']['gameModeStats']['squad-fpp']['timeSurvived']) / float(players[i+1]['rounds']) / 60, 1)
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['winrate'] = 0
    else:
        players[i+1]['winrate'] = round(float(players[i+1]['wins']) / float(players[i+1]['rounds']) * 100, 1)
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['dmg'] = 0
    else:
        players[i+1]['dmg'] = int(round(float(players[i+1]['totalDmg']) / float(players[i+1]['rounds'])))
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['kd'] = 0
    else:
        players[i+1]['kd'] = round(float(players[i+1]['kills']) / float(players[i+1]['deaths']), 2)
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['score'] = 0
    else:
        players[i+1]['score'] = round((float(players[i+1]['kills'] / 10) + float(players[i+1]['assists'] / 40) + float(players[i+1]['dbnos'] / 20) + float(players[i+1]['top10s'] / 20) + float(players[i+1]['totalDmg'] / 1000) + float(players[i+1]['revives'] / 10) + float(players[i+1]['wins'] * 2) - float(players[i+1]['teamKills'] / 2)) * 100 / players[i+1]['rounds'], 1)
    i += 1

# Add streamer tags - this is a bit of a crude way of doing it as you have to do it by hand, I'll come up with a better way someday
players[1]['isStreamer'] = True
players[2]['isStreamer'] = True
players[3]['isStreamer'] = True

# Sort players by KD
playersKd = sorted(players.items(), key = lambda x: x[1]['kd'], reverse=True)

# Print all stats to STATS variable and print them to a file
x = 0
statsOutput = ''
for i in playersKd:
    statsOutput += str(x+1) +': ' + playersKd[x][1]['name'] + ' ' + str(playersKd[x][1]['kd']) + ' kd, ' + str(playersKd[x][1]['dmg']) + ' dmg, ' + str(playersKd[x][1]['winrate']) + ' winrate. '
    x += 1

with open(workingDirectory + 'stats.txt', 'w') as f:
    print(statsOutput, file=f)

# Print KD to KD variable and print them to a file
x = 0
kdOutput = ''
for i in playersKd:
    if playersKd[x][1]['kd'] != 0:
        kdOutput += str(x+1) +': ' + playersKd[x][1]['name'] + ' ' + str(playersKd[x][1]['kd']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'kd.txt', 'w') as f:
    print(kdOutput, file=f)

# Sort players by damage
playersDmg = sorted(players.items(), key = lambda x: x[1]['dmg'], reverse=True)

# Print damages to DAMAGE variable and print them to a file
x = 0
dmgOutput = ''
for i in playersKd:
    if playersDmg[x][1]['dmg'] != 0:
        dmgOutput += str(x+1) +': ' + playersDmg[x][1]['name'] + ' ' + str(playersDmg[x][1]['dmg']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'damage.txt', 'w') as f:
    print(dmgOutput, file=f)

# Sort players by winning rate
playersWinrate = sorted(players.items(), key = lambda x: x[1]['winrate'], reverse=True)

# Print winning rate to WINRATE variable and print them to a file
x = 0
winrateOutput = ''
for i in playersKd:
    if playersWinrate[x][1]['winrate'] != 0:
        winrateOutput += str(x+1) +': ' + playersWinrate[x][1]['name'] + ' ' + str(playersWinrate[x][1]['winrate']) + '% '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'winrate.txt', 'w') as f:
    print(winrateOutput, file=f)

# Sort players by points
playersScore = sorted(players.items(), key = lambda x: x[1]['score'], reverse=True)

# Print points to POINTS variable and print them to a file
x = 0
scoreOutput = ''
for i in playersKd:
    if playersScore[x][1]['score'] != 0:
        scoreOutput += str(x+1) +': ' + playersScore[x][1]['name'] + ' ' + str(playersScore[x][1]['score']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'pisteet.txt', 'w') as f:
    print(scoreOutput, file=f)

# Sort players by time survived, reversed
playersSurvived = sorted(players.items(), key = lambda x: x[1]['timeSurvived'])

# Print minutes survived to SURVIVED variable and print them to a file
x = 0
y = 1
survivedOutput = ''
for i in playersKd:
    if playersSurvived[x][1]['timeSurvived'] != 0:
        survivedOutput += str(y) +': ' + playersSurvived[x][1]['name'] + ' ' + str(playersSurvived[x][1]['timeSurvived']) + 'min '
        x += 1
        y += 1
    else:
        x += 1

with open(workingDirectory + 'survived.txt', 'w') as f:
    print(survivedOutput, file=f)

# Sort players by matches played
playersMatchesPlayed = sorted(players.items(), key = lambda x: x[1]['matchesPlayed'], reverse=True)

# Print matches played to MATCHES variable and print them to a file
x = 0
matchesPlayedOutput = ''
for i in playersMatchesPlayed:
    if x < (numberOfPlayers - 1):
        matchesPlayedOutput += playersMatchesPlayed[x][1]['name'] + ' ' + str(playersMatchesPlayed[x][1]['matchesPlayed']) + ', '
        x += 1
    else:
        matchesPlayedOutput += playersMatchesPlayed[x][1]['name'] + ' ' + str(playersMatchesPlayed[x][1]['matchesPlayed'])
        x += 1

with open(workingDirectory + 'matches.txt', 'w') as f:
    print(matchesPlayedOutput, file=f)

# THIS MIGHT NOT WORK
# NO IT ACTUALLY DOES LOL

# Print today's streamer chicken dinners to individual files (in Finnish, translation is up to you)
for i in range(0, numberOfPlayers):
    if players[i+1]['isStreamer'] == True:
        output = ''
        players[i+1]['lastMatchID'] = data['data'][i]['relationships']['matchesSquadFPP']['data'][0]['id']

        url = 'https://api.pubg.com/shards/steam/matches/' + players[i+1]['lastMatchID']

        resp = requests.get(url, headers=headers)

        data2 = resp.json()

        lastMatchDate = data2['data']['attributes']['createdAt']
        lastMatchToDate = lastMatchDate[0:10] + ' ' + lastMatchDate[11:16]
        dt1 = datetime.strptime(lastMatchToDate, "%Y-%m-%d %H:%M")
        timeSinceLastMatch = datetime.now() - dt1

        # The 4 is compensating the time difference to PUBG API server, adjust as needed
        if timeSinceLastMatch.total_seconds() / 3600 - 4 < 16:
            wins = players[i+1]['winsToday']
            if wins == 0:
                output = 'Ei kanaa tänään :('
            if wins == 1:
                output = "Yksi kana tänään!"
            else:
                output = str(wins) + ' kanaa tänään!' 
        else:
            output = 'Ei pelejä, ei kanaa :('
        with open(workingDirectory + players[i+1]['name'] + 'wins.txt', 'w') as f:
            print(output, file=f)
