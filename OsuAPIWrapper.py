import requests
import csv
import config as config

import time

class OsuAPIWrapper():
    API_URL = "https://osu.ppy.sh/api/v2"
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"
    AUTH_CODE_URL = "https://osu.ppy.sh/oauth/authorize"

    def __init__(self):
        data = {
            'client_id': config.OSU_API_CLIENT_ID,
            'client_secret': config.OSU_API_CLIENT_SECRET,
            'grant_type': 'client_credentials',
            'redirect_uri': config.OSU_API_REDIRECT_URI,
            'scope': 'public'
        }
        response = requests.post(self.TOKEN_URL, data=data)
        self.token = response.json().get('access_token')

    # PARAMS: osu! user ID (int), valid osu!api v2 headers
    # RETURN: the associated username (str)
    def get_username(self, user_id, headers):
        response = requests.get(f'{self.API_URL}/users/{user_id}/osu', headers=headers)
        return response.json()['username']

    # PARAMS: osu! beatmap ID (int), valid osu!api v2 headers
    # RETURN: the associated beatmap (Beatmap object)
    def get_beatmap(self, beatmap_id, headers):
        response = requests.get(f'{self.API_URL}/beatmaps/{beatmap_id}', headers=headers)
        return response.json()

    # PARAMS: osu! user ID (int), valid osu!api v2 headers
    # RETURN: the top 100 scores of the user (array of Score objects)
    def get_top_100(self, user_id, headers):
        params = {
            'limit': '100',
            'mode': 'osu'
        }
        response = requests.get(f'{self.API_URL}/users/{user_id}/scores/best', headers=headers, params=params)
        return response.json()

    # PARAMS: osu! user ID (int), valid osu!api v2 headers
    # RETURN: the top 100 scores of the user
    #         (array of tuples: (username (str), mods (str), beatmap (str), diffname (str), pp (num), accuracy (num)))
    def get_top_100_simple(self, user_id, headers):
        # concatenates the array of mods into a string; if the array is empty, returns the string 'NM'
        def parse_mods(mods):
            mod_string = ''
            if not mods: 
                mod_string = mod_string + 'NM'
            else: 
                for m in mods:
                    mod_string = mod_string + m
            return mod_string

        score_array = []
        response = self.get_top_100(user_id, headers)
        username = self.get_username(user_id, headers)
        for i in range(0, 100):
            try:
                score = response[i]
            except IndexError:
                print('IndexError: Player %s does not have a %sth score' % (user_id, str(i+1)))
                break
            formatted_score = (username,
                                parse_mods(score['mods']),
                                score['beatmapset']['title'],
                                score['beatmap']['version'],
                                score['pp'],
                                score['accuracy'])
            score_array.append(formatted_score)

        return score_array

    # PARAMS: .csv file containing user IDs separated by newlines
    # RETURN: user IDs (array of int)
    def get_player_ids(self, filepath):
        player_ids = []
        with open(filepath, mode='r', newline='\n') as player_file:
            player_reader = csv.reader(player_file, delimiter=',')
            for row in player_reader:
                # Skip comment rows
                if row[0].startswith('#'):
                    continue
                player_ids.append(int(row[0]))

        return player_ids

    # PARAMS: user IDs (array of int), valid osu!api v2 headers
    # RETURN: dict: keys = mod combos (str), vals = scores (array of tuples defined in get_top_100_simple)
    def get_top_plays(self, player_ids, headers):
        scores = []
        for id in player_ids:
            print(f'Grabbing {id}\'s top plays...')
            scores.extend(self.get_top_100_simple(id, headers))
        scores.sort(reverse=True, key=lambda s: s[4])
        score_dict = {}
        for s in scores:
            mods = self.merge_mods(s[1])
            if mods in score_dict:
                score_dict[mods].append(s)
            else:
                score_dict[mods] = [s]

        return score_dict

    # PARAMS: mod combo (str)
    # RETURN: mod combo without NF/SO/SD/PF and with DT in place of NC (str)
    # TODO: do this in get_top_100_simple() instead of get_top_plays to avoid the bandaid NM fix
    def merge_mods(self, mods):
        # turn NC into DT
        if mods.find('NC') != -1:
            mods = mods.replace('NC', 'DT')
        # get rid of NF, SO, SD, PF
        if mods.find('NF') != -1:
            mods = mods.replace('NF', '')
        if mods.find('SO') != -1:
            mods = mods.replace('SO', '')
        if mods.find('SD') != -1:
            mods = mods.replace('SD', '')
        if mods.find('PF') != -1:
            mods = mods.replace('PF', '')
        # if the play was nomod but had NF/SO/SD/PF we need to add 'NM'
        if mods == '':
            mods = 'NM'
        return mods