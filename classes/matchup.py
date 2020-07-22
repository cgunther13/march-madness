class MatchUp():
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def winner(self, team1, team2, stat):
        if (team1.stats[stat] > team2.stats[stat]):
            return team1
        elif (team1.stats[stat] < team2.stats[stat]):
            return team2
        else:
            #Tiebreak is lower seed (higher ranked team)
            if (int(team1.start_seed) > int(team2.start_seed)):
                return team1
            elif (int(team1.start_seed) < int(team2.start_seed)):
                return team2
            else:
                #Second tiebreak is team1; Life's not fair
                return team1
