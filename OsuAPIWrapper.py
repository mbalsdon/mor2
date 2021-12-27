from pprint import pprint
import requests
from SimpleScore import SimpleScore

API_URL = "https://osu.ppy.sh/api/v2"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"
AUTH_CODE_URL = "https://osu.ppy.sh/oauth/authorize"

# RETURN: OAuth2 access token
def get_token(client_id, client_secret, grant_type, redirect_uri, scope):
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': grant_type,
        'redirect_uri': redirect_uri,
        'scope': scope
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json().get('access_token')

# PARAMS: user_id (Integer), headers (valid osu!api v2 headers)
# RETURN: username of player with given ID (String)
def get_username(user_id, headers):
    response = requests.get(f'{API_URL}/users/{user_id}/osu', headers=headers)
    return response.json()['username']

def get_beatmap(beatmap_id, headers):
    response = requests.get(f'{API_URL}/beatmaps/{beatmap_id}', headers=headers)
    return response.json()

# PARAMS: user_id (Integer), headers (valid osu!api v2 headers)
# RETURN: top 100 of player with given ID (Score[]) <https://osu.ppy.sh/docs/index.html?javascript#score>
def get_top_100(user_id, headers):
    params = {
        'limit': '100',
        'mode': 'osu'
    }
    response = requests.get(f'{API_URL}/users/{user_id}/scores/best', headers=headers, params=params)
    return response.json()

# PARAMS: user_id (Integer), headers (valid osu!api v2 headers)
# RETURN: top 100 of player with given ID (SimpleScore[])
def get_top_100_simple(user_id, headers):
    simple_array = []
    username = get_username(user_id, headers)
    response = get_top_100(user_id, headers)
    for i in range(0, 100):
        # Make sure user has 100 scores
        try:
            score = response[i]
        except IndexError:
            print('IndexError: Player %s does not have a %sth score' % (user_id, str(i+1)))
            break

        mods = score['mods']
        mods = parse_mods(mods)
        beatmap = score['beatmapset']['title']
        diffname = score['beatmap']['version']
        pp = score['pp']
        acc = score['accuracy']
        simple_score = SimpleScore(username, mods, beatmap, diffname, pp, acc)

        simple_array.append(simple_score)
    return simple_array

# PARAMS: mods (string array)
# RETURN: concatenated string of mods (e.g. ['HD', 'DT'] -> 'HDDT')
def parse_mods(mods):
    mod_string = ''
    # Empty mod array => nomod
    if not mods: 
        mod_string = mod_string + 'NM'
    else: 
        for m in mods:
            mod_string = mod_string + m
    return mod_string