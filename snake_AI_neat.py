import pygame
import random
import math
import neat
pygame.init()



game_run = True
#__GAME__ Snake

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
        global run

        if self.tail_size>=1:
            self.tail_x.pop(0)
            self.tail_y.pop(0)
            self.tail_x.append(self.x)
            self.tail_y.append(self.y)
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
                run = False
                allow = False
                pygame.time.delay(500)

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
#to genrate fruit
def fruit_gen():
    global fruit_x
    global fruit_y
    fruit_x = random.randrange(1,39)
    fruit_y = random.randrange(1,39)
    fruit_x *= scl
    fruit_y *= scl

#to draw the elements
def redrawgamewindow():
    if allow:
        win.fill((0, 0, 0))
        for i,snk in enumerate(snks):
            if snk.draw(win) or die_time[i]>100:
                ge[i].fitness -= 20
                snks.pop(i)
                nets.pop(i)
                ge.pop(i)
            if snk.eat():
                die_time[i] = 0
                ge[i].fitness += 5
            die_time[i]+=1
        pygame.draw.rect(win, (255, 0, 0), (fruit_x + border, fruit_y + border, size - border, size - border))
        pygame.display.update()

def main(genomes,config):
    #main loop
    global snks,nets,ge,run,allow,fruit_x,fruit_y,die_time
    snks = []
    nets = []
    ge = []
    die_time = []

    for _,g in genomes:
        net =  neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        snks.append(snake(scl*20,scl*20,size,size))
        g.fitness = 0
        ge.append(g)
        die_time.append(0)

    run = True
    allow = True
    fruit_x = scl * int(100/scl)
    fruit_y = scl * int(350/scl)

    while run and len(snks)>0:
        clock.tick(10)
        
    #To check the events done in the window  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
    #To move the snake
        for x,snk in enumerate(snks):
            ge[x].fitness += (350-((fruit_y-snk.y)**2+(fruit_x-snk.x)**2)**0.5)/500
            output = nets[x].activate(((fruit_y-snk.y)**2,(fruit_x-snk.x)**2))

            mx = 0
            dr = -1

            for ind in range(4):
                if output[ind] > mx:
                    dr = ind
                    mx = output[ind]

            if dr == 0 and snk.dir != "down":
                snk.dir = "up"
            elif  dr == 1 and snk.dir != "up":
                snk.dir = "down"
            elif dr == 2 and snk.dir != "right":
                snk.dir = "left"
            elif dr == 3 and snk.dir != "left":
                snk.dir = "right"
        redrawgamewindow()
        
                     

def start_test(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":      
    config_path = 'config_feedforward.txt'
    start_test(config_path)