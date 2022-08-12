import tkinter as tk
import cv2
import mediapipe as mp
from PIL import  ImageTk, Image
import time
import os
import json

import registerwindow
import workwindow

datapath = os.path.join(os.getcwd(), 'data')

class MAINSTATUS:
  START = 0
  RANK = 1
  QUIT = 2
  BACK = 3
  EASY = 4
  MEDIUM = 5
  HARD = 6
  NONE = -1

class MainWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()

        # 使用者名稱
        self.username = username

        # 視窗設定
        self.title("主界面")
        self.geometry('%dx%d+%d+%d' % (1920, 1080, 0, 0))
        
        # 建立攝像頭
        self.cap = cv2.VideoCapture(0)
        self.video = tk.Label(self,width=1920,height=1000,bg ='gray94',fg='blue',relief=tk.GROOVE)
        self.video.pack()

        # 初始化 mediapipe hand
        self.mediapipehand_init()
        
        # 計算 fps
        self.pTime = time.time()

        # 操控計數時間
        self.counttime = time.time()

        # 選擇的項目
        self.mainstatus = None

        # 是否在看RANK
        self.InRank = False

        # 是否在選擇LEVEL
        self.InLevel = False

        # 啓動攝像頭 並 永遠執行
        self.capture_open()
        self.mainloop()

    def capture_open(self):
        self.ret, self.img = self.cap.read()
        
        if(self.ret):
            self.img = cv2.flip(self.img, 1) # flip the img
            
            # convert color BGR to RGB
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)#轉RGB
            self.img.flags.writeable = False

            # resize img
            self.img = cv2.resize(self.img,(1280, 960))
            
            # mediapipe hand處裡
            self.mediapipe_hand() # 每個點的x、y、z資訊都在 self.hand_result

            # fps
            self.cTime = time.time()
            self.fps = 1/(self.cTime-self.pTime)
            self.pTime = self.cTime
            cv2.putText(self.img, f"FPS :{int(self.fps)}", (10,470),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (200,200,200), 3)

            # 操作佈局
            if self.InRank:
              # 個人資料讀取
              with open(os.path.join(datapath, "account.json"), 'r') as f:
                self.datas = json.load(f)
                
                cv2.rectangle(self.img, (1080, 0), (1280, 100), (245, 117, 16), -1)
                cv2.putText(self.img, 'BACK', (1100, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
                
                # 透明的Rank表格
                img_copy = self.img.copy()
                cv2.rectangle(img_copy, (100, 50), (1050, 900), (0, 0, 255), -1)
                self.img = cv2.addWeighted(img_copy, 0.5, self.img, 0.5, 1)

                cv2.putText(self.img, 'Username', (150, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, ' Easy ', (350, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, 'Medium', (500, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, ' Hard ', (650, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, ' Bonus ', (800, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, ' Rank ', (950, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)

              for i, username in enumerate(self.datas):
                user = self.datas[username]
                easy = ' ' + str(user['easy']) + ' '
                medium = ' ' + str(user['medium']) + ' '
                hard = ' ' + str(user['hard']) + ' '
                bonus = ' ' + str(user['bonus']) + ' '
                Rank = ' ' + str(user['Rank']) + ' '
                cv2.putText(self.img, username, (150, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, easy, (350, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, medium, (500, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, hard, (650, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, bonus, (800, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
                cv2.putText(self.img, Rank, (950, 115 + i * 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3, cv2.LINE_AA)
            elif self.InLevel:
              cv2.rectangle(self.img, (100, 500), (400, 650), (245, 117, 16), -1)
              cv2.putText(self.img, 'EASY', (135, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)

              cv2.rectangle(self.img, (500, 500), (800, 650), (245, 117, 16), -1)
              cv2.putText(self.img, 'MEDIUM', (505, 600), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0,0,0), 3, cv2.LINE_AA)

              cv2.rectangle(self.img, (900, 500), (1200, 650), (245, 117, 16), -1)
              cv2.putText(self.img, 'HARD', (930, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)

              cv2.rectangle(self.img, (1080, 0), (1280, 100), (245, 117, 16), -1)
              cv2.putText(self.img, 'BACK', (1100, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
            else:
              cv2.rectangle(self.img, (100, 500), (400, 650), (245, 117, 16), -1)
              cv2.putText(self.img, 'START', (115, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)

              cv2.rectangle(self.img, (500, 500), (800, 650), (245, 117, 16), -1)
              cv2.putText(self.img, 'RANK', (525, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)

              cv2.rectangle(self.img, (900, 500), (1200, 650), (245, 117, 16), -1)
              cv2.putText(self.img, 'QUIT', (945, 600), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 3, cv2.LINE_AA)
            try:
              self.img_process = Image.fromarray(self.img)
              self.img_process = ImageTk.PhotoImage(image = self.img_process)
              self.video.config(image=self.img_process)

            except:
              pass
        self.s = self.video.after(1, self.capture_open) # 持續執行open方法，1000為1秒

    def mediapipehand_init(self):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpHands = mp.solutions.hands
        self.myhands = self.mpHands.Hands()
        self.handLmsStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
        self.handConStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)
    
    def mediapipe_hand(self):
        self.hand_result = self.myhands.process(self.img)
        if self.hand_result.multi_hand_landmarks:
          for handLms in self.hand_result.multi_hand_landmarks:
              '''self.mpDraw.draw_landmarks(self.img, handLms,#點
                                    self.mpHands.HAND_CONNECTIONS,#連線
                                    self.handLmsStyle,#點的Style
                                    self.handConStyle#連接線的Style
                                    )'''
              
              for i, lm in enumerate(handLms.landmark):
                  xPos = int(lm.x * 1280)
                  yPos = int(lm.y * 960)
                  '''cv2.putText(self.img, str(i), (xPos-25,yPos+5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                              (0,0,255), 2)'''
                  if i == 8:
                    #print(xPos, yPos)
                    cv2.circle(self.img, (xPos,yPos),
                                10, (0,0,255),
                                cv2.FILLED)
                    if self.InRank == False and self.InLevel == False and 100 < xPos < 400 and 500 < yPos < 650:
                      self.mainstatus = MAINSTATUS.START
                    elif self.InRank == False and self.InLevel == False and 500 < xPos < 800 and 500 < yPos < 650:
                      self.mainstatus = MAINSTATUS.RANK
                    elif self.InRank == False and self.InLevel == False and 900 < xPos < 1200 and 500 < yPos < 650:
                      self.mainstatus = MAINSTATUS.QUIT
                    elif self.InLevel == True and 100 < xPos < 400 and 500 < yPos < 650:
                      self.mainstatus = MAINSTATUS.EASY
                    elif self.InLevel == True and 500 < xPos < 800 and 500 < yPos < 650:
                      self.mainstatus = MAINSTATUS.MEDIUM
                    elif self.InLevel == True and 900 < xPos < 1200 and 500 < yPos < 650:
                      self.mainstatus = MAINSTATUS.HARD
                    elif (self.InRank == True or self.InLevel == True) and 1080 < xPos < 1280 and 0 < yPos < 100:
                      self.mainstatus = MAINSTATUS.BACK
                    else:
                      self.counttime = time.time()
                      self.mainstatus = None
          # 顯示進度條
          holdtime = time.time() - self.counttime
          radius = 40
          center = (1200, 900)
          axes = (radius, radius)
          angle = 0
          startAngle = 0
          if holdtime >= 3:
            self.counttime = time.time()
            endAngle = 360
            cv2.ellipse(self.img, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
            if self.mainstatus == MAINSTATUS.START:
              self.InLevel = True
            elif self.mainstatus == MAINSTATUS.QUIT:
              self.QUIT()
              registerwindow.LogInWindow()
            elif self.mainstatus == MAINSTATUS.RANK:
              self.InRank = True
            elif self.mainstatus == MAINSTATUS.BACK:
              self.InRank = False
              self.InLevel = False
            elif self.mainstatus == MAINSTATUS.EASY:
              self.QUIT()
              workwindow.WorkWindow(self.username, 'easy')
            elif self.mainstatus == MAINSTATUS.MEDIUM:
              self.QUIT()
              workwindow.WorkWindow(self.username, 'medium')
            elif self.mainstatus == MAINSTATUS.HARD:
              self.QUIT()
              workwindow.WorkWindow(self.username, 'hard')
          elif holdtime > 0:
            endAngle = int(360 * (holdtime/3))
            cv2.ellipse(self.img, center, axes, angle, startAngle, endAngle, (0, 255, 255), 30)
          else:
            self.counttime = time.time()

    def QUIT(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.destroy()



if __name__ == '__main__':
    MainWindow('admin')