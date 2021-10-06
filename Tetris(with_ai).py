import pygame
import random
import sys
import Tetris_ai

class shape:
    runs=False
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
run_number=0
class Tetris:
    def __init__(self,height,width):
        self.field=[]
        self.score=0
        self.height=height
        self.width=width
        self.figure=None
        self.hold=None
        self.switched=False
        self.state="start"
        for i in range(self.height):
            new_line=[]
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)

    def new_shape_first(self):
        self.figure=shape(3,0)
        self.next=random.randint(0,6)
        
    def new_shape(self):
        self.figure=shape(3,0)
        self.figure.type=self.next
        self.figure.colour=self.next+1
        self.next=random.randint(0,6)
       
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
        self.score+=lines**2
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i*4+j in self.figure.image():
                    self.field[i+self.figure.y][j+self.figure.x]=self.figure.colour
        self.clear_lines()
        self.new_shape()
        self.switched=False
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
            
    def press_c(self):
        temp=self.hold
        self.hold=self.figure
        self.figure.x=3
        self.figure.y=0
        self.figure.rotations=0
        if temp!=None:
            self.figure=temp
        else:
            self.new_shape()

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
    refresh+=1
    if game.figure is None:
        game.new_shape_first()
    refresh_rate=game.score
    if game.score>=400:
        refresh_rate=400
    if refresh%(20-(refresh_rate//20)+1)==0:
        if game.state=="start":
            game.soft_drop()
            
    if hold_down==True:
        if game.state=="start":
            game.soft_drop()

    for event in pygame.event.get() + Tetris_ai.ai(game.field, game.figure.shapes[game.figure.type],game.figure.x,game.figure.y,game.hold,shape.shapes[game.next]):
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
            if event.key==pygame.K_c:
                if game.switched==False:
                    game.press_c()
                    game.switched=True
            if event.key==pygame.K_ESCAPE:
                game.__init__(20,10)
        
    if event.type==pygame.KEYUP:
        if event.key==pygame.K_DOWN:
            hold_down=False

    screen.fill((255,255,255))

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen,(128,128,128),[100+20*j,60+20*i,20,20],1)
            if game.field[i][j]>0:
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
                    
    pygame.draw.rect(screen,(128,128,128),(7,80,85,45),2)
    pygame.draw.rect(screen,(128,128,128),(307,80,85,45),2)
    
    if game.hold!=None:
        for i in range(4):
            for j in range(4):
                if i*4+j in shape.shapes[game.hold.type][0]:
                        pygame.draw.rect(screen,colours[game.hold.type],[10+20*j,83+20*i,20,20])

    for i in range(4):
        for j in range(4):
            if i*4+j in shape.shapes[game.next][0]:
                pygame.draw.rect(screen,colours[game.next],[310+20*j,83+20*i,20,20])

    font=pygame.font.SysFont('Calibri',30,True,False)
    font2=pygame.font.SysFont('Calibri',50,True,False)
    font3=pygame.font.SysFont('Calibri',15,True,False)
    font4=pygame.font.SysFont('Calibri',20,True,False)
    text=font.render("Score: "+str(game.score),True,(0,0,0))
    youlose=font2.render("Haha You're Bad",True,(0,0,0))
    youlose1=font2.render("Press ESC",True,(0,0,0))
    text2=font3.render('Press Backspace to Exit',True,(0,0,0))
    text3=font3.render('Holding',True,(0,0,0))
    text4=font3.render('Next',True,(0,0,0))
    
    screen.blit(text,[10,20])
    screen.blit(text2,[250,480])
    screen.blit(text3,[24,125])
    screen.blit(text4,[335,125])
    
    if game.state=="lose":
        screen.blit(youlose,[20,200])
        screen.blit(youlose1,[25,265])
        
    #fps
    clock.tick(30)
    pygame.display.flip()
