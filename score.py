
class Score():
    def __init__(self):
        
        self.current = 0
        self.highest = 0
    def __iadd__(self, other):
        self.current += other
        self.highest = max(self.highest, self.current)
        return self
    def __repr__(self):
        return ("Score: %s   Highscore: %s" % (self.current, self.highest))
    def next_Round(self):
        self.current = 0
        self.game.scbar.refresh()
