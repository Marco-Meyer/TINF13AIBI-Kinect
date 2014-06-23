from vec2d import vec2d
tolerance = 10

def get_direction(angle, tolerance):
    if (90-tolerance > angle % 90 > tolerance):return -1
    return int((angle%360+45)//90) % 4
    
    
#dataset = [get_direction(int(vec2d.fromangle1(x).angle), tolerance) for x in range(360)]

if __name__ == "__main__":
    for x in range(360):
        print(x, get_direction(vec2d.fromangle1(x).angle, 10))

        
