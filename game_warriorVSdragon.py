#width=960,height=720

from tkinter import Tk, Frame, Canvas, PhotoImage, Text, Button, messagebox, NW
import os
import random
from turtle import position

imgpath = os.path.join(os.getcwd(), 'img')

class Character:
    def __init__(self, runpath, canvas, position : bool = True, x : int = 0, y : int = 500, name='Warrior', hp : int = 1000):
        self.canvas = canvas
        self.position = position # right:False // left:True
        self.x = x
        self.y = y
        self.name = name
        self.live = True

        # run images
        self.run_images = {}
        self.move_count = 0
        self.run_images['run0']  =(PhotoImage(file = os.path.join(runpath,"run0.png")))
        self.run_images['run1']  =(PhotoImage(file = os.path.join(runpath,"run1.png")))
        #self.run_images['run2']  =(PhotoImage(file = os.path.join(runpath,"run2.png")))
        #self.run_images['run3']  =(PhotoImage(file = os.path.join(runpath,"run1.png")))
        self.run_images['stand'] =(PhotoImage(file = os.path.join(runpath,"stand.png")))
        self.run_images['attack']=(PhotoImage(file = os.path.join(runpath,"attack.png")))
        self.run_images['hurt']=(PhotoImage(file = os.path.join(runpath,"hurt.png")))
        self.run_images['lose0']  =(PhotoImage(file = os.path.join(runpath,"lose0.png")))
        self.run_images['lose1']  =(PhotoImage(file = os.path.join(runpath,"lose1.png")))
        self.run_images['win0']   =(PhotoImage(file = os.path.join(runpath,"win0.png")))
        self.run_images['win1']   =(PhotoImage(file = os.path.join(runpath,"win1.png")))
        self.image_on_canvas = self.canvas.create_image(self.x, self.y, anchor = NW, image = self.run_images['stand'])

        # HP
        self.maxhp = hp
        self.hp = hp

        # run_status
        self.run_finish = False

        # NAME HP_bar HP_status
        if position:
            self.canvas.create_text(105, 35, text=self.name, font=('Arial', 18))
            self.HP_bar = self.canvas.create_rectangle(50, 50, 50+3*(self.maxhp//10), 70,fill='green')
            self.HP_status = self.canvas.create_text(115, 85, text="[%3d/%3d]" % (self.hp,self.maxhp), font=('Arial', 18))
        else:
            self.canvas.create_text(860, 35, text=self.name, font=('Arial', 18))
            self.HP_bar = self.canvas.create_rectangle(910-3*(self.maxhp//10), 50, 910, 70,fill='blue')
            self.HP_status = self.canvas.create_text(850, 85, text="[%3d/%3d]" % (self.hp,self.maxhp), font=('Arial', 18))
    
    def run(self):
        self.move_count += 1
        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['run'+str(self.move_count%2)])
        if self.position == False:
            move_step = -7
        else:
            move_step = 7
        self.canvas.move(self.image_on_canvas, move_step, 0)
        # TODO: show the fight img
        if self.move_count < 24:
            self.canvas.after(200, self.run)
        else:
            self.canvas.after(200, self.stand)
            self.run_finish = True
    
    def stand(self):
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['stand'])

    def attack(self, enemy, dmg: int = 0):
        enemy.hurted(dmg)
        # action
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['attack'])
        self.canvas.after(500, self.stand)

    def hurted(self, hp):
        self.hp -= hp
        if self.hp < 0:
            self.hp = 0 

        # HP bar update
        x0, y0, x1, y1 = self.canvas.coords(self.HP_bar)
        if self.position:
            x1 = 50+3*(self.hp//10)
        else:
            x0 = 910-3*(self.hp//10)

        self.canvas.coords(self.HP_bar, x0, y0, x1, y1)

        # HP status update
        self.canvas.itemconfig(self.HP_status, text="[%3d/%3d]" % (self.hp,self.maxhp))

        # change bar color
        if self.hp <= self.maxhp // 5:
            self.canvas.itemconfig(self.HP_bar, fill='red')
        elif self.hp <= self.maxhp // 2:
            self.canvas.itemconfig(self.HP_bar, fill='yellow')

        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['hurt'])
        self.canvas.after(1000, self.stand)

    def lose(self):
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['lose'+str(self.move_count%2)])
        self.move_count+=1
        self.live = False
        self.canvas.after(200, self.lose)

    def win(self):
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['win'+str(self.move_count%2)])
        if self.position:
            print(1)
            if self.move_count % 2 == 0:
                move_step = 30
            else:
                move_step = -30
            self.canvas.move(self.image_on_canvas, 0, move_step)
            
        self.move_count+=1
        self.canvas.after(200, self.win)

    def destory(self):
        self.canvas.delete(self.image_on_canvas)
        self.canvas.delete(self.HP_bar)
        self.canvas.delete(self.HP_status)

