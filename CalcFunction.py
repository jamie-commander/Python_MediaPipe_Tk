import math

def calc_angle(x1, y1, x2, y2): #計算x1y1與x2y2之間的角度
    x = abs(x1 - x2)
    y = abs(y1 - y2)
    z = math.sqrt(x * x + y * y)
    
    angle = round(math.asin(y / z) / math.pi * 180)
    return angle

#直綫方程式
def calc_on_line(x, y, x1, y1, x2, y2): #計算x y 是否在 x1y1與x2y2所組成的綫上
    angle = calc_angle(x1, y1, x2, y2)
    diff = math.sqrt(abs((x - x1) * (y2 - y1) - (x2 - x1) * (y - y1)))
    # 如果 diff = 0, 説明在x y在綫上
    # 但是 diff = 0 是理想值, 因此計算偏差
    #-----------------門檻值 Hyperparameter--------------------
    # 可更改
    threshold_angle = 10 
    threshold_diff = 110
    #------------------------------------------------

    return (angle <= threshold_angle and diff <= threshold_diff)