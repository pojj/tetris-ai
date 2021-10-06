import pygame
import random
import sys

class shape:
    shapes=[
    #LINE
    [[4,5,6,7],[2,6,10,14],[8,9,10,11],[1,5,9,13]],
    #L
    [[2,4,5,6 ],[1,5,9,10],[4,5,6,8],[0,1,5,9]],
    #BACKWARD L
    [[0,4,5,6],[1,2,5,9],[4,5,6,10],[1,5,8,9]],
    #Z
    [[0,1,5,6],[2,5,6,9],[4,5,9,10],[1,4,5,8]],
    #BACKWARD Z
    [[1,2,4,5],[1,5,6,10],[5,6,8,9],[0,4,5,9]],
    #T
    [[1,4,5,6],[1,5,6,9],[4,5,6,9],[1,4,5,9]],
    #SQUARE
    [[1,2,5,6],[1,2,5,6],[1,2,5,6],[1,2,5,6]]
    ]
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.type=random.randint(0,6)
        self.colour=self.type+1
        self.rotations=0
    
    def rotate(self):
        self.rotations=(self.rotations+1)%4
        
    def image(self):
        return self.shapes[self.type][self.rotations]
    
class Tetris:
    def __init__(self,height,width):
        self.field=[]
        self.score=0
        self.height=height
        self.width=width
        self.figure=None
        self.state="start"
        for i in range(self.height):
            new_line=[]
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    def new_shape(self):
        self.figure=shape(3,0)
       
    def cross(self):
        crossing=False
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figure.image():
                    if i+self.figure.y>self.height-1 or\
                        j+self.figure.x>self.width-1 or\
                        j+self.figure.x<0 or\
                        self.field[i+self.figure.y][j+self.figure.x]>0:
                        crossing=True
        return(crossing)
                        
    def clear_lines(self):
        row=-1
        lines=0
        for i in self.field:
            zero=self.width
            row+=1
            for j in i:
                if j!=0:
                    zero-=1
            if zero==0:
                del self.field[row]
                new_line=[]
                for j in range(self.width):
                    new_line.append(0)
                self.field.insert(0,new_line)
                lines+=1
        self.score += lines**2
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figure.image():
                    self.field[i+self.figure.y][j+self.figure.x]=self.figure.colour
        self.clear_lines()
        self.new_shape()
        if self.cross()==True:
            self.state="lose"
            
    def hard_drop(self):
        while not self.cross()==True:
            self.figure.y+=1
        if self.cross()==True:
            self.figure.y-=1
            self.freeze()
        
    def soft_drop(self):
        self.figure.y+=1
        if self.cross()==True:
            self.figure.y-=1
            self.freeze()
        
    def move_side(self,direction):
        original=self.figure.x
        self.figure.x+=direction
        if self.cross()==True:
            self.figure.x=original
            
    def press_up(self):
        original=self.figure.rotations
        self.figure.rotate()
        if self.cross()==True:
            self.figure.rotations=original

pygame.init()
colours=[
    (0,255,255),
    (255,165,0),
    (0,0,255),
    (255,0,0),
    (0,255,0),
    (255,0,255),
    (255,255,0),]

screen=pygame.display.set_mode(size=(400,500))

pygame.display.set_caption("Tetris")

game=Tetris(20,10)
counter=0
clock=pygame.time.Clock()
hold_down=False
refresh=0
while True:
    if game.figure is None:
        game.new_shape()
    refresh+=1
    if refresh%(20-game.score//20)==0:
        if game.state=="start":
            game.soft_drop()
            
    if hold_down==True:
        if game.state=="start":
            game.soft_drop()

    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_BACKSPACE:
                pygame.quit()
                sys.exit()
            if event.key==pygame.K_UP:
                game.press_up()
            if event.key==pygame.K_DOWN:
                hold_down=True
            if event.key==pygame.K_LEFT:
                game.move_side(-1)
            if event.key==pygame.K_RIGHT:
                game.move_side(1)
            if event.key==pygame.K_SPACE:
                game.hard_drop()
            if event.key==pygame.K_ESCAPE:
                game.__init__(20,10)
        

    if event.type==pygame.KEYUP:
        if event.key==pygame.K_DOWN:
            hold_down=False

    screen.fill((255,255,255))

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen,(128,128,128),[100+20*j,60+20*i,20,20],1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen,colours[game.field[i][j]-1],
                                 [100+20*j+1,60+i*20+1,18,18])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                if i*4+j in game.figure.image():
                    pygame.draw.rect(screen,colours[game.figure.colour-1],
                                     [100+20*(j+game.figure.x)+1,
                                      60+20*(i+game.figure.y)+1,
                                      18,18])

    font=pygame.font.SysFont('Calibri',20,True,False)
    font2=pygame.font.SysFont('Calibri',50,True,False)
    font3=pygame.font.SysFont('Calibri',15,True,False)
    text=font.render("Score: "+str(game.score),True,(0,0,0))
    youlose=font2.render("Haha You're Bad",True,(0,0,0))
    youlose1=font2.render("Press ESC",True,(0,0,0))
    text2=font3.render('Press Backspace to Exit',True,(0,0,0))
    screen.blit(text,[10,20])
    screen.blit(text2,[250,480])
    
    if game.state=="lose":
        screen.blit(youlose,[20,200])
        screen.blit(youlose1,[25,265])
        
    clock.tick(30)
    pygame.display.flip()
