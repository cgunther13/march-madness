from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from requests import get

from classes.team import Team

def load_teams_by_round(year, load_round):
    #Website with March Madness tournament brackets
    url="https://www.sports-reference.com/cbb/postseason/"+str(year)+"-ncaa.html"
    response = get(url)

    regions = ['east', 'west', 'south', 'midwest']
    tourny_teams = []

    #Indices represent where in the list of a_tags the team names are (other a tags represent scores and location of the game)
    m_s_team_indices = [0,2,5,7,10,12,15,17,20,22,25,27,30,32,35,37]

    #East and West regions have 2 play in games each, taking up 8 indices (2 games * 2 teams * 2 scores)
    e_w_team_indices = [i + buffer for i in team_indices]

    number_of_teams = len(team_indices) // (2**load_round)
    team_indices = team_indices[0:number_of_teams]
    team_indices = [i + (80 // (2**load_round)) for i in team_indices]

    for region in regions[0:2]:
        #Only extract teams from one region at a time
        region_soup = SoupStrainer(id=region)
        soup = BeautifulSoup(response.text, 'html.parser', parse_only=region_soup)
        a_tags = soup.find_all('a') #to get team names
        temp_counter=0
        for a in a_tags:
            print(temp_counter, a.text)
            temp_counter+=1





        #Each round starts 40 <a> tags after the first team in the previous round
        print(len(e_w_team_indices))
        print(load_round)
        print(2**load_round)


        print(number_of_teams)
        print(e_w_team_indices)

        # 80 / 1 = 40
        # 80 / 2 = 40
        # 80 / 4 = 20
        # 80 / 8 = 10
        # 80 / 16 = 5

        # 1 ---> 2 ---> 3 ---> 4
        # 40 --> 60 --> 70 --> 75

        for i in e_w_team_indices:
            r_year = year
            region_name = region
            name = a_tags[i].text
            #Team's score in a round shows up one <a> tag after the team name
            score = a_tags[i+1].text

            #Create team classes with all the corresponding info
            team = Team(r_year, region_name, name, score, [], 0)
            tourny_teams.append(team)

    return (tourny_teams)
