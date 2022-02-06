import sys
from scripts import archive
from scripts import submit
from scripts import update_leaderboard
from scripts import generate_usernames
from scripts import remove_dupes

if __name__ == '__main__':
    # TODO: this is scuffed but its good for now
    if len(sys.argv) == 1:
        print('Must specify a script: archive, submit, updatelb')

    elif sys.argv[1] == 'archive':
        if len(sys.argv) == 5:
            if sys.argv[2].rfind('@gmail.com') > 0:
                if sys.argv[3].rfind('.csv') > 0:
                    if sys.argv[4].lower() == 'true':
                        archive(sys.argv[2], sys.argv[3], True)
                        print('! Remember to update the leaderboard !')
                    elif sys.argv[4].lower() == 'false':
                        archive(sys.argv[2], sys.argv[3], False)
                    else:
                        print('3rd argument should be one of "true" or "false"')
                else:
                    print('2nd argument should be a .csv file containing user IDs')
            else:
                print('1st argument should be a valid gmail address')
        else:
            print('Invalid update arguments')
    
    elif sys.argv[1] == 'submit':
        if len(sys.argv) == 3:
            try:
                id = int(sys.argv[2])
                submit(int(sys.argv[2]))
                print('! Remember to update the leaderboard !')
            except ValueError:
                print('argument should be a valid score ID.')
        else:
            print('Invalid submit arguments')

    elif sys.argv[1] == 'updatelb':
        if len(sys.argv) == 2:
            update_leaderboard()
        else:
            print('There should be no arguments!')

    # not really for general use
    elif sys.argv[1] == 'usernames':
        if len(sys.argv) == 3:
            if sys.argv[2].rfind('.csv') > 0:
                generate_usernames(sys.argv[2])
            else:
                print('1st argument should be a .csv file containing player usernames')
        else:
            print('Invalid usernames arguments')

    # not really for general use
    elif sys.argv[1] == 'remove_dupes':
        if len(sys.argv) == 3:
            if sys.argv[2].rfind('.csv') > 0:
                remove_dupes(sys.argv[2])
            else:
                print('1st argument should be a .csv file')
        else:
            print('Invalid remove_dupes arguments')
        
    else:
        print('Invalid arguments')