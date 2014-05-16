from functools import total_ordering
@total_ordering
class Version():
        
        def __init__(self, integer):
            self.int = integer
        def get_version_tuple(self):
            major, minor = divmod(self.int,10000)
            minor, micro = divmod(minor, 100)
            return major, minor, micro
        
        def get_name(self):
            return ".".join((str(i) for i in self.get_version_tuple()))
        
        def __repr__(self):
            return self.name
        
        def __eq__(self, other):
            if isinstance(other, Version):
                return self.int == other.int
            return self.int == other
        
        def __lt__(self, other):
            if isinstance(other, Version):
                return self.int < other.int
            return self.int < other
        
        name = property(get_name)
        as_tuple = property(get_version_tuple)

current = Version(100)


if __name__ == "__main__":
    print (current)
    print (current > 200)
    print (current < 100)
    print (current > Version(50))
    assert(Version(100) > 99)
    assert(99 < Version(100))
    assert(100 == Version(100))
    assert(100 != Version(99))
    assert(Version(100) == Version(100))
