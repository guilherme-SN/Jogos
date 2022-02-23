from tkinter import *
from random import choice

largura = 400
altura = 450
colors = ['yellow', 'green', 'blue', 'orange', 'purple']

player_barLar = 45
player_barAlt = 7


class Ball:
    def __init__(self, x, y, raio, velx, vely, canvas):
        self.x = x
        self.y = y
        self.raio = raio
        self.velx = velx
        self.vely = vely
        self.canvas = canvas

        self.x1 = self.x - self.raio
        self.y1 = self.y - self.raio
        self.x2 = self.x + self.raio
        self.y2 = self.y + self.raio
       
        self.ball = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill='red', tag='ball')

    def update(self, blocks, ft):
        self.canvas.move('ball', self.velx, self.vely)
        print(f'{self.velx}; {self.vely}') 
        
        self.x += self.velx
        self.y += self.vely

        if self.x - self.raio <= 0 or self.x + self.raio >= largura - 2:
            self.velx *= -1

        if self.y - self.raio <= 0:
            self.vely *= -1

        if self.y + self.raio >= altura:
            print('VOCÊ PERDEU!!!!')
            exit(0)

    def ballPos(self):
        return [self.x1, self.y1, self.x2, self.y2]
    
    def playerCollision(self, player_pos):
        if (player_pos[0] <= self.x - self.raio <= player_pos[2] or player_pos[0] <= self.x + self.raio <= player_pos[2]) and (player_pos[1] <= self.y - self.raio <= player_pos[3] or player_pos[1] <= self.y + self.raio <= player_pos[3]):
            self.vely *= -1

    def blockCollision(self, player_id, block_id, block_pos):
        ball_coord = self.canvas.bbox('ball')

        col = self.canvas.find_overlapping(*ball_coord)
        collisions = list(col)
        
        if collisions[0] == self.ball:
            collisions.pop(0)
        if len(collisions) > 0: 
            if collisions[0] != player_id:
                closest = self.canvas.find_closest(ball_coord[0], ball_coord[1])
                for block in block_id:
                    if block == closest[0]:
                        block_id.remove(block)
                        self.canvas.delete(block)

                        self.vely *= -1
                        
                        if self.velx > 0:
                            self.velx += 0.2
                        elif self.velx < 0:
                            self.velx -= 0.2

                        if self.vely > 0:
                            self.vely += 0.2
                        elif self.vely < 0:
                            self.vely -= 0.2
                        return


class Player:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        
        self.x1 = self.x - player_barLar
        self.y1 = self.y - player_barAlt 
        self.x2 = self.x + player_barLar
        self.y2 = self.y + player_barAlt

        self.player = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='white', tag='player')

    def returnPlayerID(self):
        return self.player
    
    def moveLeft(self, event):
        if self.x1 - 10> 0:
            self.x1 -= 10
            self.x2 -= 10
            self.canvas.move('player', -10, 0)

    def moveRight(self, event):
        if self.x2 + 10 < largura:
            self.x2 += 10
            self.x1 += 10
            self.canvas.move('player', 10, 0)
    
    def move(self, event):
        if event.x - player_barLar > 0 and event.x + player_barLar < largura:
            self.x1 = event.x - player_barLar 
            self.x2 = event.x + player_barLar
            self.canvas.moveto('player', event.x - player_barLar)

    def playerPos(self):
       return [self.x1, self.y1, self.x2, self.y2]


class Map:
    def __init__(self, blockLar, blockAlt, mapa, canvas):
        self.blockLar = blockLar
        self.blockAlt = blockAlt
        self.mapa = mapa
        self.canvas = canvas
        self.blocks = []
        self.blocks_pos = []

    def createMap(self):
        for linha in range(0, len(self.mapa)):
            if 'f' in self.mapa[linha]:
                global color
                color = choice(colors)
                colors.remove(color)
            for char in range(0, len(self.mapa[linha])):
                if self.mapa[linha][char] == 'f':
                    self.x1 = self.blockLar * char
                    self.y1 = self.blockAlt * linha
                    self.x2 = self.blockLar + self.x1
                    self.y2 = self.blockAlt + self.y1

                    block = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=color, width=3, tag='block')
                    self.blocks.append(block)
                    self.blocks_pos.append([self.x1, self.y1, self.x2, self.y2])

        return self.blocks_pos


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title('Block Game')
        self.canvas = Canvas(self.window, width=largura, height=altura, bg='black')
        self.canvas.pack()
        self.first_time = True
        
        self.ball = Ball(largura // 2, 390, 6, 5, -5, self.canvas)
        
        self.player = Player(largura // 2, 400 + self.ball.raio + player_barAlt, self.canvas)
        self.playerID = self.player.returnPlayerID()
        #self.window.bind('<Left>', self.player.moveLeft)
        #self.window.bind('<Right>', self.player.moveRight)
        self.window.bind('<Motion>', self.player.move)

        self.m = [
            '         ',
            '         ',
            '         ',
            'fffffffff',
            'fffffffff',
            'fffffffff',
            'fffffffff',
            'fffffffff'
                    ]

        self.mapa = Map(45, 20, self.m, self.canvas) 
        self.blocks_pos = self.mapa.createMap()

    def run(self):
        while True:
            
            self.ball_pos = self.ball.ballPos()
            self.player_pos = self.player.playerPos()

            self.ball.update(self.mapa.blocks, self.first_time)

            self.ball.playerCollision(self.player_pos)
            self.ball.blockCollision(self.playerID, self.mapa.blocks, self.blocks_pos)
            
            if self.mapa.blocks == 0:
                print('PARABÉNS, VOCÊ GANHOU!!!')
                exit(0)

            self.canvas.after(30)
            self.window.update_idletasks()
            self.window.update()


g = Game()
g.run()

