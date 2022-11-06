#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tuuhiostats downloads PUBG season statistics for a range of 1-10 players, parses and sorts them and
# outputs them to individuals files to be used with Nightbot's urlfetch function. Written for Python 2.7.
#
# Nightbot commands used:
# !commands add !stats -a=!fetch $(eval q=`$(querystring)`.toLowerCase();q)
# !commands add !fetch $(eval `$(urlfetch http://www.YOURSERVER.com/$(query))`)
#
# Copyright (C) ja sen semmoset 2022 BVK. Terveisiä kotiin!

from __future__ import print_function
import json
import sys
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime

# This is the stuff you need to fill up: your API key, season, working directory and the players to be included (10 players maximum. This is a PUBG API limitation. )
authorizationKey = ''
workingDirectory = ''
playerNames = ['BaronVonKale', 'MrSys0p', 'Diizzel', 'Dertti', 'Madfexx', 'Wubsi', 'jezpexx', 'mehumi3s', 'Topsu', 'varjolenkkari']
numberOfPlayers = len(playerNames)
season = 'division.bro.official.pc-2018-20'
lastSeason = 'division.bro.official.pc-2018-19'

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
url = 'https://api.pubg.com/shards/steam/seasons/' + season + '/gameMode/squad-fpp/players?filter[playerIds]=' + urlIds + '&filter[gamepad]=false'

resp = requests.get(url, headers=headers)

# Debug in case of errors getting the JSON data
# print(resp.status_code)
# print(resp.json())

data = resp.json()

# Create the player database
players = {}

