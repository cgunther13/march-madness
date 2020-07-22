class Team():
    def __init__(self, year, region, name, score, stats, seed):
        self.year = int(year)
        # self.max_round = int(round)
        self.region = region
        self.name = name
        self.score = score
        self.start_seed = int(seed)
        self.adj_seed = int(seed)

        self.stats = stats

    # def add_stats(self, team, stat, value):
    #     team.stats[stat] = value
