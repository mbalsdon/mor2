class SimpleScore():
    def __init__(self, username, mods, beatmap, diffname, pp, acc):
        self.username = username # string
        self.mods = mods # string
        self.beatmap = beatmap # string
        self.diffname = diffname # string
        self.pp = pp # number
        self.acc = acc # number

    def get_username(self):
        return self.username

    def get_mods(self):
        return self.mods

    def get_beatmap(self):
        return self.beatmap

    def get_diffname(self):
        return self.diffname

    def get_pp(self):
        return self.pp
    
    def get_acc(self):
        return self.acc

    # TODO: probably just get rid of SimpleScore eventually if this what we doing
    def to_array(self):
        return [self.username, self.mods, self.beatmap, self.diffname, self.pp, self.acc]