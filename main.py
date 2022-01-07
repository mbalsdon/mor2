import sys
from scripts import archive

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
    else:
        print('Invalid arguments')

# TODO: score submission script: goes to own worksheet in main, inserts in relevant worksheet
# TODO: make it so script checks submitted scores sheet -> inserts into dict -> scores_to_sheet runs
# TODO: "update leaderboard" scripts (looks @ worksheets)
# TODO: share script
# TODO: hyperlink beatmap+player in mainsheet
# TODO: main page info tabs update, worksheet note
# TODO: print('Grabbing x's top plays...') -> username instead of id (without making more reqs)
# TODO: release ?
# TODO: clean up remaining todos
# TODO: command line loading bar :3
# TODO: ids to usernames script
# TODO: argparse library