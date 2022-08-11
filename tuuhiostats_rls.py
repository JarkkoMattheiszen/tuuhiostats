#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tuuhiostats downloads PUBG season statistics for a range of 1-10 players, parses and sorts them and
# outputs them to individuals files to be used with Nightbot's urlfetch function
#
# Use !commands add !command $(urlfetch https://yourserver/path/file) with Nightbot
#
# Copyright (C) ja sen semmoset herran vuonna 2022 BaronVonKale, terveisiä kotiin

from __future__ import print_function
import json
import sys
import requests
from requests.structures import CaseInsensitiveDict

# Download the stats as JSON, replace with the URL and headers you get PUBG Developer Portal
# Change platform shard, season, gamemode, player ID's, and if needed gamepad filter
url = 'https://api.pubg.com/shards/steam/seasons/division.bro.official.pc-2018-19/gameMode/squad-fpp/players?filter[playerIds]=PLAYER_IDS_HERE&filter[gamepad]=false'

# Authorization data for the PUBG server, swap the authorization key with your PUBG Developer API key
headers = CaseInsensitiveDict()
headers['accept'] = 'application/vnd.api+json'
headers['Authorization'] = 'Bearer YOUR_API_KEY_HERE'

resp = requests.get(url, headers=headers)

# Debug in case of errors getting the JSON data
# print(resp.status_code)
# print(resp.json())

# Store the JSON data as a new dictionary
data = resp.json()

# Get wins in the last 24 hours for the streamers
wins_streamer1 = data['data'][0]['attributes']['gameModeStats']['squad-fpp']['dailyWins']
wins_streamer2 = data['data'][1]['attributes']['gameModeStats']['squad-fpp']['dailyWins']
wins_streamer3 = data['data'][2]['attributes']['gameModeStats']['squad-fpp']['dailyWins']

# Define the players
players = {
    1 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'streamer1' },
    2 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'streamer2' },
    3 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'streamer3' },
    4 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player4' },
    5 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player5' },
    6 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player6' },
    7 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player7' },
    8 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player8' },
    9 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player9 '},
    10 : { 'kd' : 0, 'dmg' : 0, 'winrate' : 0, 'kills' : 0, 'wins' : 0, 'totalDmg' : 0, 'assists' : 0, 'teamKills' : 0, 'score' : 0, 'revives' : 0, 'rounds' : 0, 'deaths' : 0, 'dbnos' : 0, 'top10s' : 0, 'name' : 'player10' }
}

numberOfPlayers = len(players.keys())

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

# Sort players by KD
playersKd = sorted(players.items(), key = lambda x: x[1]['kd'], reverse=True)

# Print all stats to STATS variable and print them to a file
x = 0
statsOutput = ''
for i in playersKd:
    statsOutput += str(x+1) +': ' + playersKd[x][1]['name'] + ' ' + str(playersKd[x][1]['kd']) + ' kd, ' + str(playersKd[x][1]['dmg']) + ' dmg, ' + str(playersKd[x][1]['winrate']) + ' winrate. '
    x += 1

with open('homedirectory/stats', 'w') as f:
    print(statsOutput, file=f)

# Print KD to KD variable and print them to a file
x = 0
kdOutput = ''
for i in playersKd:
    kdOutput += str(x+1) +': ' + playersKd[x][1]['name'] + ' ' + str(playersKd[x][1]['kd']) + ' '
    x += 1

with open('homedirectory/kd', 'w') as f:
    print(kdOutput, file=f)

# Sort players by damage
playersDmg = sorted(players.items(), key = lambda x: x[1]['dmg'], reverse=True)

# Print damages to DAMAGE variable and print them to a file
x = 0
dmgOutput = ''
for i in playersKd:
     dmgOutput += str(x+1) +': ' + playersDmg[x][1]['name'] + ' ' + str(playersDmg[x][1]['dmg']) + ' '
     x += 1

with open('homedirectory/damage', 'w') as f:
    print(dmgOutput, file=f)

# Sort players by winning rate
playersWinrate = sorted(players.items(), key = lambda x: x[1]['winrate'], reverse=True)

# Print winning rate to WINRATE variable and print them to a file
x = 0
winrateOutput = ''
for i in playersKd:
    winrateOutput += str(x+1) +': ' + playersWinrate[x][1]['name'] + ' ' + str(playersWinrate[x][1]['winrate']) + '% '
    x += 1

with open('homedirectory/winrate', 'w') as f:
    print(winrateOutput, file=f)

# Sort players by points
playersscore= sorted(players.items(), key = lambda x: x[1]['score'], reverse=True)

# Print points to POINTS variable and print them to a file
x = 0
scoreOutput = ''
for i in playersKd:
    scoreOutput += str(x+1) +': ' + playersscore[x][1]['name'] + ' ' + str(playersscore[x][1]['score']) + ' '
    x += 1

with open('homedirectory/score', 'w') as f:
    print(scoreOutput, file=f)

# Print today's streamer chicken dinners to a file
wins_streamer1_output = ''
if wins_streamer1 == 0:
    wins_streamer1_output = 'No chicken dinners tonight.'
if wins_streamer1 == 1:
    wins_streamer1_output = 'One chicken dinner tonight!'
if wins_streamer1 > 1:
    wins_streamer1_output = str(wins_streamer1) + ' chicken dinners tonight!'

with open('homedirectory/streamer1wins', 'w') as f:
    print(wins_streamer1_output, file=f)

wins_streamer2_output = ''
if wins_streamer2 == 0:
    wins_streamer2_output = 'No chicken dinners tonight.'
if wins_streamer2 == 1:
    wins_streamer2_output = 'One chicken dinner tonight!'
if wins_streamer2 > 1:
    wins_streamer2_output = str(wins_streamer2) + ' chicken dinners tonight!'

with open('homedirectory/streamer2wins', 'w') as f:
    print(wins_streamer2_output, file=f)

wins_streamer3_output = ''
if wins_streamer3 == 0:
    wins_streamer3_output = 'No chicken dinners tonight.'
if wins_streamer3 == 1:
    wins_streamer3_output = 'One chicken dinner tonight!'
if wins_streamer3 > 1:
    wins_streamer3_output = str(wins_streamer3) + ' chicken dinners tonight!'

with open('homedirectory/streamer3wins', 'w') as f:
    print(wins_streamer3_output, file=f)