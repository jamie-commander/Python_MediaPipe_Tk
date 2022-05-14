import os
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
        self.img_init= ImageTk.PhotoImage(Image.open('block.jpg'))
        self.pTime = 0 #previous time
        self.cTime = 0 #current time
        self.hand_value = True
        self.pose_value = True
        self.s = None
        
        self.gym_model_status = None
        self.gym_item_status = None
        self.gym_cycle_status = None
        self.gym_several_status = None
        self.gym_intervals_status = None
        
        self.gym_model = "only one"
        self.gym_item = "二頭肌"
        self.gym_cycle = "3"
        self.gym_several = "12"
        self.gym_intervals = "30"
        
        self.sys_start_time = time.time()
        self.sys_bus_time1 = 0
        self.sys_bus_time2 = 0
        self.sys_bus_time3 = 0
        self.sys_new_time = 0
        
        #self.plank_status = False #平板支撐的狀態
        self.out = None
        self.captrue_init()
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
        size = '%dx%d+%d+%d' % (1280, 900, (screenwidth-1280)/2, (screenheight-900)/2)
        self.geometry(size)#TK視窗大小
        self.maxsize(1280, 900)#TK視窗最大大小
        self.minsize(1280, 900)#TK視窗最小大小
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
        self.captrue = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
        #self.captrue.set(3,350) #像素
        #self.captrue.set(4,500) #像素
        # 設定擷取影像的尺寸大小
        self.captrue.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.captrue.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return
    def captrue_check(self):
        if self.captrue.isOpened(): #判斷相機是否有開啟
            self.captrue_open()
        else:
            self.captrue_init()
            self.captrue_open()
        return
    def captrue_open(self):
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
            
            self.img_original = Image.fromarray(self.img)
            self.img_original = ImageTk.PhotoImage(image = self.img_original)
            self.video1.config(image=self.img_original)
            
            # convert color BGR to RGB
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)#轉RGB
            self.img.flags.writeable = False
            
            
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
            #--------------處裡完成轉回RGB----------
            # convert color RGB to BGR
            self.img.flags.writeable = True
            self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
            
            #------------在tk第一個畫面上秀出處理圖片---------------------
            self.img_process = Image.fromarray(self.img)
            self.img_process = ImageTk.PhotoImage(image = self.img_process)
            self.video2.config(image=self.img_process)
            
            #cv2.imwrite(self.img_video_process,self.img)#儲存處裡後圖片
            #cv2.imshow('img',self.img)
        self.time_updata()
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
        #self.video3.config(image=self.img_init) #換圖片
        return
    def time_updata(self):
        self.sys_new_time = time.time()
        self.message.set(str(self.sys_new_time-self.sys_start_time))
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
        
        pose_result = self.myPose.process(self.img)
        if pose_result.pose_landmarks:
            self.mpDraw.draw_landmarks(self.img,
                                  pose_result.pose_landmarks,#點
                                  self.mpPose.POSE_CONNECTIONS,#連線
                                  self.PoseLmsStyle,#點的Style
                                  self.PoseConStyle#連接線的Style
                                  )
            for i, lm in enumerate(pose_result.pose_landmarks.landmark):
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
        #不曉得為何這樣不行
        try:
            landmarks = pose_result.pose_landmarks.landmark
            self.out = gymMove.curl(landmarks, self.mpPose)
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
    def callbackFunc(self,Event):
        #global file,filepath,myfile
        #file=combo.get()
        #print(combo.get())
        #self.focus()
        model = self.selection_model.get()
        if(model=="only one"):
            item = ["二頭肌彎舉", "三頭肌屈伸","反式屈膝捲腹","伏地挺身","單臂划船","深蹲","墊脚","啞鈴側平舉","啞鈴肩推","開合跳","平面支撐"]
            self.selection_item["values"] = item
            self.selection_item.set(item[0])
        elif(model == "fitness combo"):
            item = ["手部(二頭肌彎舉、三頭肌屈伸)","腹部(反式屈膝捲腹、伏地挺身)","背部(單臂划船)","大腿(深蹲)","小腿(墊脚)","肩膀(啞鈴側平舉、啞鈴肩推)","核心(開合跳、平面支撐)"]
            self.selection_item["values"] = item
            self.selection_item.set(item[0])
            pass
        return
    def fitness_start(self):
        self.gym_model = self.selection_model.get()
        self.gym_item = self.selection_item.get()
        self.gym_cycle = self.selection_cycle.get()
        self.gym_several = self.selection_several.get()
        self.gym_intervals = self.selection_intervals.get()
        self.message.set("您的選擇是 [" + self.gym_model + "][" + self.gym_item + "][循環" + self.gym_cycle + "次][單項" + self.gym_several + "次][循環間隔" + self.gym_intervals + "秒] 在五秒後開始")
        return
    def TK_object(self):
        #------------frame1----------------
        self.frame1 = tk.Frame(bg="#00FFFF",width = 1280 ,height = 500  ,bd=0,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame1.pack_propagate(0)
        self.frame1.grid(row = 0,column = 0)
        #用label來放照片video1
        self.video1_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '原始影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        self.video2_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '處裡影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        #self.video3_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '3D影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        self.video1 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        self.video2 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        #self.video3 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        #frame1物件布局
        self.video1_title.grid(row=0,column=0,padx=0, pady=0)
        self.video2_title.grid(row=0,column=1,padx=0, pady=0)
        #self.video3_title.grid(row=0,column=2,padx=0, pady=0)
        self.video1.grid(row=1,column=0,padx=0, pady=0)
        self.video2.grid(row=1,column=1,padx=0, pady=0)
        #self.video3.grid(row=1,column=2,padx=0, pady=0)
        #------------frame2----------------
        self.frame2 = tk.Frame(bg="#FFFFFF",width = 1270 ,height = 20  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame2.pack_propagate(0)
        self.frame2.grid(row = 1,column = 0)
        #----------對話框label---------------------
        self.message_title_label = tk.Label(self.frame2,text = "即時訊息：",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',16,'bold'))
        self.message = tk.StringVar()
        self.message.set("歡迎使用居家健身輔助軟體")
        self.message_label = tk.Label(self.frame2,textvariable = self.message,width=89,height=1,bd=1,bg="#FFFFFF",fg="#000000",anchor=tk.W,font=('微軟正黑體',16,'bold'))
        #frame2物件布局
        self.message_title_label.grid(row=0, column=0, padx=0, pady=0)
        self.message_label.grid(row=0, column=1, padx=0, pady=0)
        
        #------------frame3----------------
        self.frame3 = tk.Frame(bg="#FFFFFF",width = 1280 ,height = 360  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame3.pack_propagate(0)
        self.frame3.grid(row = 2,column = 0)
        #------------frame3物件------------
        self.selection_model_label = tk.Label(self.frame3,text = "健身模式",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',12,'bold'))
        self.selection_model = tk.ttk.Combobox(self.frame3,values=["only one","fitness combo"],width=12,font=('微軟正黑體',12),state="readonly")
        self.selection_model.set(self.gym_model)
        #self.selection_model["values"]= ["1","2"]
        self.selection_model.bind("<<ComboboxSelected>>",self.callbackFunc)
        
        self.selection_item_label = tk.Label(self.frame3,text = "健身項目",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',12,'bold'))
        self.selection_item = tk.ttk.Combobox(self.frame3,values=["二頭肌彎舉", "三頭肌屈伸","單臂划船","反式屈膝捲腹","深蹲","墊脚","啞鈴側平舉","啞鈴肩推","開合跳","平面支撐"],width=36,font=('微軟正黑體',12),state="readonly")
        self.selection_item.set(self.gym_item)
        
        self.selection_cycle_label = tk.Label(self.frame3,text = "循環次數",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',12,'bold'))
        self.selection_cycle = tk.ttk.Combobox(self.frame3,values=["1", "2","3","4","5","6","7","8","9","10"],width=4,font=('微軟正黑體',12),state="readonly")
        self.selection_cycle.set("3")
        
        self.selection_several_label = tk.Label(self.frame3,text = "單項次數",width=8,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',12,'bold'))
        self.selection_several = tk.ttk.Combobox(self.frame3,values=["3","6","9","12","15","18","21","24","27","30"],width=4,font=('微軟正黑體',12),state="readonly")
        self.selection_several.set("12")
        
        self.selection_intervals_label = tk.Label(self.frame3,text = "循環間隔(秒)",width=12,height=1,bd=1,bg="#FFFFFF",fg="#000000",font=('微軟正黑體',12,'bold'))
        self.selection_intervals = tk.ttk.Combobox(self.frame3,values=["10","20","30","40","50","60","120","180","240","300"],width=4,font=('微軟正黑體',12),state="readonly")
        self.selection_intervals.set("30")
        
        #按鈕
        self.button_fitness_start = tk.Button(self.frame3,text = '開始訓練',bd=5,height=2,width=12,bg="#000000",fg="#FFFFFF",command =self.fitness_start,font=('微軟正黑體',12,'bold'),relief=tk.GROOVE)
        
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
        self.button_open = tk.Button(self.frame4,text = '開啟網路攝像頭',bd=5,height=2,width=12,bg ='gray94',command =self.captrue_check,font=('微軟正黑體',16,'bold'))
        self.button_close = tk.Button(self.frame4,text = '關閉網路攝像頭',bd=5,height=2,width=12,bg ='gray94',command =self.captrue_close,font=('微軟正黑體',16,'bold'))
        self.button_hand_text = tk.StringVar()
        self.button_hand_text.set('關閉Hand處裡')
        self.button_hand = tk.Button(self.frame4,textvariable = self.button_hand_text,bd=5,height=2,width=12,bg ='gray94',command =self.hand_on_off,font=('微軟正黑體',16,'bold'))
        self.button_pose_text = tk.StringVar()
        self.button_pose_text.set('關閉Pose處裡')
        self.button_pose = tk.Button(self.frame4,textvariable = self.button_pose_text,bd=5,height=2,width=12,bg ='gray94',command =self.pose_on_off,font=('微軟正黑體',16,'bold'))
        
        self.button_closeTK_text = tk.StringVar()
        self.button_closeTK_text.set('關閉程式')
        self.button_closeTK = tk.Button(self.frame4,textvariable = self.button_closeTK_text,bd=5,height=2,width=12,bg ='gray94',command =self.TK_closing,font=('微軟正黑體',16,'bold'))
        
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
    
