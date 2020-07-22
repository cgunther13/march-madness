class BracketTree(object):
    def __init__(self, round_number, region_name = None, seeds = None):
        self.children = []
        self.parent = None
        self.round_name = round_dictionary[round_number]
        self.round_number = round_number
        self.region_name = region_name
        self.seeds = seeds

        self.teams = []
        self.winning_team_index = None

        def add_team(self, team):
            self.teams.append( team )

        def add_child(self, child):
            assert( child.round_number + 1 == self.round_number )
            if self.region_name != None:
                assert( child.region_name == self.region_name )
            child.set_parent( self )
            self.children.append(child)

        def set_parent(self, parent):
            self.parent = parent

        def _init_add_children(self, regional_teams, seeds, cls):
            # Helper function used by init_starting_bracket
            assert( len(seeds) == len(regional_teams) )
            assert( len(seeds) >= 2 and len(seeds) % 2 == 0 )
            if len(seeds) > 2:
                for winning_seed in seeds[:2]:
                    child = cls( self.round_number - 1, region_name = self.region_name )
                    child_seeds = [winning_seed]
                    current_round = self.round_number - 1
                    while current_round > 0:
                        new_child_seeds = [ seed_pairs_by_round[current_round][s] for s in child_seeds]
                        child_seeds.extend( new_child_seeds )
                        current_round -= 1
                    child_seeds.sort()
                    child._init_add_children(
                        { k : regional_teams[k] for k in regional_teams if k in child_seeds },
                        child_seeds, cls,
                    )
                    self.add_child( child )
            else:
                for seed in seeds:
                    if len(regional_teams[seed]) > 1:
                        # First four seed, add one more child
                        child = cls( self.round_number - 1, region_name = self.region_name )
                        for team in regional_teams[seed]:
                            child.add_team(team)
                        self.add_child( child )
                    else:
                        # Not a first four seed
                        for team in regional_teams[seed]:
                            self.add_team( team )

        def init_starting_bracket(cls):
            # Uses round_dictionary to initialize a full bracket. Bracket is filled in according to results so far.
            teams = {}
            min_seed = None
            max_seed = None

            if not os.path.isfile(default_data_file):
                urllib.request.urlretrieve(source_url, default_data_file)

            df = pd.read_csv(default_data_file)
            df = df.loc[ df['gender'] == 'mens' ].copy().sort_values('forecast_date', ascending = False )
            df = df.loc[ df['forecast_date'] == df.iloc[0]['forecast_date'] ].copy()
            df = df.loc[ df['team_alive'] == 1 ].copy()
            df = df.drop_duplicates( ['team_name'] )

            # Read in team data
            for index, row in df.iterrows():
                team = Team.init_from_row(row)
                if min_seed == None or team.seed < min_seed:
                    min_seed = team.seed
                if max_seed == None or team.seed > max_seed:
                    max_seed = team.seed

                if team.region not in teams:
                    teams[team.region] = {}
                if team.seed not in teams[team.region]:
                    teams[team.region][team.seed] = [team]
                else:
                    teams[team.region][team.seed].append( team )

        def scores(self):
            default_scores = {
                0:0,
                1:1,
                2:2,
                3:4,
                4:8,
                5:16,
                6:32
            }
            assert( self.winning_team_index != None )
            assert( len(self.teams) == 2 )
            winning_team = self.teams[self.winning_team_index]
            losing_team = self.teams[1-self.winning_team_index]

            return max( [0, winning_team.seed - losing_team.seed] ) + default_yahoo_scores[self._round_number]
