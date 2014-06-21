
try:
    from cvec2d import vec2d
    print("Using C-Extension vectors")

except:
    import traceback
    traceback.print_exc()
    import sys
    if sys.version_info >= (3, 0):
        from ._vec2d import vec2d
    else:
        from _vec2d import vec2d
    del(sys)
    print ("Could not load compiled vectors, using Python vectors")
