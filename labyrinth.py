"""
TODO
- Optimizar o jogo
"""
from tkinter import *

# Configurações da Tela
largura = 980
altura = 980

class Map:
    def __init__(self, color):
        self.color = color
        
    
    def criaObs(self, canvas, lista):
        self.squarePos = []
        self.canvas = canvas
        self.lista = lista
        for linha in range(0, len(lista)):
            for char in range(0, len(lista[linha])):
                if lista[linha][char] == 'f':
                    x1 = 20*char
                    y1 = 20*linha
                    x2 = x1+20
                    y2 = y1+20
                    self.squarePos.append([x1, y1, x2, y2, 'f'])
                    canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                if lista[linha][char] == 'd':
                    x1 = 20*char
                    y1 = 20*linha
                    x2 = x1+20
                    y2 = y1+20
                    self.squarePos.append([x1, y1, x2, y2, 'd'])
                    canvas.create_rectangle(x1, y1, x2, y2, fill='blue')

        print(self.squarePos)
        return self.squarePos



class Ball:
    def __init__(self, x, y, velx, vely, raio):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.raio = raio

    def update(self):
        # Função para movimentar a bola e para não deixá-la passar da tela
        if self.x > 0 and self.x < largura - self.raio:
            self.x += self.velx
        if self.y > 0 and self.y < altura - self.raio:
            self.y += self.vely

        if self.x == 0 and self.velx < 0:
            self.x += -self.velx
        if self.x == largura and self.velx > 0:
            self.x += -self.velx
        if self.y == 0 and self.vely < 0:
            self.y += -self.vely
        if self.y == altura and self.vely > 0:
            self.y += -self.vely

    def collision(self, obj, ball):
        self.obj = obj
        self.ball = ball
        if ((self.obj[0] <= self.ball[2] - self.raio <= self.obj[2] or self.obj[0] <= self.ball[0] + self.raio <= self.obj[2]) and (obj[1] <= ball[1] + self.raio <= obj[3] or self.obj[1] <= ball[3] - self.raio <= self.obj[3])) :
            self.velx=0
            self.vely=0
            return True 
        return False
       
class Game:
    def __init__(self):
        # Criação da Tela
        self.window = Tk()
        self.window.title('Joguin')

        # Criação do Canvas
        self.canvas = Canvas(self.window, width=largura, height=altura, bg='pink')
        self.canvas.pack()

        #self.mapa = Map(largura//2 + 100, 50, largura//2 + 110, 150, 'black')
        self.mapa = Map('black')

        # Criação da Bola a partir da class Ball
        self.bola = Ball(70, 70, 0, 0, 5)


        x = self.bola.x
        y = self.bola.y
        r = self.bola.raio
        self.cball = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='green')


        # Binda as setinhas do teclado para a movimentação da bolinha
        self.window.bind('<Up>', self.moveUp)
        self.window.bind('<Down>', self.moveDown)
        self.window.bind('<Right>', self.moveRight)
        self.window.bind('<Left>', self.moveLeft)


        self.lista = [
            'fffffffffffffffffffffffffffffffffffffffffffffffff',
            'f     f     f     f     f     f     f     f     f',
            'f           f                             f     f',
            'f           f                             f     f',
            'f           f                             f     f',
            'f     f     f     f     f     f     f     f     f',
            'ffffffff   fff   fffffffff   fffffffff   fff   ff',
            'f     f     f     f     f     f     f     f     f',
            'f                 f     f     f                 f',
            'f                 f     f     f                 f',
            'f                 f     f     f                 f',
            'f     f     f     f     f     f     f     f     f',
            'ff   fff   fffffffff   fffffffff   ffffffffffffff',
            'f     f     f     f     f     f     f     f     f',
            'f     f                 f                       f',
            'f     f                 f                       f',
            'f     f                 f                       f',
            'f     f     f     f     f     f     f     f     f',
            'ff   fff   fffffffffffffff   fffffffffffffff   ff',
            'f     f     f     f     f     f     f     f     f',
            'f     f                 f           f           f',
            'f     f                 f           f           f',
            'f     f                 f           f           f',
            'f     f     f     f     f     f     f     f     f',
            'ff   fffffffffffffff   fffffffffffffff   ffffffff',
            'f     f     f     f     f     f     f     f     f',
            'f                 f           f                 f',
            'f                 f           f                 f',
            'f                 f           f                 f',
            'f     f     f     f     f     f     f     f     f',
            'ffffffff   fff   fff   fff   fffffffffffffff   ff',
            'f     f     f     f     f     f     f     f     f',
            'f     f     f     f     f           f           f',
            'f     f     f     f     f           f           f',
            'f     f     f     f     f           f           f',
            'f     f     f     f     f     f     f     f     f',
            'ff   fff   fffffffff   fffffffff   ffffffffffffff',
            'f     f     f     f     f     f     f     f     f',
            'f           f     f           f     f           f',
            'f           f     f           f     f           f',
            'f           f     f           f     f           f',
            'f     f     f     f     f     f     f     f     f',
            'ff   fffffffff   fffffffff   fff   fff   fff   ff',
            'f     f     f     f     f     f     f     f     f',
            'f                 f           f           f     d',
            'f                 f           f           f     d',
            'f                 f           f           f     d',
            'f     f     f     f     f     f     f     f     f',
            'fffffffffffffffffffffffffffffffffffffffffffffffff' 
        ]


        self.listaPos = self.mapa.criaObs(self.canvas, self.lista)

    # Funções responsáveis por movimentar a bola
    def moveUp(self, event):
        self.bola.vely = -5
        self.bola.velx = 0

    def moveDown(self, event):
        self.bola.vely = 5
        self.bola.velx = 0

    def moveRight(self, event):
        self.bola.velx = 5
        self.bola.vely = 0

    def moveLeft(self, event):
        self.bola.velx = -5
        self.bola.vely = 0


    # Função para rodar o programa (como se fosse um mainloop, mas aqui dá para colocar diversas coisas)
    def run(self):
        while True:
            # Deleta a bola para redesenhar ela no Canvas
            self.canvas.delete(self.cball)

            # Pega dados da bola para a criação dela no Canvas
            x = self.bola.x
            y = self.bola.y
            r = self.bola.raio

            # Criação da bola
            self.cball = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='black')

            coord_bola = self.canvas.coords(self.cball) 
            print('Bola =', coord_bola)
            
            for square in self.listaPos:
                state = self.bola.collision(square, coord_bola)

                if state and square[4] == 'f':
                    self.bola.velx = 0
                    self.bola.vely = 0
                    self.bola.x = 70
                    self.bola.y = 70
                    print('Game Over!!!')
                elif state and square[4] == 'd':
                    self.window.after(2000)
                    print('VENCEU!!!')
                    exit(0)
                   
            # Update - Importante para fazer com que a bola ande
            self.bola.update()

            # Atualiza o jogo
            self.canvas.after(13)
            self.window.update_idletasks()
            self.window.update()


g = Game()
g.run()
