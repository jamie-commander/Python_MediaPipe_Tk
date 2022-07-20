#width=960,height=720

from tkinter import Tk, Frame, Canvas, PhotoImage, Text, Button, messagebox, NW
import os
import random

from Character import Character

class GameFrame(Frame):
    window_width = 960
    window_height = 720
    
    
    def __init__(self, tk, width=window_width, height=window_width):
        Frame.__init__(self, tk, width=width, height=height)
        self.focus_set()

        # display object
        self.display()

        self.bind('<Return>', self.player_attack)
        #self.bind('<space>', self.player_attack)

        # player
        self.player = Character(os.path.join(os.getcwd(), 'warrior/') ,self.canvas, position=True, x=-70, y=350, name="Warrior", hp=100)
        # dragon
        self.dragon = Character(os.path.join(os.getcwd(), 'dragon/') ,self.canvas, position=False, x=self.window_width - 200, y=350, name="dragon", hp=100)
        
        self.dragon_hit_count = random.randint(1, 100)
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
        print(self.dragon_hit_count)
        if self.dragon_hit_count == 0:
            self.dragon_hit_count = random.randint(10, 100)
            self.dragon_attack(random.randint(5, 20))
        else:
            self.dragon_hit_count -= 1

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
        path = os.path.join(os.getcwd(), 'bg.png')
        self.image_bg = PhotoImage(
            file=path)
        self.canvas.create_image(0, 0, image=self.image_bg, anchor=NW)
        self.canvas.grid(row=0, column=0, columnspan=4)

        # TextBox Creation
        self.inputtxt = Text(self, height = 2, width = 20)
        self.inputtxt.grid(row=1, column=0)
        
        # Button Creation
        attackButton = Button(self, text = "Attack", height = 2, width = 20, command = self.player_attack)
        attackButton.grid(row=1, column=1)

        restartButton = Button(self, text = "restart", height = 2, width = 20, command = self.restart)
        restartButton.grid(row=1, column=2)

        quitButton = Button(self, text = "quit", height = 2, width = 20, command = self.quit)
        quitButton.grid(row=1, column=3)

    def restart(self):
        if self.player: 
            self.player.destory()
        if self.dragon: 
            self.dragon.destory()
        del self.player
        del self.dragon
        # player
        self.player = Character(os.path.join(os.getcwd(), 'warrior/') ,self.canvas, position=True, x=-20, y=500, name="Warrior", hp=100)
        # dragon
        self.dragon = Character(os.path.join(os.getcwd(), 'dragon/') ,self.canvas, position=False, x=self.window_width - 50, y=500, name="dragon", hp=100)
        self.start_game()
    
    def quit(self):
        self.player.destory()
        self.dragon.destory()
        self.destroy()

    def dragon_attack(self, dmg, event=None):
        self.dragon.attack(self.player, dmg)

    def player_attack(self, event=None):
        dmg = self.inputtxt.get("1.0",'end-1c')
        self.inputtxt.delete("1.0",'end-1c')

        print("Damage: " + dmg)
        self.player.attack(self.dragon, int(dmg))
    
    def GAMEOVER(self, state):
        '''
        0 -> dragon win
        1 -> Warrior win
        '''
        if state == 0:
            self.player.lose()
            self.dragon.win()
            messagebox.showinfo('', 'GAME OVER\ndragon Wins')
        else:
            self.player.win()
            self.dragon.lose()
            messagebox.showinfo('', 'GAME OVER\nWarriar Wins')




if __name__ == "__main__":
    tk = Tk()
    tk.title('KILL THE DRAGON')
    tk.geometry("960x750+400+175")
    tk.resizable(width=False, height=False) # unable to resize
    gameframe = GameFrame(tk)
    gameframe.pack()
    tk.mainloop()