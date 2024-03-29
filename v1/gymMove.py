import numpy as np
import time
import math

# counter
leftcounter = 0
rightcounter = 0
leftstage = None
rightstage = None

counter = 0
stage = None

plank_starttime = None
plank_currenttime = None

leftmark = 0
rightmark = 0

hold_time = 0

def calc_angle(a, b, c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360.0 - angle
    
    return angle

def clear():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global counter
    global stage
    global plank_starttime
    global plank_currenttime
    global leftmark
    global rightmark
    global hold_time
    leftcounter = 0
    rightcounter = 0
    leftstage = None
    rightstage = None
    counter = 0
    stage = None
    plank_starttime = None
    plank_currenttime = None
    leftmark = 0
    rightmark = 0
    hold_time = 0

# 二頭肌

def curl():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark

    std = 20
    try: 
        # left
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if leftangle > 120 and leftstage == 'up':
            leftstage = 'down'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 50)
            print('leftmark:', leftmark)
            leftmark = 100000
        elif leftangle > 120:
            leftstage = 'down'
            leftmark = 100000
        elif leftangle < 70 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1

        if leftangle < 70:
            if leftmark > leftangle:
                leftmark = leftangle
        
        if rightangle > 120 and rightstage == 'up':
            rightstage = 'down'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 50)
            print('rightmark:', rightmark)
            rightmark = 100000
        elif rightangle > 120:
            rightstage = 'down'
            rightmark = 100000
        elif rightangle < 70 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1

        if rightangle < 70:
            if rightmark > rightangle:
                rightmark = rightangle
        
        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None
# 三頭肌

def triceps_extension():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark

    std = 180

    try:
        # left
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if leftangle < 100 and leftstage == 'down':
            leftstage = 'up'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 40)
            print('leftmark:', leftmark)
            leftmark = 0
        elif leftangle < 100:
            leftstage = 'up'
            leftmark = 0
        elif leftangle > 140 and leftstage == 'up':
            leftstage = 'down'
            leftcounter += 1
        
        if leftangle > 140:
            if leftmark < leftangle:
                leftmark = leftangle
        
        if rightangle < 100 and rightstage == 'down':
            rightstage = 'up'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 40)
            print('rightmark:', rightmark)
            rightmark = 0
        elif rightangle < 100:
            rightstage = 'up'
            rightmark = 0
        elif rightangle > 140 and rightstage == 'up':
            rightstage = 'down'
            rightcounter += 1
        
        if rightangle > 140:
            if rightmark < rightangle:
                rightmark = rightangle

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 大腿

def squat():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark

    std = 120

    try:
        # left
        leftangle = calc_angle(lefthip, leftknee, leftankle)
        # right
        rightangle = calc_angle(righthip, rightknee, rightankle)
        
        # counter logic
        if leftangle > 170 and leftstage == 'down':
            leftstage = 'up'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 75)
            print('leftmark:', leftmark)
            leftmark = 100000
        elif leftangle > 170:
            leftstage = 'up'
            leftmark = 100000
        elif leftangle < 150 and leftstage == 'up':
            leftstage = 'down'
            leftcounter += 1

        if leftangle < 150:
            if leftmark > leftangle:
                leftmark = leftangle
        
        if rightangle > 170 and rightstage == 'down':
            rightstage = 'up'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 80)
            print('rightmark:', rightmark)
            rightmark = 100000
        elif rightangle > 170:
            rightstage = 'up'
            rightmark = 100000
        elif rightangle < 150 and rightstage == 'up':
            rightstage = 'down'
            rightcounter += 1

        if rightangle < 150:
            if rightmark > rightangle:
                rightmark = rightangle

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 小腿

def tiptoe():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark

    std = 135

    try:
        # left
        leftangle = calc_angle(leftknee, leftankle, left_foot_index)
        # right
        rightangle = calc_angle(rightknee, rightankle, right_foot_index)

        # counter logic
        if leftangle < 120 and leftstage == 'up':
            leftstage = 'down'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 10)
            print('leftmark:', leftmark)
            leftmark = 0
        elif leftangle < 120:
            leftstage = 'down'
            leftmark = 0
        elif leftangle > 130 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1

        if leftangle > 130:
            if leftmark < leftangle:
                leftmark = leftangle

        if rightangle < 120 and rightstage == 'up':
            rightstage = 'down'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 10)
            print('rightmark:', rightmark)
            rightmark = 0
        elif rightangle < 120:
            rightstage = 'down'
            rightmark = 0
        elif rightangle > 130 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1

        if rightangle > 130:
            if rightmark < rightangle:
                rightmark = rightangle

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 肩膀