for i in range(numberOfPlayers):
    players[(i+1)] = { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'reviveRate' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'timeSurvived' : 0, 'matchesPlayed' : 0, 'headshotPercent' : 0, 'winsToday' : 0, 'killsToday' : 0, 'longestKill' : 0, 'headshotKills' : 0, 'name' : playerNames[i], 'isStreamer' : False, 'lastMatchID' : '' }

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
    players[i+1]['killsToday'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['dailyKills']
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['headshotKills'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['headshotKills']
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['kills'] != 0:
        players[i+1]['headshotPercent'] = round(float(data['data'][i]['attributes']['gameModeStats']['squad-fpp']['headshotKills']) / float(data['data'][i]['attributes']['gameModeStats']['squad-fpp']['kills']) * 100, 2)
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['longestKill'] = round(float(data['data'][i]['attributes']['gameModeStats']['squad-fpp']['longestKill']), 1)
    i += 1

for i in range(0, numberOfPlayers):
    players[i+1]['suicides'] = data['data'][i]['attributes']['gameModeStats']['squad-fpp']['suicides']
    i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['reviveRate'] = 0
    else:  
        players[i+1]['reviveRate'] = round(float(players[i+1]['revives']) / float(players[i+1]['rounds']), 2)  
        i += 1

for i in range(0, numberOfPlayers):
    if players[i+1]['rounds'] == 0:
        players[i+1]['timeSurvived'] = 0
    else:
        players[i+1]['timeSurvived'] = round(float(data['data'][i]['attributes']['gameModeStats']['squad-fpp']['timeSurvived']) / float(players[i+1]['rounds']) / 60, 2)
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
        players[i+1]['score'] = round((float(players[i+1]['kills'] * 10) + float(players[i+1]['headshotKills'] * 2) - float(players[i+1]['suicides'] * 10) + float(players[i+1]['assists'] * 2.5) + float(players[i+1]['dbnos'] * 5) + float(players[i+1]['top10s'] * 5) + float(players[i+1]['totalDmg'] * 0.1) + float(players[i+1]['revives'] * 10) + float(players[i+1]['wins'] * 200) - float(players[i+1]['teamKills'] * 50)) / players[i+1]['rounds'], 1)
    i += 1

# Repeat for previous season
urlLastseason = 'https://api.pubg.com/shards/steam/seasons/' + lastSeason + '/gameMode/squad-fpp/players?filter[playerIds]=' + urlIds + '&filter[gamepad]=false'

respLastseason = requests.get(urlLastseason, headers=headers)

# Debug in case of errors getting the JSON data
# print(resp.status_code)
# print(resp.json())

dataLastseason = respLastseason.json()

# Create the player database
playersLastseason = {}

for i in range(numberOfPlayers):
    playersLastseason[(i+1)] = { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'reviveRate' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'timeSurvived' : 0, 'matchesPlayed' : 0, 'headshotPercent' : 0, 'winsToday' : 0, 'longestKill' : 0, 'headshotKills' : 0, 'name' : playerNames[i], 'isStreamer' : False, 'lastMatchID' : '' }

# Populate PLAYERS dictionary with the season data
for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['deaths'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['losses']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['assists'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['assists']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['teamKills'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['teamKills']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['revives'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['revives']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['kills'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['kills']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['wins'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['wins']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['totalDmg'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['damageDealt']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['rounds'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['roundsPlayed']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['dbnos'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['dBNOs']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['top10s'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['top10s']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['matchesPlayed'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['roundsPlayed']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['winsToday'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['dailyWins']
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['headshotKills'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['headshotKills']
    i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['kills'] != 0:
        playersLastseason[i+1]['headshotPercent'] = round(float(dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['headshotKills']) / float(dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['kills']) * 100, 2)
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['longestKill'] = round(float(dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['longestKill']), 1)
    i += 1

for i in range(0, numberOfPlayers):
    playersLastseason[i+1]['suicides'] = dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['suicides']
    i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['rounds'] == 0:
        playersLastseason[i+1]['reviveRate'] = 0
    else:  
        playersLastseason[i+1]['reviveRate'] = round(float(playersLastseason[i+1]['revives']) / float(playersLastseason[i+1]['rounds']), 2)  
        i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['rounds'] == 0:
        playersLastseason[i+1]['timeSurvived'] = 0
    else:
        playersLastseason[i+1]['timeSurvived'] = round(float(dataLastseason['data'][i]['attributes']['gameModeStats']['squad-fpp']['timeSurvived']) / float(playersLastseason[i+1]['rounds']) / 60, 2)
    i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['rounds'] == 0:
        playersLastseason[i+1]['winrate'] = 0
    else:
        playersLastseason[i+1]['winrate'] = round(float(playersLastseason[i+1]['wins']) / float(playersLastseason[i+1]['rounds']) * 100, 1)
    i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['rounds'] == 0:
        playersLastseason[i+1]['dmg'] = 0
    else:
        playersLastseason[i+1]['dmg'] = int(round(float(playersLastseason[i+1]['totalDmg']) / float(playersLastseason[i+1]['rounds'])))
    i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['rounds'] == 0:
        playersLastseason[i+1]['kd'] = 0
    else:
        playersLastseason[i+1]['kd'] = round(float(playersLastseason[i+1]['kills']) / float(playersLastseason[i+1]['deaths']), 2)
    i += 1

for i in range(0, numberOfPlayers):
    if playersLastseason[i+1]['rounds'] == 0:
        playersLastseason[i+1]['score'] = 0
    else:
        playersLastseason[i+1]['score'] = round((float(playersLastseason[i+1]['kills'] * 10) + float(playersLastseason[i+1]['headshotKills'] * 2) - float(playersLastseason[i+1]['suicides'] * 10) + float(playersLastseason[i+1]['assists'] * 2.5) + float(playersLastseason[i+1]['dbnos'] * 5) + float(playersLastseason[i+1]['top10s'] * 5) + float(playersLastseason[i+1]['totalDmg'] * 0.1) + float(playersLastseason[i+1]['revives'] * 10) + float(playersLastseason[i+1]['wins'] * 200) - float(playersLastseason[i+1]['teamKills'] * 50)) / playersLastseason[i+1]['rounds'], 1)
    i += 1


# Add streamer tags - this is a bit of a crude way of doing it as you have to do it by hand, I'll come up with a better way someday
players[1]['isStreamer'] = True
players[2]['isStreamer'] = True
players[3]['isStreamer'] = True

# Sort players by KD
playersKd = sorted(players.items(), key = lambda x: x[1]['kd'], reverse=True)

# Print KD to KD variable and print them to a file
x = 0
kdOutput = 'KD: '
for i in playersKd:
    if playersKd[x][1]['kd'] != 0:
        kdOutput += str(x+1) +': ' + playersKd[x][1]['name'] + ' ' + str(playersKd[x][1]['kd']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'kd.txt', 'w') as f:
    print(kdOutput, file=f)

# Sort players by revive rate
playersReviveRate = sorted(players.items(), key = lambda x: x[1]['reviveRate'], reverse=True)

# Print revive rate to REVIVERATE variable and print them to a file
x = 0
reviveRateOutput = 'Nostoja per peli: '
for i in playersReviveRate:
    if playersReviveRate[x][1]['reviveRate'] != 0:
        reviveRateOutput += str(x+1) +': ' + playersReviveRate[x][1]['name'] + ' ' + str(playersReviveRate[x][1]['reviveRate']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'reviverate.txt', 'w') as f:
    print(reviveRateOutput, file=f)

# Sort players by damage
playersDmg = sorted(players.items(), key = lambda x: x[1]['dmg'], reverse=True)

# Print damages to DAMAGE variable and print them to a file
x = 0
dmgOutput = 'Damagea per peli: '
for i in playersDmg:
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
winrateOutput = 'Voittoprosentti (voitot): '
for i in playersWinrate:
    if playersWinrate[x][1]['winrate'] != 0:
        winrateOutput += str(x+1) +': ' + playersWinrate[x][1]['name'] + ' ' + str(playersWinrate[x][1]['winrate']) + '% (' + str(playersWinrate[x][1]['wins']) + ') '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'winrate.txt', 'w') as f:
    print(winrateOutput, file=f)

# Sort players by points
playersScore = sorted(players.items(), key = lambda x: x[1]['score'], reverse=True)

# Print points to POINTS variable and print them to a file
x = 0
scoreOutput = 'Pistepörssi: '
for i in playersScore:
    if playersScore[x][1]['score'] != 0:
        scoreOutput += str(x+1) +': ' + playersScore[x][1]['name'] + ' ' + str(playersScore[x][1]['score']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'pisteet.txt', 'w') as f:
    print(scoreOutput, file=f)

# Sort players by longest kill
playersLongestKill = sorted(players.items(), key = lambda x: x[1]['longestKill'], reverse=True)

# Print longest kill to LONGESTKILL variable and print them to a file
x = 0
longestKillOutput = 'Pisin tappo: '
for i in playersLongestKill:
    if playersLongestKill[x][1]['longestKill'] != 0:
        longestKillOutput += str(x+1) +': ' + playersLongestKill[x][1]['name'] + ' ' + str(playersLongestKill[x][1]['longestKill']) + 'm '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'longestkill.txt', 'w') as f:
    print(longestKillOutput, file=f)

# Sort players by suicides
playersSuicides = sorted(players.items(), key = lambda x: x[1]['suicides'], reverse=True)

# Print longest kill to LONGESTKILL variable and print them to a file
x = 0
suicidesOutput = 'YOU FINALLY KILLED YOURSELF: '
for i in playersSuicides:
    if playersSuicides[x][1]['suicides'] != 0:
        suicidesOutput += str(x+1) +': ' + playersSuicides[x][1]['name'] + ' ' + str(playersSuicides[x][1]['suicides']) + ' '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'suicides.txt', 'w') as f:
    print(suicidesOutput, file=f)

# Sort players by headshot percentage
playersheadshotPercent = sorted(players.items(), key = lambda x: x[1]['headshotPercent'], reverse=True)

# Print headshot percentage to headshot variable and print them to a file
x = 0
headshotPercentOutput = 'Heduprosentti: '
for i in playersheadshotPercent:
    if playersheadshotPercent[x][1]['headshotPercent'] != 0:
        headshotPercentOutput += str(x+1) +': ' + playersheadshotPercent[x][1]['name'] + ' ' + str(playersheadshotPercent[x][1]['headshotPercent']) + '% '
        x += 1
    else:
        x += 1

with open(workingDirectory + 'headshots.txt', 'w') as f:
    print(headshotPercentOutput, file=f)    

# Sort players by time survived, reversed
playersSurvived = sorted(players.items(), key = lambda x: x[1]['timeSurvived'])

# Print minutes survived to SURVIVED variable and print them to a file
x = 0
y = 1
survivedOutput = 'Elinajanodote: '
for i in playersSurvived:
    if playersSurvived[x][1]['timeSurvived'] != 0:
        seconds = playersSurvived[x][1]['timeSurvived'] * 60
        minutes, seconds = divmod(seconds, 60)

        survivedOutput += str(y) +': ' + playersSurvived[x][1]['name'] + ' ' + str(int(round(minutes, 0))) + ':' + str(int(round(seconds, 0))) + ' '
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
matchesPlayedOutput = 'Pelejä pelattu: '
for i in playersMatchesPlayed:
    if x < (numberOfPlayers - 1):
        matchesPlayedOutput += playersMatchesPlayed[x][1]['name'] + ' ' + str(playersMatchesPlayed[x][1]['matchesPlayed']) + ', '
        x += 1
    else:
        matchesPlayedOutput += playersMatchesPlayed[x][1]['name'] + ' ' + str(playersMatchesPlayed[x][1]['matchesPlayed'])
        x += 1
with open(workingDirectory + 'matches.txt', 'w') as f:
    print(matchesPlayedOutput, file=f)

# Sort players by teamkills
playersTeamKills = sorted(players.items(), key = lambda x: x[1]['teamKills'], reverse=True)

# Print teamkills to TEAMKILLS variable and print them to a file
x = 0
teamKillsOutput = 'Teamkillit: '
for i in playersTeamKills:
    if playersTeamKills[x][1]['teamKills'] != 0:
        teamKillsOutput += str(x+1) +': ' + str(playersTeamKills[x][1]['name']) + ' ' + str(playersTeamKills[x][1]['teamKills']) + ' '
        x += 1
    else:
        x += 1
with open(workingDirectory + 'teamkills.txt', 'w') as f:
    print(teamKillsOutput, file=f)

# THIS MIGHT NOT WORK
# NO IT ACTUALLY DOES LOL

# Print today's streamer chicken dinners and player stats to individual files (in Finnish, translation is up to you) 
for i in range(0, numberOfPlayers):
    if players[i+1]['isStreamer'] == True and players[i+1]['matchesPlayed'] != 0:
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
            elif wins == 1:
                output = "Yksi kana tänään!"
            elif wins > 1:
                output = str(wins) + ' kanaa tänään!' 
        else:
            output = 'Ei pelejä, ei kanaa :('
        with open(workingDirectory + players[i+1]['name'] + 'wins.txt', 'w') as f:
            print(output, file=f)

        if timeSinceLastMatch.total_seconds() / 3600 - 4 < 16:
            killsToday = players[i+1]['killsToday']
            if killsToday == 0:
                output = 'Illan tappo ei ole vielä tullut.'
            elif killsToday == 1:
                output = "Tappo otettu!"
            elif killsToday > 1:
                output = str(killsToday) + ' tappoa otettu!' 
        else:
            output = 'Ei pelejä, ei tappoja :('
        with open(workingDirectory + players[i+1]['name'] + 'killsToday.txt', 'w') as f:
            print(output, file=f)

    # Get the differences from the previous season and print them
    scoreDifference = 0
    kdDifference = 0
    winrateDifference = 0

    if players[i+1]['score'] >= playersLastseason[i+1]['score']:
        scoreDifference = "+" + str((players[i+1]['score'] - playersLastseason[i+1]['score']))
    else:
        scoreDifference = str((players[i+1]['score'] - playersLastseason[i+1]['score']))   

    if players[i+1]['kd'] >= playersLastseason[i+1]['kd']:
        kdDifference = "+" + str((players[i+1]['kd'] - playersLastseason[i+1]['kd']))
    else:
        kdDifference = str((players[i+1]['kd'] - playersLastseason[i+1]['kd']))  

    if players[i+1]['winrate'] >= playersLastseason[i+1]['winrate']:
        winrateDifference = "+" + str((players[i+1]['winrate'] - playersLastseason[i+1]['winrate']))
    else:
        winrateDifference = str((players[i+1]['winrate'] - playersLastseason[i+1]['winrate']))  

    output = players[i+1]['name'] + ': Pisteet ' + str(players[i+1]['score']) + ' (' + str(scoreDifference) + ')' + ', KD ' + str(players[i+1]['kd']) + ' (' + str(kdDifference) + ')' + ', voittoprosentti ' + str(players[i+1]['winrate']) + '%' + ' (' + str(winrateDifference) + '%)'
    with open(workingDirectory + players[i+1]['name'].lower(), 'w') as f:
            print(output, file=f)