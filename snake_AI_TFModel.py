import pygame
import random
import math
import tensorflow as tf
from tensorflow import keras
import numpy as np
pygame.init()

# neural network model 
model = keras.Sequential([
    keras.layers.InputLayer(16), 
    keras.layers.Dense(4,activation="softmax")
    ])

model.compile(optimizer='adam',loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])

test_data = []
test_label = []
curr_data = []
curr_label = 0


#constants
scl = 12
size = scl
border = 1

#define window witth size and name "SNAKE GAME"
win = pygame.display.set_mode((size * 40, size * 40))
pygame.display.set_caption("SNAKE GAME")
clock = pygame.time.Clock()

#to calculate distance between two point
def distance(x, y, x1 ,y1):
    ret = math.sqrt((x-x1)**2+(y-y1)**2)
    return ret


class snake(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.height = height
        self.width = width
        self.vel = scl
        self.dir = "stop"
        self.tail_size = 0
        self.tail_x = []
        self.tail_y = []

#To check fruit is eaten   
    def eat(self):
        dist = distance(self.x, self.y, fruit_x, fruit_y)
        if dist < scl:
            fruit_gen()
            self.tail_size+=1
            self.tail_x.insert(0,self.x)
            self.tail_y.insert(0,self.y)
            return True
        return False

#To draw the snake and the fruit
    def draw(self,win):
        global allow

        if self.tail_size>=1:
            self.tail_x.pop(0)
            self.tail_y.pop(0)
            self.tail_x.append(self.x)
            self.tail_y.append(self.y)
        self.prev_x = self.x
        self.prev_y = self.y
        if self.dir == "up":
            self.y -= self.vel
        elif self.dir == "down":
            self.y += self.vel
        elif self.dir == "left":
            self.x -= self.vel
        elif self.dir == "right":
            self.x += self.vel
        self.x = self.x%(size*40)
        self.y = self.y%(size*40)

        for i in range(self.tail_size):
            if self.x==self.tail_x[i] and self.y == self.tail_y[i]:
                pygame.time.delay(500)
                return True

                
        if allow:
            pygame.draw.rect(win, (0, 255, 0), (self.x + border, self.y + border, self.width - border, self.height - border))
        x=250
        c=10

        for i in range(self.tail_size):
            x -= c
            if x == 80 or x == 250:
                c *= -1
            if allow:
                pygame.draw.rect(win, (0, x, 0), (self.tail_x[i] + border, self.tail_y[i] + border, self.width - border, self.height - border))

        return False

def fruit_gen():
    global fruit_x
    global fruit_y
    fruit_x = random.randrange(1,39)
    fruit_y = random.randrange(1,39)
    fruit_x *= scl
    fruit_y *= scl

#to draw the elements
def redrawgamewindow():
    global run,m_cnt
    if allow:
        win.fill((0, 0, 0))
        switch = ["up","right","down","left"]
        bs = random.randrange(100)
        if snk.draw(win):
            test_data.append(curr_data)
            test_label.append((curr_label+bs)%4)
            run = False
        elif snk.eat():
            m_cnt = 0
            test_data.append(curr_data)
            test_label.append(curr_label)
        elif distance(fruit_x,fruit_y,snk.prev_x,snk.prev_y)>distance(fruit_x,fruit_y,snk.x,snk.y):
            test_data.append(curr_data)
            test_label.append(curr_label)
        else:
            min_dst = 1000000
            bst_move = (curr_label+2)%4
            for mv in [(1,0,1),(-1,0,3),(0,1,2),(0,-1,0)]:
                if distance(fruit_x,fruit_y,snk.prev_x+mv[0],snk.prev_y+mv[1])<min_dst:
                    min_dst= distance(fruit_x,fruit_y,snk.prev_x+mv[0],snk.prev_y+mv[1])
                    bst_move = mv[2]
            test_data.append(curr_data)
            test_label.append(bst_move)
        m_cnt+=1
        if m_cnt >= 150:
            run = False
        pygame.draw.rect(win, (255, 0, 0), (fruit_x + border, fruit_y + border, size - border, size - border))
        pygame.display.update()

#main loop
def game():
    global allow,run,snk,fruit_y,fruit_x,curr_data,curr_label,m_cnt
    run = True
    allow = True
    snk = snake(scl * 20, scl * 20, size, size)
    m_cnt = 0
    fruit_x = scl * int(100/scl)
    fruit_y = scl * int(350/scl)
 
     
    while run:
        clock.tick(10)
            
    #To check the events done in the window  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


    # input Data for Model
        coff_lst = [1,0,-1]
        curr_data = []
        for c1 in coff_lst:
            for c2 in coff_lst:
                if c1==0 and c2==0:
                    continue
                dst_f = -1
                while True:
                    dst_f+=1
                    x = snk.x + c1*dst_f
                    y = snk.y + c2*dst_f
                    if y<0 or y>size*40 or x<0 or x>size*40:
                        dst_f = -1
                        break
                    flg = False
                    for i in range(snk.tail_size):
                        if x==snk.tail_x[i] and y == snk.tail_y[i]:
                            dst_f*=-1
                            flg = True
                    if flg:
                        break
                curr_data.append(dst_f)

                dst_f = -1
                while True:
                    dst_f+=1
                    x = snk.x + c1*dst_f
                    y = snk.y + c2*dst_f
                    if y<0 or y>size*40 or x<0 or x>size*40:
                        dst_f = -1
                        break
                    if x==fruit_x and y==fruit_y:
                        break
                curr_data.append(dst_f)
        
    #To take the inputs of keys pressed
        curr_label = np.argmax(model.predict(np.expand_dims(curr_data,0))[0])
    #To move the snake
        if curr_label == 0 and snk.dir != "down":
            snk.dir = "up"
        elif curr_label == 2 and snk.dir != "up":
            snk.dir = "down"
        elif curr_label == 3 and snk.dir != "right":
            snk.dir = "left"
        elif curr_label == 1 and snk.dir != "left":
            snk.dir = "right"   
        redrawgamewindow()
    
                     


for gen in range(50):
    print("GEN - ",gen+1)
    game()
    print(test_label)
    model.fit(np.asarray(test_data),np.asarray(test_label),epochs=100)
    test_data = []
    test_label = []
    curr_data = []
    curr_label = 0