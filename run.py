# Example I found online
# https://github.com/kylebarlow/marchmadness/blob/master/predict.py
import datetime
now = datetime.datetime.now()

#Load class information
from classes.team import Team
from classes.matchup import MatchUp

#Load data
from sports_reference_data import load_teams
from sports_reference_teams_by_round import load_teams_by_round
# from data.load_stats import load_stats
# from data.load_teams_by_round import load_teams_by_round

import xlsxwriter
# Create a workbook and add a points_worksheet to keep track of total points by year, round, and stat
# points_worksheet columns are "Year", "Stat", "R64 points", "R32 points", "Sweet 16 points", "Elite 8 points", "Final 4 points", "Championship points", "Total points"
# teamss_worksheet columns are "Year & Stat", "R64 teams", "R32 teams", "Sweet 16 teams", "Elite 8 teams", "Final 4 teams", "Championship teams", "Champion"
workbook = xlsxwriter.Workbook('march_madness_points_by_round_by_team_stat.xlsx')
points_worksheet = workbook.add_worksheet()
teams_worksheet = workbook.add_worksheet()

#Write in column titles
points_worksheet.write(0,0,"Year")
points_worksheet.write(0,1,"Stat")
points_worksheet.write(0,2,"R32 Points")
points_worksheet.write(0,3,"Sweet 16 Points")
points_worksheet.write(0,4,"Elite 8 Points")
points_worksheet.write(0,5,"Final 4 Points")
points_worksheet.write(0,6,"Championship Points")
points_worksheet.write(0,7,"Total Points")
points_worksheet_row = 1
points_worksheet_col = 0

teams_worksheet.write(0,1,"Year Stat")
teams_worksheet.write(0,2,"R64 Teams")
teams_worksheet.write(0,2,"R32 Teams")
teams_worksheet.write(0,3,"Sweet 16 Teams")
teams_worksheet.write(0,4,"Elite 8 Teams")
teams_worksheet.write(0,5,"Final 4 Teams")
teams_worksheet.write(0,6,"Championship Teams")
teams_worksheet.write(0,7,"Champion")
teams_worksheet_row = 1
teams_worksheet_col = 0

#Define points for each correct team in each round
r32_points = 10
sweet_sixteen_points = 20
elite_eight_points = 40
final_four_points = 80
championship_points = 160
champion_points = 320
points_by_round = [r32_points, sweet_sixteen_points, elite_eight_points, final_four_points, championship_points, champion_points]

years = range(1999, 2020, 1)

# print(str(year) + ': ')