def Dumbbell_Lateral_Raise():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark

    std = 80
    try:
        # left
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if leftangle > 140 and leftstage == None:
            leftmark = 100000
        if leftangle < 95:
            leftstage = 'down'
        elif leftangle > 140 and leftstage == 'down':
            leftstage = 'up'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 80)
            print('leftmark:', leftmark)
            leftmark = 100000
            leftcounter += 1

        if leftangle < 95:
            if leftmark > leftangle:
                leftmark = leftangle

        if rightangle > 140 and rightstage == None:
            rightmark = 100000
        if rightangle < 95:
            rightstage = 'down'
        elif rightangle > 140 and rightstage == 'down':
            rightstage = 'up'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 80)
            print('rightmark:', rightmark)
            rightmark = 100000
            rightcounter += 1

        if rightangle < 95:
            if rightmark > rightangle:
                rightmark = rightangle

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

def Dumbbell_Shoulder_Press():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark
    

    std = 90
    
    try:
        # left
        leftangle = calc_angle(lefthip, leftshoulder, leftelbow)
        # right
        rightangle = calc_angle(righthip, rightshoulder, rightelbow)
        
        # counter logic
        if leftangle < 20 and leftstage == 'up':
            leftstage = 'down'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 40)
            print('leftmark:', leftmark)
            leftmark = 0
        elif leftangle < 20:
            leftstage = 'down'
            leftmark = 0
        elif leftangle > 50 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if leftangle > 50 :
            if leftmark < leftangle:
                leftmark = leftangle

        if rightangle < 20 and rightstage == 'up':
            rightstage = 'down'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 40)
            print('rightmark:', rightmark)
            rightmark = 0
        elif rightangle < 20:
            rightstage = 'down'
            rightmark = 0
        elif rightangle > 50 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1
        
        if rightangle > 50 :
            if rightmark < rightangle:
                rightmark = rightangle


        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 背部

def one_arm_row():
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    global leftmark
    global rightmark
    
    std = 55

    try:
        # left
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        left_move_angle = calc_angle(lefthip, leftshoulder, leftelbow)
        # right
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)
        right_move_angle = calc_angle(righthip, rightshoulder, rightelbow)
        
        # counter logic
        if leftangle > 160 and left_move_angle <= 45 and leftstage == 'up':
            leftstage = 'down'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 20)
            print('leftmark:', leftmark)
            leftmark = 0
        elif leftangle > 160 and left_move_angle <= 45:
            leftstage = 'down'
            leftmark = 0
        elif leftangle < 120 and left_move_angle >= 35 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1

        if leftangle < 120 and left_move_angle >= 35:
            if leftmark < left_move_angle:
                leftmark = left_move_angle

        if rightangle > 160 and right_move_angle <= 45 and rightstage == 'up':
            rightstage = 'down'
            rightmark = math.sqrt((rightmark - std) * (rightmark - std)) 
            rightmark = 100 - int(rightmark * 100 / 20)
            print('rightmark:', rightmark)
            rightmark = 0
        elif rightangle > 160 and right_move_angle <= 45:
            rightstage = 'down'
            rightmark = 0
        elif rightangle < 120 and right_move_angle >= 35 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1

        if rightangle < 120 and right_move_angle >= 35:
            if rightmark < right_move_angle:
                rightmark = right_move_angle

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 核心

def plank():
    global plank_starttime
    global plank_currenttime
    global stage
    global hold_time
    
    std = 170
    try:
        # left
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)
        
        angle = calc_angle(leftshoulder, lefthip, leftankle)

        # counter logic
        if stage == None:
            stage = 'down'
            hold_time = 0
        elif 70 <= leftangle <= 120 and 70 <= rightangle <= 120 and angle >= 150 and stage == 'down':
            stage = 'up'
            plank_starttime = time.time()
        elif 70 <= leftangle <= 120 and 70 <= rightangle <= 120 and angle >= 150:
            pass
        else:
            stage = 'down'
            plank_starttime = time.time()
        
        if time.time() - plank_starttime >= 1:
            plank_starttime = time.time()
            leftmark = angle
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 40)
            print('leftmark:', leftmark)
            hold_time += 1 

        return (hold_time, hold_time, stage, stage)
    except:
        return None

def starjump():
    global counter
    global stage
    global leftmark
    try:
        # left hand
        left_hand_angle = calc_angle(leftwrist, leftshoulder, lefthip)
        # right hand
        right_hand_angle = calc_angle(rightwrist, rightshoulder, righthip)
        # leg
        left_leg_angle = calc_angle(leftknee, lefthip, rightknee)
        right_leg_angle = calc_angle(leftknee, righthip, rightknee)
        leg_angle = int((left_leg_angle + right_leg_angle) / 2)
        
        std = 170

        # counter logic
        if left_hand_angle < 80 and right_hand_angle < 80 and leg_angle < 30 and stage == 'up':
            stage = 'down'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 20)
            print('leftmark:', leftmark)
            leftmark = 0
        elif left_hand_angle < 80 and right_hand_angle < 80 and leg_angle < 30:
            stage = 'down'
            leftmark = 0
        elif left_hand_angle > 150 and right_hand_angle > 150 and leg_angle >= 30 and stage == 'down':
            stage = 'up'
            counter += 1
        
        if left_hand_angle > 150 and right_hand_angle > 150 and leg_angle >= 30:
            if leftmark < left_hand_angle and leftmark < right_hand_angle:
                leftmark = (left_hand_angle + right_hand_angle) // 2

        return (counter, counter, stage, stage)
    except:
        return None

