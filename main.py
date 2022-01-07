from OsuAPIWrapper import OsuAPIWrapper
from SheetsWrapper import SheetsWrapper
from datetime import date

def main():
    # Initialize osu api
    osu_api = OsuAPIWrapper()
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {osu_api.token}'
    }
    
    # Initialize sheets api
    print('Initializing Sheets API...')
    sheets_api = SheetsWrapper()

    # Create the archive sheet
    print('Creating archive sheet...')
    sheet_title = f'mouseonlyrecords archive {date.today().strftime("[%d %b %Y]").upper()}'
    user_email = 'minermathew@gmail.com' # TODO: paramaterize as user input
    archive_sheet = sheets_api.create_sheet(sheet_title, user_email)

    # Create archive worksheets
    print('Initializing archive worksheets...')
    archive_worksheets = sheets_api.init_mod_worksheets(archive_sheet)

    # Create a dict of player scores with mod combo as the key
    print('Collecting and sorting player scores...')
    player_ids = osu_api.get_player_ids('testplayerlist.csv') # TODO: switch file
    player_scores = osu_api.get_top_plays(player_ids, headers)
    

    # Put the scores in the archive sheet
    print('Putting scores in the archive sheet...')
    sheets_api.scores_to_sheet(player_scores, archive_worksheets, 1, 2, 6, 1)

    # Put the scores in the main sheet
    print('Putting scores in the main sheet...')
    main_sheet = sheets_api.get_mor_sheet()
    main_worksheets = [main_sheet.worksheet('1MOD'),
                       main_sheet.worksheet('2MOD'),
                       main_sheet.worksheet('3MOD'),
                       main_sheet.worksheet('4MOD')]
    reformatted_player_scores = osu_api.archive_to_main(player_scores)
    sheets_api.scores_to_sheet(reformatted_player_scores, main_worksheets, 4, 8, 3, 1)
    sheets_api.update_last_updated_tag(main_worksheets)

if __name__ == '__main__':
    main()

# TODO: less work done in main.py
# TODO: make script run w user input (email, updatemain?, etc)
# TODO: score submission script: goes to own worksheet in main, inserts in relevant worksheet
# TODO: make it so script checks submitted scores sheet -> inserts into dict -> scores_to_sheet runs
# TODO: "update leaderboard" scripts (looks @ worksheets)
# TODO: share script
# TODO: hyperlink beatmap+player in mainsheet
# TODO: main page info tabs update, worksheet note
# TODO: release ?