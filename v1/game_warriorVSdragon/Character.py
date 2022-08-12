from tkinter import PhotoImage, NW
import os

from sqlalchemy import true

class Character:
    def __init__(self, runpath, canvas, position : bool = True, x : int = 0, y : int = 500, name='Warrior', hp : int = 100):
        self.canvas = canvas
        self.position = position # left:False // right:True
        self.x = x
        self.y = y
        self.name = name

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
            self.HP_bar = self.canvas.create_rectangle(50, 50, 50+3*self.hp, 70,fill='green')
            self.HP_status = self.canvas.create_text(115, 85, text="[%3d/%3d]" % (self.hp,self.maxhp), font=('Arial', 18))
        else:
            self.canvas.create_text(860, 35, text=self.name, font=('Arial', 18))
            self.HP_bar = self.canvas.create_rectangle(910-3*self.hp, 50, 910, 70,fill='blue')
            self.HP_status = self.canvas.create_text(850, 85, text="[%3d/%3d]" % (self.hp,self.maxhp), font=('Arial', 18))
    
    def run(self):
        self.move_count += 1
        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['run'+str(self.move_count%2)])
        if self.position == False:
            move_step = -5
        else:
            move_step = 5
        self.canvas.move(self.image_on_canvas, move_step, 0)
        # TODO: show the fight img
        if self.move_count < 42:
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
        self.canvas.after(1000, self.stand)

    def hurted(self, hp):
        self.hp -= hp
        if self.hp < 0:
            self.hp = 0 

        # HP bar update
        x0, y0, x1, y1 = self.canvas.coords(self.HP_bar)
        if self.position:
            x1 -= 3*hp
            if x1 < x0:
                x1 = x0
        else:
            x0 += 3*hp
            if x0 > x1:
                x0 = x1
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
        self.canvas.after(200, self.lose)

    def win(self):
        self.canvas.itemconfig(self.image_on_canvas, image = self.run_images['win'+str(self.move_count%2)])
        self.move_count+=1
        self.canvas.after(200, self.win)

    def destory(self):
        self.canvas.delete(self.image_on_canvas)
        self.canvas.delete(self.HP_bar)
        self.canvas.delete(self.HP_status)
