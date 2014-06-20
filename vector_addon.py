from vec2d import vec2d
tolerance = 10

def get_direction(angle, tolerance):
    if angle % 90 < 10 or angle%90 > 80:
        dire = (angle%360+45)//90
        if dire == 4:dire = 0
        return int(dire)
    else:return -1
    
    
#dataset = [get_direction(int(vec2d.fromangle1(x).angle), tolerance) for x in range(360)]

if __name__ == "__main__":
    for x in range(360):
        print(x, get_direction(vec2d.fromangle1(x).angle, 10))

        
