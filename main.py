import csv
from pprint import pprint
import requests
import OsuAPIWrapper as api
import config as config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

def main():
    token = api.get_token(config.OSU_API_CLIENT_ID, config.OSU_API_CLIENT_SECRET, 'client_credentials', 'http://localhost:9274/', 'public')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    player_ids = []
    scores = []

    # TODO: change from testplayerlist.csv
    with open('testplayerlist.csv', mode='r', newline='\n') as player_file:
        player_reader = csv.reader(player_file, delimiter=',')
        for row in player_reader:
            # Skip comment rows
            if row[0].startswith('#'):
                continue
            player_ids.append(int(row[0]))

    # player_ids = [6385683] # TODO: remove

    for pid in player_ids:
        print('Grabbing %s\'s top plays...' % (pid))
        scores.extend(api.get_top_100_simple(pid, headers))

    # TODO: Sort into ~36 different lists and place in spreadsheet
    # Outer for loop with big switch on mods, probably
    # Want to place into google spreadsheets in as few requests as possible

    scores.sort(reverse=True, key=lambda s: s.get_pp())
    score_dict = {}

    # TODO: comment
    def merge_mods(mods):
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
        # if it was NM with NF/SO/SD/PF, add it back in (bit of a bandaid fix)
        if mods == '':
            mods = 'NM'
        return mods

    for s in scores:
        mods = s.get_mods()
        mods = merge_mods(mods)
        if mods in score_dict:
            score_dict[mods].append(s)
        else:
            score_dict[mods] = [s]


    # init sheets (TODO: module)
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # create the sheet
    # TODO: why time no work
    sheet = client.create('ok mouseonlyrecords %s' % date.today().strftime("%x"))
    # make you the owner of the sheet
    user_email = 'm.mathewbalsdon@gmail.com'
    sheet.share(user_email, perm_type='user', role='owner', notify=True)


    # create worksheets
    titlerow = ['USER', 'MODS', 'MAP', 'DIFF', 'PP', 'ACC', '']
    onemod_ws = sheet.add_worksheet(title='1 mod', rows='10000', cols='91')
    onemod_ws.update('A1:AW1', [titlerow * 7])

    sheet.del_worksheet(sheet.sheet1) # get rid of the default sheet

    twomod_ws = sheet.add_worksheet(title='2 mods', rows='10000', cols='91')
    twomod_ws.update('A1:CN1', [titlerow * 13])

    threemod_ws = sheet.add_worksheet(title='3 mods', rows='10000', cols='91')
    # TODO
    
    fourmod_ws = sheet.add_worksheet(title='4 mods', rows='10000', cols='91')
    # TODO


    # TODO: make this readable later
    for k in score_dict:
        if len(k) == 2:
            # turn em back into arrays... TODO: cut out middleman
            outerarr = []
            for score in score_dict[k]:
                outerarr.append(score.to_array())
                num_scores = str(len(outerarr) + 1)
                sheet_range = ''
            # TODO: is switch on type avoidable ? ugly
            # TODO: function: column num => number (e.g. 0 -> A)
            if k == 'NM':
                sheet_range = f'A2:F{num_scores}'
            elif k == 'DT':
                sheet_range = f'H2:M{num_scores}'
            elif k == 'HR':
                sheet_range = f'O2:T{num_scores}'
            elif k == 'HD':
                sheet_range = f'V2:AA{num_scores}'
            elif k == 'EZ':
                sheet_range = f'AC2:AH{num_scores}'
            elif k == 'HT':
                sheet_range = f'AJ2:AO{num_scores}'
            elif k == 'FL':
                sheet_range = f'AQ2:AV{num_scores}'

            onemod_ws.update(sheet_range, outerarr)
        
        elif len(k) == 4:
            outerarr = []
            for score in score_dict[k]:
                # TODO duplicate code :)
                outerarr.append(score.to_array())
                num_scores = str(len(outerarr) + 1)
                sheet_range = ''
            # TODO: plz no huge elif block if possible
            if k == 'HDDT':
                sheet_range = f'A2:F{num_scores}'
            elif k == 'DTHR':
                sheet_range = f'H2:M{num_scores}'
            elif k == 'EZDT':
                sheet_range = f'O2:T{num_scores}'
            elif k == 'DTFL':
                sheet_range = f'V2:AA{num_scores}'
            elif k == 'EZHT':
                sheet_range = f'AC2:AH{num_scores}'
            elif k == 'HDHR':
                sheet_range = f'AJ2:AO{num_scores}'
            elif k == 'HDHT':
                sheet_range = f'AQ2:AV{num_scores}'
            elif k == 'EZHD':
                sheet_range = f'AX2:BC{num_scores}'
            elif k == 'HTHR':
                sheet_range = f'BE2:BJ{num_scores}'
            elif k == 'EZFL':
                sheet_range = f'BL2:BQ{num_scores}'
            elif k == 'HRFL':
                sheet_range = f'BS2:BY{num_scores}'
            elif k == 'HTFL':
                sheet_range = f'CA2:CF{num_scores}'
            elif k == 'HDFL':
                sheet_range = f'CH2:CM{num_scores}'
            
            twomod_ws.update(sheet_range, outerarr)
        elif len(k) == 6:
            continue # TODO
        elif len(k) == 8:
            continue # TODO
        else:
            raise KeyError("len(k) != 2, 4, 6, or 8")
    
    # for k in score_dict:
    #     print('\n=== %s ===' % k)
    #     for s in score_dict[k]:
    #         print('%s - %s [%s] +%s %spp' % (s.get_username(), s.get_beatmap(), s.get_diffname(), s.get_mods(), round(s.get_pp())))








if __name__ == '__main__':
    main()

# Given a masterlist of players, takes the top100s of each player and sorts them into mod categories, and then by pp.
# Places the list of sorted plays into spreadsheets. Should include player, mods, beatmap, pp.
# (Might want to store overwritten sheets elsewhere, by date, for posterity)

# TODO: SimpleScore might be unneeded since sheets just takes arrays anyway
#   -> create an array [username, mods, beatmap, diffname, pp, acc]
# TODO: modularize properly for readability..