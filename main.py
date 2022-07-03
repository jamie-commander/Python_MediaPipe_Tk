import os
from pickle import FALSE
import random
import json
import time
import sys
#from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import  ImageTk, Image, ImageDraw
import cv2
from threading import Timer
import mediapipe as mp

import gymMove
from hand_detect import hand_angle, hand_pos

import pygame
pygame.init()
pygame.mixer.init()
pygame.time.delay(1000)#等待1秒讓mixer完成初始化


def mkdir():
    filepath = os.getcwd()#取得本地位置
    #if os.path.isdir(os.path.join(filepath,"resource")):
    #    os.mkdir("resource")
    flag = True
    for i in os.listdir(filepath):
        if(i == "resource"):
            flag = False
    if(flag):
        os.mkdir("resource")



class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        mkdir()
        self.img_video = r'.\resource\screen.jpg'
        self.img_video_process = r'.\resource\screen_process.jpg'
        #開啟照片
        self.img_init = ImageTk.PhotoImage(Image.open('block.jpg'))
        
        self.Resting = False
        
        self.pTime = 0 #previous time
        self.cTime = 0 #current time
        self.hand_value = True
        self.pose_value = False
        self.s = None
        
        self.hand_ok_status = False
        self.hand_ok_time = time.time()
        self.hand_ok_count = 0

        self.hand_control_status = False
        self.hand_control_xy = (0, 0)
        self.hand_control_time = time.time()
        self.hand_control_show_status = 'None'
        self.hand_control_real_status = 'None'
        
        self.count = 0
        #self.gym_model_status = None#暫時用不到
        self.gym_item_status = None
        self.gym_cycle_status = None
        
        self.gym_items_status = 0
        
        #self.gym_model = "only one"
        self.gym_model = ""
        self.gym_item = "二頭肌彎舉"
        self.gym_cycle = "3"
        self.gym_several = "12"
        self.gym_intervals = "30"
        
        self.sys_start_time = time.time()
        
        self.gym_new_time = 0
        self.gym_start_time = 0
        self.gym_count_time_1 = 0
        self.gym_buf_time = 0
        
        self.gym_several_status = False
        
        self.gym_status = False
        
        self.sys_bus_time2 = 0
        self.sys_bus_time3 = 0
        
        self.leftcounter = 0
        self.rightcounter = 0
        self.leftstage = None
        self.rightstage = None
        
        self.model = ["only one","fitness combo"]
        self.item = ["二頭肌彎舉", "三頭肌屈伸","反式屈膝捲腹","伏地挺身","單臂划船","深蹲","墊脚","啞鈴側平舉","啞鈴肩推","開合跳","平面支撐"]
        self.cycle = ["1", "2","3","4","5","6","7","8","9","10"]
        self.several = ["3","6","9","12","15","18","21","24","27","30"]
        self.intervals = ["10","20","30","40","50","60","120","180","240","300"]
        
        self.hand_control_real_status_before = False
        #[{self.model},{self.item},{self.cycle},{self.several},{self.intervals}]
        self.control = list()
        self.control.append(self.model)
        self.control.append(self.item)
        self.control.append(self.cycle)
        self.control.append(self.several)
        self.control.append(self.intervals)
        
        self.control_x = 0
        #self.control_y = 0
        self.control_value = [0,0,0,0,0]
        self.gym_items = {
            "二頭肌彎舉": gymMove.curl,
            "三頭肌屈伸": gymMove.triceps_extension,
            #"三頭肌屈伸": gymMove.plank,
            #"三頭肌屈伸": gymMove.curl,
            "反式屈膝捲腹": gymMove.reverse_crunch,
            "伏地挺身": gymMove.pushup,
            "單臂划船": gymMove.one_arm_row,
            "深蹲": gymMove.squat,
            "墊脚": gymMove.tiptoe,
            "啞鈴側平舉": gymMove.Dumbbell_Lateral_Raise,
            "啞鈴肩推": gymMove.Dumbbell_Shoulder_Press,
            "開合跳": gymMove.starjump,
            "平面支撐": gymMove.plank,
            }
        
        self.gym_items_example = {
            "二頭肌彎舉": "./DemoVideo/1.mp4",
            "三頭肌屈伸": "./DemoVideo/2.mp4",
            "反式屈膝捲腹": "./DemoVideo/3.mp4",
            "伏地挺身": "./DemoVideo/4.mp4",
            "單臂划船": "./DemoVideo/5.mp4",
            "深蹲": "./DemoVideo/6.mp4",
            "墊脚": "./DemoVideo/7.mp4",
            "啞鈴側平舉": "./DemoVideo/8.mp4",
            "啞鈴肩推": "./DemoVideo/9.mp4",
            "開合跳": "./DemoVideo/10.mp4",
            "平面支撐": "./DemoVideo/11.mp4",
            }
        
        self.gym_models = {
            "手部(二頭肌彎舉、三頭肌屈伸)":{"二頭肌彎舉","三頭肌屈伸"},
            "腹部(反式屈膝捲腹、伏地挺身)":{"反式屈膝捲腹","伏地挺身"},
            "背部(單臂划船)":{"單臂划船"},
            "大腿(深蹲)":{"深蹲"},
            "小腿(墊脚)":{"墊脚"},
            "肩膀(啞鈴側平舉、啞鈴肩推)":{"啞鈴側平舉","啞鈴肩推"},
            "核心(開合跳、平面支撐)":{"開合跳","平面支撐"},
            }
        '''self.gym_models = {
            "手部(二頭肌彎舉、三頭肌屈伸)":{"三頭肌屈伸","二頭肌彎舉"},
            "腹部(反式屈膝捲腹、伏地挺身)":{"伏地挺身","反式屈膝捲腹"},
            "背部(單臂划船)":{"單臂划船"},
            "大腿(深蹲)":{"深蹲"},
            "小腿(墊脚)":{"墊脚"},
            "肩膀(啞鈴側平舉、啞鈴肩推)":{"啞鈴肩推","啞鈴側平舉"},
            "核心(開合跳、平面支撐)":{"平面支撐","開合跳"},
            }'''
    
        #self.plank_status = False #平板支撐的狀態
        self.out = None
        self.captrue_init()
        self.captrue.release()
        
        self.mediapipe_init()
        self.TK_main()
    def TK_main(self):
        #-----------------基礎視窗設定--------------------
        self.Close_Control = True
        #self.root = Tk()
        self.title("人體骨架辨識軟體v1.0")
        #self.root.geometry("1824x1026+0+0")
        screenwidth = self.winfo_screenwidth()#取得作業系統視窗寬度
        screenheight = self.winfo_screenheight()#取得作業系統視窗高度
        #size = '%dx%d+%d+%d' % (screenwidth * 0.9, screenheight * 0.9, (screenwidth * (1 - 0.9) )/2, (screenheight * (1 - 0.9))/3)
        size = '%dx%d+%d+%d' % (1920, 1000, 0, 0)
        self.geometry(size)#TK視窗大小
        self.maxsize(1920, 1000)#TK視窗最大大小
        self.minsize(1920, 1000)#TK視窗最小大小
        #--------------------------------------------------
        #------------------觸發刷新函式-------------------
        #Updata_Start=Timer(0.5,self.TK_updata,[])#thread
        #Updata_Start.start()
        #--------------------------------------------------
        #------------------產生視窗物件--------------------
        self.TK_object()
        #--------------------------------------------------
        
        self.protocol("WM_DELETE_WINDOW", self.TK_closing)#當視窗關閉時觸發
        self.mainloop()
        return
    def captrue_init(self):
        self.captrue_example = cv2.VideoCapture("./test.mp4")
        
        
        
        
        self.captrue = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
        #self.captrue.set(3,350) #像素
        #self.captrue.set(4,500) #像素
        # 設定擷取影像的尺寸大小
        self.captrue.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.captrue.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return
    def captrue_check(self):
        '''if self.captrue.isOpened(): #判斷相機是否有開啟
            self.captrue_open()
        else:
            self.captrue_init()
            self.captrue_open()'''
        self.captrue_init()
        self.captrue_open()
        return
    def captrue_open(self):
        '''self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
        
        self.ret_example,self.img_example = self.captrue_example.read()
        if(self.ret_example):
            self.img_example = cv2.flip(self.img_example, 1)
            self.img_example = cv2.cvtColor(self.img_example, cv2.COLOR_BGR2RGB)
            self.img_original_example = cv2.resize(self.img_example,(960,720))
            self.img_original_example = Image.fromarray(self.img_original_example)
            self.img_original_example = ImageTk.PhotoImage(image = self.img_original_example)
            self.video1.config(image=self.img_original_example)
            if(self.captrue_example.get(cv2.CAP_PROP_POS_FRAMES) == self.captrue_example.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                self.captrue_example.set(cv2.CAP_PROP_POS_FRAMES,0)
                #self.captrue_example = cv2.VideoCapture("./test2.mp4")'''
        
        
        
        #----------------------------------------------------------------------------------------
        self.button_open["state"] = tk.DISABLED
        #【Opencv学习（一）】VideoCapture读数据内存泄漏
        #https://blog.csdn.net/liuhuicsu/article/details/62418054
        self.ret,self.img = self.captrue.read() #取得相機畫面
        #cv2.imwrite(self.img_viode,img)
        if(self.ret):
            
            self.img = cv2.flip(self.img, 1) #
            #cv2.imwrite(self.img_video,self.img) #儲存最原始圖片
            
            #self.imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            
            #------------在tk第一個畫面上秀出原始圖片---------------------
            #https://blog.csdn.net/weixin_39450145/article/details/103874310
            #Image.fromarray的作用：简而言之，就是实现array到image的转换
            #ImageTk.PhotoImage
            #https://stackoverflow.com/questions/28670461/read-an-image-with-opencv-and-display-it-with-tkinter
            
            # convert color BGR to RGB
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)#轉RGB
            self.img.flags.writeable = False
            
            self.img_original = cv2.resize(self.img,(960,720))
            self.img_original = Image.fromarray(self.img_original)
            self.img_original = ImageTk.PhotoImage(image = self.img_original)
            #self.video1.config(image=self.img_original)
            
            #取得圖片高度寬度
            self.imgHeight = self.img.shape[0]
            self.imgWidth = self.img.shape[1]
            #---------------mediapipe_hand處裡--------------------
            if(self.hand_value):
                self.mediapipe_hand() #每個點的x、y、z資訊都在 self.hand_result
            #---------------mediapipe_hand處裡--------------------
            if(self.pose_value):
                self.mediapipe_pose() #每個點的x、y、z資訊都在 self.pose_result處裡的資料
            #-------------------fps-------------------------------
            self.cTime = time.time()
            self.fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(self.img, f"FPS :{int(self.fps)}",
                        (10,470),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (200,200,200),
                        3)
            
            self.time_updata()
            self.img = cv2.resize(self.img,(960,720))
            #--------------處裡完成轉回RGB----------
            # convert color RGB to BGR
            #self.img.flags.writeable = True
            #self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
            
            #------------在tk第一個畫面上秀出處理圖片---------------------
            self.img_process = Image.fromarray(self.img)
            self.img_process = ImageTk.PhotoImage(image = self.img_process)
            self.video2.config(image=self.img_process)
            
            #cv2.imwrite(self.img_video_process,self.img)#儲存處裡後圖片
            #cv2.imshow('img',self.img)
        #---------------------更新圖片方法，這方法不太好一直讀寫圖片-----------------------------
        '''self.img_original = ImageTk.PhotoImage(Image.open(self.img_video)) #讀取圖片
        #self.video1.imgtk=self.img_original #換圖片
        self.video1.config(image=self.img_original) #換圖片

        self.img_process = ImageTk.PhotoImage(Image.open(self.img_video_process)) #讀取圖片
        #self.video2.imgtk=self.img_process #換圖片
        self.video2.config(image=self.img_process) #換圖片'''
        #------------------------------------------------------------
        
        #self.img_original = ImageTk.PhotoImage(Image.open(self.img_video)) #讀取圖片
        #self.video1.imgtk=self.img_original #換圖片
        #self.video1.config(image=self.img_original) #換圖片
        
        self.s = self.video1.after(10, self.captrue_open) #持續執行open方法，1000為1秒'''
    def captrue_close(self):
        self.button_open["state"] = tk.NORMAL
        self.captrue.release() #關閉相機
        if(self.s != None):
            self.video1.after_cancel(self.s) #結束拍照
        
        self.video1.config(image=self.img_init) #換圖片
        self.video2.config(image=self.img_init) #換圖片
        
        self.gym_items_status = 0
        gymMove.clear()
        self.gym_model = ""
        self.message.set("攝像頭已經關閉，若想繼續訓練請開啟攝像頭。")
        #self.video3.config(image=self.img_init) #換圖片
        return
    def time_updata(self):
        self.gym_new_time = int(time.time() - self.gym_start_time)
        #self.leftcounter, self.rightcounter, self.leftstage, self.rightstage
        #round(1.2312, 2)#1.23
        #self.message.set(str(int(self.gym_new_time)))

        hand_status = None
        finger_points = []   
        if(self.hand_value): # 偵測 ok
            if self.hand_result.multi_hand_landmarks:
                for hand_landmarks in self.hand_result.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x * self.imgWidth
                        y = i.y * self.imgHeight
                        finger_points.append((x,y))
                    if finger_points:
                        finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                        #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )76
                        hand_status = hand_pos(finger_angle)     # 取得手勢所回傳的內容
            if hand_status == 'ok' and self.hand_ok_status == False:
                self.hand_ok_status = True
                self.hand_ok_time = time.time()
            elif hand_status == 'ok':
                self.hand_ok_count = time.time() - self.hand_ok_time
            else:
                self.hand_ok_status = False
                self.hand_ok_time = time.time()
                self.hand_ok_count = 0
            if finger_points != []:
                x1, y1 = self.hand_control_xy 
                x1, y1 = int(x1), int(y1)
                x2, y2 = finger_points[8]
                x2, y2 = int(x2), int(y2)
                if hand_status == 'control' and self.hand_control_status == False:
                    self.hand_control_status = True
                    self.hand_control_xy = tuple([x2, y2])
                    self.hand_control_time = time.time()
                    self.hand_control_show_status = 'get'
                elif hand_status == 'control' and self.hand_control_status == True and (abs(x1 - x2) >= 50) and x1 - x2 < 0:
                    self.hand_control_show_status = 'ToRight'
                elif hand_status == 'control' and self.hand_control_status == True and (abs(x1 - x2) >= 50) and x1 - x2 > 0:
                    self.hand_control_show_status = 'ToLeft'
                elif hand_status == 'control' and self.hand_control_status == True and (abs(y1 - y2) >= 50) and y1 - y2 < 0:
                    self.hand_control_show_status = 'ToDown'
                elif hand_status == 'control' and self.hand_control_status == True and (abs(y1 - y2) >= 50) and y1 - y2 > 0:
                    self.hand_control_show_status = 'ToUp'
                elif hand_status != 'control':
                    self.hand_control_status = False
                    self.hand_control_real_status = self.hand_control_show_status
                    self.hand_control_show_status = 'None'
            
            if hand_status == 'control' and self.hand_control_show_status != 'get':
                cv2.circle(self.img, self.hand_control_xy, 20, (255, 0, 0), -1)
                cv2.line(self.img, self.hand_control_xy, (x2, y2), 1, 4)
                cv2.circle(self.img, (x2, y2), 20, (255, 0, 0), -1)
            elif self.hand_control_show_status == 'get':
                cv2.circle(self.img, self.hand_control_xy, 20, (255, 0, 0), -1)
            

            if(self.hand_control_real_status != self.hand_control_real_status_before):
                #self.control_x = 0
                #self.control_y = 0
                if(self.hand_control_real_status == "ToRight"):
                    if(self.control_x < 4):
                        self.control_x = self.control_x + 1
                    #self.control_y = 0
                    self.control_y = self.control_value[self.control_x]
                    #print(self.control_x,self.control_y)
                    text = self.control[self.control_x][self.control_y]
                    if(self.control_x == 0):
                        self.message.set("健身模式：" + text)
                        self.selection_model.set(text)
                        self.selection_model_label["bg"] = "#FF9797"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 1):
                        self.message.set("健身項目：" + text)
                        self.selection_item.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FF9797"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 2):
                        self.message.set("循環次數：" + text)
                        self.selection_cycle.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FF9797"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 3):
                        self.message.set("單項次數：" + text)
                        self.selection_several.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FF9797"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 4):
                        self.message.set("循環間隔(秒)：" + text)
                        self.selection_intervals.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FF9797"
                elif(self.hand_control_real_status == "ToLeft"):
                    if(self.control_x > 0):
                        self.control_x = self.control_x - 1
                    #self.control_y = 0
                    self.control_y = self.control_value[self.control_x]
                    #print(self.control_x,self.control_y)
                    text = self.control[self.control_x][self.control_y]
                    if(self.control_x == 0):
                        self.message.set("健身模式：" + text)
                        self.selection_model.set(text)
                        self.selection_model_label["bg"] = "#FF9797"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 1):
                        self.message.set("健身項目：" + text)
                        self.selection_item.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FF9797"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 2):
                        self.message.set("循環次數：" + text)
                        self.selection_cycle.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FF9797"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 3):
                        self.message.set("單項次數：" + text)
                        self.selection_several.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FF9797"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 4):
                        self.message.set("循環間隔(秒)：" + text)
                        self.selection_intervals.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FF9797"
                        
                elif(self.hand_control_real_status == "ToDown"):
                    if(self.control_y < len(self.control[self.control_x])-1):
                        self.control_y = self.control_y + 1
                    self.control_value[self.control_x] = self.control_y
                    #print(self.control_x,self.control_y)
                    text = self.control[self.control_x][self.control_y]
                    if(self.control_x == 0):
                        self.message.set("健身模式：" + text)
                        self.selection_model.set(text)
                        self.selection_model_label["bg"] = "#FF9797"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 1):
                        self.message.set("健身項目：" + text)
                        self.selection_item.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FF9797"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 2):
                        self.message.set("循環次數：" + text)
                        self.selection_cycle.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FF9797"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 3):
                        self.message.set("單項次數：" + text)
                        self.selection_several.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FF9797"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 4):
                        self.message.set("循環間隔(秒)：" + text)
                        self.selection_intervals.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FF9797"
                        
                    if(self.control_x == 0):    
                        self.callbackFunc()
                elif(self.hand_control_real_status == "ToUp"):
                    if(self.control_y > 0):
                        self.control_y = self.control_y - 1
                    self.control_value[self.control_x] = self.control_y
                    #print(self.control_x,self.control_y)
                    text = self.control[self.control_x][self.control_y]
                    if(self.control_x == 0):
                        self.message.set("健身模式：" + text)
                        self.selection_model.set(text)
                        self.selection_model_label["bg"] = "#FF9797"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 1):
                        self.message.set("健身項目：" + text)
                        self.selection_item.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FF9797"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 2):
                        self.message.set("循環次數：" + text)
                        self.selection_cycle.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FF9797"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 3):
                        self.message.set("單項次數：" + text)
                        self.selection_several.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FF9797"
                        self.selection_intervals_label["bg"] = "#FFFFFF"
                    elif(self.control_x == 4):
                        self.message.set("循環間隔(秒)：" + text)
                        self.selection_intervals.set(text)
                        self.selection_model_label["bg"] = "#FFFFFF"
                        self.selection_item_label["bg"] = "#FFFFFF"
                        self.selection_cycle_label["bg"] = "#FFFFFF"
                        self.selection_several_label["bg"] = "#FFFFFF"
                        self.selection_intervals_label["bg"] = "#FF9797"
                        
                    if(self.control_x == 0):    
                        self.callbackFunc()
                else:
                    pass
                pass
            self.hand_control_real_status_before = self.hand_control_real_status
            
        if self.hand_ok_count >= 3:
            print(self.gym_count_time_1,self.gym_buf_time,self.gym_new_time)
            self.hand_ok_status = False
            self.fitness_start()
            self.hand_ok_count = 0
            #self.hand_value = False
            radius = 40
            center = tuple([int(finger_points[9][0]), int(finger_points[9][1])])
            axes = (radius, radius)
            angle = 0
            startAngle = 0
            endAngle = 360
        
            # http://docs.opencv.org/modules/core/doc/drawing_functions.html#ellipse
            cv2.ellipse(self.img, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
            
        elif self.hand_ok_count > 0:
            radius = 40
            center = tuple([int(finger_points[9][0]), int(finger_points[9][1])])
            axes = (radius, radius)
            angle = 0
            startAngle = 0
            endAngle = int(360 * (self.hand_ok_count/3))
        
            # http://docs.opencv.org/modules/core/doc/drawing_functions.html#ellipse
            cv2.ellipse(self.img, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
        
        
        cv2.rectangle(self.img, (470, 0), (625, 50), (255,255,255), -1)
        cv2.putText(self.img, str(self.hand_control_show_status), (490, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        
        if(self.gym_model == "only one" or self.gym_model == "fitness combo"):
            #self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
            
            self.ret_example,self.img_example = self.captrue_example.read()
            if(self.ret_example):
                #self.img_example = cv2.flip(self.img_example, 1)
                self.img_example = cv2.cvtColor(self.img_example, cv2.COLOR_BGR2RGB)
                self.img_original_example = cv2.resize(self.img_example,(960,720))
                self.img_original_example = Image.fromarray(self.img_original_example)
                self.img_original_example = ImageTk.PhotoImage(image = self.img_original_example)
                self.video1.config(image=self.img_original_example)
                if(self.captrue_example.get(cv2.CAP_PROP_POS_FRAMES) == self.captrue_example.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                    self.captrue_example.set(cv2.CAP_PROP_POS_FRAMES,0)
                    #self.captrue_example = cv2.VideoCapture("./test2.mp4")
            #self.message.set("only one")
            #self.message.set("fitness combo")
            if(self.Resting == False):
                if(self.gym_buf_time != self.gym_new_time):
                    self.Second_trigger()
                    pass
                if(self.gym_count_time_1 == 6):
                    cv2.rectangle(self.img, (210, 220), (430, 300), (255, 255, 255), -1)
                    cv2.putText(self.img, "COUNT DOWN", (215, 275),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
                elif(self.gym_count_time_1 > 0 ):
                    t = ""
                    if(self.gym_count_time_1 < int(self.gym_intervals)):
                        t = str(self.gym_count_time_1)
                    else:
                        t = str(self.gym_intervals)
                    if(self.gym_count_time_1 > 99):
                        cv2.rectangle(self.img, (190, 160), (450, 280), (0, 0, 0), -1)
                        cv2.putText(self.img, t, (200, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4, cv2.LINE_AA)
                    elif(self.gym_count_time_1 > 9):
                        cv2.rectangle(self.img, (230, 160), (410, 280), (0, 0, 0), -1)
                        cv2.putText(self.img, t, (240, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4, cv2.LINE_AA)
                    else:
                        cv2.rectangle(self.img, (270, 160), (370, 280), (0, 0, 0), -1)
                        cv2.putText(self.img, t, (280, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4, cv2.LINE_AA)
                    self.message.set("鍛鍊項目：" + self.gym_item_status[self.gym_items_status])
                elif(self.gym_count_time_1 == 0):
                    cv2.rectangle(self.img, (220, 220), (420, 300), (255, 255, 255), -1)
                    cv2.putText(self.img, "START", (230, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            else:
                if(self.gym_buf_time != self.gym_new_time):
                    self.Second_trigger2()
                    pass
                if(self.gym_count_time_1 >= 0 ):
                    t = ""
                    if(self.gym_count_time_1 < int(self.gym_intervals)):
                        t = "Resting " + str(self.gym_count_time_1)
                    else:
                        t = "Resting " + str(self.gym_intervals)
                    if(self.gym_count_time_1 > 99):
                        cv2.rectangle(self.img, (125, 220), (515, 300), (0, 0, 0), -1)
                        cv2.putText(self.img, t, (135, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                    elif(self.gym_count_time_1 > 9):
                        cv2.rectangle(self.img, (140, 220), (500, 300), (0, 0, 0), -1)
                        cv2.putText(self.img, t, (150, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                    elif(self.gym_count_time_1 == 0):
                        cv2.rectangle(self.img, (155, 220), (485, 300), (0, 0, 0), -1)
                        cv2.putText(self.img, 'Now', (270, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                    else:
                        cv2.rectangle(self.img, (155, 220), (485, 300), (0, 0, 0), -1)
                        cv2.putText(self.img, t, (160, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                    self.message.set("鍛鍊項目：" + self.gym_item_status[self.gym_items_status])
                
            if(self.gym_count_time_1 < 0):
                if(self.gym_model == "only one"):
                    if(int(self.gym_cycle_status) > 0):
                        try:
                            landmarks = self.pose_result.pose_landmarks.landmark
                            #self.out = gymMove.curl(landmarks, self.mpPose)
                            #self.out = (self.gym_items[self.gym_item])(landmarks, self.mpPose)
                            #self.out = (self.gym_items[self.gym_item_status[self.gym_items_status]])(landmarks, self.mpPose)
                            gymMove.update(landmarks, self.mpPose)
                            self.out = (self.gym_items[self.gym_item_status[self.gym_items_status]])()
                        except:
                            pass
                        if self.out != None:
                            (self.leftcounter, self.rightcounter, self.leftstage, self.rightstage) = self.out
                            # status box
                            cv2.rectangle(self.img, (0, 0), (250, 73), (245, 117, 16), -1)
                            cv2.rectangle(self.img, (390, 0), (640, 73), (245, 117, 16), -1)

                            # LEFT REPS
                            cv2.putText(self.img, 'REPS', (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.leftcounter), (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                            # LEFT STAGE
                            cv2.putText(self.img, 'STAGE', (85, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.leftstage), (90, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                            # RIGHT REPS
                            cv2.putText(self.img, 'REPS', (405, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.rightcounter), (400, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                            
                            # RIGHT STAGE
                            cv2.putText(self.img, 'STAGE', (475, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.rightstage), (480, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                            
                            
                        if((self.rightcounter >= int(self.gym_several)) and (self.leftcounter >= int(self.gym_several))):
                            self.gym_several_status = True
                        else:
                            self.gym_several_status = False
                            
                        if((self.gym_several_status) == True):
                            self.gym_items_status = 0#重製項目順序
                            self.gym_cycle_status = str(int( self.gym_cycle_status) - 1) #做完一個cycle
                            gymMove.clear()#清空
                            if(int(self.gym_cycle_status) == 0):
                                self.control_x = 0
                                self.control_y = 0
                                self.selection_model_label["bg"] = "#FF9797"
                                self.selection_item_label["bg"] = "#FFFFFF"
                                self.selection_cycle_label["bg"] = "#FFFFFF"
                                self.selection_several_label["bg"] = "#FFFFFF"
                                self.selection_intervals_label["bg"] = "#FFFFFF"
                                self.hand_value = True
                                self.pose_value = False
                                self.captrue_example = cv2.VideoCapture("./test.mp4")
                                self.message.set("已完成所有循環，請選擇健身項目繼續下一個訓練。")
                                self.Resting = False
                                #self.gym_count_time_1 = 0
                                pass
                            else:
                                self.Resting = True
                                self.gym_count_time_1 = int(self.gym_intervals) + 1 #循環間隔
                                self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
                                self.message.set( self.gym_intervals + "秒後開始下一個循環，下一個鍛鍊項目：" + self.gym_item_status[self.gym_items_status])
                            pass
                        else:
                            pass
                        
                        pass
                    else:
                        #self.gym_cycle_status = str(int( self.gym_cycle_status) - 1)
                        #self.gym_items_status = 0
                        #self.gym_count_time_1 = -1
                        #gymMove.clear()
                        pass
                    pass
                elif(self.gym_model == "fitness combo"):
                    if(int(self.gym_cycle_status) > 0):
                        try:
                            landmarks = self.pose_result.pose_landmarks.landmark
                            #self.out = gymMove.curl(landmarks, self.mpPose)
                            #self.out = (self.gym_items[self.gym_item])(landmarks, self.mpPose)
                            #self.out = (self.gym_items[self.gym_item_status[self.gym_items_status]])(landmarks, self.mpPose)
                            gymMove.update(landmarks, self.mpPose)
                            self.out = (self.gym_items[self.gym_item_status[self.gym_items_status]])()
                        except:
                            pass
                        if self.out != None:
                            (self.leftcounter, self.rightcounter, self.leftstage, self.rightstage) = self.out
                            # status box
                            cv2.rectangle(self.img, (0, 0), (250, 73), (245, 117, 16), -1)
                            cv2.rectangle(self.img, (390, 0), (640, 73), (245, 117, 16), -1)

                            # LEFT REPS
                            cv2.putText(self.img, 'REPS', (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.leftcounter), (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                            # LEFT STAGE
                            cv2.putText(self.img, 'STAGE', (85, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.leftstage), (90, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                            # RIGHT REPS
                            cv2.putText(self.img, 'REPS', (405, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.rightcounter), (400, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                            
                            # RIGHT STAGE
                            cv2.putText(self.img, 'STAGE', (475, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                            cv2.putText(self.img, str(self.rightstage), (480, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                            
                            
                        if((self.rightcounter >= int(self.gym_several)) and (self.leftcounter >= int(self.gym_several))):
                            self.gym_several_status = True
                        else:
                            self.gym_several_status = False
                            
                        if((self.gym_several_status) == True):
                            if((len(self.gym_item_status) - 1) == self.gym_items_status):
                                self.gym_items_status = 0#重製項目順序
                                self.gym_cycle_status = str(int( self.gym_cycle_status) - 1) #做完一個cycle
                                if(int(self.gym_cycle_status) == 0):
                                    self.control_x = 0
                                    self.control_y = 0
                                    self.selection_model_label["bg"] = "#FF9797"
                                    self.selection_item_label["bg"] = "#FFFFFF"
                                    self.selection_cycle_label["bg"] = "#FFFFFF"
                                    self.selection_several_label["bg"] = "#FFFFFF"
                                    self.selection_intervals_label["bg"] = "#FFFFFF"
                                    self.hand_value = True
                                    self.pose_value = False
                                    self.captrue_example = cv2.VideoCapture("./test.mp4")
                                    self.message.set("已完成所有循環，請選擇健身項目繼續下一個訓練。")
                                    self.Resting = False
                                    #self.gym_count_time_1 = 0
                                    pass
                                else:
                                    self.Resting = True
                                    self.gym_count_time_1 = int(self.gym_intervals) + 1 #循環間隔
                                    self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
                                    self.message.set( self.gym_intervals + "秒後開始下一個循環，下一個鍛鍊項目：" + self.gym_item_status[self.gym_items_status])
                                pass
                            else:
                                self.Resting = True
                                self.gym_items_status = self.gym_items_status + 1
                                self.gym_count_time_1 = 7 #項目間隔預設7秒
                                self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
                                self.message.set("5秒後開始下一個項目，下一個鍛鍊項目：" + self.gym_item_status[self.gym_items_status])
                                pass
                            gymMove.clear()#清空
                            pass
                        else:
                            pass
                        
                        pass
                    else:
                        #self.gym_cycle_status = str(int( self.gym_cycle_status) - 1)
                        #self.gym_items_status = 0
                        #self.gym_count_time_1 = -1
                        #gymMove.clear()
                        pass
                    pass
                else:
                    pass
        
        else:
            #self.message.set("請選擇好訓練項目、設定好參數後，按下""開始訓練""得繼續訓練。")
            pass
        self.gym_buf_time = int(time.time() - self.gym_start_time)
        #self.message.set(str(self.gym_new_time-self.gym_start_time))
        return
    def Second_trigger(self):
        #測試是不是一秒執行一次用
        #self.message.set(str(self.count))
        #self.count = self.count + 1
        if(self.gym_count_time_1 == 7):
            #self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
            soundwav=pygame.mixer.Sound('sound_5_4_3_2_1.mp3')
            soundwav.play()
        self.gym_count_time_1 = self.gym_count_time_1 - 1
        
        return
    def Second_trigger2(self):
        #測試是不是一秒執行一次用
        #self.message.set(str(self.count))
        #self.count = self.count + 1
        if(self.gym_count_time_1 == 4):
            #self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
            soundwav=pygame.mixer.Sound('sound_3_2_1.mp3')
            soundwav.play()
        self.gym_count_time_1 = self.gym_count_time_1 - 1
        
        return
    def mediapipe_init(self):
        self.mpDraw = mp.solutions.drawing_utils
        #-------------hand-------------
        self.mpHands = mp.solutions.hands
        self.myhands = self.mpHands.Hands()
        self.handLmsStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
        self.handConStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)
        #-------------pose--------------
        self.mpPose = mp.solutions.pose
        #self.myPose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.myPose = self.mpPose.Pose()
        self.PoseLmsStyle = self.mpDraw.DrawingSpec(color=(0,0,0),thickness=5)
        self.PoseConStyle = self.mpDraw.DrawingSpec(color=(255,255,0),thickness=10)
        return
    def mediapipe_hand(self):
        #mediapipe_hands處裡
        #b_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.hand_result = self.myhands.process(self.img)
        if self.hand_result.multi_hand_landmarks:
            #print(len(self.hand_result.multi_hand_landmarks))
            for handLms in self.hand_result.multi_hand_landmarks:#兩隻手所以多一層迴圈
                self.mpDraw.draw_landmarks(self.img,
                                      handLms,#點
                                      self.mpHands.HAND_CONNECTIONS,#連線
                                      self.handLmsStyle,#點的Style
                                      self.handConStyle#連接線的Style
                                      )
                
                for i, lm in enumerate(handLms.landmark):
                    #print(handLms.landmark)
                    xPos = int(lm.x * self.imgWidth)
                    yPos = int(lm.y * self.imgHeight)
                    cv2.putText(self.img,
                                str(i),#字
                                (xPos-25,yPos+5),#位置
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.4,#大小
                                (0,0,255),#顏色
                                2,#租度
                                )
                    '''if i == 4:
                        cv2.circle(self.img,
                                   (xPos,yPos),#中心位置
                                   10,#大小
                                   (0,0,255),#顏色
                                   cv2.FILLED#填滿
                                   )'''
        return
    def mediapipe_pose(self):
        #mediapipe_pose處裡
        
        self.pose_result = self.myPose.process(self.img)
        if self.pose_result.pose_landmarks:
            self.mpDraw.draw_landmarks(self.img,
                                  self.pose_result.pose_landmarks,#點
                                  self.mpPose.POSE_CONNECTIONS,#連線
                                  self.PoseLmsStyle,#點的Style
                                  self.PoseConStyle#連接線的Style
                                  )
            for i, lm in enumerate(self.pose_result.pose_landmarks.landmark):
                xPos = int(lm.x * self.imgWidth)
                yPos = int(lm.y * self.imgHeight)
                #zPos = lm.z
                cv2.putText(self.img,
                            str(i),#字
                            (xPos-25,yPos+5),#位置
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.4,#大小
                            (0,0,255),#顏色
                            2,#租度
                            )
                if (i == 11 or i == 12 or i == 13 or i == 14 or i == 15 or i == 16):
                    cv2.circle(self.img,
                               (xPos,yPos),#中心位置
                               10,#大小
                               (0,255,255),#顏色
                               cv2.FILLED#填滿
                               )
                #print(i, xPos, yPos,zPos)
                #print("i:{} x:{} y:{} z:{}".format(i,xPos,yPos,zPos))
        '''try:
            landmarks = pose_result.pose_landmarks.landmark
            #self.out = gymMove.curl(landmarks, self.mpPose)
            gymMove.update(landmarks, self.mpPose) # update 各個landmarks 後 再進行判斷
            self.out = (self.gym_items[self.gym_item])() # 這樣副函式可以縮短一些
        except:
            pass
        if self.out != None:
            (self.leftcounter, self.rightcounter, self.leftstage, self.rightstage) = self.out
            # status box
            cv2.rectangle(self.img, (0, 0), (250, 73), (245, 117, 16), -1)
            cv2.rectangle(self.img, (390, 0), (640, 73), (245, 117, 16), -1)

            # LEFT REPS
            cv2.putText(self.img, 'REPS', (15, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(self.img, str(self.leftcounter), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # LEFT STAGE
            cv2.putText(self.img, 'STAGE', (85, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(self.img, str(self.leftstage), (90, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # RIGHT REPS
            cv2.putText(self.img, 'REPS', (405, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(self.img, str(self.rightcounter), (400, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            
            # RIGHT STAGE
            cv2.putText(self.img, 'STAGE', (475, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(self.img, str(self.rightstage), (480, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)'''
        
        # 更改動作偵測
        
        #self.pose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)#這行會把記憶體弄爆
        
        #這種寫法在這裡不知道為什麼會讓fps變得特別慢可能與with self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:有關
        '''with self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            pass
            result = pose.process(self.imgRGB)
            try:
                landmarks = result.pose_landmarks.landmark
                self.out = gymMove.curl(landmarks, self.mpPose)
                #self.out = gymMove.triceps_extension(landmarks, self.mpPose)
            except:
                pass
            if self.out != None:
                (leftcounter, rightcounter, leftstage, rightstage) = self.out
                # status box
                cv2.rectangle(self.img, (0, 0), (250, 73), (245, 117, 16), -1)
                cv2.rectangle(self.img, (390, 0), (640, 73), (245, 117, 16), -1)

                # LEFT REPS
                cv2.putText(self.img, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(self.img, str(leftcounter), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                # LEFT STAGE
                cv2.putText(self.img, 'STAGE', (85, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(self.img, str(leftstage), (90, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                # RIGHT REPS
                cv2.putText(self.img, 'REPS', (405, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(self.img, str(rightcounter), (400, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                
                # RIGHT STAGE
                cv2.putText(self.img, 'STAGE', (475, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(self.img, str(rightstage), (480, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)'''
        return
        
    
    def hand_on_off(self):
        if(self.hand_value):
            self.button_hand_text.set("開啟Hand處裡")
            self.hand_value = False
        else:
            self.button_hand_text.set("關閉Hand處裡")
            self.hand_value = True
        return
    def pose_on_off(self):
        if(self.pose_value):
            self.button_pose_text.set("開啟Pose處裡")
            self.pose_value = False
        else:
            self.button_pose_text.set("關閉Pose處裡")
            self.pose_value = True
        return
    def callbackFunc(self,Event = None):
        #global file,filepath,myfile
        #file=combo.get()
        #print(combo.get())
        #self.focus()
        model = self.selection_model.get()
        if(model=="only one"):
            self.item = ["二頭肌彎舉", "三頭肌屈伸","反式屈膝捲腹","伏地挺身","單臂划船","深蹲","墊脚","啞鈴側平舉","啞鈴肩推","開合跳","平面支撐"]
            self.selection_item["values"] = self.item
            self.selection_item.set(self.item[0])
            self.control[1] = self.item
        elif(model == "fitness combo"):
            self.item = ["手部(二頭肌彎舉、三頭肌屈伸)","腹部(反式屈膝捲腹、伏地挺身)","背部(單臂划船)","大腿(深蹲)","小腿(墊脚)","肩膀(啞鈴側平舉、啞鈴肩推)","核心(開合跳、平面支撐)"]
            self.selection_item["values"] = self.item
            self.selection_item.set(self.item[0])
            self.control[1] = self.item
            pass
        return
    def fitness_start(self):
        self.hand_value = False
        self.pose_value = True
        if self.captrue.isOpened():
            self.gym_items_status = 0
            gymMove.clear()
            
            self.gym_model = self.selection_model.get()
            self.gym_item = self.selection_item.get()
            self.gym_cycle = self.selection_cycle.get()
            self.gym_several = self.selection_several.get()
            self.gym_intervals = self.selection_intervals.get()
            
            #self.Resting = False
            if(self.gym_model == "only one"):
                self.gym_item_status = list({self.gym_item})
                #print(self.gym_item_status)
            elif(self.gym_model == "fitness combo"):
                self.gym_item_status = list(self.gym_models[self.gym_item])
                #print(self.gym_item_status)
            else:
                pass
            self.gym_cycle_status = self.gym_cycle
            self.gym_intervals_status = self.gym_intervals
            
            self.message.set("您的選擇是 [" + self.gym_model + "][" + self.gym_item + "][循環" + self.gym_cycle + "次][單項" + self.gym_several + "次][循環間隔" + self.gym_intervals + "秒] 倒數五秒後開始")
            
            self.captrue_example = cv2.VideoCapture(self.gym_items_example[self.gym_item_status[self.gym_items_status]])
            
            self.gym_start_time = time.time()
            self.gym_count_time_1 = 7
            pass
        else:
            self.message.set("請先開啟攝像頭才可以開始訓練。")
        return
    def TK_object(self):
        #------------frame1----------------
        self.frame1 = tk.Frame(bg="#00FFFF",width = 1920 ,height = 720  ,bd=0,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame1.pack_propagate(0)
        self.frame1.grid(row = 0,column = 0)
        #用label來放照片video1
        self.video1_title = tk.Label(self.frame1,width=48,height=1,bg ='gray94',fg='blue',text = '示範影像',font=('微軟正黑體',24,'bold'),relief=tk.GROOVE)
        self.video2_title = tk.Label(self.frame1,width=48,height=1,bg ='gray94',fg='blue',text = '處裡影像',font=('微軟正黑體',24,'bold'),relief=tk.GROOVE)
        #self.video3_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '3D影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        self.video1 = tk.Label(self.frame1,width=960,height=720,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        self.video2 = tk.Label(self.frame1,width=960,height=720,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        #self.video3 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        #frame1物件布局
        self.video1_title.grid(row=0,column=0,padx=0, pady=0)
        self.video2_title.grid(row=0,column=1,padx=0, pady=0)
        #self.video3_title.grid(row=0,column=2,padx=0, pady=0)
        self.video1.grid(row=1,column=0,padx=0, pady=0)
        self.video2.grid(row=1,column=1,padx=0, pady=0)
        #self.video3.grid(row=1,column=2,padx=0, pady=0)
        #------------frame2----------------
        self.frame2 = tk.Frame(bg="#FFFFFF",width = 1920 ,height = 50  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame2.pack_propagate(0)
        self.frame2.grid(row = 1,column = 0)
        #----------對話框label---------------------
        self.message_title_label = tk.Label(self.frame2,text = "即時訊息：",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',16,'bold'))
        self.message = tk.StringVar()
        self.message.set("歡迎使用居家健身輔助軟體，請先開啟攝像頭得繼續操作。")
        self.message_label = tk.Label(self.frame2,textvariable = self.message,width=138,height=1,bd=1,bg="#FFFFFF",fg="#000000",anchor=tk.W,font=('微軟正黑體',16,'bold'))
        #frame2物件布局
        self.message_title_label.grid(row=0, column=0, padx=0, pady=0)
        self.message_label.grid(row=0, column=1, padx=0, pady=0)
        
        #------------frame3----------------
        self.frame3 = tk.Frame(bg="#FFFFFF",width = 1920 ,height = 50  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame3.pack_propagate(0)
        self.frame3.grid(row = 2,column = 0)
        #------------frame3物件------------
        self.selection_model_label = tk.Label(self.frame3,text = "健身模式",width=8,height=1,bd=1,bg="#FF9797",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_model = tk.ttk.Combobox(self.frame3,values=["only one","fitness combo"],width=12,font=('微軟正黑體',20),state="readonly")
        self.selection_model.set("only one")
        #self.selection_model["values"]= ["1","2"]
        self.selection_model.bind("<<ComboboxSelected>>",self.callbackFunc)
        
        self.selection_item_label = tk.Label(self.frame3,text = "健身項目",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_item = tk.ttk.Combobox(self.frame3,values=self.item,width=28,font=('微軟正黑體',20),state="readonly")
        self.selection_item.set(self.gym_item)
        #self.selection_item.bind("<<ComboboxSelected>>",self.callbackFunc1)
        
        self.selection_cycle_label = tk.Label(self.frame3,text = "循環次數",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_cycle = tk.ttk.Combobox(self.frame3,values=["1", "2","3","4","5","6","7","8","9","10"],width=4,font=('微軟正黑體',20),state="readonly")
        self.selection_cycle.set("3")
        #self.selection_cycle.bind("<<ComboboxSelected>>",self.callbackFunc2)
        
        self.selection_several_label = tk.Label(self.frame3,text = "單項次數",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_several = tk.ttk.Combobox(self.frame3,values=["3","6","9","12","15","18","21","24","27","30"],width=4,font=('微軟正黑體',20),state="readonly")
        self.selection_several.set("3")
        #self.selection_several.bind("<<ComboboxSelected>>",self.callbackFunc3)
        
        self.selection_intervals_label = tk.Label(self.frame3,text = "循環間隔(秒)",width=12,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_intervals = tk.ttk.Combobox(self.frame3,values=["10","20","30","40","50","60","120","180","240","300"],width=4,font=('微軟正黑體',20),state="readonly")
        self.selection_intervals.set("10")
        #self.selection_intervals.bind("<<ComboboxSelected>>",self.callbackFunc3)
        
        #按鈕
        self.button_fitness_start = tk.Button(self.frame3,text = '開始訓練',bd=5,height=2,width=12,bg="#000000",fg="#FFFFFF",command =self.fitness_start,font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        
        #self.selection_item["values"]= ["1","2"]
        #self.selection_item.bind("<<ComboboxSelected>>",self.callbackFunc)
        #frame3物件布局
        self.selection_model_label.grid(row=0, column=0, padx=0, pady=0)
        self.selection_model.grid(row=0, column=1, padx=0, pady=0)
        self.selection_item_label.grid(row=0, column=2, padx=0, pady=0)
        self.selection_item.grid(row=0, column=3, padx=0, pady=0)
        self.selection_cycle_label.grid(row=0, column=4, padx=0, pady=0)
        self.selection_cycle.grid(row=0, column=5, padx=0, pady=0)
        self.selection_several_label.grid(row=0, column=6, padx=0, pady=0)
        self.selection_several.grid(row=0, column=7, padx=0, pady=0)
        self.selection_intervals_label.grid(row=0, column=8, padx=0, pady=0)
        self.selection_intervals.grid(row=0, column=9, padx=0, pady=0)
        
        self.button_fitness_start.grid(row=0, column=10, padx=7, pady=2)
        #------------frame4----------------
        self.frame4 = tk.Frame(bg="#FFFFFF",width = 1280 ,height = 20  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame4.pack_propagate(0)
        self.frame4.grid(row = 3,column = 0)
        #------------frame4物件------------
        #frame4物件布局
        #按鈕
        self.button_open = tk.Button(self.frame4,text = '開啟網路攝像頭',bd=5,height=2,width=12,bg ='gray94',command =self.captrue_check,font=('微軟正黑體',12,'bold'))
        self.button_close = tk.Button(self.frame4,text = '關閉網路攝像頭',bd=5,height=2,width=12,bg ='gray94',command =self.captrue_close,font=('微軟正黑體',12,'bold'))
        self.button_hand_text = tk.StringVar()
        self.button_hand_text.set('關閉Hand處裡')
        self.button_hand = tk.Button(self.frame4,textvariable = self.button_hand_text,bd=5,height=2,width=12,bg ='gray94',command =self.hand_on_off,font=('微軟正黑體',12,'bold'))
        self.button_pose_text = tk.StringVar()
        self.button_pose_text.set('關閉Pose處裡')
        self.button_pose = tk.Button(self.frame4,textvariable = self.button_pose_text,bd=5,height=2,width=12,bg ='gray94',command =self.pose_on_off,font=('微軟正黑體',12,'bold'))
        
        self.button_closeTK_text = tk.StringVar()
        self.button_closeTK_text.set('關閉程式')
        self.button_closeTK = tk.Button(self.frame4,textvariable = self.button_closeTK_text,bd=5,height=2,width=12,bg ='gray94',command =self.TK_closing,font=('微軟正黑體',12,'bold'))
        
        #self.label_plank_text = tk.StringVar()
        #self.label_plank_text.set('平板支撐狀態:{}'.format(self.plank_status))
        #self.label_plank = tk.Label(self.frame2,textvariable = self.label_plank_text,bd=5,height=2,width=24,bg ='gray94',font=('微軟正黑體',16,'bold'),anchor=tk.W)

        #frame4物件布局
        self.button_open.grid(row=0, column=0, padx=0, pady=0)
        self.button_close.grid(row=0, column=1, padx=0, pady=0)
        self.button_hand.grid(row=0, column=2, padx=0, pady=0)
        self.button_pose.grid(row=0, column=3, padx=0, pady=0)
        self.button_closeTK.grid(row=0, column=4, padx=0, pady=0)
        #self.label_plank.grid(row=1, column=0, padx=0, pady=0,columnspan = 2)
        return
    def TK_updata(self):
        while True:
            try:
                if(self.Close_Control == False):
                    return
                else:
                    self.update()#更新視窗資訊
                    '''self.frame1['width'] = self.root.winfo_width()
                    self.frame1['height'] = self.root.winfo_height()'''
                    Updata_Start=Timer(0.5,self.TK_updata,[])#thread
                    Updata_Start.start()
                    break
            except:
                continue
        return
    def TK_closing(self):
        #del self.img
        cv2.destroyAllWindows()
        self.Close_Control = False
        self.captrue.release() #關閉相機
        self.quit()
        self.destroy()
        sys.exit()
        return
if __name__ == '__main__':
    Start = MainApplication()
    cv2.destroyAllWindows()
    
