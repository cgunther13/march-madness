
import csv
import datetime
now = datetime.datetime.now()

#Load class information
from classes.team import Team

'''Fill in the starting bracket (list of 64 teams, with names, regions, and seeds)'''

#Read through the file once, getting the first team
def load_teams_by_round(tourny_round):
    teams = []
    for year in range(2019, now.year + 1):
        with open('data/Big_Dance_CSV.csv', 'r') as teams1_file:
            readCSV = csv.reader(teams1_file, delimiter=',')
            #Skip the header row
            header = next(readCSV)
            for row in readCSV:
                #Record region_num, region, seed, and team name for each team
                r_year = row[0]
                round = row[1]
                if (int(r_year) == year and int(round) == tourny_round):
                    region_number = row[2]
                    region_name = row[3]
                    seed = row[4]
                    score = row[5]
                    team = row[6]

                    team = Team(r_year, round, region_number, region_name, seed, score, team)
                    teams.append(team)

        #Read through the file once, getting the other, opponent team
        with open('data/Big_Dance_CSV.csv', 'r') as teams2_file:
            readCSV = csv.reader(teams2_file, delimiter=',')
            #Skip the header row
            header = next(readCSV)
            for row in readCSV:
                #Record region_num, region, seed, and team name for each team
                r_year = row[0]
                round = row[1]
                if (int(r_year) == year and int(round) == tourny_round):
                    region_number = row[2]
                    region_name = row[3]
                    seed = row[7]
                    score = row[8]
                    team = row[9]

                    team = Team(r_year, round, region_number, region_name, seed, score, team)
                    teams.append(team)

    #Confirm there are the right number of teams in each round
    assert len(teams) == int(64 / 2**(tourny_round-1)), "Wrong number of teams. Check team name spelling"

    return teams
