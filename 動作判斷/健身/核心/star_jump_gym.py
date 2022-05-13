# 開合跳 star jump
import cv2
import mediapipe as mp
import numpy as np


def calc_angle(a, b, c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360.0 - angle
    
    return angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# curl counter
counter = 0
stage = None


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        # convert color BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        result = pose.process(image)

        # convert color RGB to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract Landmarks
        try:
            landmarks = result.pose_landmarks.landmark
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

            # visualize
            cv2.putText(image, str(int(leg_angle)),
                        tuple(np.multiply(leftknee, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA
                    )
            cv2.putText(image, str(int(left_hand_angle)),
                        tuple(np.multiply(leftshoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA
                    )
            cv2.putText(image, str(int(right_hand_angle)),
                        tuple(np.multiply(rightshoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA
                    )
            
            # curl counter logic
            if left_hand_angle < 80 and right_hand_angle < 80 and leg_angle < 30:
                stage = 'down'
            if left_hand_angle > 160 and right_hand_angle > 160 and leg_angle >= 30 and stage == 'down':
                stage = 'up'
                counter += 1

        except:
            pass

        # render curl status box
        cv2.rectangle(image, (0, 0), (250, 73), (245, 117, 16), -1)
        cv2.rectangle(image, (390, 0), (640, 73), (245, 117, 16), -1)

        # LEFT REPS
        cv2.putText(image, 'REPS', (15, 12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # LEFT STAGE
        cv2.putText(image, 'STAGE', (85, 12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(stage), (90, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # RIGHT REPS
        cv2.putText(image, 'REPS', (405, 12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (400, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        # RIGHT STAGE
        cv2.putText(image, 'STAGE', (475, 12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(stage), (480, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)


        # render detection
        mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        
        cv2.imshow('Mediapipe read', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    else:
        print('NOT DETECT CAMERA')
  

cap.release()
cv2.destroyAllWindows()