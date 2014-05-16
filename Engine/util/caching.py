def cache(func):
    c = None
    def newfunc():
        nonlocal c
        if not c:c = func()
        return c
    return newfunc

def precache(func):
    c = func()
    def newfunc():
        nonlocal c
        return c
    return newfunc

def cache_copy(func):
    c = None
    def newfunc():
        nonlocal c
        if not c:c = func()
        return c.copy()
    return newfunc

def cache_args(func):
    c = {}
    def newfunc(*args):
        nonlocal c
        if args not in c:c[args] = func(*args)
        return c[args]
    return newfunc

if __name__ == "__main__":
    from random import random
    @precache
    def r():return random()
    for _ in range(10):print(r())
