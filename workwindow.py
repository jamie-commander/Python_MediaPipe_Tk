import tkinter as tk
import os
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import time
import pygame
import json
import random

import mainwindow
import gymMove
 
import game_warriorVSdragon as game

# 路徑
filepath = os.getcwd() # 取得本地位置
imgpath = os.path.join(filepath, 'img')
videopath = os.path.join(filepath, 'video')
soundpath = os.path.join(filepath, 'sound')
videoDEMOpath = os.path.join(filepath, 'videoDEMO')
datapath = os.path.join(filepath,"data")

class WORKSTATUS:
    DEMOVIDEO = 0
    COUNTDOWN = 1
    WORK = 2
    NEXT = 3 # determine next stage
    RESTING = 4
    NEXT_MOVE = 5
    CHANGE_MOVE = 6
    RANK = 7
    END = 8
    NONE = -1

class WorkWindow(tk.Tk):
    def __init__(self, username, level):
        super().__init__()
        print(username, level)
        self.username = username
        self.level = level

        self.pTime = time.time()

        self.buildpygame()

        # 視窗設定
        self.title("游戲界面")
        size = '%dx%d+%d+%d' % (1920, 1000, 0, 0)
        self.geometry(size)

        # build frame
        self.build_frame1()
        self.build_frame2()

        # build capture
        self.cap = cv2.VideoCapture(0)

        # demo video
        self.capture_demovideo = None

        # build_game
        self.build_GAME = False
        self.gameover = False
        self.gamemark = [0, 0] # [marks, total marks]

        # build mediapipe hand and pose
        self.using_mphand = True
        self.using_mppose = False
        self.build_mp()

        # handstatus (GO) count
        self.handtime = time.time()

        # WORKSTATUS
        self.workstatus = WORKSTATUS.DEMOVIDEO

        # sound
        self.enable_countdown321 = True

        # gymMove 資料
        self.gym_chinese = {
            'curl':                     "二頭肌彎舉",
            'triceps_extension':        "三頭肌屈伸",
            'reverse_crunch':           "反式屈膝捲腹",
            'pushup':                   "伏地挺身",
            'one_arm_row':              "單臂划船",
            'squat':                    "深蹲",
            'tiptoe':                   "墊脚",
            'Dumbbell_Lateral_Raise':   "啞鈴側平舉",
            'Dumbbell_Shoulder_Press':  "啞鈴肩推",
            'starjump':                 "開合跳",
            'plank':                    "平面支撐"
        }
        self.gym_function = {
            "curl":                     gymMove.curl,
            "triceps_extension":        gymMove.triceps_extension,
            "reverse_crunch":           gymMove.reverse_crunch,
            "pushup":                   gymMove.pushup,
            "one_arm_row":              gymMove.one_arm_row,
            "squat":                    gymMove.squat,
            "tiptoe":                   gymMove.tiptoe,
            "Dumbbell_Lateral_Raise":   gymMove.Dumbbell_Lateral_Raise,
            "Dumbbell_Shoulder_Press":  gymMove.Dumbbell_Shoulder_Press,
            "starjump":                 gymMove.starjump,
            "plank":                    gymMove.plank
            }  
        self.gym_demovideo = {
            "curl":                     os.path.join(videoDEMOpath, '1.mp4'),
            "triceps_extension":        os.path.join(videoDEMOpath, '2.mp4'),
            "reverse_crunch":           os.path.join(videoDEMOpath, '3.mp4'),
            "pushup":                   os.path.join(videoDEMOpath, '4.mp4'),
            "one_arm_row":              os.path.join(videoDEMOpath, '5.mp4'),
            "squat":                    os.path.join(videoDEMOpath, '6.mp4'),
            "tiptoe":                   os.path.join(videoDEMOpath, '7.mp4'),
            "Dumbbell_Lateral_Raise":   os.path.join(videoDEMOpath, '8.mp4'),
            "Dumbbell_Shoulder_Press":  os.path.join(videoDEMOpath, '9.mp4'),
            "starjump":                 os.path.join(videoDEMOpath, '10.mp4'),
            "plank":                    os.path.join(videoDEMOpath, '11.mp4'),
            }
        self.gym_quotations = ['流汗太快乐',
                        '享受大汗淋漓的畅快',
                        '健身不需要文案，只要流汗',
                        '不开心的时候，流泪不如流汗',
                        '除了汗水，什么水都不要浪费',
                        '最好的护肤水是运动后的汗水',
                        '汗水的味道，有时候比香水好闻',
                        '你流下的每一滴汗水，都会变成他们羡慕的口水',
                        '汗水会让你感觉每天都是真实存在的，而不是虚无']
        self.gym_quotation = random.choice(self.gym_quotations)

        # level
        assert (level == 'easy' or level == 'medium' or level == 'hard'), f"level {level} is invalid"

        # (rest time, [[gymmove, cycle, several], [gymmove, cycle, several], ...])
        if level == 'easy':
            self.rest_time = 10
            self.gym_set = [
                ['curl', 2, 8], 
                ['Dumbbell_Lateral_Raise', 1, 8], 
                # ['squat', 1, 8], 
                ['Dumbbell_Shoulder_Press', 1, 8],
                #['reverse_crunch', 3, 8],
            ]
        elif level == 'medium':
            self.rest_time = 7
            self.gym_set = [
                ['curl', 3, 8], 
                ['Dumbbell_Lateral_Raise', 3, 8], 
                ['tiptoe', 3, 12],
                ['plank', 3, 20],
                ['starjump', 3, 15],
            ]
        elif level == 'hard':
            self.rest_time = 5
            self.gym_set = [
                ['Dumbbell_Shoulder_Press', 3, 15], 
                ['one_arm_row', 3, 12],
                ['triceps_extension', 3, 12], 
                ['plank', 3, 20],
                ['reverse_crunch', 3, 20],
                ['starjump', 3, 15],
            ]

        # counter
        self.count_gym = 0
        self.count_cycle = 1
        self.count_resttime = 0
        self.record_resttime = time.time()
        
        self.start()
        
        self.mainloop()

    def start(self):
        ret, self.img = self.cap.read()
        
        if(ret):
            self.img = cv2.flip(self.img, 1) # flip the img
            
            # convert color BGR to RGB
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)#轉RGB
            self.img.flags.writeable = False

            # resize img
            self.img = cv2.resize(self.img,(960, 720))

            # mphand mppose
            if self.workstatus == WORKSTATUS.WORK:
                self.using_mphand = False
                self.using_mppose = True
            
            # mediapipe 處裡
            if self.using_mphand:
                self.mphand_process(self.img)
            elif self.workstatus != WORKSTATUS.CHANGE_MOVE: # reset time
                self.handtime = time.time()
            if self.using_mppose:
                self.mppose_process(self.img)

            # fps
            self.cTime = time.time()
            self.fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(self.img, f"FPS :{int(self.fps)}", (10,470),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (200,200,200), 3)
            
            # block
            if self.workstatus == WORKSTATUS.DEMOVIDEO:
                img_copy = self.img.copy()
                cv2.rectangle(img_copy, (730, 285), (960, 435), (245, 117, 16), -1)
                cv2.putText(img_copy, 'GO', (775, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)
                self.img = cv2.addWeighted(img_copy, 0.7, self.img, 0.3, 1)
            elif self.workstatus == WORKSTATUS.COUNTDOWN:
                if self.countdown + 1 == 6:
                    text = 'READY'
                    img_copy = self.img.copy()
                    cv2.rectangle(img_copy, (300, 285), (600, 435), (245, 117, 16), -1)
                    cv2.putText(img_copy, text, (350, 380), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
                    self.img = cv2.addWeighted(img_copy, 0.7, self.img, 0.3, 1)
                elif 5 >= self.countdown + 1 >= 1:
                    text = str(self.countdown + 1)
                    img_copy = self.img.copy()
                    cv2.rectangle(img_copy, (380, 285), (580, 435), (245, 117, 16), -1)
                    cv2.putText(img_copy, text, (450, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)
                    self.img = cv2.addWeighted(img_copy, 0.7, self.img, 0.3, 1)
            elif self.workstatus == WORKSTATUS.RANK:
                self.using_mphand = True

                # 個人資料讀取
                with open(os.path.join(datapath, "account.json"), 'r') as f:
                    self.datas = json.load(f)
                    
                    cv2.rectangle(self.img, (730, 285), (960, 435), (245, 117, 16), -1)
                    cv2.putText(self.img, 'QUIT', (775, 380), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
                    
                    # 透明的Rank表格
                    img_copy = self.img.copy()
                    cv2.rectangle(img_copy, (30, 50), (930, 670), (0, 0, 255), -1)
                    self.img = cv2.addWeighted(img_copy, 0.5, self.img, 0.5, 1)

                    cv2.putText(self.img, 'Username', (70, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                    cv2.putText(self.img, ' Easy ', (270, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                    cv2.putText(self.img, 'Medium', (420, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                    cv2.putText(self.img, ' Hard ', (550, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                    cv2.putText(self.img, ' Bonus ', (650, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                    cv2.putText(self.img, ' Rank ', (800, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)

                    for i, username in enumerate(self.datas):
                        user = self.datas[username]
                        easy = ' ' + str(user['easy']) + ' '
                        medium = ' ' + str(user['medium']) + ' '
                        hard = ' ' + str(user['hard']) + ' '
                        bonus = ' ' + str(user['bonus']) + ' '
                        Rank = ' ' + str(user['Rank']) + ' '
                        cv2.putText(self.img, username, (70, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                        cv2.putText(self.img, easy, (270, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                        cv2.putText(self.img, medium, (420, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                        cv2.putText(self.img, hard, (550, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                        cv2.putText(self.img, bonus, (650, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                        cv2.putText(self.img, Rank, (800, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3, cv2.LINE_AA)
                
            # game
            if self.workstatus == WORKSTATUS.COUNTDOWN:
                if self.countdown + 1 == 6 :
                    if self.build_GAME == False:
                        self.game = game.GameFrame(self.frame1)
                        self.video1 = self.game
                        self.video1.grid(row = 0, column = 0)
                        self.build_GAME = True
                    else:
                        self.video1 = self.game
                        self.video1.grid(row = 0, column = 0)
            # gymmove
            if self.workstatus == WORKSTATUS.WORK:
                self.workout = None
                try:
                    landmarks = self.pose_result.pose_landmarks.landmark
                    gymMove.update(landmarks, self.mpPose)
                    gym = self.gym_set[self.count_gym]
                    # [gymmove, cycle, several]
                    gymname = gym[0]
                    several = gym[2]

                    self.workout = self.gym_function[gymname]()
                except:
                    pass
                if self.workout != None:
                    (status, mark, leftcounter, rightcounter, leftstage, rightstage) = self.workout
                    # 不讓 次數 超過 最大次數
                    if leftcounter >= several: 
                        self.leftreps_text.set('%2d/%2d'%(several, several))
                    else:
                        self.leftreps_text.set('%2d/%2d'%(leftcounter, several))
                    if rightcounter >= several:
                        self.rightreps_text.set('%2d/%2d'%(several, several))
                    else:
                        self.rightreps_text.set('%2d/%2d'%(rightcounter, several))
                    self.leftstage_text.set(leftstage)
                    self.rightstage_text.set(rightstage)
                    
                    if status: # 如果status == True，説明計分
                        print(mark)
                        self.gamemark[0] += mark
                        self.gamemark[1] += 100
                        if self.gameover:
                            self.bonus_text.set(str(int(self.bonus_text.get()) + mark))
                        else:
                            if mark < 0:
                                mark = 0
                            self.game.player_attack(mark//2)
                            if self.game.gameover and self.game.dragon.live == False:
                                self.gameover = True
                            cv2.putText(self.img, str(mark), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)

                    if leftcounter >= several and rightcounter >= several:
                        self.workstatus = WORKSTATUS.NEXT
                    
            try:
                self.img_process = Image.fromarray(self.img)
                self.img_process = ImageTk.PhotoImage(image = self.img_process)
                self.video2.config(image=self.img_process)
            except:
                pass
        self.timeupdate()
        self.video2.after(1, self.start) # 持續執行open方法，1000為1秒
    
    def timeupdate(self):
        if self.workstatus == WORKSTATUS.DEMOVIDEO:
            # message
            self.message_text.set('即時訊息：觸碰 GO 來開始運動吧')
            # setting info
            gym = self.gym_set[self.count_gym]
            gymname = self.gym_chinese[gym[0]]
            gymcycle= gym[1]
            gymseveral = gym[2]
            self.gymname_text.set(gymname)
            self.leftreps_text.set('%2d / %2d' % (0, gymseveral))
            self.rightreps_text.set('%2d / %2d' % (0, gymseveral))
            self.leftstage_text.set('None')
            self.rightstage_text.set('None')
            self.cycle_text.set('%2d / %2d' % (self.count_cycle, gymcycle))
            # open demo video
            if self.capture_demovideo == None:
                self.capture_demovideo = cv2.VideoCapture(self.gym_demovideo[gym[0]])
                print(self.gym_demovideo[gym[0]])

            ret_demo, self.img_demo = self.capture_demovideo.read()
            if(ret_demo):
                self.img_demo = cv2.cvtColor(self.img_demo, cv2.COLOR_BGR2RGB)
                self.img_demo = cv2.resize(self.img_demo,(960,720))
                self.img_demo = Image.fromarray(self.img_demo)
                self.img_demo = ImageTk.PhotoImage(image = self.img_demo)
                self.video1.config(image=self.img_demo)
                if(self.capture_demovideo.get(cv2.CAP_PROP_POS_FRAMES) == self.capture_demovideo.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                    self.capture_demovideo.set(cv2.CAP_PROP_POS_FRAMES,0)
            self.countdown = 5
            self.countdown_time = time.time()
        elif self.workstatus == WORKSTATUS.COUNTDOWN:
            # message
            if time.time() - self.countdown_time >= 1:
                self.message_text.set(f'即時訊息：倒數 {self.countdown}')
                
            self.capture_demovideo = None
            if self.countdown == -1:
                self.workstatus = WORKSTATUS.WORK
                self.gym_quotation = random.choice(self.gym_quotations)
            elif time.time() - self.countdown_time >= 1:
                self.countdown -= 1
                self.countdown_time = time.time()
        elif self.workstatus == WORKSTATUS.WORK:
            self.message_text.set(f'即時訊息：'+ self.gym_quotation)
            # start / continue game
            self.game.continueGAME()
        elif self.workstatus == WORKSTATUS.NEXT:
            gymMove.clear()
            gym = self.gym_set[self.count_gym]
            # [gymmove, cycle, several]
            cycle = gym[1]
            if self.count_cycle == cycle:                
                self.workstatus = WORKSTATUS.NEXT_MOVE
                self.count_cycle = 1                
            else:
                self.workstatus = WORKSTATUS.RESTING
                self.count_cycle += 1
                print(self.count_cycle, cycle)
                self.cycle_text.set('%2d/%2d' % (self.count_cycle, cycle))
                self.record_resttime = time.time()
        elif self.workstatus == WORKSTATUS.RESTING:
            # message
            self.message_text.set(f'即時訊息：休息一下咯~')
            # stop game
            self.game.pauseGAME()
            # open demo video
            gym = self.gym_set[self.count_gym]
            if self.capture_demovideo == None:
                self.capture_demovideo = cv2.VideoCapture(self.gym_demovideo[gym[0]])
                print(self.gym_demovideo[gym[0]])

            ret_demo, self.img_demo = self.capture_demovideo.read()
            if(ret_demo):
                self.img_demo = cv2.cvtColor(self.img_demo, cv2.COLOR_BGR2RGB)
                self.img_demo = cv2.resize(self.img_demo,(960,720))

                # block 
                cv2.rectangle(self.img_demo, (700, 620), (960, 720), (77, 117, 200), -1)
                cv2.putText(self.img_demo, 'resting', (720, 690), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
                if self.count_resttime - 1 == 0:
                    text = 'GO'
                    img_copy = self.img_demo.copy()
                    cv2.rectangle(img_copy, (380, 285), (580, 435), (245, 117, 16), -1)
                    cv2.putText(img_copy, text, (420, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)
                    self.img_demo = cv2.addWeighted(img_copy, 0.7, self.img_demo, 0.3, 1)
                elif self.count_resttime - 1 <= 3:
                    text = str(self.count_resttime - 1)
                    img_copy = self.img_demo.copy()
                    cv2.rectangle(img_copy, (380, 285), (580, 435), (245, 117, 16), -1)
                    cv2.putText(img_copy, text, (450, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)
                    self.img_demo = cv2.addWeighted(img_copy, 0.7, self.img_demo, 0.3, 1)

                self.img_demo = Image.fromarray(self.img_demo)
                self.img_demo = ImageTk.PhotoImage(image = self.img_demo)
                self.video2.config(image=self.img_demo)
                if(self.capture_demovideo.get(cv2.CAP_PROP_POS_FRAMES) == self.capture_demovideo.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                    self.capture_demovideo.set(cv2.CAP_PROP_POS_FRAMES,0)
            
            # disable mppose
            self.using_mppose = False

            self.count_resttime = self.rest_time - int(time.time() - self.record_resttime)
            if self.count_resttime == 4 and self.enable_countdown321 == True:
                self.enable_countdown321 = False
                self.countdown321()
            elif self.count_resttime == 3:
                self.enable_countdown321 = True
            
            if self.count_resttime == 0:
                self.workstatus = WORKSTATUS.WORK
                # enable mppose
                self.using_mppose = True
        elif self.workstatus == WORKSTATUS.NEXT_MOVE:
            self.gym_quotation = random.choice(self.gym_quotations)
            self.using_mppose = False
            self.workstatus = WORKSTATUS.CHANGE_MOVE
            # next gym
            self.count_gym += 1 
            # pause game
            self.game.pauseGAME()
            # clear demo video
            self.capture_demovideo = None
        elif self.workstatus == WORKSTATUS.CHANGE_MOVE:
            # message
            self.message_text.set(f'即時訊息：往下一個目標去吧！！！')
            if self.count_gym == len(self.gym_set):
                self.update_data()
                self.workstatus = WORKSTATUS.RANK
                return
            # setting info
            gym = self.gym_set[self.count_gym]
            gymname = self.gym_chinese[gym[0]]
            gymcycle= gym[1]
            gymseveral = gym[2]
            self.gymname_text.set(gymname)
            self.leftreps_text.set('%2d / %2d' % (0, gymseveral))
            self.rightreps_text.set('%2d / %2d' % (0, gymseveral))
            self.leftstage_text.set('None')
            self.rightstage_text.set('None')
            self.cycle_text.set('%2d / %2d' % (self.count_cycle, gymcycle))

            # open demo video
            if self.capture_demovideo == None:
                self.capture_demovideo = cv2.VideoCapture(self.gym_demovideo[gym[0]])
                print(self.gym_demovideo[gym[0]])

            ret_demo, self.img_demo = self.capture_demovideo.read()
            if(ret_demo):
                self.img_demo = cv2.cvtColor(self.img_demo, cv2.COLOR_BGR2RGB)
                self.img_demo = cv2.resize(self.img_demo,(960,720))

                # process
                self.mphand_process2(self.img, self.img_demo)

                # block
                img_copy = self.img_demo.copy()
                cv2.rectangle(img_copy, (730, 285), (960, 435), (245, 117, 16), -1)
                cv2.putText(img_copy, 'GO', (775, 400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)
                self.img_demo = cv2.addWeighted(img_copy, 0.7, self.img_demo, 0.3, 1)

                self.img_demo = Image.fromarray(self.img_demo)
                self.img_demo = ImageTk.PhotoImage(image = self.img_demo)
                self.video2.config(image=self.img_demo)
                if(self.capture_demovideo.get(cv2.CAP_PROP_POS_FRAMES) == self.capture_demovideo.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                    self.capture_demovideo.set(cv2.CAP_PROP_POS_FRAMES,0) 
            self.countdown = 5
            self.countdown_time = time.time() 
        elif self.workstatus == WORKSTATUS.RANK:
            # message
            self.message_text.set(f'即時訊息：看看你那驕傲的成績吧！！！')
            self.QUIT()
        elif self.workstatus == WORKSTATUS.END:
            self.QUIT()
    
    def mphand_process2(self, img, img_demo):
        self.hand_result = self.myhands.process(img)
        if self.hand_result.multi_hand_landmarks:
            # only one hands
            handLms = self.hand_result.multi_hand_landmarks[0]
            lm = handLms.landmark[8]
            xPos = int(lm.x * 960)
            yPos = int(lm.y * 720)
            cv2.circle(img_demo, (xPos,yPos), 10, (0,0,255), cv2.FILLED)
            if not(730 < xPos < 960 and 285 < yPos < 435):
                self.handtime = time.time()

            # 顯示進度條
            holdtime = time.time() - self.handtime
            print(holdtime)
            radius = 40
            center = (850, 650)
            axes = (radius, radius)
            angle = 0
            startAngle = 0
            if holdtime >= 3:
                self.handtime = time.time()
                endAngle = 360
                cv2.ellipse(img_demo, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
                self.workstatus = WORKSTATUS.COUNTDOWN
                print(self.workstatus)
                self.countdown54321()
            elif holdtime > 0:
                endAngle = int(360 * (holdtime/3))
                cv2.ellipse(img_demo, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)

    def mphand_process(self, img):
        self.hand_result = self.myhands.process(img)
        if self.hand_result.multi_hand_landmarks:
            # only one hands
            handLms = self.hand_result.multi_hand_landmarks[0]
            lm = handLms.landmark[8]
            xPos = int(lm.x * 960)
            yPos = int(lm.y * 720)
            cv2.circle(img, (xPos,yPos), 10, (0,0,255), cv2.FILLED)
            if self.workstatus == WORKSTATUS.DEMOVIDEO and 730 < xPos < 960 and 285 < yPos < 435:
                pass
            elif self.workstatus == WORKSTATUS.RANK and 730 < xPos < 960 and 285 < yPos < 435:
                pass
            else:
                self.handtime = time.time()
            # 顯示進度條
            holdtime = time.time() - self.handtime
            radius = 40
            center = (850, 650)
            axes = (radius, radius)
            angle = 0
            startAngle = 0
            if holdtime >= 3:
                self.handtime = time.time()
                endAngle = 360
                cv2.ellipse(img, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
                if self.workstatus == WORKSTATUS.DEMOVIDEO:
                    self.workstatus = WORKSTATUS.COUNTDOWN
                    self.countdown54321()
                if self.workstatus == WORKSTATUS.RANK:
                    self.workstatus = WORKSTATUS.END
            elif holdtime > 0:
                endAngle = int(360 * (holdtime/3))
                cv2.ellipse(img, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
            else:
                self.counttime = time.time()
                            
    def mppose_process(self, img):
        # mediapipe_pose處裡
        self.pose_result = self.myPose.process(img)

        if self.pose_result.pose_landmarks:
            self.mpDraw.draw_landmarks(img,
                                    self.pose_result.pose_landmarks,# 點
                                    self.mpPose.POSE_CONNECTIONS,   # 連線
                                    self.PoseLmsStyle,              # 點的Style
                                    self.PoseConStyle               # 連接線的Style
                                    )

            for i, lm in enumerate(self.pose_result.pose_landmarks.landmark):
                xPos = int(lm.x * 960)
                yPos = int(lm.y * 720)
                cv2.putText(img,
                            str(i),                     # 字
                            (xPos-25,yPos+5),           # 位置
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.4,                        # 大小
                            (0,0,255),                  # 顏色
                            2,                          # 租度
                            )

    def build_mp(self):
        self.mpDraw = mp.solutions.drawing_utils
        # mediapipe hand
        self.mpHands = mp.solutions.hands
        self.myhands = self.mpHands.Hands()
        self.handLmsStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
        self.handConStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

        # mediapipe pose
        self.mpPose = mp.solutions.pose
        self.myPose = self.mpPose.Pose()
        self.PoseLmsStyle = self.mpDraw.DrawingSpec(color=(0,0,0),thickness=5)
        self.PoseConStyle = self.mpDraw.DrawingSpec(color=(255,255,0),thickness=10)

    def build_frame1(self):
        self.frame1 = tk.Frame(self, bg="#00FFFF", width = 1920, height = 720, bd=0, relief=tk.GROOVE)
        self.frame1.pack_propagate(0)
        self.frame1.grid(row = 0, column = 0)

        self.img_init = None # ImageTk.PhotoImage(Image.open(os.path.join(imgpath, 'block.jpg')))
        self.video1 = tk.Label(self.frame1, width=960, height=720, bg ='gray94', image=self.img_init, fg='blue', relief=tk.GROOVE)
        self.video2 = tk.Label(self.frame1, width=960, height=720, bg ='gray94', image=self.img_init, fg='blue', relief=tk.GROOVE)
        self.video1.grid(row = 0, column= 0, padx=0, pady=0)
        self.video2.grid(row = 0, column= 1, padx=0, pady=0)

    def build_frame2(self):
        self.frame2 = tk.Frame(self, bg="#FFFFFF",width = 1920 ,height = 50, background="#97FF97" ,bd = 5, relief = tk.GROOVE)
        self.frame2.pack_propagate(0)
        self.frame2.grid(row = 1, column = 0)

        self.message_text = tk.StringVar()
        self.message_text.set('即時訊息：我是信息')
        self.message_label = tk.Label(self.frame2, textvariable=self.message_text, width=81, height=1, 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.gymname_text = tk.StringVar()
        self.gymname_text.set('動作名稱')
        self.gymname_label = tk.Label(self.frame2, textvariable=self.gymname_text, width=81, height=1, bg="#97FF97", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))
        
        self.leftrepstitle_label = tk.Label(self.frame2, text='REPS:', width=20, height=1, bd=1, bg="#979797", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.leftreps_text = tk.StringVar()
        self.leftreps_text.set('%2d/%2d'%(0, 10))
        self.leftreps_label = tk.Label(self.frame2, textvariable=self.leftreps_text, width=20, height=1, bd=1, bg="#FF9797", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.rightrepstitle_label = tk.Label(self.frame2, text='REPS:', width=20, height=1, bd=1, bg="#979797", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.rightreps_text = tk.StringVar()
        self.rightreps_text.set('%2d/%2d'%(0, 10))
        self.rightreps_label = tk.Label(self.frame2, textvariable=self.rightreps_text, width=20, height=1, bd=1, bg="#FF9797", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.leftstagetitle_label = tk.Label(self.frame2, text='STAGE:', width=20, height=1, bd=1, bg="#AAAA97", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.leftstage_text = tk.StringVar()
        self.leftstage_text.set('None')
        self.leftstage_label = tk.Label(self.frame2, textvariable=self.leftstage_text, width=20, height=1, bd=1, bg="#FF6767", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.rightstagetitle_label = tk.Label(self.frame2, text='STAGE:', width=20, height=1, bd=1, bg="#AAAA97", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.rightstage_text = tk.StringVar()
        self.rightstage_text.set('None')
        self.rightstage_label = tk.Label(self.frame2, textvariable=self.rightstage_text, width=20, height=1, bd=1, bg="#FF6767", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))
        
        self.cycletitle_label = tk.Label(self.frame2, text='CYCLE:', width=20, height=1, bd=1, bg="#9999AA", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.cycle_text = tk.StringVar()
        self.cycle_text.set('%2d/%2d' % (1, 3))
        self.cycle_label = tk.Label(self.frame2, textvariable=self.cycle_text, width=20, height=1, bd=1, bg="#FF4747", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.bonustitle_label = tk.Label(self.frame2, text='BONUS:', width=20, height=1, bd=1, bg="#9999AA", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.bonus_text = tk.StringVar()
        self.bonus_text.set('0')
        self.bonus_label = tk.Label(self.frame2, textvariable=self.bonus_text, width=20, height=1, bd=1, bg="#FF4747", 
                            fg="#000000", font=('微軟正黑體', 26, 'bold'))

        self.message_label.grid(row=0, column=0, columnspan=4, padx=0, pady=0)
        self.gymname_label.grid(row=1, column=0, columnspan=4, padx=0, pady=0)
        self.leftrepstitle_label.grid(row=2, column=0, padx=0, pady=0)
        self.leftreps_label.grid(row=2, column=1, padx=0, pady=0)
        self.rightrepstitle_label.grid(row=2, column=2, padx=0, pady=0)
        self.rightreps_label.grid(row=2, column=3, padx=0, pady=0)
        self.leftstagetitle_label.grid(row=3, column=0, padx=0, pady=0)
        self.leftstage_label.grid(row=3, column=1, padx=0, pady=0)
        self.rightstagetitle_label.grid(row=3, column=2, padx=0, pady=0)
        self.rightstage_label.grid(row=3, column=3, padx=0, pady=0)
        self.cycletitle_label.grid(row=4, column=0, padx=0, pady=0)
        self.cycle_label.grid(row=4, column=1, padx=0, pady=0)
        self.bonustitle_label.grid(row=4, column=2, padx=0, pady=0)
        self.bonus_label.grid(row=4, column=3, padx=0, pady=0)
    
    def buildpygame(self):
        pygame.init()
        pygame.mixer.init()
        pygame.time.delay(1000)#等待1秒讓mixer完成初始化

    def update_data(self):
        mark = self.gamemark[0] * 100 // self.gamemark[1]
        print('mymark:',mark)

        with open(os.path.join(datapath, "account.json"), 'r') as f:
            datas = json.load(f)

        for i in datas:
            print(i, datas[i]['Rank'])

        if mark > datas[self.username][self.level]:
            datas[self.username][self.level] = mark
            datas[self.username]['bonus'] += int(self.bonus_text.get())
            
            # calculate all the mark
            mark_dict = {}
            for user in datas:
                d = datas[user]
                mark_dict[user] = d['easy'] + d['medium'] + d['hard'] + d['bonus']

            # sorting
            mark_dict = dict(sorted(mark_dict.items(), key=lambda item: item[1], reverse=True))
            print(mark_dict)
            update_datas = {}

            # update rank
            for rank, user in enumerate(mark_dict):
                update_datas[user] = datas[user]
                update_datas[user]['Rank'] = rank + 1

            with open(os.path.join(datapath, "account.json"), 'w') as f:
                json.dump(update_datas, f)

    def countdown54321(self):
        music = pygame.mixer.Sound(os.path.join(soundpath, 'sound_5_4_3_2_1.mp3'))
        music.play()
    
    def countdown321(self):
        music = pygame.mixer.Sound(os.path.join(soundpath, 'sound_3_2_1.mp3'))
        music.play()

    def QUIT(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.destroy()
        mainwindow.MainWindow(self.username)

if __name__ == '__main__':
    WorkWindow('admin', 'easy')
