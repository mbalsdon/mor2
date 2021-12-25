import requests
import OsuAPIWrapper as api
import config as config

def main():
    token = api.get_token(config.OSU_API_CLIENT_ID, config.OSU_API_CLIENT_SECRET, 'client_credentials', 'http://localhost:9274/', 'public')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get('https://sheets.googleapis.com/v4/spreadsheets/1Rxhsz2fO-q77qWiJmOO3hnxCdjm9dtWAFFV_J_ld1_Y/values/Sheet1!A1')
    print(response)
    
    # for ss in api.get_top_100_simple(6385683, headers):
    #     data = (ss.get_beatmap(), ss.get_mods(), ss.get_pp())
    #     format_string = "%s +%s // %spp"
    #     print(format_string % data)

if __name__ == '__main__':
    main()

# Given a masterlist of players, takes the top100s of each player and sorts them into mod categories, and then by pp.
# Places the list of sorted plays into spreadsheets. Should include player, mods, beatmap, pp.
# (Might want to store overwritten sheets elsewhere, by date, for posterity)

# TODO: add acc, combo to scores?
# TODO: errors