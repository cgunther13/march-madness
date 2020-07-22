import csv
from data.api_data_pull import load_tourny_teams
import datetime
now = datetime.datetime.now()

years = [2013, now.year-1]

# for year in years:
(tourny_teams, stats) = load_tourny_teams(2018)
print(year)
with open('march_madness_team_stats_' + str(2018) + '.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    teams_details = ['name', 'region', 'start_seed']
    teams_details = teams_details + stats
    writer.writerow(teams_details)

    for team in tourny_teams:
        # print(team.stats.values())
        team_stats = list(team.stats.values())
        team_details = [team.name, team.region, team.start_seed]
        team_details = team_details + team_stats
        writer.writerows([team_details])

    csvFile.close()
