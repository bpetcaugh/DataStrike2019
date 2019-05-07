class Player():
    def __init__(self, r, color, name):
        self.resources = r
        self.game_color = color
        self.team_name = name

    def player_turn(self, game_stats):
        #In PROGRESS
        pass

    def get_resources(self):
        return self.resources

    def get_color(self):
        return self.game_color

    def get_name(self):
        return self.team_name

    def mod_resources(self, amount):
        self.resources += amount
