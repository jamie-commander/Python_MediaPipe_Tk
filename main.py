import tkinter as tk
import tkinter.ttk as ttk

import cv2
from PIL import  ImageTk, Image
import mediapipe as mp

import os
import sys
import time
import pygame

import gymMove
from hand_detect import hand_angle, hand_pos

# 路徑
filepath = os.getcwd() # 取得本地位置
imgpath = os.path.join(filepath, 'img')
videopath = os.path.join(filepath, 'video')
soundpath = os.path.join(filepath, 'sound')
videoDEMOpath = os.path.join(filepath, 'videoDEMO')

class STATUS:
    MENU = 0
    GYM_COUNTDOWN = 1
    GYM_WORKOUT = 2
    GYM_RESTING = 3

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.img_init = ImageTk.PhotoImage(Image.open(os.path.join(imgpath, 'block.jpg')))

        # mediapipe hand and pose's status
        self.hand_value = True
        self.pose_value = False

        # 使用mediapipe hand操控的parameter
        self.hand_ok_status = False
        self.hand_ok_time = time.time()
        self.hand_ok_count = 0

        self.hand_control_status = False
        self.hand_control_xy = (0, 0)
        self.hand_control_time = time.time()
        self.hand_control_show_status = 'None'
        self.hand_control_real_status = 'None'
        self.hand_control_real_status_before = None
        self.hand_flag = False

        # 播放sound的delay
        self.delay_time = time.time()

        # 播放可愛小動畫
        self.capture_cute = cv2.VideoCapture(os.path.join(videopath, 'cute.mp4'))

        # 該做的動作
        self.now_item = []

        # fps
        self.pTime = 0 # previous time
        self.cTime = 0 # current time

        # 界面選項
        self.model = ["only one","fitness combo"]
        self.item = ["二頭肌彎舉", "三頭肌屈伸","反式屈膝捲腹","伏地挺身","單臂划船","深蹲","墊脚","啞鈴側平舉","啞鈴肩推","開合跳","平面支撐"]
        self.cycle = list(str(i) for i in range(2, 6))
        self.several = ["6","8","10","12","15","20","24","30"]
        self.intervals = [str(i) for i in range(3, 11)] + ['15', '30']
        self.control = [self.model, self.item, self.cycle, self.several, self.intervals]

        # 界面選項初始化
        self.control_value = [0,0,0,0,2]

        # 初始化界面選項的x y軸
        self.control_x = 0
        self.control_y = 0

        # parameter
        self.COUNT = {'GYM_COUNTDOWN' : 7,
                        'GYM_RESTING' : 5,
                        }
        self.TIME = {}
        self.Status = STATUS.MENU
        
        # LUT
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
        
        self.gym_items_demo = {
            "二頭肌彎舉": os.path.join(videoDEMOpath, '1.mp4'),
            "三頭肌屈伸": os.path.join(videoDEMOpath, '2.mp4'),
            "反式屈膝捲腹": os.path.join(videoDEMOpath, '3.mp4'),
            "伏地挺身": os.path.join(videoDEMOpath, '4.mp4'),
            "單臂划船": os.path.join(videoDEMOpath, '5.mp4'),
            "深蹲": os.path.join(videoDEMOpath, '6.mp4'),
            "墊脚": os.path.join(videoDEMOpath, '7.mp4'),
            "啞鈴側平舉": os.path.join(videoDEMOpath, '8.mp4'),
            "啞鈴肩推": os.path.join(videoDEMOpath, '9.mp4'),
            "開合跳": os.path.join(videoDEMOpath, '10.mp4'),
            "平面支撐": os.path.join(videoDEMOpath, '11.mp4'),
            }
        
        self.gym_models = {
            "手部(二頭肌彎舉、三頭肌屈伸)":["二頭肌彎舉","三頭肌屈伸"],
            "腹部(反式屈膝捲腹、伏地挺身)":["反式屈膝捲腹","伏地挺身"],
            "背部(單臂划船)":["單臂划船"],
            "大腿(深蹲)":["深蹲"],
            "小腿(墊脚)":["墊脚"],
            "肩膀(啞鈴側平舉、啞鈴肩推)":["啞鈴側平舉","啞鈴肩推"],
            "核心(開合跳、平面支撐)":["開合跳","平面支撐"],
            }

        self.capture_init()
        # self.capture.release()
        
        self.mediapipe_init()
        self.TK_main()
    
    def mediapipe_init(self):
        self.mpDraw = mp.solutions.drawing_utils
        # -------------hand-------------
        self.mpHands = mp.solutions.hands
        self.myhands = self.mpHands.Hands()
        self.handLmsStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
        self.handConStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)
        # -------------pose--------------
        self.mpPose = mp.solutions.pose
        #self.myPose = self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.myPose = self.mpPose.Pose()
        self.PoseLmsStyle = self.mpDraw.DrawingSpec(color=(0,0,0),thickness=5)
        self.PoseConStyle = self.mpDraw.DrawingSpec(color=(255,255,0),thickness=10)
    
    def mediapipe_hand(self):
        # mediapipe_hands處裡
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

    def mediapipe_pose(self):
        # mediapipe_pose處裡
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

    def TK_main(self):
        # -----------------基礎視窗設定--------------------
        self.title("人體骨架辨識軟體v1.0")
        #screenwidth = self.winfo_screenwidth() # 取得作業系統視窗寬度
        #screenheight = self.winfo_screenheight() # 取得作業系統視窗高度
        size = '%dx%d+%d+%d' % (1920, 1000, 0, 0)
        self.geometry(size)#TK視窗大小
        self.maxsize(1920, 1000)#TK視窗最大大小
        self.minsize(1920, 1000)#TK視窗最小大小
        
        # ------------------觸發刷新函式-------------------
        #Updata_Start=Timer(0.5,self.TK_updata,[])#thread
        #Updata_Start.start()

        # ------------------產生視窗物件--------------------
        self.TK_object()

        #--------------------------------------------------
        self.protocol("WM_DELETE_WINDOW", self.TK_closing)#當視窗關閉時觸發
        self.mainloop()

    def TK_object(self):
        #------------frame1----------------
        self.frame1 = tk.Frame(bg="#00FFFF",width = 1920 ,height = 720  ,bd=0,relief=tk.GROOVE) # FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame1.pack_propagate(0)
        self.frame1.grid(row = 0,column = 0)
        #用label來放照片video1
        self.video1_title = tk.Label(self.frame1,width=48,height=1,bg ='gray94',fg='blue',text = '示範影像',font=('微軟正黑體',24,'bold'),relief=tk.GROOVE)
        self.video2_title = tk.Label(self.frame1,width=48,height=1,bg ='gray94',fg='blue',text = '處裡影像',font=('微軟正黑體',24,'bold'),relief=tk.GROOVE)
        self.video1 = tk.Label(self.frame1,width=960,height=720,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        self.video2 = tk.Label(self.frame1,width=960,height=720,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        #frame1物件布局
        self.video1_title.grid(row=0,column=0,padx=0, pady=0)
        self.video2_title.grid(row=0,column=1,padx=0, pady=0)
        self.video1.grid(row=1,column=0,padx=0, pady=0)
        self.video2.grid(row=1,column=1,padx=0, pady=0)

        # ------------frame2----------------
        self.frame2 = tk.Frame(bg="#FFFFFF",width = 1920 ,height = 50  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame2.pack_propagate(0)
        self.frame2.grid(row = 1,column = 0)
        # 對話框 label
        self.message_title_label = tk.Label(self.frame2,text = "即時訊息：",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',16,'bold'))
        self.message = tk.StringVar()
        self.message.set("歡迎使用居家健身輔助軟體，請先開啟攝像頭得繼續操作。")
        self.message_label = tk.Label(self.frame2,textvariable = self.message,width=138,height=1,bd=1,bg="#FFFFFF",fg="#000000",anchor=tk.W,font=('微軟正黑體',16,'bold'))
        # frame2 物件布局
        self.message_title_label.grid(row=0, column=0, padx=0, pady=0)
        self.message_label.grid(row=0, column=1, padx=0, pady=0)

        # ------------frame3----------------
        self.frame3 = tk.Frame(bg="#FFFFFF",width = 1920 ,height = 50  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame3.pack_propagate(0)
        self.frame3.grid(row = 2,column = 0)
        # frame3 物件
        self.selection_model_label = tk.Label(self.frame3,text = "健身模式",width=8,height=1,bd=1,bg="#FF9797",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_model = tk.ttk.Combobox(self.frame3,values=["only one","fitness combo"],width=12,font=('微軟正黑體',20),state="readonly")
        self.selection_model.set("only one")
        self.selection_model.bind("<<ComboboxSelected>>",self.change_model)
        
        self.selection_item_label = tk.Label(self.frame3,text = "健身項目",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_item = ttk.Combobox(self.frame3,values=self.item,width=28,font=('微軟正黑體',20),state="readonly")
        self.selection_item.set(self.item[0])
        
        self.selection_cycle_label = tk.Label(self.frame3,text = "循環次數",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_cycle = ttk.Combobox(self.frame3,values=self.cycle,width=4,font=('微軟正黑體',20),state="readonly")
        self.selection_cycle.set("2")
                
        self.selection_several_label = tk.Label(self.frame3,text = "單項次數",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_several = ttk.Combobox(self.frame3,values=self.several,width=4,font=('微軟正黑體',20),state="readonly")
        self.selection_several.set("6")
        
        self.selection_intervals_label = tk.Label(self.frame3,text = "循環間隔(秒)",width=12,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',20,'bold'))
        self.selection_intervals = ttk.Combobox(self.frame3,values=self.intervals,width=4,font=('微軟正黑體',20),state="readonly")
        self.selection_intervals.set("5")
        
        # 按鈕
        self.button_fitness_start = tk.Button(self.frame3,text = '開始訓練',bd=5,height=2,width=12,bg="#000000",fg="#FFFFFF",command =self.fitness_start,font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        
        # frame3 物件布局
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

        # ------------frame4----------------
        self.frame4 = tk.Frame(bg="#FFFFFF",width = 1280 ,height = 20  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame4.pack_propagate(0)
        self.frame4.grid(row = 3,column = 0)

        # 按鈕
        self.button_open = tk.Button(self.frame4,text = '開啟網路攝像頭',bd=5,height=2,width=12,bg ='gray94',command =self.capture_check,font=('微軟正黑體',12,'bold'))
        self.button_close = tk.Button(self.frame4,text = '關閉網路攝像頭',bd=5,height=2,width=12,bg ='gray94',command =self.capture_close,font=('微軟正黑體',12,'bold'))
        self.button_hand_text = tk.StringVar()
        self.button_hand_text.set('關閉Hand處裡')
        self.button_hand = tk.Button(self.frame4,textvariable = self.button_hand_text,bd=5,height=2,width=12,bg ='gray94',command =self.hand_on_off,font=('微軟正黑體',12,'bold'))
        self.button_pose_text = tk.StringVar()
        self.button_pose_text.set('關閉Pose處裡')
        self.button_pose = tk.Button(self.frame4,textvariable = self.button_pose_text,bd=5,height=2,width=12,bg ='gray94',command =self.pose_on_off,font=('微軟正黑體',12,'bold'))
        
        self.button_closeTK_text = tk.StringVar()
        self.button_closeTK_text.set('關閉程式')
        self.button_closeTK = tk.Button(self.frame4,textvariable = self.button_closeTK_text,bd=5,height=2,width=12,bg ='gray94',command =self.TK_closing,font=('微軟正黑體',12,'bold'))

        # frame4物件布局
        self.button_open.grid(row=0, column=0, padx=0, pady=0)
        self.button_close.grid(row=0, column=1, padx=0, pady=0)
        self.button_hand.grid(row=0, column=2, padx=0, pady=0)
        self.button_pose.grid(row=0, column=3, padx=0, pady=0)
        self.button_closeTK.grid(row=0, column=4, padx=0, pady=0)
    
    def change_model(self, Event = None):
        model = self.selection_model.get()
        print(model)
        if(model=="only one"):
            self.item = ["二頭肌彎舉", "三頭肌屈伸","反式屈膝捲腹","伏地挺身","單臂划船","深蹲","墊脚","啞鈴側平舉","啞鈴肩推","開合跳","平面支撐"]
            self.selection_item["values"] = self.item
            self.selection_item.set(self.item[0])
            self.control[1] = self.item
        else: # fitness combo
            self.item = ["手部(二頭肌彎舉、三頭肌屈伸)","腹部(反式屈膝捲腹、伏地挺身)","背部(單臂划船)","大腿(深蹲)","小腿(墊脚)","肩膀(啞鈴側平舉、啞鈴肩推)","核心(開合跳、平面支撐)"]
            self.selection_item["values"] = self.item
            self.selection_item.set(self.item[0])
            self.control[1] = self.item
    
    def fitness_start(self):
        self.hand_value = False
        self.pose_value = True
        if self.capture.isOpened():
            self.Status = STATUS.GYM_COUNTDOWN # 進入倒數
            gymMove.clear()
            
            self.now_model = self.selection_model.get()
            self.now_item = self.selection_item.get()
            self.now_cycle = self.selection_cycle.get()
            self.now_several = self.selection_several.get()
            self.now_intervals = self.selection_intervals.get()
            
            self.message.set("您的選擇是 [" + self.now_model + "][" + self.now_item + "][循環" + self.now_cycle + "次][單項" + self.now_several + "次][循環間隔" + self.now_intervals + "秒] 倒數五秒後開始")

            if(self.now_model == "fitness combo"):
                self.now_item = [i for i in self.gym_models[self.now_item]]

            else:
                self.now_item = list({self.now_item})
            print(self.now_item)
            self.now_cycle_count = int(self.now_cycle)
            self.now_intervals_count = int(self.now_intervals)
            self.delay_time = time.time()
        else:
            self.message.set("請先開啟攝像頭才可以開始訓練。")

    def capture_check(self):
        self.capture_open()
    
    def capture_init(self):
        self.capture_demo = cv2.VideoCapture("./test.mp4")

        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
        # 設定擷取影像的尺寸大小
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def capture_open(self):
        self.button_open["state"] = tk.DISABLED

        #【Opencv学习（一）】VideoCapture读数据内存泄漏
        # https://blog.csdn.net/liuhuicsu/article/details/62418054
        self.ret, self.img = self.capture.read() # 取得相機畫面
        
        if(self.ret):
            self.img = cv2.flip(self.img, 1) # flip the img
            
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
            
            # 取得圖片高度寬度
            self.imgHeight = self.img.shape[0]
            self.imgWidth = self.img.shape[1]
            # ---------------mediapipe_hand處裡--------------------
            if(self.hand_value):
                self.mediapipe_hand() # 每個點的x、y、z資訊都在 self.hand_result

            # ---------------mediapipe_pose處裡--------------------
            if(self.pose_value):
                self.mediapipe_pose() # 每個點的x、y、z資訊都在 self.pose_result處裡的資料
            # -------------------fps-------------------------------
            self.cTime = time.time()
            self.fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(self.img, f"FPS :{int(self.fps)}",
                        (10,470),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (200,200,200),
                        3)
            
            self.time_update()
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
        
        self.s = self.video1.after(10, self.capture_open) #持續執行open方法，1000為1秒'''
    
    def capture_close(self):
        self.button_open["state"] = tk.NORMAL
        self.capture.release() # 關閉相機
        if(self.s != None):
            self.video1.after_cancel(self.s) # 結束拍照
        
        self.video1.config(image=self.img_init) # 換圖片
        self.video2.config(image=self.img_init) # 換圖片
        
        gymMove.clear()
        self.message.set("攝像頭已經關閉，若想繼續訓練請開啟攝像頭。")

    def time_update(self):
        if self.Status == STATUS.MENU:
            self.INMENU()
        elif self.Status == STATUS.GYM_COUNTDOWN:
            self.INCOUNTDOWN()
            self.capture_demo = cv2.VideoCapture(self.gym_items_demo[self.now_item[0]])
            print("COUNDDOWN:", self.gym_items_demo[self.now_item[0]])
            self.message.set(str(self.now_intervals_count) + "秒後開始下一個循環，下一個鍛鍊項目：" + self.now_item[0])
        elif self.Status == STATUS.GYM_WORKOUT:
            self.INWORKOUT()
        elif self.Status == STATUS.GYM_RESTING:
            self.INRESTING()
        
        if len(self.now_item) != 0:
            # 顯示 demo 影片
            self.ret_demo, self.img_demo = self.capture_demo.read()
            if(self.ret_demo):
                #self.img_demo = cv2.flip(self.img_demo, 1)
                self.img_demo = cv2.cvtColor(self.img_demo, cv2.COLOR_BGR2RGB)
                self.img_original_example = cv2.resize(self.img_demo,(960,720))
                self.img_original_example = Image.fromarray(self.img_original_example)
                self.img_original_example = ImageTk.PhotoImage(image = self.img_original_example)
                self.video1.config(image=self.img_original_example)
                if(self.capture_demo.get(cv2.CAP_PROP_POS_FRAMES) == self.capture_demo.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                    self.capture_demo.set(cv2.CAP_PROP_POS_FRAMES,0)
        else:
            self.ret_demo, self.img_demo = self.capture_cute.read()
            if(self.ret_demo):
                #self.img_demo = cv2.flip(self.img_demo, 1)
                self.img_demo = cv2.cvtColor(self.img_demo, cv2.COLOR_BGR2RGB)
                self.img_original_example = cv2.resize(self.img_demo,(960,720))
                self.img_original_example = Image.fromarray(self.img_original_example)
                self.img_original_example = ImageTk.PhotoImage(image = self.img_original_example)
                self.video1.config(image=self.img_original_example)
                if(self.capture_demo.get(cv2.CAP_PROP_POS_FRAMES) == self.capture_demo.get(cv2.CAP_PROP_FRAME_COUNT) - 1 ):
                    self.capture_demo.set(cv2.CAP_PROP_POS_FRAMES,0)

    def INWORKOUT(self):
        # 判斷動作
        if self.now_cycle_count == 0:
            gymMove.clear() # 清空
            self.now_item.pop(0) # pop 最前一個
            if len(self.now_item) == 0:
                self.message.set("已完成所有循環，請選擇健身項目繼續下一個訓練。")
                self.Status = STATUS.MENU
                self.selection_model_label["bg"] = "#FF9797"
                self.selection_item_label["bg"] = "#FFFFFF"
                self.selection_cycle_label["bg"] = "#FFFFFF"
                self.selection_several_label["bg"] = "#FFFFFF"
                self.selection_intervals_label["bg"] = "#FFFFFF"
                self.hand_value = True
                self.pose_value = False
                self.hand_flag = True
            else:
                self.now_cycle_count = int(self.now_cycle)
                self.Status = STATUS.GYM_COUNTDOWN
                self.capture_demo.release()
        else:
            try:
                landmarks = self.pose_result.pose_landmarks.landmark
                gymMove.update(landmarks, self.mpPose)
                self.out = (self.gym_items[self.now_item[0]])()
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
                
            
            # 完成一個cycle
            if((self.rightcounter >= int(self.now_several)) and (self.leftcounter >= int(self.now_several))):
                gymMove.clear() # 清空
                self.rightcounter = 0
                self.leftcounter = 0
                self.now_cycle_count = self.now_cycle_count - 1
                self.delay_time = time.time()
                if self.now_cycle_count != 0:
                    self.COUNT['GYM_RESTING']  = int(self.now_intervals)
                    self.Status = STATUS.GYM_RESTING

    def INCOUNTDOWN(self):
        if int(time.time() - self.delay_time) == 1:
            self.Second_trigger()
            self.delay_time = time.time()
        if self.COUNT['GYM_COUNTDOWN'] == 6:
            cv2.rectangle(self.img, (210, 220), (430, 300), (255, 255, 255), -1)
            cv2.putText(self.img, "COUNT DOWN", (215, 275),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
        elif(self.COUNT['GYM_COUNTDOWN'] == 0):
            cv2.rectangle(self.img, (220, 220), (420, 300), (255, 255, 255), -1)
            cv2.putText(self.img, "START", (230, 280),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
        else:
            t = ""
            if(self.COUNT['GYM_COUNTDOWN'] < int(self.now_intervals)):
                t = str(self.COUNT['GYM_COUNTDOWN'])
            else:
                t = str(self.now_intervals)
            if(self.COUNT['GYM_COUNTDOWN'] > 99):
                cv2.rectangle(self.img, (190, 160), (450, 280), (0, 0, 0), -1)
                cv2.putText(self.img, t, (200, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4, cv2.LINE_AA)
            elif(self.COUNT['GYM_COUNTDOWN'] > 9):
                cv2.rectangle(self.img, (230, 160), (410, 280), (0, 0, 0), -1)
                cv2.putText(self.img, t, (240, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4, cv2.LINE_AA)
            elif(self.COUNT['GYM_COUNTDOWN'] != 7):
                cv2.rectangle(self.img, (270, 160), (370, 280), (0, 0, 0), -1)
                cv2.putText(self.img, t, (280, 260),
                cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4, cv2.LINE_AA)
            self.message.set("鍛鍊項目：" + self.now_item[0])
    
    def INRESTING(self):
        if int(time.time() - self.delay_time) == 1:
            self.Second_trigger()
            self.delay_time = time.time()
        t = ""
        if(self.COUNT['GYM_RESTING'] < int(self.now_intervals)):
            t = "Resting " + str(self.COUNT['GYM_RESTING'])
        else:
            t = "Resting " + str(self.COUNT['GYM_RESTING'])

        if(self.COUNT['GYM_RESTING'] > 99):
            cv2.rectangle(self.img, (125, 220), (515, 300), (0, 0, 0), -1)
            cv2.putText(self.img, t, (135, 280),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        elif(self.COUNT['GYM_RESTING'] > 9):
            cv2.rectangle(self.img, (140, 220), (500, 300), (0, 0, 0), -1)
            cv2.putText(self.img, t, (150, 280),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        elif(self.COUNT['GYM_RESTING'] == 0):
            cv2.rectangle(self.img, (155, 220), (485, 300), (0, 0, 0), -1)
            cv2.putText(self.img, 'Now', (270, 280),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        else:
            cv2.rectangle(self.img, (155, 220), (485, 300), (0, 0, 0), -1)
            cv2.putText(self.img, t, (160, 280),
            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        self.message.set("鍛鍊項目：" + self.now_item[0])

    def INMENU(self):
        # --------------只使用mediapipe hand 進行操控 ------------------
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
                
            if self.hand_flag == True:
                self.hand_flag = False
            elif finger_points != []:
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
                        self.change_model()
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

    def Second_trigger(self):
        #測試是不是一秒執行一次用
        #self.message.set(str(self.count))
        #self.count = self.count + 1
        if self.Status == STATUS.GYM_COUNTDOWN:
            if(self.COUNT['GYM_COUNTDOWN'] == 7):
                soundwav=pygame.mixer.Sound(os.path.join(soundpath, 'sound_5_4_3_2_1.mp3'))
                soundwav.play()
            if(self.COUNT['GYM_COUNTDOWN'] == 0):
                self.COUNT['GYM_COUNTDOWN'] = 7
                self.Status = STATUS.GYM_WORKOUT
            else:
                self.COUNT['GYM_COUNTDOWN'] = self.COUNT['GYM_COUNTDOWN'] - 1
        else:
            if(self.COUNT['GYM_RESTING'] == 4):
                soundwav=pygame.mixer.Sound(os.path.join(soundpath, 'sound_3_2_1.mp3'))
                soundwav.play()
            if(self.COUNT['GYM_RESTING'] == 0):
                self.COUNT['GYM_RESTING'] = int(self.now_intervals)
                self.Status = STATUS.GYM_WORKOUT
            else:
                self.COUNT['GYM_RESTING'] = self.COUNT['GYM_RESTING'] - 1
        
    def hand_on_off(self):
        if(self.hand_value):
            self.button_hand_text.set("開啟Hand處裡")
            self.hand_value = False
        else:
            self.button_hand_text.set("關閉Hand處裡")
            self.hand_value = True

    def pose_on_off(self):
        if(self.pose_value):
            self.button_pose_text.set("開啟Pose處裡")
            self.pose_value = False
        else:
            self.button_pose_text.set("關閉Pose處裡")
            self.pose_value = True

    def TK_closing(self):
        cv2.destroyAllWindows()
        self.Close_Control = False
        self.capture.release() # 關閉相機
        self.quit()
        self.destroy()
        sys.exit()

if __name__ == '__main__':
    # TODO: sign in

    # init pygame
    pygame.init()
    pygame.mixer.init()
    pygame.time.delay(1000)#等待1秒讓mixer完成初始化
    # start APP
    MainApplication()
    cv2.destroyAllWindows()


