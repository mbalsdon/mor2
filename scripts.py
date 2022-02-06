from datetime import date
from OsuAPIWrapper import OsuAPIWrapper
from SheetsWrapper import SheetsWrapper
import time
import csv

# PARAMS: email of archive sheet owner (str), should main sheet be updated? (boolean)
# RETURN: none
def archive(email, ids_file, update_main, ):
    osu_api = OsuAPIWrapper()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {osu_api.token}'
    }
    sheets_api = SheetsWrapper()

    print('Creating archive sheet...')
    sheet_title = f'mouseonlyrecords archive {date.today().strftime("[%d %b %Y]").upper()}'
    user_email = email
    archive_sheet = sheets_api.create_sheet(sheet_title, user_email)
    archive_worksheets = sheets_api.init_mod_worksheets(archive_sheet)
    main_sheet = sheets_api.get_mor_sheet()

    submitted_worksheet = main_sheet.worksheet('Submitted Scores')
    submitted_scores = submitted_worksheet.get('D6:G1000')
    archive_submitted_scores = osu_api.submitted_to_archive(submitted_scores)

    # This is done after making the archive sheet to allow the sheets API to
    # "cool down" since there is a limit on requests per minute.
    print('Collecting and sorting player scores...')
    player_ids = osu_api.get_player_ids(ids_file)
    player_scores = osu_api.get_top_plays(player_ids, archive_submitted_scores, headers)
    
    print('Putting scores in the archive sheet...')
    sheets_api.scores_to_sheet(player_scores, archive_worksheets, 1, 2, 6, 1)

    if update_main == True:
        print('Putting scores in the main sheet...')
        main_worksheets = [main_sheet.worksheet('1MOD'),
                            main_sheet.worksheet('2MOD'),
                            main_sheet.worksheet('3MOD'),
                            main_sheet.worksheet('4MOD')]
        reformatted_player_scores = osu_api.archive_to_main(player_scores)
        print('Waiting for sheets API to cool down...')
        for i in range(6): # TODO: magic numbers =D
            print('...')
            time.sleep(5)
        sheets_api.scores_to_sheet(reformatted_player_scores, main_worksheets, 4, 8, 3, 1)
        sheets_api.update_last_updated_tag(main_worksheets)

# PARAMS: player (str), mods (str), score id (int), pp (int)
# RETURN: none
def submit(score_id):
    osu_api = OsuAPIWrapper()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {osu_api.token}'
    }
    sheets_api = SheetsWrapper()
    main_sheet = sheets_api.get_mor_sheet()
    submitted_worksheet = main_sheet.worksheet('Submitted Scores')
    mod_worksheets = [main_sheet.worksheet('1MOD'),
                        main_sheet.worksheet('2MOD'),
                        main_sheet.worksheet('3MOD'),
                        main_sheet.worksheet('4MOD')]

    score = osu_api.get_score(score_id, headers)
    mods = osu_api.parse_mods(score['mods'])
    beatmap = '%s [%s]' % (score['beatmapset']['title'], score['beatmap']['version'])
    score_link = f'https://osu.ppy.sh/scores/osu/{score_id}'
    s = [score['user']['username'], 
            mods, 
            beatmap, 
            score_link, 
            int(round(score['pp'], 0))]

    print(f'Adding score {s} to the "Submitted Scores" sheet...')
    num_submitted = len(submitted_worksheet.get('D6:G1000'))
    row = num_submitted + 6
    submitted_worksheet.update(f'D{row}:G{row}', [[s[0], s[1], s[3], s[4]]])

    print(f'Adding score to the {mods} score list...')
    mods_len = len(mods)
    if mods_len != 2 and mods_len != 4 and mods_len != 6 and mods_len != 8:
        raise KeyError('mods length != 2/4/6/8')
    else:
        wks = mod_worksheets[int((mods_len/2) - 1)]
        str_vals = sheets_api.get_str_vals(mods, 10000, 4, 8, 3, 1)
        col_range = '%s%s:%s%s' % str_vals
    
        score_list = wks.get(col_range)
        # Remove empty rows
        for i in range(score_list.count([])):
            index = score_list.index([])
            score_list.pop(index)
        # The list is already sorted, so O(n) is possible using insert, however I am lazy :)
        score_list.append([s[0], s[3], s[4]])
        score_list.sort(reverse=True, key=lambda sc: int(sc[2]))
        wks.update(col_range, score_list)

# PARAMS: none
# RETURN: none
def update_leaderboard():
    osu_api = OsuAPIWrapper()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {osu_api.token}'
    }
    sheets_api = SheetsWrapper()
    main_sheet = sheets_api.get_mor_sheet()
    main_worksheet = main_sheet.worksheet('Main')
    leaderboard_scores = main_worksheet.get('E5:H112')
    lb_players = osu_api.get_lb_players(leaderboard_scores)
    print('Updating main sheet...')
    sheets_api.lb_players_to_main_sheet(main_worksheet, lb_players)

# PARAMS: .csv file containing usernames separated by newlines
# RETURN: none
def generate_usernames(filepath):
    osu_api = OsuAPIWrapper()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {osu_api.token}'
    }
    players = []
    non_matched_usernames = []
    with open(filepath, mode='r', newline='\n') as usernames_file:
        username_reader = csv.reader(usernames_file, delimiter=',')
        for row in username_reader:
            # Skip comment rows
            if row[0].startswith('#'):
                continue
            try:
                player_info = osu_api.get_user(row[0], headers)
                print('Found ID given username ' + row[0])
                if player_info[1] == row[0]:
                    players.append(player_info)
                else:
                    print('Searched player did not match given username \'' + row[0] + '\'')
                    non_matched_usernames.append(row[0] + ' - search returned \'' + player_info[1] + '\'')
            except KeyError:
                print('Couldn\'t find ID given username \'' + row[0] + '\'')
                non_matched_usernames.append(row[0] + ' - no results returned from search')
                continue

    with open('generated_playerlist.csv', mode='w', newline='\n') as playerlist_file:
        player_writer = csv.writer(playerlist_file, delimiter=',')
        for p in players:
            player_writer.writerow([p[0], p[1]])

    with open('non_matched_usernames.csv', mode='w', newline='\n') as nmu_file:
        nmu_writer = csv.writer(nmu_file, delimiter=',')
        for nmu_string in non_matched_usernames:
            nmu_writer.writerow([nmu_string])

# PARAMS: .csv file separated by newlines
# RETURNS: none
def remove_dupes(filepath):
    rows = []
    with open(filepath, mode='r', newline='\n') as dupes_file:
        dupes_reader = csv.reader(dupes_file, delimiter=',')
        for row in dupes_reader:
            # Skip comment rows
            if row[0].startswith('#'):
                continue
            rows.append(row)
    
    result = []
    for r in rows:
        if r not in result:
            result.append(r)
        else:
            print('Found dupe ' + str(r))

    with open(filepath, mode='w', newline='\n') as new_file:
        new_writer = csv.writer(new_file, delimiter=',')
        for r in result:
            new_writer.writerow(r)