for year in years:
    # reset tourny_teams and stats each year
    tourny_teams = []
    stats = []

    # print(str(year) + ': ')

    #Fill in the starting bracket (list of 64 teams, with names, regions, stats, and seeds
    regions, tourny_teams, stat_names, actual_r32, actual_sweet_sixteen, actual_elite_eight, actual_final_four, actual_championship, actual_champion = load_teams(year)

    #Set final four bracket matchups
    for team in tourny_teams:
        if team.name == actual_final_four[0]:
            game1_region1 = team.region
        elif team.name == actual_final_four[1]:
            game1_region2 = team.region
        elif team.name == actual_final_four[2]:
            game2_region1 = team.region
        elif team.name == actual_final_four[3]:
            game2_region2 = team.region

    best_stat = ''
    most_points = 0

    for stat in stat_names:

        #Reset spot in the excel writing
        points_worksheet_col = 0
        teams_worksheet_col+=1
        teams_worksheet_row=1

        #Write the year and stat names in points_worksheet and teams_worksheet columns 1 and 2
        points_worksheet.write(points_worksheet_row, points_worksheet_col, year)
        points_worksheet_col+=1
        points_worksheet.write(points_worksheet_row, points_worksheet_col, stat)
        points_worksheet_col+=1

        teams_worksheet.write(teams_worksheet_row, teams_worksheet_col, str(year) + " " + stat)
        teams_worksheet_col+=1

        #Have the right seeds play each other in each round (with the winner determined by the stat of interest) and advance the winner to the next round
        #Number of teams remaining in each region (starts with 16 per region)
        max_seed = 16

        #Start with all the teams in the tournamnet as winners (e.g. made round 0); reset to be all teams for each stat
        winners = tourny_teams

        #Reset seeds for each new stat
        for team in winners:
            #Write in starting teams to the excel
            teams_worksheet.write(teams_worksheet_row, teams_worksheet_col, str(team.start_seed) + " " + team.name)
            teams_worksheet_row+=1

            team.adj_seed = team.start_seed

        #Initialize empty lists used to store the teams that make it to each round of the torunament
        r32 = []
        sweet_sixteen = []
        elite_eight = []
        final_four = []
        championship = []
        champion = []

        #For each round of the tournament (R64, R32, Sweet 16, Elite 8, Final 4, Championship)
        for round in range(0,6):

            #Reset spot in the excel writing
            teams_worksheet_row = 1
            teams_worksheet_col+=1

            #Pair all the teams to play in this round; reset at the beginning of each round
            matchups = []

            if (round < 4):
                #Within each region
                for region in regions:
                    for team1 in winners:
                        for seed in range(1, max_seed // 2 + 1):
                            #Select the lower seed team in the matchup
                            if (team1.year == year and team1.region == region and team1.adj_seed == seed):
                                first_team = team1
                                for team2 in winners:
                                    #Select the higher seed team in the matchup; #1 vs 16, 2 vs 15, 3 vs 14 etc.; then 1 vs 8, 2 vs 7 etc. etc.
                                    if (team2.year == year and team2.region == region and team2.adj_seed == (max_seed + 1 - seed)):
                                        second_team = team2
                                        #Record the matchup
                                        matchup = MatchUp(team1, team2)
                                        matchups.append(matchup)
                                        break

            #Final 4; treated differently since teams play across regions
            elif (round == 4):
                for team in winners:
                    if (team.year == year):
                        if (team.region == game1_region1):
                            game1_team1 = team
                        elif (team.region == game1_region2):
                            game1_team2 = team
                        elif (team.region == game2_region1):
                            game2_team1 = team
                        elif (team.region == game2_region2):
                            game2_team2 = team

                #Record the matchup
                matchup1 = MatchUp(game1_team1, game1_team2)
                matchup2 = MatchUp(game2_team1, game2_team2)
                matchups.append(matchup1)
                matchups.append(matchup2)

            #Championship; final 2 teams play
            elif (round == 5):
                matchup = MatchUp(winners[0], winners[1])
                matchups.append(matchup)

            #Put all the winners into an array; reset it every round
            winners = []
            for matchup in matchups:
                winner = matchup.winner(matchup.team1, matchup.team2, stat)
                winners.append(winner)

            #Recategorize the winners into the correct seeds for the next round (e.g. if a 15 beats a 2 in the first round, the 15 "becomes" a 2, for the purposes of deciding which team to play next (the 7 seed))
            #Final 4 / Championship
            # if stat == "DRB":
            #     print(round)
            for winner in winners:

                #Write winning teams to the excel
                teams_worksheet.write(teams_worksheet_row, teams_worksheet_col,str(winner.start_seed) + " " + winner.name)
                teams_worksheet_row+=1

                #Chalk, no need to change seed
                if (winner.adj_seed <= max_seed / 2):
                    winner.adj_seed = winner.adj_seed
                else:
                    winner.adj_seed = max_seed - winner.adj_seed + 1
                # if stat == "DRB":
                #     print(winner.name)


            #Adjust max_seed for the next round (R32 has 8 teams in each region, Swet 16 has 4, etc.
            max_seed = max_seed // 2

            #Record the teams that make it to each round
            for winner in winners:
                if (round == 0):
                    r32.append(winner)
                elif (round == 1):
                    sweet_sixteen.append(winner)
                elif (round == 2):
                    elite_eight.append(winner)
                elif (round == 3):
                    final_four.append(winner)
                elif (round == 4):
                    championship.append(winner)
                elif (round == 5):
                    champion.append(winner)

        predicted_rounds = [r32, sweet_sixteen, elite_eight, final_four, championship, champion]
        # if(stat == "DRB"):
        #     print("R32")
        #     for team in r32:
        #         print(team.name)
        #     print("S16")
        #     for team in sweet_sixteen:
        #         print(team.name)
        #     print("E8")
        #     for team in elite_eight:
        #         print(team.name)
        #     print("F4")
        #     for team in final_four:
        #         print(team.name)
        #     print("Championship")
        #     for team in championship:
        #         print(team.name)
        #     print("Champion")
        #     for team in champion:
        #         print(team.name)

        actual_rounds = [actual_r32, actual_sweet_sixteen, actual_elite_eight, actual_final_four, actual_championship, actual_champion]
        # if(stat == "DRB"):
            # print("A R32", actual_r32)
            # print("A S16", actual_sweet_sixteen)
            # print("A E8", actual_elite_eight)
            # print("A F4", actual_final_four)
            # print("A Championship", actual_championship)
            # print("A Champion", actual_champion)

        #Record points for each correct team in each round
        points = 0

        #Calculate points won in each round
        for round in range(0,3):
            #For each team in the actual rounds
            for i in range(0, len(actual_rounds[round])):
                if actual_rounds[round][i] == predicted_rounds[round][i].name:
                    points += points_by_round[round]
            #Write points to the excel
            points_worksheet.write(points_worksheet_row, points_worksheet_col, points)
            points_worksheet_col+=1
        #In the Final 4 and on, order can be different between actual and predicted
        for round in range(3,len(actual_rounds)):
            for i in range(0, len(actual_rounds[round])):
                for j in range(0, len(predicted_rounds[round])):
                    if actual_rounds[round][i] == predicted_rounds[round][j].name:
                        points += points_by_round[round]
            #Write points to the excel
            points_worksheet.write(points_worksheet_row, points_worksheet_col, points)
            points_worksheet_col+=1

        if points > most_points:
            most_points = points
            best_stat = stat

        #Write the points picking a given stat gets in a given year ()
        #Increment the points_worksheet_colum for each stat
        # points_worksheet.write(points_worksheet_row, points_worksheet_col, points)
        points_worksheet_row+=1
    print("\nBest Stat: " + best_stat, most_points)


workbook.close()
