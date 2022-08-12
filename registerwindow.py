import tkinter as tk
import os
import json

import mainwindow

datapath = os.path.join(os.getcwd(), 'data')
if not os.path.exists(datapath):
    os.mkdir(datapath)

class LogInWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # 視窗設定
        self.title("登入界面")
        # size = '%dx%d+%d+%d' % (1920, 1000, 0, 0)
        # self.geometry('350x150+790+460')

        # 個人資料讀取
        self.data = dict()
        try:
            with open(os.path.join(datapath, "account.json"), 'r') as f:
                self.data =json.load(f)
        except:
            #print("data尚未擁有任何資料")
            with open(os.path.join(datapath, "account.json"), 'w') as f:
                json.dump(self.data,f)

        # 界面
        self.username_label = tk.Label(self, text="帳號  ：",width=8,height=2,bg="#0000A0",fg="#00FFFF",font=('微軟正黑體',22,'bold'),relief=tk.GROOVE)
        self.username_text = tk.StringVar()
        self.username_text.set("")
        self.username_entry = tk.Entry(self,textvariable = self.username_text,width=20,font=('微軟正黑體',45),relief=tk.GROOVE)

        self.password_label = tk.Label(self,text="密碼  ：",width=8,height=2,bg="#0000A0",fg="#00FFFF",font=('微軟正黑體',22,'bold'),relief=tk.GROOVE)
        self.password_text = tk.StringVar()
        self.password_text.set("")
        self.password_entry = tk.Entry(self,textvariable = self.password_text,width=20,font=('微軟正黑體',45),relief=tk.GROOVE)
        
        self.login_button=tk.Button(self,text= "登入",command=lambda : self.LOGIN(),width=8, height=2,bg="#004040",fg="#FFFFFF",font=('微軟正黑體',18),relief=tk.GROOVE)
        self.register_button=tk.Button(self,text= "註冊",command=lambda : self.REGISTER_START(),width=8, height=2,bg="#004040",fg="#FFFFFF",font=('微軟正黑體',18),relief=tk.GROOVE)
        
        self.checkbox_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(self, text="顯示" ,width=8, height=2 , variable=self.checkbox_var, anchor=tk.W,font=('微軟正黑體',15,'bold'), command=self.CHANGE_PATTERN)

        self.message_text = tk.StringVar()
        self.message_text.set("請輸入帳號密碼進行登入。")
        self.message_label = tk.Label(self,textvariable = self.message_text,width=44,height=2,bd=5,bg="#FFFFFF",fg="#000000",anchor=tk.W,font=('微軟正黑體',26,'bold'))
        
        # 按鍵設定
        self.bind('<Return>',self.LOGIN)
        self.password_entry.config(show='*')

        # 物件布局
        self.username_label.grid(row=0, column=0, padx=0, pady=0)
        self.username_entry.grid(row=0, column=1, padx=0, pady=0)
        self.password_label.grid(row=1, column=0, padx=0, pady=0)
        self.password_entry.grid(row=1, column=1, padx=0, pady=0)
        self.login_button.grid(row=0, column=2, padx=0, pady=0)
        self.register_button.grid(row=1, column=2, padx=0, pady=0)
        self.checkbox.grid(row=2, column=2, padx=0, pady=0)
        self.message_label.grid(row=3, column=0, padx=0, pady=0,rowspan = 1,columnspan = 3)

        # others button
        self.reg_yes_button=tk.Button(self,text= "確定",command=lambda : self.REGISTER_DONE(),width=8, height=2,bg="#004040",fg="#FFFFFF",font=('微軟正黑體',18),relief=tk.GROOVE)
        self.reg_no_button=tk.Button(self,text= "取消",command=lambda : self.REGISTER_CANCEL(),width=8, height=2,bg="#004040",fg="#FFFFFF",font=('微軟正黑體',18),relief=tk.GROOVE)
        
        self.password_again_label = tk.Label(self,text="重複密碼：",width=8,height=2,bg="#0000A0",fg="#00FFFF",font=('微軟正黑體',22,'bold'),relief=tk.GROOVE)
        self.password_again_text = tk.StringVar()
        self.password_again_text.set("")
        self.password_again_entry = tk.Entry(self,textvariable = self.password_again_text,width=20,font=('微軟正黑體',45),relief=tk.GROOVE)
        self.password_again_entry.config(show='*')

        self.mainloop()

    def REGISTER_START(self):
        self.message_text.set("請輸入帳號密碼進行注冊。")

        # 清空輸入
        self.username_text.set("")
        self.password_text.set("")

        # remove button
        self.login_button.grid_remove()
        self.register_button.grid_remove()

        # change 按鍵觸發
        self.unbind('<Return>')
        self.bind('<Return>',self.REGISTER_DONE)
        
        # add new button

        self.reg_yes_button.grid(row=0, column=2, padx=0, pady=0)
        self.reg_no_button.grid(row=1, column=2, padx=0, pady=0)
        self.password_again_label.grid(row=2, column=0, padx=0, pady=0)
        self.password_again_entry.grid(row=2, column=1, padx=0, pady=0)
        

    def REGISTER_DONE(self, event = None):
        # username and password are not null
        username = self.username_text.get()
        password = self.password_text.get()
        password_again = self.password_again_text.get()
        if username == "" or password == "" :
            self.message_text.set("帳號密碼不可為空。")
            self.username_text.set("")
            self.password_text.set("")
            self.password_again_text.set("")
            return

        # username cannot be registered repeatly
        repeat = False
        for user in self.data:
            if user == username:
                repeat = True

        # password and password(again) must are same
        same = False
        if password == password_again:
            same = True

        if not repeat and same:
            account_data = {
                    "password" : password,
                    "easy": 0,
                    "medium": 0,
                    "hard": 0,
                    "bonus": 0,
                    "Rank": len(self.data) + 1,
                }
            
            self.data[username] = account_data

            # update data
            with open(os.path.join(datapath,"account.json"),"w") as f:
                json.dump(self.data,f)

            self.message_text.set("帳號" + username + "註冊成功！")
            self.username_text.set("")
            self.password_text.set("")
            self.password_again_text.set("")
            self.after(1000, self.REGISTER_END)
        else:
            if repeat:
                self.message_text.set("帳號名稱已存在。")
            elif not same:
                self.message_text.set("密碼不一致。")
            self.username_text.set("")
            self.password_text.set("")
            self.password_again_text.set("")

        

    def REGISTER_CANCEL(self):
        self.message_text.set("取消注冊。")
        self.after(1000, self.REGISTER_END)
    
    def REGISTER_END(self):
        # remove button
        self.reg_yes_button.grid_remove()
        self.reg_no_button.grid_remove()
        self.password_again_label.grid_remove()
        self.password_again_entry.grid_remove()

        # change 按鍵觸發
        self.unbind('<Return>')
        self.bind('<Return>',self.LOGIN)

        self.login_button.grid(row=0, column=2, padx=0, pady=0)
        self.register_button.grid(row=1, column=2, padx=0, pady=0)
        self.message_text.set("請輸入帳號密碼進行登入。")
    
    def LOGIN(self, event = None):
        username = self.username_text.get()
        password = self.password_text.get()

        if username == "" or password == "" :
            self.message_text.set("帳號密碼不可為空。")
            self.username_text.set("")
            self.password_text.set("")
            return

        if username in self.data:
            if self.data[username]['password'] == password:
                self.destroy()
                mainwindow.MainWindow(username)
            else :
                self.message_text.set("密碼錯誤。")
                self.password_text.set("")
        else :
            self.message_text.set("查無此賬號。")
            self.username_text.set("")
            self.password_text.set("")


    def CHANGE_PATTERN(self):
        if self.checkbox_var.get() == 1:
            self.password_entry.config(show='')
            self.password_again_entry.config(show='')
        else:
            self.password_entry.config(show='*')
            self.password_again_entry.config(show='*')

if __name__ == '__main__':
    LogInWindow()