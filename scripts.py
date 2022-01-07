from datetime import date
from OsuAPIWrapper import OsuAPIWrapper
from SheetsWrapper import SheetsWrapper

# PARAMS: email of archive sheet owner (str), should main sheet be updated? (boolean)
# RETURN: none
def archive(email, update_main):

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

    # This is done after making the archive sheet to allow the sheets API to
    # "cool down" since there is a limit on requests per minute.
    print('Collecting and sorting player scores...')
    player_ids = osu_api.get_player_ids('testplayerlist.csv') # TODO: switch file
    player_scores = osu_api.get_top_plays(player_ids, headers)
    
    print('Putting scores in the archive sheet...')
    sheets_api.scores_to_sheet(player_scores, archive_worksheets, 1, 2, 6, 1)

    if update_main == True:
        print('Putting scores in the main sheet...')
        main_sheet = sheets_api.get_mor_sheet()
        main_worksheets = [main_sheet.worksheet('1MOD'),
                        main_sheet.worksheet('2MOD'),
                        main_sheet.worksheet('3MOD'),
                        main_sheet.worksheet('4MOD')]
        reformatted_player_scores = osu_api.archive_to_main(player_scores)
        sheets_api.scores_to_sheet(reformatted_player_scores, main_worksheets, 4, 8, 3, 1)
        sheets_api.update_last_updated_tag(main_worksheets)

# TODO: this
# PARAMS:
# RETURN: none
def submit():
    return