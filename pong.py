from tkinter import *


largura = 600
altura = 400
barLar = 20
barAlt = 80


class Square:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura

class Ball:
    def __init__(self, x, y, raio, velx, vely):
        self.x = x
        self.y = y
        self.raio = raio
        self.velx = velx
        self.vely = vely
    

    def update(self):
        self.x += self.velx
        self.y += self.vely

        if self.y <= 0:
            self.vely = -self.vely

        if self.y > altura - self.raio:
            self.vely = -self.vely


class Game:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=largura, height=altura, bg='black')
        self.canvas.pack()
        
        
        self.window.bind("w", self.moveUp)
        self.window.bind("s", self.moveDown)
        self.window.bind('<Up>', self.moveUp_comp)
        self.window.bind('<Down>', self.moveDown_comp)


        self.bola = Ball(largura//2, altura//2, 5, -5, 5)
        self.player = Square(0, 30, barLar, barAlt)
        self.comp = Square(largura-barLar, 30, barLar, barAlt)

    def moveUp(self, event):
        if self.player.y > 0:
            self.player.y -= 10

    def moveDown(self, event):
        if self.player.y < altura - barAlt:
            self.player.y += 10

    def moveUp_comp(self, event):
        if self.comp.y > 0:
            self.comp.y -= 10

    def moveDown_comp(self, event):
        if self.comp.y < altura - barAlt:
            self.comp.y += 10



    def run(self):
        while True:
            self.canvas.delete('all')
            

            self.canvas.create_oval(self.bola.x - self.bola.raio, self.bola.y - self.bola.raio, self.bola.x + self.bola.raio, self.bola.y + self.bola.raio, fill='green')
            self.canvas.create_rectangle(self.player.x, self.player.y, self.player.x + self.player.largura, self.player.y + self.player.altura, fill='white')
            
            self.canvas.create_rectangle(self.comp.x, self.comp.y, self.comp.x + self.comp.largura, self.comp.y + self.comp.altura, fill='white')
            
            print(f'Bola = {self.bola.x}, {self.bola.y}')

            # Rebate
            if self.player.y < self.bola.y < self.player.y + barAlt and 0 <= self.bola.x <= self.player.x + barLar:
                self.bola.velx *= -1
            if self.comp.y < self.bola.y < self.comp.y + barAlt and self.comp.x <= self.bola.x <= largura:
                self.bola.velx *= -1
            

            if self.bola.x <= 0 or self.bola.x >= largura:
                print('GAME OVER!!')
                exit(0)
            
            self.bola.update()

            self.canvas.after(30)
            self.window.update_idletasks()
            self.window.update()



g = Game()
g.run()
