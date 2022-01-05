import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsWrapper():

    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        self.client = gspread.authorize(creds)

    # Thank you to 0e4ef622#2241 (on discord) for this function
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

    def create_sheet(self, sheet_name, email):
        sheet = self.client.create(sheet_name)
        sheet.share(email, perm_type='user', role='owner', notify=True)
        return sheet
     
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

        onemod_sheet = init_mod_ws('1mod', 7)
        twomod_sheet = init_mod_ws('2mod', 13)
        threemod_sheet = init_mod_ws('3mod', 12)
        fourmod_sheet = init_mod_ws('4mod', 4)

        return [onemod_sheet, twomod_sheet, threemod_sheet, fourmod_sheet]

    def scores_to_sheet(self, player_scores, worksheets):
        for k in player_scores:
            print(f'Putting {k} scores in the sheet...')
            num_scores = str(len(player_scores[k]) + 1)
            str_vals = self.get_str_vals(k, num_scores)
            col_range = '%s2:%s%s' % str_vals
            if len(k) == 2:
                worksheets[0].update(col_range, player_scores[k])
            elif len(k) == 4:
                worksheets[1].update(col_range, player_scores[k])
            elif len(k) == 6:
                worksheets[2].update(col_range, player_scores[k])
            elif len(k) == 8:
                worksheets[3].update(col_range, player_scores[k])
            else:
                raise KeyError('Key len != 2, 4, 6, 8')

    # TODO: top 5 worst functions i've ever written (FIX)
    def get_str_vals(self, mods, num_scores):
        # https://docs.google.com/spreadsheets/d/1mXSpmGrdJukGwq5VpE9O9vuLJktu35mBR5TIHdK_Jl0/edit#gid=721483945 (by Magnus Cosmos)
        one = ['NM', 'DT', 'HR', 'HD', 'EZ', 'HT', 'FL']
        two = ['HDDT', 'HRDT', 'EZDT', 'DTFL', 'EZHT', 'HDHR', 'HDHT', 'EZHD', 'HRHT', 'EZFL', 'HRFL', 'HTFL', 'HDFL']
        three = ['HDHRDT', 'HDDTFL', 'EZHDDT', 'HRDTFL', 'EZDTFL', 'HDHTFL', 'HDHRHT', 'HRHTFL', 'EZHDHT', 'EZHTFL', 'EZHDFL', 'HDHRFL']
        four = ['HDHRDTFL', 'EZHDDTFL', 'EZHDHTFL', 'HDHRHTFL']
        first = 1 # starting column
        length = 6 # num. data columns
        space = 1 # num. empty columns inbetween
        total = length + space

        def str_vals(start, end):
            return (self.colname(start), self.colname(end), num_scores)
        
        if mods == one[0] or mods == two[0] or mods == three[0] or mods == four[0]:
            return str_vals(first, length)

        elif mods == one[1] or mods == two[1] or mods == three[1] or mods == four[1]:
            return str_vals(first+total, length+total)

        elif mods == one[2] or mods == two[2] or mods == three[2] or mods == four[2]:
            return str_vals(first+total*2, length+total*2)

        elif mods == one[3] or mods == two[3] or mods == three[3] or mods == four[3]:
            return str_vals(first+total*3, length+total*3)

        elif mods == one[4] or mods == two[4] or mods == three[4]:
            return str_vals(first+total*4, length+total*4)

        elif mods == one[5] or mods == two[5] or mods == three[5]:
            return str_vals(first+total*5, length+total*5)

        elif mods == one[6] or mods == two[6] or mods == three[6]:
            return str_vals(first+total*6, length+total*6)

        elif mods == two[7] or mods == three[7]:
            return str_vals(first+total*7, length+total*7)

        elif mods == two[8] or mods == three[8]:
            return str_vals(first+total*8, length+total*8)

        elif mods == two[9] or mods == three[9]:
            return str_vals(first+total*9, length+total*9)

        elif mods == two[10] or mods == three[10]:
            return str_vals(first+total*10, length+total*10)

        elif mods == two[11] or mods == three[11]:
            return str_vals(first+total*11, length+total*11)

        elif mods == two[12]:
            return str_vals(first+total*12, length+total*12)

        else:
            raise KeyError('Invalid mods parameter')
        
