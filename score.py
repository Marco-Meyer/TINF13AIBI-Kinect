import pickle

class Score():
    def __init__(self):
        self.current = 0
        self.highest = 0
        try:
            self.load()
        except IOError:
            print("No save.p found, so start Highscore = 0")
        except AttributeError:
            print("No 'first' in dict of save.p, so start Highscore = 0")
        except Exception as e:
            import warnings
            warnings.warn(str(e))
    def __iadd__(self, other):
        self.current += other
        self.highest = max(self.highest, self.current)
        return self
    def __repr__(self):
        return ("Score: %s   Highscore: %s" % (self.current, self.highest))
    def next_Round(self):
        self.current = 0
        self.game.scbar.refresh()
    def save(self):
        scorelist = { "first": self.highest }# I called this scorelist if we want to add something e.g. the ten best scores
        pickle.dump(scorelist, open("save.p","wb"),protocol = 2)
    def load(self):
        scorelist = pickle.load(open("save.p","rb"))
        #scorelist is now { "first": self.highest }
        self.highest = scorelist["first"]
