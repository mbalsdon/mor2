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

    # Create the sheet
    print('Creating archive sheet...')
    sheet_title = f'mouseonlyrecords archive {date.today().strftime("%x")}'
    user_email = 'minermathew@gmail.com' # TODO: paramaterize as user input
    archive_sheet = sheets_api.create_sheet(sheet_title, user_email)

    # Create worksheets
    print('Initializing worksheets...')
    worksheets = sheets_api.init_mod_worksheets(archive_sheet)
    onemod_sheet = worksheets[0]
    twomod_sheet = worksheets[1]
    threemod_sheet = worksheets[2]
    fourmod_sheet = worksheets[3]

    # Create a dict of player scores with mod combo as the key
    print('Collecting and sorting player scores...')
    player_ids = osu_api.get_player_ids('testplayerlist.csv') # TODO: switch file
    player_scores = osu_api.get_top_plays(player_ids, headers)

    sheets_api.scores_to_sheet(player_scores, worksheets)

if __name__ == '__main__':
    main()

# TODO: complete refactoring (push to github)
# TODO: method signatures
# TODO: functionality for updating main sheet, email needs to be authorized on it
# TODO: make script run w user input (email, updatemain?, etc)
# TODO: "update leaderboard" scripts (need to consider submitted scores)
# TODO: score submission: goes to own worksheet, somehow need to insert into archive part
# TODO: 