# 胸部
def pushup():
    global counter
    global stage
    global leftmark

    std = 65
    try:
        # left
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        angle = calc_angle(leftshoulder, lefthip, leftankle)

        # counter logic
        if 50 <= leftangle <= 100 and 50 <= rightangle <= 100 and angle >= 150:
            stage = 'down'
        elif leftangle > 150 and rightangle > 150 and stage == None:
            stage = 'up'
            leftmark = 100000
        elif leftangle > 150 and rightangle > 150 and stage == 'down':
            stage = 'up'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 35)
            print('leftmark:', leftmark)
            leftmark = 100000
            counter += 1
        
        if 50 <= leftangle <= 100 and 50 <= rightangle <= 100 and angle >= 150:
            if leftmark > leftangle:
                leftmark = leftangle

        return (counter, counter, stage, stage)
    except:
        return None

# 腹肌
def reverse_crunch():
    global counter
    global stage
    global leftmark

    std = 60
    try:
        # left
        leftangle = calc_angle(leftshoulder, lefthip, leftknee)
        # right
        rightangle = calc_angle(rightshoulder, righthip, rightknee)

        # curl counter logic
        if leftangle > 100 and rightangle > 100 and stage == None:
            stage = 'up'
            leftmark = 100000
        elif leftangle > 100 and rightangle > 100 and stage == 'down':
            stage = 'up'
            leftmark = math.sqrt((leftmark - std) * (leftmark - std)) 
            leftmark = 100 - int(leftmark * 100 / 20)
            print('leftmark:', leftmark)
            leftmark = 100000
        elif leftangle < 80 and rightangle < 80 and stage == 'up':
            stage = 'down'
            counter += 1
        
        if leftangle < 80 and rightangle < 80:
            if leftmark > leftangle:
                leftmark = leftangle

        return (leftangle, counter, counter, stage, stage)
    except:
        return None

nose = None
left_eye_inner = None
left_eye = None
left_eye_outer = None
right_eye_inner = None
right_eye = None
right_eye_outer = None
leftear = None
rightear = None
mouthleft = None
mouthright = None
leftshoulder = None
rightshoulder = None
leftelbow = None
rightelbow = None
leftwrist = None
rightwrist = None
leftpinky = None
rightpinky = None
leftindex = None
rightindex = None
leftthumb = None
rightthumb = None
lefthip = None
righthip = None
leftknee = None
rightknee = None
leftankle = None
rightankle = None
leftheel = None
rightheel = None
left_foot_index = None
right_foot_index = None

def update(landmarks, mp_pose):
    global nose
    global left_eye_inner
    global left_eye
    global left_eye_outer
    global right_eye_inner
    global right_eye
    global right_eye_outer
    global leftear
    global rightear
    global mouthleft
    global mouthright
    global leftshoulder
    global rightshoulder
    global leftelbow
    global rightelbow
    global leftwrist
    global rightwrist
    global leftpinky
    global rightpinky
    global leftindex
    global rightindex
    global leftthumb
    global rightthumb
    global lefthip
    global righthip
    global leftknee
    global rightknee
    global leftankle
    global rightankle
    global leftheel
    global rightheel
    global left_foot_index
    global right_foot_index

    nose = (landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y)
    left_eye_inner = (landmarks[mp_pose.PoseLandmark.LEFT_EYE_INNER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE_INNER.value].y)
    left_eye = (landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y)
    left_eye_outer = (landmarks[mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].y)
    right_eye_inner = (landmarks[mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].y)
    right_eye = (landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y)
    right_eye_outer = (landmarks[mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value].y)
    leftear = (landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y)
    rightear = (landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y)
    mouthleft = (landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y)
    mouthright = (landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x, landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].y)
    leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
    rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
    leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
    rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
    leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
    rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
    leftpinky = (landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].x, landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].y)
    rightpinky = (landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].y)
    leftindex = (landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y)
    rightindex = (landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y)
    leftthumb = (landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].x, landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].y)
    rightthumb = (landmarks[mp_pose.PoseLandmark.RIGHT_THUMB.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_THUMB.value].y)
    lefthip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
    righthip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
    leftknee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
    rightknee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
    leftankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
    rightankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
    leftheel = (landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y)
    rightheel = (landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y)
    left_foot_index = (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y)
    right_foot_index = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y)


'''def check(landmarks, mp_pose):
    print(nose,
    left_eye_inner,
    left_eye,
    left_eye_outer,
    right_eye_inner,
    right_eye,
    right_eye_outer,
    leftear,
    rightear,
    mouthleft,
    mouthright,
    leftshoulder,
    rightshoulder,
    leftelbow,
    rightelbow,
    leftwrist,
    rightwrist,
    leftpinky,
    rightpinky,
    leftindex,
    rightindex,
    leftthumb,
    rightthumb,
    lefthip,
    righthip,
    leftknee,
    rightknee,
    leftankle,
    rightankle,
    leftheel,
    rightheel,
    left_foot_index,
    right_foot_index)
'''