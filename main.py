import sys
from scripts import archive
from scripts import submit

if __name__ == '__main__':
    # TODO: this is scuffed but its good for now
    if sys.argv[1] == 'archive':
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
