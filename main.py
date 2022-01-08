import sys
from scripts import archive
from scripts import submit

if __name__ == '__main__':
    # TODO: this is scuffed but its good for now
    if sys.argv[1] == 'update':
        if len(sys.argv) == 4:
            if sys.argv[2].rfind('@gmail.com') > 0:
                if sys.argv[3].lower() == 'true':
                    archive(sys.argv[2], True)
                elif sys.argv[3].lower() == 'false':
                    archive(sys.argv[2], False)
                else:
                    print('2nd argument should be one of "true" or "false"')
            else:
                print('1st argument should be a valid gmail address.')
        else:
            print('Invalid update arguments')
    
    elif sys.argv[1] == 'submit':
        if len(sys.argv) == 3:
            try:
                id = int(sys.argv[2])
                submit(int(sys.argv[2]))
            except ValueError:
                print('argument should be a valid score ID.')
        else:
            print('Invalid submit arguments')
    else:
        print('Invalid arguments')

# TODO: make it so update() checks submitted scores sheet -> inserts into dict -> scores_to_sheet runs
# TODO: make submit() nicer
# TODO: method descriptions for scripts

# TODO: "update leaderboard" scripts (looks @ worksheets)
# TODO: argparse library, usage, script robustness (what happens if invalid score ID, etc), etc.
# TODO: ids to usernames script
# TODO: share script

# TODO: hyperlink beatmap+player in mainsheet
# TODO: main page info tabs update, worksheet note
# TODO: print('Grabbing x's top plays...') -> username instead of id (without making more reqs)
# TODO: clean up remaining todos
# TODO: command line loading bar :3
# TODO: reduce api calls with gspread batch methods
# TODO: get_str_vals -> get_mod_col_range (do %s%s:%s%s in function, cut out middleman)
# TODO: change colour palette of sheet :3
# TODO: scores_to_sheet() change 2/4/6/8 to be like submit()