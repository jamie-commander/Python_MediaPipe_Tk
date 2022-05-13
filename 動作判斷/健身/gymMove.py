import numpy as np
import time

# counter
leftcounter = 0
rightcounter = 0
leftstage = None
rightstage = None

counter = 0
stage = None

plank_starttime = None
plank_currenttime = None


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
    leftcounter = 0
    rightcounter = 0
    leftstage = None
    rightstage = None
    counter = 0
    stage = None
    plank_starttime = None
    plank_currenttime = None

# 二頭肌

def curl(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try: 
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if leftangle > 160:
            leftstage = 'down'
        if leftangle < 30 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if rightangle > 160:
            rightstage = 'down'
        if rightangle < 30 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1
        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None
# 三頭肌

def triceps_extension(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if leftangle < 100:
            leftstage = 'up'
        if leftangle > 160 and leftstage == 'up':
            leftstage = 'down'
            leftcounter += 1
        
        if rightangle < 100:
            rightstage = 'up'
        if rightangle > 160 and rightstage == 'up':
            rightstage = 'down'
            rightcounter += 1
        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 大腿

def squat(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        lefthip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
        leftknee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
        leftankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
        leftangle = calc_angle(lefthip, leftknee, leftankle)
        # right
        righthip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
        rightknee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
        rightankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
        rightangle = calc_angle(righthip, rightknee, rightankle)
        
        # counter logic
        if leftangle > 170:
            leftstage = 'up'
        if leftangle < 140 and leftstage == 'up':
            leftstage = 'down'
            leftcounter += 1
        
        if rightangle > 170:
            rightstage = 'up'
        if rightangle < 140 and rightstage == 'up':
            rightstage = 'down'
            rightcounter += 1
        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 小腿

def tiptoe(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        leftknee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
        leftankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
        leftfoot = (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y)
        leftangle = calc_angle(leftknee, leftankle, leftfoot)
        # right
        rightknee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
        rightankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
        rightfoot = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y)
        rightangle = calc_angle(rightknee, rightankle, rightfoot)

        # counter logic
        if leftangle < 120:
            leftstage = 'down'
        if leftangle > 135 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if rightangle < 120:
            rightstage = 'down'
        if rightangle > 135 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1
        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 小腿

def tiptoe(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        leftknee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
        leftankle = (landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
        leftfoot = (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y)
        leftangle = calc_angle(leftknee, leftankle, leftfoot)
        # right
        rightknee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
        rightankle = (landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
        rightfoot = (landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y)
        rightangle = calc_angle(rightknee, rightankle, rightfoot)

        # counter logic
        if leftangle < 120:
            leftstage = 'down'
        if leftangle > 135 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if rightangle < 120:
            rightstage = 'down'
        if rightangle > 135 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1
        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 肩膀

def Dumbbell_Lateral_Raise(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # curl counter logic
        if leftangle < 95:
            leftstage = 'down'
        if leftangle > 140 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if rightangle < 95:
            rightstage = 'down'
        if rightangle > 140 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

def Dumbbell_Shoulder_Press(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        lefthip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftangle = calc_angle(lefthip, leftshoulder, leftelbow)
        # right
        righthip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightangle = calc_angle(righthip, rightshoulder, rightelbow)
        
        # curl counter logic
        if leftangle < 20:
            leftstage = 'down'
        if leftangle > 75 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if rightangle < 20:
            rightstage = 'down'
        if rightangle > 75 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 背部

def one_arm_row(landmarks, mp_pose):
    global leftcounter
    global rightcounter
    global leftstage
    global rightstage
    try:
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        lefthip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        left_move_angle = calc_angle(lefthip, leftshoulder, leftelbow)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        righthip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)
        right_move_angle = calc_angle(righthip, rightshoulder, rightelbow)
        
        # counter logic
        if leftangle > 160 and left_move_angle <= 30:
            leftstage = 'down'
        if leftangle < 100 and left_move_angle >= 45 and leftstage == 'down':
            leftstage = 'up'
            leftcounter += 1
        
        if rightangle > 160 and right_move_angle <= 30:
            rightstage = 'down'
        if rightangle < 100 and right_move_angle >= 45 and rightstage == 'down':
            rightstage = 'up'
            rightcounter += 1

        return (leftcounter, rightcounter, leftstage, rightstage)
    except:
        return None

# 核心

def plank(landmarks, mp_pose):
    global plank_starttime
    global plank_currenttime
    global stage
    try:
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if 70 <= leftangle <= 95 and 70 <= rightangle <= 95 and stage == 'up':
            stage = 'down'
            plank_starttime = time.time()
            plank_currenttime = time.time()
        elif 70 <= leftangle <= 95 and 70 <= rightangle <= 95 and stage == 'down':
            plank_currenttime = time.time()
        else:
            stage = 'up'
            plank_starttime = time.time()
            plank_currenttime = time.time()

        hold_time = int(plank_currenttime - plank_starttime)

        return (hold_time, hold_time, stage, stage)
    except:
        return None

def starjump(landmarks, mp_pose):
    global counter
    global stage
    try:
        # left hand
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        lefthip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
        left_hand_angle = calc_angle(leftwrist, leftshoulder, lefthip)
        # right hand
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        righthip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
        right_hand_angle = calc_angle(rightwrist, rightshoulder, righthip)
        # left leg
        leftknee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
        rightknee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
        left_leg_angle = calc_angle(leftknee, lefthip, rightknee)
        right_leg_angle = calc_angle(leftknee, righthip, rightknee)
        leg_angle = int((left_leg_angle + right_leg_angle) / 2)
        
        # curl counter logic
        if left_hand_angle < 80 and right_hand_angle < 80 and leg_angle < 30:
            stage = 'down'
        if left_hand_angle > 160 and right_hand_angle > 160 and leg_angle >= 30 and stage == 'down':
            stage = 'up'
            counter += 1

        return (counter, counter, stage, stage)
    except:
        return None

# 胸部
def pushup(landmarks, mp_pose):
    global counter
    global stage
    try:
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        leftelbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        leftwrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y)
        leftangle = calc_angle(leftshoulder, leftelbow, leftwrist)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        rightelbow = (landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y)
        rightwrist = (landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y)
        rightangle = calc_angle(rightshoulder, rightelbow, rightwrist)

        # counter logic
        if 50 <= leftangle <= 70 and 50 <= rightangle <= 70:
            stage = 'down'
        elif leftangle > 160 and rightangle > 160 and stage == 'down':
            stage = 'up'
            counter += 1

        return (counter, counter, stage, stage)
    except:
        return None

# 腹肌
def reverse_crunch(landmarks, mp_pose):
    global counter
    global stage
    try:
        # left
        leftshoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)
        lefthip = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y)
        leftknee = (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
        leftangle = calc_angle(leftshoulder, lefthip, leftknee)
        # right
        rightshoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
        righthip = (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y)
        rightknee = (landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
        rightangle = calc_angle(rightshoulder, righthip, rightknee)

        # curl counter logic
        if leftangle > 80 and rightangle > 80:
            stage = 'up'
        if leftangle < 60 and rightangle < 60 and stage == 'up':
            stage = 'down'
            counter += 1
        return (counter, counter, stage, stage)
    except:
        return None
