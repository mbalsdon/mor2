import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

class SheetsWrapper():

    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        self.client = gspread.authorize(creds)

    # Thanks 0e4ef622#2241 (on discord) for this function
    # PARAMS: column number (int)
    # RETURN: column letter (str)
    def colname(self, n):
        # n += 1
        name = ""
        digit = ".ABCDEFGHIJKLMNOPQRSTUVWXY"
        while n > 0:
            if n % 26 == 0:
                n -= 26
                name += "Z"
            else:
                name += digit[n % 26]
            n //= 26
        return name[::-1]

    # PARAMS: title of sheet (str), email of sheet owner (str)
    # RETURN: the created sheet (gspread sheet)
    def create_sheet(self, sheet_name, email):
        sheet = self.client.create(sheet_name)
        sheet.share(email, perm_type='user', role='owner', notify=True)
        return sheet

    # PARAMS: none
    # RETURN: mouseonlyrecords v2 sheet (gspread sheet)
    def get_mor_sheet(self):
        return self.client.open('mouseonlyrecords v2')
    
    # Sets up the 1mod/2mod/3mod/4mod worksheets, ready for scores to be input to them
    # PARAMS: the sheet to be edited (gspread sheet)
    # RETURN: the created worksheets (array of gspread worksheets)
    def init_mod_worksheets(self, sheet):
        num_rows = '10000'
        num_cols = '100'
        title_row = ['USER', 'MODS', 'MAP', 'DIFF', 'PP', 'ACC', '']

        def init_mod_ws(title, num_mod_combos):
            mod_sheet = sheet.add_worksheet(title=title, rows=num_rows, cols=num_cols)
            num_cols_needed = num_mod_combos * len(title_row)
            col_range = f'{self.colname(1)}1:{self.colname(num_cols_needed)}1'
            mod_sheet.update(col_range, [title_row * num_mod_combos])
            return mod_sheet

        onemod_sheet = init_mod_ws('1MOD', 7)
        twomod_sheet = init_mod_ws('2MOD', 13)
        threemod_sheet = init_mod_ws('3MOD', 12)
        fourmod_sheet = init_mod_ws('4MOD', 4)
        # remove the default sheet
        sheet.del_worksheet(sheet.sheet1)

        return [onemod_sheet, twomod_sheet, threemod_sheet, fourmod_sheet]
    
    # PARAMS: player scores dict (keys = mod combos (str), vals = scores (array of tuples)), 
    #         worksheets to put scores in (array of gspread worksheet),
    #         first col (int), first row (int), num. cols used per mod (int),
    #         num. blank cols between mods (int)
    def scores_to_sheet(self, player_scores, worksheets, first_col, first_row, length, space):
        for k in player_scores:
            print(f'Putting {k} scores in...')
            num_scores = str(len(player_scores[k]) + first_row - 1)
            str_vals = self.get_str_vals(k, num_scores, first_col, first_row, length, space)
            col_range = '%s%s:%s%s' % str_vals
            size = len(col_range)
            last_size = len(str_vals[3])
            clear_col_range = col_range[:size - last_size] + '10000'
            # worksheets[int((len(k)/2)-1)].update(col_range, player_scores[k])
            if len(k) == 2:
                worksheets[0].batch_clear([clear_col_range])
                worksheets[0].update(col_range, player_scores[k])
            elif len(k) == 4:
                worksheets[1].batch_clear([clear_col_range])
                worksheets[1].update(col_range, player_scores[k])
            elif len(k) == 6:
                worksheets[2].batch_clear([clear_col_range])
                worksheets[2].update(col_range, player_scores[k])
            elif len(k) == 8:
                worksheets[3].batch_clear([clear_col_range])
                worksheets[3].update(col_range, player_scores[k])
            else:
                raise KeyError('key len != 2/4/6/8')

    # PARAMS: mod combo (str), number of scores with specified mod combo (int),
    #         first col (int), first row (int), num. cols taken per mod (int),
    #         num. blank cols between mods (int)
    # RETURN: start column letter, start row num, end column letter, end row num (tuple: (str, int, str, int))
    # TODO: this is a terribly written method
    def get_str_vals(self, mods, num_scores, first_col, first_row, length, space):
        # https://docs.google.com/spreadsheets/d/1mXSpmGrdJukGwq5VpE9O9vuLJktu35mBR5TIHdK_Jl0/edit#gid=721483945 (by Magnus Cosmos)
        one = ['NM', 'DT', 'HR', 'HD', 'EZ', 'HT', 'FL']
        two = ['HDDT', 'HRDT', 'EZDT', 'DTFL', 'EZHT', 'HDHR', 'HDHT', 'EZHD', 'HRHT', 'EZFL', 'HRFL', 'HTFL', 'HDFL']
        three = ['HDHRDT', 'HDDTFL', 'EZHDDT', 'HRDTFL', 'EZDTFL', 'HDHTFL', 'HDHRHT', 'HRHTFL', 'EZHDHT', 'EZHTFL', 'EZHDFL', 'HDHRFL']
        four = ['HDHRDTFL', 'EZHDDTFL', 'EZHDHTFL', 'HDHRHTFL']
        total = length + space
        last_col = first_col+length-1

        def str_vals(start, end):
            return (self.colname(start), first_row, self.colname(end), num_scores)
        
        if mods == one[0] or mods == two[0] or mods == three[0] or mods == four[0]:
            return str_vals(first_col, last_col)
        elif mods == one[1] or mods == two[1] or mods == three[1] or mods == four[1]:
            return str_vals(first_col+total, last_col+total)
        elif mods == one[2] or mods == two[2] or mods == three[2] or mods == four[2]:
            return str_vals(first_col+total*2, last_col+total*2)
        elif mods == one[3] or mods == two[3] or mods == three[3] or mods == four[3]:
            return str_vals(first_col+total*3, last_col+total*3)
        elif mods == one[4] or mods == two[4] or mods == three[4]:
            return str_vals(first_col+total*4, last_col+total*4)
        elif mods == one[5] or mods == two[5] or mods == three[5]:
            return str_vals(first_col+total*5, last_col+total*5)
        elif mods == one[6] or mods == two[6] or mods == three[6]:
            return str_vals(first_col+total*6, last_col+total*6)
        elif mods == two[7] or mods == three[7]:
            return str_vals(first_col+total*7, last_col+total*7)
        elif mods == two[8] or mods == three[8]:
            return str_vals(first_col+total*8, last_col+total*8)
        elif mods == two[9] or mods == three[9]:
            return str_vals(first_col+total*9, last_col+total*9)
        elif mods == two[10] or mods == three[10]:
            return str_vals(first_col+total*10, last_col+total*10)
        elif mods == two[11] or mods == three[11]:
            return str_vals(first_col+total*11, last_col+total*11)
        elif mods == two[12]:
            return str_vals(first_col+total*12, last_col+total*12)
        else:
            raise KeyError('Invalid mods parameter')

    # PARAMS: main sheet worksheets (array of gspread worksheet)
    # RETURN: none
    def update_last_updated_tag(self, main_worksheets):
        for worksheet in main_worksheets:
            worksheet.update('B6', f'LAST UPDATE: {date.today().strftime("%d %B %Y").upper()}')

    # TODO: def
    def lb_players_to_main_sheet(self, main_sheet, lb_players):
        lb_array = []
        for k in lb_players:
            lb_array.append((k, lb_players[k]))
        print(lb_array)
        lb_array.sort(reverse=True, key=lambda s: s[1])
        main_sheet.update('L6:M113', lb_array)