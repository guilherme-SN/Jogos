from tkinter import *
from random import choice

# Configurações da tela
w = 680
h = 680

# Configuração dos "quadradinhos da tela"
grid_size = 20

# Posições possíveis para aparecer a comida
positions = [] 
for i in range(grid_size, w + 1 - grid_size):
    if i % 20 == 0:
        positions.append(i)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        
    def createFood(self, x, y):
        self.x1 = x
        self.y1 = y
        self.x2 = x + grid_size
        self.y2 = y + grid_size
        self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='red', tag='food')

    def update(self, player_pos):
        if player_pos[0] == self.x1 and player_pos[1] == self.y1:
            self.canvas.delete('food')
            return True 
        return False 

class Player:
    def __init__(self, size, vel, canvas):
        self.size = size
        self.vel = vel
        self.canvas = canvas
        self.snake_pos = []
        self.snake_ID = []
        self.body_vel = []

        self.x1 = w // 2
        self.y1 = h // 2
        self.x2 = w // 2 + self.size
        self.y2 = h // 2 + self.size

        self.snake_head = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='white', tag='head')
        self.snake_ID.append(self.snake_head)
        self.snake_pos.append([self.x1, self.y1])

    def moveUp(self, event):
        if self.vel[1] == 0 and self.y1 > 0:
            self.vel = [0, -grid_size]

    def moveDown(self, event):
        if self.vel[1] == 0 and self.y2 < h:
            self.vel = [0, grid_size]

    def moveLeft(self, event):
        if self.vel[0] == 0 and self.x1 > 0:
            self.vel = [-grid_size, 0]

    def moveRight(self, event):
        if self.vel[0] == 0 and self.x2 < w:
            self.vel = [grid_size, 0]
            
    def update(self, points):
        if len(self.body_vel) == 0:
            self.body_vel.append(self.vel)
        else:
            self.body_vel[0] = self.vel

        if (self.y1 >= 0 and self.y2 <= h) and (self.x1 >= 0 and self.x2 <= w):
            self.x1 += self.vel[0]
            self.x2 += self.vel[0]    
            self.y1 += self.vel[1]
            self.y2 += self.vel[1]

            self.pos_copy = self.snake_pos[::]
            self.body_vel_copy = self.body_vel[::]

            self.canvas.move('head', self.vel[0], self.vel[1])
            self.snake_pos[0] = [self.x1, self.y1]

            for v, i in enumerate(self.snake_ID):
                if i != self.snake_head:
                    self.snake_pos[v] = self.pos_copy[v-1]
                    self.body_vel[v] = self.body_vel_copy[v-1]

                    self.canvas.moveto(i, self.snake_pos[v][0], self.snake_pos[v][1])

        else:
            print('GAME OVER!!!')
            print(f'YOU DID {points} POINTS!')
            exit(0)

        for v in range(1, len(self.snake_pos)):
            if self.snake_pos[0] == self.snake_pos[v]:
                print('GAME OVER!!!')
                print(f'YOU DID {points} POINTS!')
                exit(0)

        
    def pos(self):
        return [self.x1, self.y1, self.x2, self.y2]


    def createSnake(self):
        last = self.snake_pos[-1]

        if self.body_vel[-1][0] == 0:
            body_x1 = last[0]
            body_y1 = last[1] + (self.body_vel[-1][1] * -1)
            body_x2 = body_x1 + self.size
            body_y2 = body_y1 + self.size

        elif self.body_vel[-1][1] == 0:
            body_x1 = last[0] + (self.body_vel[-1][0] * -1)
            body_y1 = last[1]
            body_x2 = body_x1 + self.size
            body_y2 = body_y1 + self.size

        self.snake_body = self.canvas.create_rectangle(body_x1, body_y1, body_x2, body_y2, fill='green', tag='body')

        self.snake_pos.append([body_x1, body_y1])
        self.snake_ID.append(self.snake_body)
        self.body_vel.append(self.body_vel[-1])

class Game:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=w, height=h, bg='black')
        self.canvas.pack()
        
        self.player = Player(grid_size, [0, 0], self.canvas)
        
        self.window.bind('<Up>', self.player.moveUp)
        self.window.bind('<Down>', self.player.moveDown)
        self.window.bind('<Left>', self.player.moveLeft)
        self.window.bind('<Right>', self.player.moveRight)
        
        
        self.food_x = choice(positions)
        self.food_y = choice(positions)
        self.food = Food(self.canvas)
        self.food.createFood(self.food_x, self.food_y)
        self.food_eaten = 0

    def run(self):
        while True:
            self.player.update(self.food_eaten)
            self.player_pos = self.player.pos()

            self.eaten = self.food.update(self.player_pos)
            if self.eaten:
                self.food_x = choice(positions)
                self.food_y = choice(positions)
                self.food_eaten += 1
                print(self.food_eaten)
                self.player.createSnake()

                self.food.createFood(self.food_x, self.food_y)
            

            self.canvas.after(40)
            self.window.update_idletasks()
            self.window.update()


g = Game()
g.run()

