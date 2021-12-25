class SimpleScore():
    def __init__(self, username, mods, beatmap, pp):
        self.username = username # string
        self.mods = mods # string
        self.beatmap = beatmap # string
        self.pp = pp # number

    def get_username(self):
        return self.username

    def get_mods(self):
        return self.mods

    def get_beatmap(self):
        return self.beatmap

    def get_pp(self):
        return self.pp