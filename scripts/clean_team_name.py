
import re

def clean_team_name(team_name):
    team_name = team_name.lower()
    team_name = team_name.replace('state', 'st')
    team_name = team_name.replace('saint', 'st')
    team_name = team_name.replace('st.', 'st')
    team_name = team_name.replace('-', ' ')
    team_name = team_name.replace('\'', '')
    team_name = team_name.replace('.', '')

    weird_team_names = {
        'louisiana st': 'lsu',
        'mississippi' : 'ole miss',
        'virginia commonwealth' : 'vcu',
        'texas christian' : 'tcu',
        'maryland baltimore county' : 'umbc',
        'loyola (il)' : 'loyola chicago',
        'loyola (md)' : 'loyola maryland',
        'miami (fl)' : 'miami',
        'miami (oh)' : 'miami ohio',
        'north carolina greensboro': 'unc greensboro',
        'north carolina st' : 'nc state',
        'st francis (pa)' : 'st francis pa',
        'st francis (ny)' : 'st francis ny'
    }

    if team_name[:-5] in weird_team_names.keys():
        team_name = (weird_team_names[team_name[:-5]] + ' ncaa')

    team_name = re.sub(r' \(*\)','', team_name)
    team_name = re.sub(r' \([^)]*\)', '', team_name)

    # if (team_name[:-5] == 'louisiana st'):
    #     team_name = 'lsu ncaa'
    # if (team_name[:-5] == 'mississippi'):
    #     team_name = 'ole miss ncaa'
    # if (team_name[:-5] == 'virginia commonwealth'):
    #     team_name = 'vcu ncaa'
    # if (team_name[:-5] == 'texas christian'):
    #     team_name = 'tcu ncaa'
    # if (team_name[:-5] == 'maryland baltimore county'):
    #     team_name = 'umbc ncaa'

    return team_name
