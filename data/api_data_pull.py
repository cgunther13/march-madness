import requests
# import requests_cache
import xml.etree.ElementTree as ET
import time

#Load class information
from classes.team import Team

#Cache the API data; backend=None uses sqlite if possible, memory if not; Never flush the data
# requests_cache.install_cache('march_madness_cache', backend=None, expire_after=None)

def load_tourny_teams(year):
    #Get NCAA Men's Division I Basketball Tournament (aka March Madness) tournament id
    tournaments_url = 'https://api.sportradar.us/ncaamb/trial/v7/en/tournaments/'+str(year)+'/pst/schedule.xml?api_key=qg6gaqr9f4x4b5utrynfp4jx'
    march_madness_id = ''

    #Get the data in XML format
    tournaments_xml = requests.get(tournaments_url)
    print(tournaments_xml.content)
    #Capture the start of the XML DOM
    tournaments_root = ET.fromstring(tournaments_xml.content)
    #For each tournament tag in the DOM, if name = March Madess capture the id
    # print(tournaments_root.tag)
    # print(tournaments_root.attrib)
    print(year)
    print(tournaments_root)
    print(tournaments_root.tag)
    print(tournaments_root.attrib)
    for tournament in tournaments_root[0]:
        if (tournament.attrib['name'] == 'NCAA Men\'s Division I Basketball Tournament'):
            march_madness_id = tournament.attrib['id']
            break

    #Need to wait a second before calling the API again
    time.sleep(1)

    #Get the teams (along with region and seed) in march madness
    tourny_teams_url = 'https://api.sportradar.us/ncaamb/trial/v4/en/tournaments/'+march_madness_id+'/summary.xml?api_key=qtcxhk2mzua35x23m5hh96d8'
    tourny_teams = []
    tourny_teams_xml = requests.get(tourny_teams_url)
    tourny_teams_root = ET.fromstring(tourny_teams_xml.content)
    # print(tourny_teams_xml.content)
    #Check that we are looking at the right tournament
    if (tourny_teams_root.attrib['name'] == 'NCAA Men\'s Division I Basketball Tournament'):
        for bracket in tourny_teams_root:
            region = bracket.attrib['name'][:-1*len(' Regional')]
            for team in bracket:
                team_id = team.attrib['id']
                team_name = team.attrib['market']
                seed = team.attrib['seed']

                team = Team(year, team_id, team_name, region, seed)
                tourny_teams.append(team)
    else:
        print('Wrong tournament id')

    #Need to wait a second before calling the API again
    time.sleep(1)

    #Get the regular season stat names
    for team in tourny_teams:
        stats = []
        stats_url = 'https://api.sportradar.us/ncaamb/trial/v4/en/seasons/'+str(year)+'/REG/teams/'+team.id+'/statistics.xml?api_key=qtcxhk2mzua35x23m5hh96d8'
        stats_xml = requests.get(stats_url)
        stats_root = ET.fromstring(stats_xml.content)
        #season --> team_id --> team_records --> overall
        if stats_root.tag != 'h1':
            stats = list(stats_root[0][0][0][0].attrib.keys())

    #Need to wait a second before calling the API again
    time.sleep(1)

    #Get the regular season stats
    for team in tourny_teams:
        stats_url = 'https://api.sportradar.us/ncaamb/trial/v4/en/seasons/'+str(year)+'/REG/teams/'+team.id+'/statistics.xml?api_key=qtcxhk2mzua35x23m5hh96d8'
        stats_xml = requests.get(stats_url)
        stats_root = ET.fromstring(stats_xml.content)
        for i in range(0, len(stats)):
            team.add_stats(team, stats[i], stats_root[0][0][0][0].attrib[stats[i]])
            #Need to wait a second before calling the API again
            time.sleep(0.1)

    return (tourny_teams, stats)
