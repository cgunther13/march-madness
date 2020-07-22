#API to get team IDs

#API to get team stats
# https://api.sportradar.us/ncaamb/trial/v4/en/seasons/+str(year)+/REG/teams/+team.id+/statistics.xml?api_key={your_api_key}


import csv
import datetime
now = datetime.datetime.now()

from scripts.clean_team_name import clean_team_name

#Map statistics of interest to each of the 64 teams in the tournament
def load_stats(tourny_teams, year):
    stats_url = 'data/sportsref_stats_' + str(year) + '.csv'
    with open(stats_url, 'r') as stats_file:
        readCSV = csv.reader(stats_file, delimiter=',')
        #Get the stats from the header row to use as keys in the stats dictionary
        keys = next(readCSV)

        #For each team in Division 1
        for row in readCSV:
            team_name = row[0]

            #Clean up formatting to match with stats names
            team_name = clean_team_name(team_name)

            # print(team_name)
            #Only consider teams that made the tournament, as marked by the ncaa tag at the end
            if (team_name[-5:] == ' ncaa'):
                for team in tourny_teams:
                    if (team.year == year):
                        #Match the right team class instance
                        if (team.name == team_name[:-5]):
                            # print(team.name, team_name)
                            #Insert each stat into the stats dictionary, with the stat name key
                            for i in range(1, len(row)):
                                team.add_stats(team, keys[i], row[i])
