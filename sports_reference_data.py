from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from requests import get

from classes.team import Team

def load_teams(year):
    #Website with March Madness tournament brackets
    url="https://www.sports-reference.com/cbb/postseason/"+str(year)+"-ncaa.html"
    response = get(url)

    #Get region names (east, west, midwest, south for most, but changes some years)
    bracket_names_soup = SoupStrainer('div', class_='switcher filter')
    soup = BeautifulSoup(response.text, 'html.parser', parse_only=bracket_names_soup)
    bracket_names = soup.find_all('a')
    regions = []
    for a_tag in bracket_names:
        regions.append(a_tag.text.lower())
    # print(regions[0:4])

    # regions = ['east', 'west', 'south', 'midwest']
    tourny_teams = []

    r32 = []
    sweet_sixteen = []
    elite_eight = []

    for region in regions[0:4]:
        #Only extract teams from one region at a time
        stripped_region = region.replace(" ", "")
        stripped_region = stripped_region.replace(".", "")
        region_soup = SoupStrainer(id=stripped_region)
        soup = BeautifulSoup(response.text, 'html.parser', parse_only=region_soup)
        # a_tags = soup.find_all('a', {"class": "team16"}) #to get team names
        a_tags = []
        for brackets in soup.find_all('div', class_='team16'):
            for a in brackets.find_all('a'):
                a_tags.append(a)
        # temp = 0
        # for a in a_tags:
        #     print("here", temp, a.text)
        #     temp+=1

        #Indices represent where in the list of a_tags the team names are (other a tags represent scores and location of the game)
        team_indices = [0,2,5,7,10,12,15,17,20,22,25,27,30,32,35,37]

        #East and West regions have 2 play in games each, taking up 8 indices (2 games * 2 teams * 2 scores)
        # buffer = 0
        # if region in ["east", "west"]:
        #     team_indices = [i + buffer for i in team_indices]

        seed_index_counter = 0
        seeds = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15]

        for i in team_indices:
            r_year = year
            region_name = region
            name = a_tags[i].text
            #Team's score in a round shows up one <a> tag after the team name
            score = a_tags[i+1].text

            #Get a team's stats
            stats = {}
            stat_names = []
            stat_values = []

            #Link to the team's page that has their stats, rosters, etc.
            stats_url="https://www.sports-reference.com/"+a_tags[i]["href"]
            stats_response = get(stats_url)
            team_stats_soup = SoupStrainer(id="team_stats")
            #Only focus on the team stat table (other tables show the roster, conference stats, etc.)
            team_stats_soup = BeautifulSoup(stats_response.text, 'html.parser', parse_only=team_stats_soup)

            #Get the names of the reported stats (e.g. G = games, MP = minutes played, etc.)
            team_stats_table = team_stats_soup.find_all('th')
            #Append Games played
            # counter = 0
            # for th in team_stats_table:
            #      print(counter, th.text)
            #      counter+=1
            stat_names.append(team_stats_table[1].text)
            #Skip Minutes Played (blank some years) then append other stat names
            for th in team_stats_table[3:-4]:
                stat_names.append(th.text)

            #Get the values associated with each stat for a given team
            team_stats = team_stats_soup.find_all('td')
            #Append Games played
            # counter = 0
            # for td in team_stats:
            #      print(counter, td.text)
            #      counter+=1
            stat_values.append(team_stats[0].text)
            # print("Len", len(stat_names))
            #Skip Minutes Played (blank some years) then append other stat names
            for td in team_stats[2:len(stat_names)+1]:
                stat_values.append(td.text)

            # for s in range(0,len(stat_values)):
            #     print(stat_values[s])

            # Combine the stat names and values (dictionary with names as keys, values as values)
            for i in range(0, len(stat_names)-1):
                #Convert stats to floating point numbers, unless the stat is blank
                # print(stat_names[i], stat_values[i])
                try:
                    stats[stat_names[i]] = float(stat_values[i])
                except:
                    stats[stat_names[i]] = 0

            #Add per game stat names
            per_game_stat_names = ["FG","FGA","2P","2PA","3P","3PA","FT","FTA","ORB","DRB","TRB","AST","STL","BLK","TOV","PF"]
            for per_game_stat_name in per_game_stat_names:
                stat_names.append(per_game_stat_name+"/G")

            #Add per game stats
            for per_game_stat_name in per_game_stat_names:
                per_game_stat_value = stats[per_game_stat_name] / stats["G"]
                stat_values.append(per_game_stat_value)

            #Combine the stat names and values (with per game stats)
            for i in range(0, len(stat_names)):
                #Convert stats to floating point numbers, unless the stat is blank
                try:
                    stats[stat_names[i]] = float(stat_values[i])
                except:
                    stats[stat_names[i]] = 0
                # except:
                #     stats[stat_names[i]] = stat_values[i]

            #Create team classes with all the corresponding info
            team = Team(r_year, region_name, name, score, stats, seeds[seed_index_counter])
            tourny_teams.append(team)

            seed_index_counter += 1

        r32_indices = [i + 40 for i in team_indices[0:len(team_indices) // 2]]
        sweet_sixteen_indices = [i + 60 for i in team_indices[0:len(team_indices) // 4]]
        elite_eight_indices = [i + 70 for i in team_indices[0:len(team_indices) // 8]]

        for i in r32_indices:
            name = a_tags[i].text
            r32.append(name)
        for i in sweet_sixteen_indices:
            name = a_tags[i].text
            sweet_sixteen.append(name)
        for i in elite_eight_indices:
            name = a_tags[i].text
            elite_eight.append(name)

    #Only extract teams from one region at a time
    final_four_soup = SoupStrainer(id="national")
    soup = BeautifulSoup(response.text, 'html.parser', parse_only=final_four_soup)
    a_tags = soup.find_all('a') #to get team names

    final_four = []
    championship = []
    champion = []

    final_four_indices = team_indices[0:4]
    championship_indices = team_indices[4:6]
    champion_index = team_indices[6]

    for i in final_four_indices:
        name = a_tags[i].text
        final_four.append(name)
    for i in championship_indices:
        name = a_tags[i].text
        championship.append(name)
    champion.append(a_tags[champion_index].text)


    return (regions[0:4], tourny_teams, stat_names, r32, sweet_sixteen, elite_eight, final_four, championship, champion)
