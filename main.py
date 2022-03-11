import os
import random
import json
import time
import sys
#from tkinter import *
import tkinter as tk
from PIL import  ImageTk, Image, ImageDraw
import cv2
from threading import Timer
import mediapipe as mp
from CalcFunction import calc_on_line, calc_angle

from torch import threshold

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
        self.plank_status = False #平板支撐的狀態
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
        size = '%dx%d+%d+%d' % (1920, 900, (screenwidth-1920)/2, (screenheight-900)/2)
        self.geometry(size)#TK視窗大小
        self.maxsize(1920, 900)#TK視窗最大大小
        self.minsize(1920, 900)#TK視窗最小大小
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
        ret,self.img = self.captrue.read() #取得相機畫面
        self.img = cv2.flip(self.img, 1) # 
        #cv2.imwrite(self.img_viode,img)
        if(ret):
            cv2.imwrite(self.img_video,self.img) #儲存最原始圖片
            
            self.imgRGB = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)#轉RGB
            
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
                        (30,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255,0,0),
                        3)
            cv2.imwrite(self.img_video_process,self.img)#儲存處裡後圖片
            #cv2.imshow('img',self.img)
        self.img_original = ImageTk.PhotoImage(Image.open(self.img_video)) #讀取圖片
        self.video1.imgtk=self.img_original #換圖片
        self.video1.config(image=self.img_original) #換圖片

        self.img_process = ImageTk.PhotoImage(Image.open(self.img_video_process)) #讀取圖片
        self.video2.imgtk=self.img_process #換圖片
        self.video2.config(image=self.img_process) #換圖片

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
        self.video3.config(image=self.img_init) #換圖片
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
        self.myPose = self.mpPose.Pose()
        self.PoseLmsStyle = self.mpDraw.DrawingSpec(color=(0,0,0),thickness=5)
        self.PoseConStyle = self.mpDraw.DrawingSpec(color=(255,255,0),thickness=10)
        return
    def mediapipe_hand(self):
        #mediapipe_hands處裡
        
        self.hand_result = self.myhands.process(self.imgRGB)
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
        
        self.pose_result = self.myPose.process(self.imgRGB)
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
                '''if (i == 11 or i == 12 or i == 13 or i == 14 or i == 15 or i == 16):
                    cv2.circle(self.img,
                               (xPos,yPos),#中心位置
                               10,#大小
                               (0,255,255),#顏色
                               cv2.FILLED#填滿
                               )'''
                #print(i, xPos, yPos,zPos)
                #print("i:{} x:{} y:{} z:{}".format(i,xPos,yPos,zPos))
            self.detect_plank(self.pose_result.pose_landmarks.landmark)
        return
    
    def detect_plank(self, lms): #偵測是否有平板支撐的動作
        # 12 -> right shoulder
        # 24 -> right hip
        # 26 -> right knee
        # 28 -> right ankle

        shoulder_x = lms[12].x
        shoulder_y = lms[12].y
        elbow_x = lms[14].x
        elbow_y = lms[14].y
        hip_x = lms[24].x
        hip_y = lms[24].y
        knee_x = lms[26].x
        knee_y = lms[26].y
        ankle_x = lms[28].x
        ankle_y = lms[28].y
        #-----------------門檻值 Hyperparameter--------------------
        # 可更改
        threshold_max_ShoulderAnkle_angle = 10
        threshold_min_ShoulderElbow_angle = 63
        threshold_max_ShoulderElbow_angle = 83
        threshold_Hip = 110
        threshold_Knee = 110
        #------------------------------------------------
        # 計算ankle與shoulder之間的角度
        status1 = calc_angle(shoulder_x, shoulder_y, ankle_x, ankle_y, threshold_max_angle=threshold_max_ShoulderAnkle_angle) 
        # 計算elbow與shoulder之間的角度
        status2 = calc_angle(shoulder_x, shoulder_y, elbow_x, elbow_y, threshold_min_ShoulderElbow_angle, threshold_max_ShoulderElbow_angle) 
        # 計算hip是否在ankle與shoulder之間
        status3 = calc_on_line(hip_x, hip_y, shoulder_x, shoulder_y, ankle_x, ankle_y, threshold_Hip)
        # 計算膝蓋是否在ankle與shoulder之間
        status4 = calc_on_line(knee_x, knee_y, shoulder_x, shoulder_y, ankle_x, ankle_y, threshold_Knee)

        self.plank_status = (status1 and status2 and status3 and status4)
        self.label_plank_text.set('平板支撐狀態:{}'.format(self.plank_status))
        
    
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
    def TK_object(self):
        #------------frame1----------------
        self.frame1 = tk.Frame(bg="#00FFFF",width = 1920 ,height = 500  ,bd=0,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame1.pack_propagate(0)
        self.frame1.grid(row = 0,column = 0)
        #用label來放照片video1
        self.video1_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '原始影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        self.video2_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '處裡影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        self.video3_title = tk.Label(self.frame1,width=49,height=1,bg ='gray94',fg='blue',text = '3D影像',font=('微軟正黑體',16,'bold'),relief=tk.GROOVE)
        self.video1 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        self.video2 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        self.video3 = tk.Label(self.frame1,width=640,height=480,bg ='gray94',fg='blue',image = self.img_init,relief=tk.GROOVE)
        #frame1物件布局
        self.video1_title.grid(row=0,column=0,padx=0, pady=0)
        self.video2_title.grid(row=0,column=1,padx=0, pady=0)
        self.video3_title.grid(row=0,column=2,padx=0, pady=0)
        self.video1.grid(row=1,column=0,padx=0, pady=0)
        self.video2.grid(row=1,column=1,padx=0, pady=0)
        self.video3.grid(row=1,column=2,padx=0, pady=0)
        #------------frame2----------------
        self.frame2 = tk.Frame(bg="#FFFFFF",width = 1920 ,height = 400  ,bd=5,relief=tk.GROOVE)#FLAT SUNKEN RAISED GROOVE RIDGE
        self.frame2.pack_propagate(0)
        self.frame2.grid(row = 1,column = 0)
        #按鈕
        self.button_open = tk.Button(self.frame2,text = '開啟網路攝像頭',bd=5,height=2,width=22,bg ='gray94',command =self.captrue_check,font=('微軟正黑體',16,'bold'))
        self.button_close = tk.Button(self.frame2,text = '關閉網路攝像頭',bd=5,height=2,width=22,bg ='gray94',command =self.captrue_close,font=('微軟正黑體',16,'bold'))
        self.button_hand_text = tk.StringVar()
        self.button_hand_text.set('關閉Hand處裡')
        self.button_hand = tk.Button(self.frame2,textvariable = self.button_hand_text,bd=5,height=2,width=22,bg ='gray94',command =self.hand_on_off,font=('微軟正黑體',16,'bold'))
        self.button_pose_text = tk.StringVar()
        self.button_pose_text.set('關閉Pose處裡')
        self.button_pose = tk.Button(self.frame2,textvariable = self.button_pose_text,bd=5,height=2,width=22,bg ='gray94',command =self.pose_on_off,font=('微軟正黑體',16,'bold'))
        self.label_plank_text = tk.StringVar()
        self.label_plank_text.set('平板支撐狀態:{}'.format(self.plank_status))
        self.label_plank = tk.Label(self.frame2,textvariable = self.label_plank_text,bd=5,height=2,width=22,bg ='gray94',font=('微軟正黑體',16,'bold'))
        #frame2物件布局
        self.button_open.grid(row=0, column=0, padx=0, pady=0)
        self.button_close.grid(row=0, column=1, padx=0, pady=0)
        self.button_hand.grid(row=0, column=2, padx=0, pady=0)
        self.button_pose.grid(row=0, column=3, padx=0, pady=0)
        self.label_plank.grid(row=1, column=0, padx=0, pady=0)
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
        self.Close_Control = False
        self.captrue.release() #關閉相機
        self.quit()
        self.destroy()
        sys.exit()
        return
if __name__ == '__main__':
    Start = MainApplication()
    

