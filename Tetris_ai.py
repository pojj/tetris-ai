import pygame
import copy
import random
import time

class Event():
    type = None
    key = None
    def __init__(self, type, key):
        self.type = type
        self.key = key

def ai(game_field,figure,x,y,hold,next_piece):
    original=copy.deepcopy(game_field)
    field=copy.deepcopy(original)
    def all_spots(field,figure,x,y):
        spots=[]
        save=x
        for rotation in figure:
            x=save
            temp=[]
            spots.append(temp)
            while cross(rotation,field,x,y)!=True:
                x-=1
                if cross(rotation,field,x,y)==True:
                    break
                temp.insert(0,x)
        x=save
        for rotation in figure:
            x=save
            temp=[]
            spots.append(temp)
            x-=1
            while cross(rotation,field,x,y)!=True:
                x+=1
                if cross(rotation,field,x,y)==True:
                    break
                temp.append(x)
        x=save
        spots[0],spots[1],spots[2],spots[3]=spots[0]+spots[4],spots[1]+spots[5],spots[2]+spots[6],spots[3]+spots[7]
        del spots[4::]
        return spots
        
    def try_all(field,figure,x,y,spots):
        states=[]
        time=-1
        for i in spots:
            time+=1
            rotation=figure[time]
            temp=[]
            for test_x in i:
                score=0
                hard_drop(rotation,field,figure,test_x,y,)
                temp.append(field)
                field=copy.deepcopy(original)
            states.append(temp)
        return states
    
    def scoring(states):
        scores=[]
        for i in states:
            temp=[]
            for j in i:
                score=5
                if find_holes(j)==True:
                    score-=4
                if make_3_tall(j)==True:
                    score-=1
                score-=too_high(j)
                temp.append(score)
            scores.append(temp)
        return scores
    
    def best_spot(scores,spots):
        moves=[]
        temp=[]
        for i in scores:
            for j in i:
                temp.append(j)
        if temp==[]:
            return False
        biggest=max(temp)
        for i in range(len(scores)):
            for j in range(len(scores[i])):
                temp=[]
                if scores[i][j]==biggest:
                    temp.append(i)
                    temp.append(spots[i][j])
                    temp.append(scores[i][j])
                    moves.append(temp)
        return moves
                               
    def hard_drop(rotation,field,figure,test_x,y):
        test_y=0
        while cross(rotation,field,test_x,test_y)!=True:
            test_y+=1
        if cross(rotation,field,test_x,test_y)==True:
            test_y-=1
            freeze(rotation,field,test_x,test_y)
        
    def cross(rotation,field,x,y):
        for i in range(4):
            for j in range(4):
                if (i*4+j) in rotation:
                    if j+x<0 or j+x>9 or i+y>19 or field[i+y][j+x]>0:
                        return True
            
    def freeze(rotation,field,x,y):
        for i in range(4):
            for j in range(4):
                if i*4+j in rotation:
                    field[i+y][j+x]=10
    
    def find_holes(field):
        holes=0
        past_holes=0
        for i in range(10):
            for j in range(19):
                if field[j][i]!=0:
                    if field[j+1][i]==0:
                        holes+=1
        for i in range(10):
            for j in range(19):
                if original[j][i]!=0:
                    if original[j+1][i]==0:
                        past_holes+=1
        if holes>past_holes:
            return True
        return False
    
    def too_high(field):
        height=0
        for i in reversed(range(len(field))):
            for j in range(len(field[i])):
                if field[i][j]==10:
                    height=i
        return 20-height
    
    def make_3_tall(field):
        old_3=0
        new_3=0
        for i in range(10):
            for j in reversed(range(2,20)):
                if field[j][i]!=0 and field[j-1][i]!=0 and field[j-2][i]!=0:
                    if i!=9:
                        if field[j][i+1]==0 and field[j-1][i+1]==0 and field[j-2][i+1]==0:
                            new_3+=1
                            continue
                if field[j][i]!=0 and field[j-1][i]!=0 and field[j-2][i]!=0:
                    if i!=0:
                        if field[j][i-1]==0 and field[j-1][i-1]==0 and field[j-1][i-1]==0:
                            new_3+=1
                            continue
        for i in range(9):
            for j in reversed(range(2,20)):
                if original[j][i]!=0 and original[j-1][i]!=0 and original[j-2][i]!=0:
                    if i!=9:
                        if original[j][i+1]==0 and original[j-1][i+1]==0 and original[j-2][i+1]==0:
                            old_3+=1
                            continue
                if original[j][i]!=0 and original[j-1][i]!=0 and original[j-2][i]!=0:
                    if i!=0:
                        if original[j][i-1]==0 and original[j-1][i-1]==0 and original[j-1][i-1]==0:
                            old_3+=1
                            continue
        if new_3>old_3:
            return True
        return False
                
    if hold==None:
        hold=next_piece
    else:
        hold=hold.shapes[hold.type]
    
    current_spots=all_spots(field,figure,x,y)
    current_states=try_all(field,figure,x,y,current_spots)
    current_scores=scoring(current_states)
    current_moves=best_spot(current_scores,current_spots)
    hold_spots=all_spots(field,hold,x,y)
    hold_states=try_all(field,hold,x,y,hold_spots)
    hold_scores=scoring(hold_states)
    hold_moves=best_spot(hold_scores,hold_spots)
    
    if current_moves!=False and hold_moves!=False:
        move_order=[]
        choosen=random.choice(current_moves)
        x=random.choice(hold_moves)
        if x[2]>choosen[2]:
            choosen=x
            move_order.append(Event(pygame.KEYDOWN, pygame.K_c))
        for i in range(choosen[0]):
            move_order.append(Event(pygame.KEYDOWN, pygame.K_UP))
        if choosen[1]>3:
            for i in range(choosen[1]-3):
                move_order.append(Event(pygame.KEYDOWN, pygame.K_RIGHT))
        if choosen[1]<3:
            for i in range(3-choosen[1]):
                move_order.append(Event(pygame.KEYDOWN, pygame.K_LEFT))
        move_order.append(Event(pygame.KEYDOWN, pygame.K_SPACE))
        time.sleep(0)
        return move_order
    else:
        return []

    

    
    
    
    
    
    