class GameFrame(Frame):
    window_width = 960
    window_height = 720
    PAUSE = False
    warning = None
    
    def __init__(self, tk, width=window_width, height=window_width):
        Frame.__init__(self, tk, width=width, height=height)
        self.focus_set()

        self.gameover = False

        # display object
        self.display()

        self.bind('<Return>', self.player_attack)
        #self.bind('<space>', self.player_attack)

        # font counter
        self.font_counter = []

        # check font counter
        popList = []
        for i in range(len(self.font_counter)):
            if self.font_counter[i][1] == 0:
                self.canvas.delete(self.font_counter[i][0])
                popList.append(i)
            else:
                self.font_counter[i][1] -= 1

        for count, i in enumerate(popList):
            self.font_counter.pop(i - count)

        # player
        self.player = Character(os.path.join(imgpath, 'warrior/') ,self.canvas, position=True, x=-70, y=350, name="Warrior", hp=1000)
        # dragon
        self.dragon = Character(os.path.join(imgpath, 'dragon/') ,self.canvas, position=False, x=self.window_width - 200, y=350, name="dragon", hp=1000)
        
        self.dragon_hit_count = random.randint(50, 100)
        self.start_game()
    
    def start_game(self):
        self.player.run()
        self.dragon.run()
        self.update()

    def update(self):
        if self.player.run_finish == False or self.dragon.run_finish == False:
            self.after(100, self.update)
            return
        # dragon attack in random time
        if not self.PAUSE:
            if self.dragon_hit_count == 0:
                self.dragon_hit_count = random.randint(25, 50)
                self.dragon_attack(random.randint(20, 100))
            else:
                self.dragon_hit_count -= 1
                if self.dragon_hit_count == 0:
                    self.canvas.delete(self.warning)
                elif self.dragon_hit_count == 20:
                    self.warning=self.canvas.create_text(700,150,text='CAREFUL!!',font=('Helvetica',36, 'bold'),fill = 'red')
        
        # check font counter
        popList = []
        for i in range(len(self.font_counter)):
            if self.font_counter[i][1] == 0:
                self.canvas.delete(self.font_counter[i][0])
                popList.append(i)
            else:
                self.font_counter[i][1] -= 1

        for count, i in enumerate(popList):
            self.font_counter.pop(i - count)

        if self.dragon.hp == 0:
            self.GAMEOVER(1)
        elif self.player.hp == 0:
            self.GAMEOVER(0)
        else:
            self.after(100, self.update)

    def display(self):
        self.canvas = Canvas(
            self,
            width=self.window_width,
            height=self.window_height,
            highlightthickness=0)
        # Author: Carol Ling Mei Xin 
        path = os.path.join(imgpath, 'bg.png')
        self.image_bg = PhotoImage(
            file=path)
        self.canvas.create_image(0, 0, image=self.image_bg, anchor=NW)
        self.canvas.pack()
        '''
        # TextBox Creation
        self.inputtxt = Text(self, height = 2, width = 20)
        self.inputtxt.grid(row=1, column=0)
        
        # Button Creation
        attackButton = Button(self, text = "Attack", height = 2, width = 20, command = self.player_attack)
        attackButton.grid(row=1, column=1)

        restartButton = Button(self, text = "restart", height = 2, width = 20, command = self.restart)
        restartButton.grid(row=1, column=2)

        quitButton = Button(self, text = "quit", height = 2, width = 20, command = self.quit)
        quitButton.grid(row=1, column=3)'''

    def restart(self):
        if self.player: 
            self.player.destory()
        if self.dragon: 
            self.dragon.destory()
        del self.player
        del self.dragon
        # player
        self.player = Character(os.path.join(imgpath, 'warrior/') ,self.canvas, position=True, x=-70, y=350, name="Warrior", hp=100)
        # dragon
        self.dragon = Character(os.path.join(imgpath, 'dragon/') ,self.canvas, position=False, x=self.window_width - 200, y=350, name="dragon", hp=100)
        self.dragon_hit_count = random.randint(1, 100)
        self.start_game()
    
    def quit(self):
        self.player.destory()
        self.dragon.destory()
        self.destroy()

    def dragon_attack(self, dmg, event=None):
        self.dragon.attack(self.player, dmg)
        x = random.randint(400, 700)
        y = random.randint(200, 300)
        c = self.canvas.create_text(x,y,text=str(dmg),font=('Helvetica',36, 'bold'),fill = 'red')
        self.font_counter.append([c, 10])

    def player_attack(self, dmg, event=None):
        self.player.attack(self.dragon, int(dmg))
        x = random.randint(400, 700)
        y = random.randint(200, 300)
        c = self.canvas.create_text(x,y,text=str(dmg),font=('Helvetica',36, 'bold'),fill = 'blue')
        self.font_counter.append([c, 10])
    
    
    def pauseGAME(self):
        self.PAUSE = True
    
    def continueGAME(self):
        self.PAUSE = False
    
    def GAMEOVER(self, state):
        '''
        0 -> dragon win
        1 -> Warrior win
        '''
        self.gameover = True
        # clear all word
        for i in range(len(self.font_counter)):
            self.canvas.delete(self.font_counter[i][0])
        self.canvas.delete(self.warning)

        if state == 0:
            self.player.lose()
            self.dragon.win()
            #messagebox.showinfo('', 'GAME OVER\ndragon Wins')
        else:
            self.player.win()
            self.dragon.lose()
            #messagebox.showinfo('', 'GAME OVER\nWarriar Wins')




if __name__ == "__main__":
    tk = Tk()
    tk.title('KILL THE DRAGON')
    tk.geometry("960x720+400+175")
    tk.resizable(width=False, height=False) # unable to resize
    gameframe = GameFrame(tk)
    gameframe.pack()
    tk.mainloop()