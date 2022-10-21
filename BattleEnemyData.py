import pygame
import sys
import random
import copy
from pygame.locals import *
from playerconstants import Fredrick, holy, GrayCloak, Genmu, MagiNyu
from playerconstants import spell
#from battleroutine import battleplayer, enemy

#human reaction time is 8 frames?

class Enemyinfo:
    def __init__(self,startpoint,events,strategy):
        self.startpoint = startpoint
        self.events = events
        self.strategy = strategy
def basicmovement(self,game,speed=10):
    if self.movecounter >= speed or (self.movecounter >= (speed//2) and self.fast):
        if self.moveneeded:
            h = self.moveneeded
            if h == 'left':
                self.currentpos[0] -= 1
                if self.currentpos[0] <= 0:
                    self.currentpos[0] = 1
                
                
            if h == 'right':
                self.currentpos[0] += 1
                if self.currentpos[0] >= 9:
                    self.currentpos[0] = 8
                
            if h == 'down':
                self.currentpos[1] += 1
                if self.currentpos[1] >= 5:
                    self.currentpos[1] = 4
                
            if h == 'up':
                self.currentpos[1] -= 1
                if self.currentpos[1] <= 0:
                    self.currentpos[1] = 1
            if self.currentpos in [[1,1],[1,4],[8,1],[8,4]]:
                #corners are illegal
                #this is a quick and dirty fix
                if self.moveneeded == 'right':
                    self.currentpos[0] -= 1
                if self.moveneeded == 'left':
                    self.currentpos[0] += 1
                if self.moveneeded == 'up':
                    self.currentpos[1] += 1
                if self.moveneeded == 'down':
                    self.currentpos[1] -= 1

        if game.playerbehind:
            self.currentpos[0] += 1
        if self.currentpos[0] == 0:
            self.currentpos[0] += 1
        if self.currentpos[1] == 0:
            self.currentpos[1] += 1
def GenmuStrategy(self,target,game,alltiles):
    player = target
    self.battlecounter += 1
    self.guard = False
    if self.battlecounter % 15 == 0 :
        if game.distancefromplayer <= 4:
            for i in alltiles:
                if i.coords[1] == self.currentpos[1] - 1:
                    i.damagealert()
                                       
        pass
def TemplateStrategy(self,target,game,alltiles):
    player = target
    self.battlecounter += 1
    print(self.strat)
    if self.strat == 'attack':
        self.cooldown = 10
        self.strat = 'firstattack'
    if not self.cooldown:
        basicmovement(self,game)
        #match player's loadout or no???
        if self.Chealth >= (self.Mhealth*0.5):
            if self.battlecounter % 50 == 0:
                self.strat == 'beam'
            if game.distancefromplayer == 1:
                self.strat == 'slice'
        elif self.Chealth < (self.Mhealth*0.5):
            if self.battlecounter % 75 == 0:
                if self.strat == 'beam':
                    pass
        if self.strat == 'beam':
            damage = 10
            targetarea = copy.copy(self.currentpos)
            targetarea[0] -= 1
            for i in alltiles:
                            if i.coords == targetarea:
                                targetarea = i
                               
            
            moo = {'type':'animation','width':60,'frames':2,'elapsedframes':0,
                   'image':'laser.png','location':copy.copy(targetarea.rect.midbottom),'coords':targetarea.coords,
                   'damageframe':'all','tile':targetarea,'damage':damage,'damages':'player','projectile':8,'direction':'left','onehit':1}
            game.specialblits.append(moo)
            self.strat = 'slice'
        if self.strat == 'slice':
            if game.distancefromplayer > 2:
                self.moveneeded = 'left'
            else:
                self.moveneeded = 'right'
                pass
            
            
def OFredrickStrategy(self,target,game,alltiles):
    player = target
   
    self.battlecounter += 1
    self.movecounter += 1
    print(self.strat)
    self.guard = False
    if self.strat == 'intro':
        self.strat = 'attack'
    if self.strat == 'attack':
        self.cooldown = 10
        self.strat = 'beam'
    if self.cooldown:
        self.cooldown -= 1
    if not self.cooldown:
        if self.Chealth <= 300:
            self.fast = True
        basicmovement(self,game)
        
##        if self.movecounter >= 10 or (self.movecounter >= 5 and self.fast):
##            if self.moveneeded:
##                h = self.moveneeded
##                if h == 'left':
##                    self.currentpos[0] -= 1
##                if h == 'right':
##                    self.currentpos[0] += 1
##                    if self.currentpos[0] >= 9:
##                        self.currentpos[0] = 8
##                if h == 'down':
##                    self.currentpos[1] -= 1
##                if h == 'up':
##                    self.currentpos[1] += 1
##            self.movecounter = 0
##            self.moveneeded = None
        #match player's loadout or no???
##        if self.Chealth >= (self.Mhealth*0.5):
##            if self.battlecounter % 50 == 0:
##                self.strat == 'beam'
##            if game.distancefromplayer == 1:
##                self.strat == 'slice'
##        elif self.Chealth < (self.Mhealth*0.5):
##            if self.battlecounter % 75 == 0:
##                if self.strat == 'beam':
##                    pass
        if self.strat == 'beam':
            if game.distancefromplayer < 4:
                self.moveneeded = 'right'
            else:
                
                if player.currentpos[1] > self.currentpos[1]:
                    self.moveneeded = 'down'
                if player.currentpos[1] < self.currentpos[1]:
                    self.moveneeded = 'up'
                if self.moo <=10:
                    self.moo += 1
                    if self.Chealth >= (self.Mhealth*0.5):
                        self.moo += 1
                    damage = 10
                    targetarea = copy.copy(self.currentpos)
                    targetarea[0] -= 1
                    for i in alltiles:
                        if i.coords == targetarea:
                            targetarea = i
                    moo = {'type':'animation','width':60,'frames':2,'elapsedframes':0,
                           'image':'laser.png','location':copy.copy(targetarea.rect.midbottom),'coords':targetarea.coords,
                           'damageframe':'all','tile':targetarea,'damage':damage,'damages':'player','projectile':8,'direction':'left','onehit':1}
                    game.specialblits.append(moo)
                    self.cooldown = 7
                else:
                    self.strat = 'slice'
                    self.cooldown = 10
                    self.moo = 0
        if self.strat == 'burst':
            for x in alltiles:
                x.damagealert()
                x.damage(10,10,'player',['stagger','player'])
            self.strat = 'beam'
        if self.strat == 'slice':
            
            if game.distancefromplayer >= 2:
                self.moveneeded = 'left'
            else:
                self.moveneeded = 'right'
                targetarea = copy.copy(game.player.currentpos)
                for x in alltiles:          
                    if (x.coords == targetarea) or (x.coords == [targetarea[0] + 1,targetarea[1]]):
                        x.damagealert()
                        x.damage(15,15,'player',['staggeronblock',self], ['stagger','player'])
                self.strat = 'beam'
                if self.Chealth >= 150:
                    self.cooldown = 50
                else:
                    self.strat = 'burst'
                    self.cooldown = 30
                
        
            
        print(self.moveneeded)

    

def DarkStrategy(self,target,game,alltiles):
    player = target
    self.battlecounter += 1
    if self.strat == 'intro':
        self.strat = 'attack'
    if self.battlecounter % 100 == 0 and self.strat == None:
        num = random.randint(0,1)
        if num // 2 == 0:
            
            self.strat = 'upswipe'
            self.moo = 0
        else:
            self.strat = 'downswipe'
            self.moo = 0
    
    if self.strat == 'upswipe':
        for i in alltiles:
            if i.coords[1] == 4:
                moo = {'type':'animation','width':60,'frames':10,'elapsedframes':0,
                           'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'up','projectile':8,'onehit':1}
                game.specialblits.append(moo)
        if self.moo < 1:
            self.moo = 1
            self.strat = 'downswipe'
        else:
            self.strat = 'pierce'

    if self.strat == 'downswipe':
        for i in alltiles:
            if i.coords[1] == 0:
                moo = {'type':'animation','width':60,'frames':10,'elapsedframes':0,
                           'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'down','projectile':8,'onehit':1}
                game.specialblits.append(moo)
        if self.moo < 1:
            self.moo = 1
            self.strat = 'upswipe'
        else:
            self.strat = 'pierce'
        pass
def MagicShibaStrategy(self,target,game,alltiles):
    player = target
    self.movecounter += 1
    if self.strat == 'intro':
        self.strat = 'attack'
    #print(self.strat)

    
    
    #print(self.strat)
    if self.movecounter >= 10 or (self.movecounter >= 5 and self.fast):
        if self.moveneeded:
            h = self.moveneeded
            if h == 'left':
                self.currentpos[0] -= 1
            if h == 'right':
                self.currentpos[0] += 1
                if self.currentpos[0] >= 9:
                    self.currentpos[0] = 8
            if h == 'down':
                self.currentpos[1] += 1
            if h == 'up':
                self.currentpos[1] -= 1
        self.movecounter = 0
        self.moveneeded = None
    self.battlecounter += 1
    if self.cooldown:
        self.guard = False
        self.cooldown -= 1
        return
    if self.Chealth >= (self.Mhealth*.66):
        
        if self.strat == 'attack':
            self.guard = False
            if self.hit:
                self.strat = 'countercharge'
                
                
            if game.distancefromplayer >= 1 and game.playerinfront:
                self.moveneeded = 'left'
            if game.playerbehind:
                self.moveneeded = 'right'
            if game.distancefromplayer == 1:
                self.moveneeded = None
                if self.battlecounter % 10 == 0:
                    targetarea = self.currentpos.copy()
                    area = [(-1,0),(-1,-1),(-1,1)]
                    for i in area:
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damagealert()
                                x.damage(10,9,'player',['staggeronblock',self],['stagger',True])
                        self.movecounter = 0
                        targetarea = self.currentpos.copy()
                    self.strat = 'defend'
        if self.strat == 'countercharge':
            self.guard = True
            self.moo += 1
            if self.moo == 15:
                targetarea = self.currentpos.copy()
                for x in alltiles:
                    if x.coords[1] == self.currentpos[1]:
                        x.damagealert()
                        x.damage(10,9,'player',['stagger',True],['staggeronblock',self])
                self.moo = 0
                self.strat = 'defend'
        if self.strat == 'defend':
            self.guard = False
            

            if self.currentpos[0] < 8:
                print(game.distancefromplayer)
                self.moveneeded = 'right'
            else:
                self.strat = 'charge'
                    #self.strat = 'attack'
        if self.strat == 'charge':
            self.guard = True
            self.moo += 1
            print(self.moo)
            if self.moo == 20:
                for x in alltiles:
                    if (x.coords[1] < 4 and x.coords[1] > 1):
                        x.damagealert()
                        x.damage(15,20,'player',['stagger',True])
                
                self.strat = 'attackwait'
                game.countdown = 40
                game.countdownattribute = 'SPcheck'
                game.countdownvalue = 'True'
                game.countdownchar = None
                
                self.moo = 0
                self.cooldown = 30
        if self.strat == 'attackwait':
            self.guard = False
            self.moo += 1
            if self.moo == 30:
                self.strat = 'attack'
                self.moo = 0
    if self.Chealth < (self.Mhealth*0.66) and self.Chealth > (self.Mhealth*.33):
        #print('mid transition')
        
        if self.midtransition:
            self.strat = 'ice'
##            if self.strat == 'attack' or self.strat == 'charge':
##                self.strat = 'ice'
##            elif self.strat == 'countercharge' or self.strat == 'defend':
##                self.strat = 'flee'
            self.moo = 0
            self.midtransition = False
            
        self.fast = True
        if self.currentpos[0] <= 8:
            self.moveneeded = 'right'
        else:
            self.moveneeded = 'None'
        if self.strat == 'wait':
            self.moo += 1
            if self.moo >= 200:
                self.strat = 'ice'
                self.moo = 0
        if self.strat == 'ice' or self.strat == 'finalice' or self.strat == 'finalice2':
            fasttile = random.randint(0,3)
            area = [[-1,-1],[-1,0],[-1,1],[-1,2]]
            done = False
            num = -1
            
            while not done:
                num += 1
                
                targetarea = copy.copy(self.currentpos)
                targetarea[0] += area[num][0]
                targetarea[1] += area[num][1]
                if fasttile == num:
                    z = 4
                    x = 5
                    targetarea[0] -= 1
                else:
                    z = 0
                    x = 6
                for i in alltiles:
                    if i.coords == targetarea:
                        moo = {'type':'animation','width':60,'frames':x,'elapsedframes':z,
                           'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
                        game.specialblits.append(moo)
                if num == 3:
                    done = True
                    if self.strat == 'finalice2':
                        self.strat = 'wait'
                    if self.strat == 'finalice':
                        if self.Chealth <= (self.Mhealth*0.5):
                            self.strat = 'icewait2'
                        else:
                            self.strat = 'wait'
                            self.moo = 0
                    
                    
                    if self.strat == 'ice':
                        self.strat = 'icewait'
        if self.strat == 'icewait' or 'icewait2':
            self.moo += 1
            if self.moo == 25:
                if self.strat == 'icewait2':
                    self.strat = 'finalice2'
                    self.moo = 0
                elif self.strat == 'icewait':
                    self.strat = 'finalice'
                    self.moo = 0
               
                
                
                
        
            pass
        self.guard = False
            
    if self.Chealth <= (self.Mhealth//3):
        self.fast = False
        if self.finaltransition == False:
            if self.strat == 'attack' or self.strat == 'charge':
                self.strat = 'lightning'
            elif self.strat == 'countercharge' or self.strat == 'defend':
                self.strat = 'cower'
            else:
                self.strat = 'lightning'
        self.finaltransition = True
        if self.strat == 'lightning':
            if self.currentpos[0] <5:
                self.moveneeded = 'right'
            else:
                self.moveneeded = 'none'
            if self.chargecounter <= 100:
                self.chargecounter += 1
            
            if self.chargecounter % 33 == 0:   
                #call down lightning at random(???)
                
                cast = 0
              
                x = random.randint(0,4)
                if x == self.prevcast:
                    x = self.prevcast + 1
                    if x == 5:
                        x = 1
               # currentcol = 8
               # while cast <= 9:
                targetarea = [8,x]
                
                for i in alltiles:
                        if i.coords == targetarea:
                            i.damagealert()
                            moo = {'type':'animation','width':60,'frames':5,'elapsedframes':0,'initialframes':1,
                           'image':'lightning.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1,'splitlightning':1}
                            game.specialblits.append(moo)
                cast += 1
                self.prevcast = copy.copy(x)
                    #currentcol -= 1
                
                        
                        
            if self.chargecounter >= 200:
                self.strat = 'cower'
                self.chargecounter = 0
                
        if self.strat == 'cower':
            if self.currentpos[0] < 8:
                self.moveneeded = 'right'
            if self.currentpos[0] >= 9:
                self.moveneeded = 'left'
            else:
                self.strat = 'casting'
        if self.strat == 'casting':
            self.moo += 1
            if self.moo >= 150:
                self.strat = 'lightning'
                player.currentpos[0] = 1
                self.moo = 0
        if self.Chealth <= 300 and self.spattacked == False:
            self.SPevent = True
            self.spattacked = True
            
    
                            
    if self.hit:
        self.hit = None
    
def MagicDogStrategy(self,target,game,alltiles):
    player = target
    self.movecounter += 1
    if self.strat == 'intro':
        self.strat = 'attack'
    
    
    #print(self.strat)
    if self.movecounter >= 10 or (self.movecounter >= 5 and self.fast):
        if self.moveneeded:
            h = self.moveneeded
            if h == 'left':
                self.currentpos[0] -= 1
            if h == 'right':
                self.currentpos[0] += 1
                if self.currentpos[0] >= 9:
                    self.currentpos[0] = 8
            if h == 'down':
                self.currentpos[1] += 1
            if h == 'up':
                self.currentpos[1] -= 1
        self.movecounter = 0
        self.moveneeded = None
    self.battlecounter += 1
    if self.cooldown:
        self.guard = False
        self.cooldown -= 1
        return
    if self.Chealth >= (self.Mhealth*.50):
        
        if self.strat == 'attack':
            self.guard = False
            if self.hit:
                self.strat = 'countercharge'
                
                
            if game.distancefromplayer >= 1 and game.playerinfront:
                self.moveneeded = 'left'
            if game.playerbehind:
                self.moveneeded = 'right'
            if game.distancefromplayer == 1:
                self.moveneeded = None
                if self.battlecounter % 10 == 0:
                    targetarea = self.currentpos.copy()
                    area = [(-1,0),(-1,-1),(-1,1)]
                    for i in area:
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damagealert()
                                x.damage(10,9,'player',['staggeronblock',self],['stagger',True])
                        self.movecounter = 0
                        targetarea = self.currentpos.copy()
                    self.strat = 'defend'
        if self.strat == 'countercharge':
            self.guard = True
            self.moo += 1
            if self.moo == 15:
                targetarea = self.currentpos.copy()
                for x in alltiles:
                    if x.coords[1] == self.currentpos[1]:
                        x.damagealert()
                        x.damage(10,9,'player',['stagger',True],['staggeronblock',self])
                self.moo = 0
                self.strat = 'defend'
        if self.strat == 'defend':
            self.guard = False
            

            if self.currentpos[0] < 6:
                print(game.distancefromplayer)
                self.moveneeded = 'right'
            else:
                x = random.randint(1,2)
                if x == 1:
                    self.strat = 'charge'
                else:
                    self.strat = 'attack'
                    #self.strat = 'attack'
        if self.strat == 'charge':
            self.guard = True
            self.moo += 1
            print(self.moo)
            if self.moo == 20:
                for x in alltiles:
                    if (x.coords[1] < 4 and x.coords[1] > 1):
                        x.damagealert()
                        x.damage(15,20,'player',['stagger',True])
                
                self.strat = 'attackwait'
                game.countdown = 40
                game.countdownattribute = 'SPcheck'
                game.countdownvalue = 'True'
                game.countdownchar = None
                
                self.moo = 0
                self.cooldown = 5
        if self.strat == 'attackwait':
            self.guard = False
            self.moo += 1
            if self.moo == 30:
                self.strat = 'attack'
                self.moo = 0
    if self.Chealth < (self.Mhealth*0.50):
        #print('mid transition')
        
        if self.midtransition:
            self.strat = 'ice'
##            if self.strat == 'attack' or self.strat == 'charge':
##                self.strat = 'ice'
##            elif self.strat == 'countercharge' or self.strat == 'defend':
##                self.strat = 'flee'
            self.moo = 0
            self.midtransition = False
            
        self.fast = True
        if self.currentpos[0] <= 8:
            self.moveneeded = 'right'
        else:
            self.moveneeded = 'None'
        if self.strat == 'wait':
            self.moo += 1
            if self.moo >= 200:
                self.strat = 'ice'
                self.moo = 0
        if self.strat == 'ice' or self.strat == 'finalice' or self.strat == 'finalice2':
            fasttile = random.randint(0,3)
            area = [[-1,-1],[-1,0],[-1,1],[-1,2]]
            done = False
            num = -1
            
            while not done:
                num += 1
                
                targetarea = copy.copy(self.currentpos)
                targetarea[0] += area[num][0]
                targetarea[1] += area[num][1]
                if fasttile == num:
                    z = 4
                    x = 5
                    targetarea[0] -= 1
                else:
                    z = 0
                    x = 6
                for i in alltiles:
                    if i.coords == targetarea:
                        moo = {'type':'animation','width':60,'frames':x,'elapsedframes':z,
                           'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
                        game.specialblits.append(moo)
                if num == 3:
                    done = True
                    if self.strat == 'finalice2':
                        self.strat = 'wait'
                    if self.strat == 'finalice':
                        if self.Chealth <= (self.Mhealth*0.5):
                            self.strat = 'icewait2'
                        else:
                            self.strat = 'wait'
                            self.moo = 0
                    
                    
                    if self.strat == 'ice':
                        self.strat = 'icewait'
        if self.strat == 'icewait' or 'icewait2':
            self.moo += 1
            if self.moo == 25:
                if self.strat == 'icewait2':
                    self.strat = 'finalice2'
                    self.moo = 0
                elif self.strat == 'icewait':
                    self.strat = 'finalice'
                    self.moo = 0
               
                
                
                
        
            pass
        self.guard = False
            
##    if self.Chealth <= (self.Mhealth//3):
##        self.fast = False
##        if self.finaltransition == False:
##            if self.strat == 'attack' or self.strat == 'charge':
##                self.strat = 'lightning'
##            elif self.strat == 'countercharge' or self.strat == 'defend':
##                self.strat = 'cower'
##            else:
##                self.strat = 'lightning'
##        self.finaltransition = True
##        if self.strat == 'lightning':
##            if self.currentpos[0] <5:
##                self.moveneeded = 'right'
##            else:
##                self.moveneeded = 'none'
##            if self.chargecounter <= 100:
##                self.chargecounter += 1
##            
##            if self.chargecounter % 5 == 0:   
##                #call down lightning at random(???)
##                
##                cast = 0
##              
##                x = random.randint(0,4)
##                if x == self.prevcast:
##                    x = self.prevcast + 1
##                    if x == 5:
##                        x = 1
##               # currentcol = 8
##               # while cast <= 9:
##                targetarea = [8,x]
##                
##                for i in alltiles:
##                        if i.coords == targetarea:
##                            i.damagealert()
##                            moo = {'type':'animation','width':60,'frames':3,'elapsedframes':4,'initialframes':4,
##                           'image':'lightning.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
##                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
##                            game.specialblits.append(moo)
##                cast += 1
##                self.prevcast = copy.copy(x)
##                    #currentcol -= 1
##                
##                        
##                        
##            if self.chargecounter >= 200:
##                self.strat = 'cower'
##                self.chargecounter = 0
##                
##        if self.strat == 'cower':
##            if self.currentpos[0] < 8:
##                self.moveneeded = 'right'
##            if self.currentpos[0] >= 9:
##                self.moveneeded = 'left'
##            else:
##                self.strat = 'casting'
##        if self.strat == 'casting':
##            self.moo += 1
##            if self.moo >= 150:
##                self.strat = 'lightning'
##                player.currentpos[0] = 1
##                self.moo = 0
##        if self.Chealth <= 300 and self.spattacked == False:
##            self.SPevent = True
##            self.spattacked = True
##            
    
                            
    if self.hit:
        self.hit = None
def WhiteCloakStrategy(self,target,game,alltiles):
    pass
def BlackCloakStrategy(self,target,game,alltiles):
    player = target
    self.movecounter += 1
    self.guard = True
    print(self.strat)
    if self.movecounter >= 10 or (self.movecounter >= 2 and self.fast):
        if self.moveneeded:
            h = self.moveneeded
            if h == 'left':
                self.currentpos[0] -= 1
            if h == 'right':
                self.currentpos[0] += 1
                if self.currentpos[0] >= 9:
                    self.currentpos[0] = 8
            if h == 'down':
                self.currentpos[1] -= 1
            if h == 'up':
                self.currentpos[1] += 1
        self.movecounter = 0
        self.moveneeded = None
            
                
                
                
                   
##                if h == 'down':
##                    self.currentpos[1] += 1
##                if h == 'up':
##                    self.currentpos[1] -= 1
           
    self.battlecounter += 1
    if self.cooldown:
        self.guard = False
        self.cooldown -= 1
        return
    if self.hit:
        self.hit = False
        self.strat = 'retreat'
        self.weirdrects = False
    #right out of the gate
    #self.strat == 'attack'
    if self.strat == 'intro':
        self.image.scroll(-0,-340)
        self.weirdrects = True
        self.rect.width = 100
        self.rect.height = 85
        self.moo += 1
        if self.moo >= 10 and self.moo < 20:
            self.image.scroll(-99,-340)
        if self.moo >= 20 and self.moo < 40:
            self.image.scroll(-198,-340)
        if self.moo == 60:
            game.SPcheck = True
            self.weirdrects = False
            self.strat = 'dash'
            self.moo = 0

        
    if self.Chealth >= (0.50*self.Mhealth):
        if self.strat == 'reset':
            self.rect.width = copy.copy(self.defwidth)
            self.rect.height = copy.copy(self.defheight)
        if self.strat == 'reset' or self.strat == 'attack':
           
            self.strat = 'dash'
##        if self.strat == 'dash':
##            self.guard = False
##            if game.distancefromplayer >= 2:
##                self.fast = True
##                if game.playerinfront:
##                    self.moveneeded = 'left'
##                if game.playerisabove:
##                    self.moveneeded = 'up'
##                if game.playerisbelow:
##                    self.moveneeded = 'down'
##                if game.playerbehind:
##                    self.moveneeded = 'right'
##            
##            else:
        if self.strat == 'heavyslash':
            if game.distancefromplayer > 2:
                self.moveneeded = 'left'
            else:
                self.moo2 += 1
                if self.moo2 == 45:
                    self.moo2 = 0
                    area = [(-1,0),(-1,1)]
                    for i in area:
                            targetarea = self.currentpos.copy()
                            targetarea[0] += i[0]
                            targetarea[1] += i[1]
                            for x in alltiles:
                                if x.coords == targetarea:
                                    x.damage(30,10,'player',['pierceinvis',True],['stagger','player'])
                            self.cooldown = 30
                    
        if self.strat == 'swordwaves':
            if self.currentpos[0] < 8:
                if game.playerinfront:
                    self.moveneeded = 'right'
                
            else:
                
                moo = {'type':'animation','width':60,'frames':19,'elapsedframes':0,
                    'image':'battlesprites/swordwave.png','location':copy.copy(alltiles[15].rect.midbottom),
                    'damageframe':7,'tile':alltiles[15],'damage':10,'damages':'player'}
                     #moo = {'type':'animation','width':60,'frames':4,'elapsedframes':0,
                     #  'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                     #  'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
                game.specialblits.append(moo)
                print('cool')
                self.strat = 'heavyslash'
        if self.strat == 'twinslash2':
            self.moveneeded = None
            self.moo2 += 1
            if self.moo2 == 40:
                self.moo = 2
                area = [(-1,1),(-1,0)]
                for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,15,'player',['pierceinvis',True],['stagger','player'],['staggeronblock',self])
                self.cooldown = 10
                self.weirdrects = False
                self.strat = 'retreat'
            
        if self.strat == 'twinslash1':
            self.moveneeded = None
            self.moo2 += 1
            if self.moo2 == 40:
                self.moo = 2
                area = [(-1,-1),(-1,0)]
                for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,15,'player',['pierceinvis',True],['stagger','player'],['staggeronblock',self])
                self.cooldown = 10
                self.weirdrects = False
                self.strat = 'twinslash2'
        #attack multiple times right out of the gate
        
        if self.strat == 'dash5':
            self.moveneeded = None
            self.moo2 += 1
            self.image.scroll(-198,-425)
            if self.moo2 == 10:
                self.moo2 = 0
                area = [(-1,-1), (-1,0),(-1,1),(-2,-1),(-2,0),(-2,1)]
                for i in area:
                        targetarea = self.currentpos.copy()
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,10,'player',['pierceinvis',True],['stagger','player'],['staggeronblock',self])
                self.cooldown = 30
                self.weirdrects = False
                self.strat = 'retreat'
        if self.strat == 'dash4':
            self.image.scroll(-198,-425)
            self.moveneeded = None
            self.moo2 += 1
            if self.moo2 == 10:
                self.moo2 = 0
                area = [(0,-1),(-1,0),(-2,1)]
                for i in area:
                        targetarea = self.currentpos.copy()
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,10,'player',['pierceinvis',True])
                self.strat = 'dash5'
        if self.strat == 'dash3':
            self.moveneeded = None
            self.moo2 += 1
            self.image.scroll(-99,-425)
            if self.moo2 == 10:
                self.moo2 = 0
                area = [(-2,-1),(-1,0),(0,1)]
                for i in area:
                        targetarea = self.currentpos.copy()
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,10,'player',['pierceinvis',True])
                self.strat = 'dash4'
        if self.strat == 'dash2':
            self.image.scroll(-99,-425)
            self.moveneeded = None
            self.moo2 += 1
            if self.moo2 == 10:
                self.moo2 = 0
                area = [(-1,-1), (-1,0),(-1,1)]
                for i in area:
                        targetarea = self.currentpos.copy()
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,10,'player',['pierceinvis',True])
                self.strat = 'dash3'
        if self.strat == 'dash':
            if game.distancefromplayer >= 1:
                if game.playerinfront:
                    self.moveneeded = 'left'
                if game.playerbehind:
                    self.moveneeded = 'right'
            if game.playerinfront and game.distancefromplayer == 1:
                #if strat == 'closecut'
                #if strat == 'combocut'
                self.moveneeded = None
                self.moo2 += 1
                self.rect.width = 100
                self.rect.height = 85
                self.weirdrects = True
                self.image.scroll(0,-425)
                if self.moo2 >= 15:
                    self.moo2 = 0
                    area = [(-2,0), (-1,0)]
                    for i in area:
                        targetarea = self.currentpos.copy()
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(10,10,'player',['pierceinvis',True])
                    self.moo += 1
                    self.strat = 'dash2'

                    
        if game.playerbehind:
            self.moveneeded = 'right'
        if self.strat == 'retreat':
            self.fast = True
            if self.currentpos[0] <= 7:
                self.moveneeded = 'right'
            else:
                self.fast = False
                self.moveneeded = None
                x = random.randint(0,1)
                if x == 1:
                    self.cooldown = 10
                    self.strat = 'swordwaves'
                   
                    self.moo = 0
                else:
                    self.strat = 'dash'
                    self.moo = 0
def GrayCloakStrategy(self, target, game, alltiles):
        player = target
        print(self.battlecounter)
        self.battlecounter += 1
        if self.guard == True:
            print('Guard')
        self.guard = False
        
        if self.Chealth >= self.Mhealth:
            self.guard = False
            if game.playerbehind:
            
                for i in alltiles:
                    if i.coords[1] >= self.coords[1]:
                        i.damagealert()
                        if i.occupied:
                            if i.occupant.isplayer:
                                i.occupant.coords[1] = (self.coords[1] - 1)
                self.cooldown = True
        
        if (not self.cooldown and not self.spattacking and self.Chealth < self.Mhealth and not self.stunned and not self.stunsp):
            self.guard = True
            
            if not game.playerinfront:
                self.currentpos[0] += 1
            #if game.distancefromplayer <= 3 and game.playerinsamerow:
            #    game.playertooclose += 1
            #    if game.playertooclose >= 5:
            #        self.currentpos[0] += 1
            #        game.playertooclose = 0
            
           
##            if not game.playerinfront:
##                self.currentpos[0] += 1
##            if game.distancefromplayer <= 3 and game.playerinsamerow:
##                game.playertooclose += 1
##                #if game.distancefromplayer == 1:
##    ##                if game.playertooclose >= 10:
##    ##                    self.guard = True
##                if game.playertooclose >= 60:
##                    self.currentpos[0] += 1
##                if game.distancefromplayer == 2:
##                    pass#self.guard = False
            if game.playerisabove:
                if self.battlecounter % 20 == 0:
                    self.currentpos[1] += 1
            if game.playerisbelow:
                if self.battlecounter % 20 == 0:
                    self.currentpos[1] -= 1
##                 
            #if game.playertooclose and game.playerattacking and game.distancefromplayer <= 1:
            #    self.currentpos[0] += 1
            #    game.aggressive = True
##                #self.guard = True
##                self.aggrocounter = True
##                # punish for aggressive play
##                
##
##            if game.playertooclose == 90:
##                    print('too close')
##                    for x in alltiles:
##                        if x.coords == player.currentpos:
##                            x.damagealert()
##                            x.damage(8,10,'player',['staggeronblock',self])
##                    #game.playertooclose = 0
            if game.distancefromplayer >= 2:
                game.playertooclose = 0
            if self.battlecounter % 5 == 0:
                if game.distancefromplayer > 3:
                    self.currentpos[0] -= 1
##                
##          #make more lenient  
            if self.battlecounter % 50 == 0:#(60-((game.difficulty-1)*20)) == 0:
                self.attackready = True
                
            if self.attackready == True:
                if game.playerinfront:
                    if game.playerinsamerow and ((game.distancefromplayer >=3 and self.Chealth <=1000) or (self.Chealth >=1001)):
                        self.frontswipe = 1
                        for x in alltiles:
                            if x.coords[0] == player.currentpos[0]:
                                #make warning longer
                                if self.Chealth >= 1001:
                                    x.damage(10,30,'player',['stagger','player'])
                                else:
                                    x.damage(10,30,'player',['stagger','player','staggeronblock',self])
                                
                        
                        self.attackready = False
                    elif game.playerinsamerow and game.distancefromplayer <= 2 and self.Chealth <= 1000:
                        self.sideswipe = 1
                        for x in alltiles:
                            
                            if x.coords[1] == player.currentpos[1]:
                                 
                                 x.damagealert()
                                 x.damage(15,25,'player',['staggeronblock',self], ['stagger','player'])
                        self.attackready = False
                        
                                                  
                
            if self.Chealth <= 500 and self.sptrigger == False:
                 # Trigger the special attack randomly
                x = random.randint(0,50)
                if x == 50:
                    self.spattacking = True
                    self.sptrigger = True
        else:
            
            if self.cooldown:
                self.image = self.staggerimage
                self.image.scroll(-330,-255)
                self.cooldown += 1
                self.guard = False
##                if self.cooldown == 1:
##                    self.imagereset()
##                    self.image.scroll(-330,-255)
##                    #self.image.fill((255,0,0), special_flags=pygame.BLEND_RGB_ADD)
##                    self.staggerimage = self.image.copy()
##                self.cooldown += 1
##                self.guard = False
##                #print('Cooldown remaining',self.cooldown)
##                
##                    
##                if self.cooldown >= 3:
##                    #1 and 2 execute at same time, skip to 3
##                    self.imagereset()
##                    self.image = copy.copy(self.staggerimage)
##                    self.image.scroll(-330,-255)
                if self.cooldown >= 60:#(70 - (game.difficulty*20)):
                    self.imagereset()
                    self.battlecounter = 0
                    self.cooldown = 0

        #######
        if self.aggrocounter:
            self.aggrocounter += 1
            if self.aggrocounter == 10:
                player.currentpos[0] = 1
            if self.aggrocounter == 40:
                game.aggressive = True
                self.aggrocounter = 0
##        if self.magicattacking:
##            if self.magicattacking < 5:
##                self.imagereset()
##                self.image.scroll(-55,-170)
##                self.magicattacking += 1
##            elif self.magicattacking >= 5:
##                self.magicattacking = 0
##                self.imagereset()
        if self.sideswipe:
            self.sideswipe += 1
            if self.sideswipe < 36:
                self.imagereset()
                #if self.slicing % 2 == 0:
                self.image.scroll(55*(self.sideswipe//6)*-1,-340)
                self.sideswipe += 1
            else:
                self.imagereset()
                self.sideswipe = 0
                self.cooldown = 1
                self.animation = False
        if self.frontswipe:
            self.frontswipe += 1
            if self.frontswipe < 36:
                self.imagereset()
                self.image.scroll(55*(self.frontswipe//6)*-1,-255)
                self.frontswipe += 1
            else:
                #if self.frontswipe == 18:
                #    self.cooldown = True
                #if self.frontswipe == 63:
                self.imagereset()
                self.frontswipe = 0
                self.animation = False
                self.cooldown = 1
            
        if self.spattacking:
            #print(self.spattacking)
            self.statuseffect = 'SPattack'
            self.spattacking += 1
            if self.spattacking == 136 or ( self.spattacking == 40 and self.spattackpart == 4):
                #print(self.spattackpart,'moo')
                self.spattackpart += 1
                self.spattacking = 1
                if self.spattackpart >= 5:
                    self.spattacking = None
                    self.statuseffect = 'Normal'
                    game.SPattacked = True
                    return
            if self.spattacking % 15 == 0 and self.spattackpart == 1:
                for x in alltiles:
                    if x.coords[0] == (9 - (self.spattacking/15)) and x.spchanged != True:
                    #if x.coords [0] == 1 and x.coords[1] == 2:
                        #x.state = 'animation'
                        moo = {'type':'animation','width':60,'frames':19,'elapsedframes':0,'image':'creatorattack.png','location':copy.copy(x.rect.midbottom),'damageframe':7,'tile':x,'damage':10,'damages':'player'}
                        game.specialblits.append(moo)
                        #x.damagealert()
            if self.spattacking % 30 == 0  and self.spattackpart == 2:
                for x in alltiles:
                    if x.coords[1] == (5 - (self.spattacking/30)) and x.spchanged != True:
                        moo = {'type':'animation','width':60,'frames':19,'elapsedframes':0,'image':'creatorattack.png','location':copy.copy(x.rect.midbottom),'damageframe':7,'tile':x,'damage':10,'damages':'player'}
                        game.specialblits.append(moo)
            if self.spattacking % 4 == 0 and self.spattackpart == 3:
                if self.spattacking == 4:
                    self.battletiles = copy.copy(alltiles)
               # print(self.battletiles)
                
                if len(self.battletiles) == 0:
                    #self.spattacking = 136
                    return
                    
                if len(self.battletiles) != 1:   
                    x = self.battletiles[random.randint(1,(len(self.battletiles)-1))]
                else:
                    x = self.battletiles[0]
                self.battletiles.remove(x)
##                for x in self.battletiles:
##                    if x.spchanged == True:
##                        self.battletiles.remove(x)
                #battletiles.remove(x)
                moo = {'type':'animation','width':60,'frames':19,'elapsedframes':0,'image':'creatorattack.png','location':copy.copy(x.rect.midbottom),'damageframe':7,'tile':x,'damage':5,'damages':'player'}
                game.specialblits.append(moo)

def SwordNyuStrategy(self,target,game,alltiles):
    player = target
    self.movecounter += 1
    self.guard = False
    print(self.strat)
    if self.movecounter >= 10 or (self.movecounter >= 5 and self.fast):
        if self.moveneeded:
            h = self.moveneeded
            if h == 'left':
                self.currentpos[0] -= 1
            if h == 'right':
                self.currentpos[0] += 1
                if self.currentpos[0] >= 9:
                    self.currentpos[0] = 8
            if h == 'down':
                self.currentpos[1] -= 1
            if h == 'up':
                self.currentpos[1] += 1
        self.movecounter = 0
        self.moveneeded = None
            
                
                
                
                   
##                if h == 'down':
##                    self.currentpos[1] += 1
##                if h == 'up':
##                    self.currentpos[1] -= 1
           
    self.battlecounter += 1
    if self.cooldown:
        self.guard = False
        self.cooldown -= 1
        return
    
    if self.Chealth >= (0.50*self.Mhealth):
        if self.strat == 'reset' or self.strat == 'attack':
            self.strat = 'dash'
##        if self.strat == 'dash':
##            self.guard = False
##            if game.distancefromplayer >= 2:
##                self.fast = True
##                if game.playerinfront:
##                    self.moveneeded = 'left'
##                if game.playerisabove:
##                    self.moveneeded = 'up'
##                if game.playerisbelow:
##                    self.moveneeded = 'down'
##                if game.playerbehind:
##                    self.moveneeded = 'right'
##            
##            else:
        if self.strat == 'circlecut':
            if game.distancefromplayer >= 1:
                if game.playerinfront:
                    self.moveneeded = 'left'
                if game.playerbehind:
                    self.moveneeded = 'right'
            if game.playerinfront and game.distancefromplayer == 1:
                self.moveneeded = None
                self.moo += 1
                #circlecut after hitting
                if self.moo == 10:
                    area = [(1,1),(1,0),(1,-1),(-1,1),(-1,0),(-1,-1),(0,1),(0,-1)]
                        
                        
                    targetarea = self.currentpos.copy()
                    
                    for i in area:
                        targetarea[0] -= i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(5,10,'player',['staggeronblock',self], ['stagger','player'])
                                targetarea = self.currentpos.copy()
                    self.strat = 'retreat'
                    self.moo = 0
        if self.strat == 'dash':
            if game.distancefromplayer >= 1:
                if game.playerinfront:
                    self.moveneeded = 'left'
                if game.playerbehind:
                    self.moveneeded = 'right'
            if game.playerinfront and game.distancefromplayer == 1:
                #if strat == 'closecut'
                #if strat == 'combocut'
                self.moveneeded = None
                self.moo2 += 1
                if self.moo2 >= 7:
                    self.moo2 = 0
                    target = copy.copy(self.currentpos)
                    target[0] -= 1
                    for i in alltiles:
                        if i.coords == target:
                            i.damage(10,10,'player',['stagger','player'])
                    self.moo += 1
                    
                        
                    self.strat = 'retreat'
                    
        if game.playerbehind:
            self.moveneeded = 'right'
        if self.strat == 'retreat':
            if self.currentpos[0] <= 7:
                self.moveneeded = 'right'
            else:
                self.moveneeded = None
                x = random.randint(0,1)
                if x == 1:
                    self.cooldown = 10
                    self.strat = 'circlecut'
                   
                    self.moo = 0
                else:
                    self.strat = 'dash'
                    self.moo = 0


def MagiNyuStrategy(self,target,game,alltiles):
        player = target
        self.movecounter += 1
        self.moo2 += 1
        self.guard = False
        print(self.strat)
        if self.movecounter >= 40 or (self.movecounter >= 20 and self.fast):
            #if self.moveneeded:
            #    h = self.moveneeded
            #what i wouldn't do for a switch function
            if self.currentpos == [5,4]:
                self.currentpos[0] += 1
                self.currentpos[1] -= 3#4
                
            elif self.currentpos == [7,3]:
                self.currentpos[0] -= 2
                self.currentpos[1] += 1#3
            elif self.currentpos == [6,1]:
                self.currentpos[1] += 1
            
            elif self.currentpos == [5,1]:
                self.currentpos[0] += 2
                self.currentpos[1] += 2#2
            elif self.currentpos == [6,2]:
                self.currentpos[0] -= 1
                self.currentpos[1] -= 1#1
            else:
                moo = random.randint(0,2)
                areas = [[6,1],[5,4],[7,3]]
                self.currentpos = copy.copy(areas[moo])
                
                
                
                
                   
##                if h == 'down':
##                    self.currentpos[1] += 1
##                if h == 'up':
##                    self.currentpos[1] -= 1
            self.movecounter = 0
            self.moveneeded = None
        self.battlecounter += 1
        if self.cooldown:
            self.guard = False
            self.cooldown -= 1
            return
        
        #if self.Chealth >= (0.50*self.Mhealth):
        if self.moo2 == 200:
                self.strat = 'snipe'
                self.moo2 = 0
        if self.battlecounter >= 50 and self.battlecounter <= 53:
            self.strat = 'firestorm'
        
        
        
            #if self.battlecounter >= 53:
            #    self.battlecounter = 0
            #    i = random.randint(1,3)
            #    if i == 2:
            #        self.strat = 'snipe'
       
            if self.strat == 'firestorm':
                order = [4,3,2,1]
                random.shuffle(order)
                
                targetarea = [8,order[self.moo]]
                
                for i in alltiles:
                    
                    if i.coords == targetarea:
                        moo = {'type':'animation','width':60,'frames':4,'elapsedframes':0,
                       'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                       'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
                        game.specialblits.append(moo)
                self.moo += 1
                if self.moo >= 4:
                    self.moo = 0
                if self.battlecounter >= 53:
                    self.battlecounter = 0
            if self.strat == 'circlecut':
                pass
            if game.distancefromplayer >= 1:
                if game.playerinfront:
                    self.moveneeded = 'left'
                if game.playerbehind:
                    self.moveneeded = 'right'
            if game.playerinfront and game.distancefromplayer == 1:
                self.moveneeded = None
                self.moo += 1
                #circlecut after hitting
                if self.moo == 10:
                    area = [(1,1),(1,0),(1,-1),(-1,1),(-1,0),(-1,-1),(0,1),(0,-1)]
                        
                        
                    targetarea = self.currentpos.copy()
                    
                    for i in area:
                        targetarea[0] -= i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damage(5,10,'player',['staggeronblock',self], ['stagger','player'])
                                targetarea = self.currentpos.copy()
                    self.strat = 'retreat'
                    self.moo = 0
        if self.strat == 'dash':
            if game.distancefromplayer >= 1:
                if game.playerinfront:
                    self.moveneeded = 'left'
                if game.playerbehind:
                    self.moveneeded = 'right'
            if game.playerinfront and game.distancefromplayer == 1:
                #if strat == 'closecut'
                #if strat == 'combocut'
                self.moveneeded = None
                self.moo2 += 1
                if self.moo2 >= 7:
                    self.moo2 = 0
                    target = copy.copy(self.currentpos)
                    target[0] -= 1
                    for i in alltiles:
                        if i.coords == target:
                            i.damage(10,10,'player',['stagger','player'])
                    self.moo += 1
                    
                        
                    self.strat = 'retreat'

            
                   
            #for i in alltiles:
            #    pass
        if self.strat == 'snipe':
            self.currentpos[1] = copy.copy(player.currentpos[1])
            if self.currentpos[1] == player.currentpos[1]:
                for i in alltiles:
                    if i.coords[1] == self.currentpos[1] and i.coords[0] < self.currentpos[0]:
                        i.damage(5,20,'player',['staggeronblock',self], ['stagger','player'])
                self.cooldown = 40
                self.strat = 'firestorm'
                            
##                    targetarea = copy.copy(self.currentpos)
##                    targetarea[0] -= 1
##                    for i in alltiles:
##                        if i.coords == targetarea:
##                            moo = {'type':'animation','width':60,'frames':8,'elapsedframes':0,
##                           'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
##                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1,'reflectable':True}
##                            game.specialblits.append(moo)
##                            
##                        
##                    #hit the rock back at the enemy?

def DarkNyuStrategy(self,target,game,alltiles):
        player = target
        self.movecounter += 1
        self.moo2 += 1
        self.guard = False
        print(self.strat)
        if self.movecounter >= 40 or (self.movecounter >= 20 and self.fast):
            #if self.moveneeded:
            #    h = self.moveneeded
            #what i wouldn't do for a switch function
            if self.currentpos == [5,4]:
                self.currentpos[0] += 1
                self.currentpos[1] -= 3#4
                
            elif self.currentpos == [7,3]:
                self.currentpos[0] -= 2
                self.currentpos[1] += 1#3
            elif self.currentpos == [6,1]:
                self.currentpos[1] += 1
            
            elif self.currentpos == [5,1]:
                self.currentpos[0] += 2
                self.currentpos[1] += 2#2
            elif self.currentpos == [6,2]:
                self.currentpos[0] -= 1
                self.currentpos[1] -= 1#1
            else:
                moo = random.randint(0,2)
                areas = [[6,1],[5,4],[7,3]]
                self.currentpos = copy.copy(areas[moo])
                
                
                
                
                   
##                if h == 'down':
##                    self.currentpos[1] += 1
##                if h == 'up':
##                    self.currentpos[1] -= 1
            self.movecounter = 0
            self.moveneeded = None
        self.battlecounter += 1
        if self.cooldown:
            self.guard = False
            self.cooldown -= 1
            return
        
        #if self.Chealth >= (0.50*self.Mhealth):
        if self.moo2 == 200:
                self.strat = 'snipe'
                self.moo2 = 0
        if self.battlecounter >= 50 and self.battlecounter <= 53:
            self.strat = 'firestorm'
        
        
        
            #if self.battlecounter >= 53:
            #    self.battlecounter = 0
            #    i = random.randint(1,3)
            #    if i == 2:
            #        self.strat = 'snipe'
       
            if self.strat == 'firestorm':
                order = [4,3,2,1]
                random.shuffle(order)
                
                targetarea = [8,order[self.moo]]
                
                for i in alltiles:
                    
                    if i.coords == targetarea:
                        moo = {'type':'animation','width':60,'frames':4,'elapsedframes':0,
                       'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                       'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
                        game.specialblits.append(moo)
                self.moo += 1
                if self.moo >= 4:
                    self.moo = 0
                if self.battlecounter >= 53:
                    self.battlecounter = 0
            

            
                   
            #for i in alltiles:
            #    pass
        if self.strat == 'snipe':
            self.currentpos[1] = copy.copy(player.currentpos[1])
            if self.currentpos[1] == player.currentpos[1]:
                for i in alltiles:
                    if i.coords[1] == self.currentpos[1] and i.coords[0] < self.currentpos[0]:
                        i.damage(5,20,'player',['staggeronblock',self], ['stagger','player'])
                self.cooldown = 40
                self.strat = 'firestorm'
                            
##                    targetarea = copy.copy(self.currentpos)
##                    targetarea[0] -= 1
##                    for i in alltiles:
##                        if i.coords == targetarea:
##                            moo = {'type':'animation','width':60,'frames':8,'elapsedframes':0,
##                           'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
##                           'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1,'reflectable':True}
##                            game.specialblits.append(moo)
##                            
##                        
##                    #hit the rock back at the enemy?
def FallenWarriorStrategy(self,target,game,alltiles):
    
    if self.moveneeded:
        if self.movecounter >= 10 or (self.movecounter >= 5 and self.fast):

            h = self.moveneeded
            if h == 'left':
                self.currentpos[0] -= 1
            if h == 'right':
                self.currentpos[0] += 1
                if self.currentpos[0] >= 9:
                    self.currentpos[0] = 8
            if h == 'down':
                self.currentpos[1] -= 1
            if h == 'up':
                self.currentpos[1] += 1
            self.movecounter = 0
            self.moveneeded = None
        self.movecounter += 1
    if self.cooldown:
        
        self.guard = False
        self.cooldown -= 1

    else:
                   
            
        
        if self.strat == None:
            self.strat = 'attack'
        if self.Chealth >= (self.Mhealth*0.75):
            if self.strat == 'attack':
                if game.distancefromplayer >= 2:
                    self.moveneeded = 'left'
                if game.playerbehind:
                    self.moveneeded = 'right'
                
                if game.distancefromplayer == 1:
                    #three hit attack (third hit can be blocked for a stun)
                    self.strat = 'attack1'
                    self.cooldown = 60
                    self.moveneeded == None
            if self.strat == 'retreat':
                if self.currentpos[0] < 7:
                    self.moveneeded = 'right'
                else:
                    self.strat = 'attack'
            if self.strat == 'attack1' or self.strat == 'attack2' or self.strat == 'attack3':
                self.moveneeded = None
                targetarea = copy.copy(self.currentpos)
                targetarea1 = copy.copy(self.currentpos)
                targetarea2 = copy.copy(self.currentpos)
                targetarea2[0] -= 2
                targetarea1[0] -= 1
                
                for i in alltiles:
                    if i.coords == targetarea1 or i.coords == targetarea2:
                        if self.strat == 'attack1':
                            i.damage(5,10,'player',['stagger','player'])
                        if self.strat == 'attack2':
                            i.damage(5,10,'player',['stagger','player'])
                        if self.strat == 'attack3':
                            i.damage(5,10,'player',['staggeronblock',self], ['stagger','player'])
                if self.strat == 'attack3':
                    self.cooldown = 30
                    self.strat = 'attack'
                if self.strat == 'attack2':
                    self.cooldown = 20
                    self.strat = 'attack3'
                if self.strat  == 'attack1':
                    self.cooldown = 20
                    self.strat = 'attack2'
            if self.strat == 'wave slash':
                #3 waves of slash attacks, maintains distance
                if self.currentpos[0] < 7:
                    self.moveneeded = 'right'
                fasttile = random.randint(0,3)
                area = [[-1,-1],[-1,0],[-1,1],[-1,2]]
                done = False
                num = -1
                
                while not done:
                    num += 1
                    
                    targetarea = copy.copy(self.currentpos)
                    targetarea[0] += area[num][0]
                    targetarea[1] += area[num][1]
                    if fasttile == num:
                        z = 4
                        x = 5
                        targetarea[0] -= 1
                    else:
                        z = 0
                        x = 6
                    for i in alltiles:
                        if i.coords == targetarea:
                            moo = {'type':'animation','width':60,'frames':x,'elapsedframes':z,
                               'image':'blizzard.png','location':copy.copy(i.rect.midbottom),'coords':i.coords,
                               'damageframe':'all','tile':i,'damage':10,'damages':'player','direction':'left','projectile':8,'onehit':1}
                            game.specialblits.append(moo)
                    if num == 3:
                        done = True
                        self.cooldown = 60
                        self.strat = 'retreat'
            
            if self.strat == 'cast':
                #i = random.randint(1,3)
                #if i == 1:
                #    self.strat == 'storm'
                #if i == 2:
                #    
                #    self.strat == 'blaze'
                #if i == 3:
                #    self.strat == 'blizzard'
               self.strat = 'wave slash' 
                
def oldgraycloakstrat():
    print('this is dummied out')
    return
    if game.playerinfront:
                if game.playerapproaching and game.playerinsamerow:
                    if self.currentpos[0] >= 9:
                        self.currentpos[0] = 8
                    self.magicattacking = True
                    for x in alltiles:
                        #try to make them run into the attack
                        if game.distancefromplayer <= 2:
                            self.sideswipe = True
                            if x.coords[0] == player.currentpos[0] + 1:
                                x.damagealert()
                                x.damage(4,15,'player',['damageduration',10],['moo',11])
                       
                      
                elif game.playerretreating and game.playerinsamerow:
                    
                    self.magicattacking = True
                    for x in alltiles:
                        #they retreat into the attack
                        if x.coords[0] == player.currentpos[0] - 1:
                            x.damagealert()
                            x.damage(4,15,'player',['damageduration',10])
                        
                else:                        
                        #They get punished for being too far back
                        if game.distancefromplayer >= 3:
                            game.playertoofar += 1
                            print(game.playertoofar, 'How far?')
                            for x in alltiles:
                                if x.coords[0] == player.currentpos[0]:
                                    x.damagealert()
                                    x.damage(4,15,'player',['damageduration',10])
                            if game.playertoofar >= 10:
                                for x in alltiles:
                                    if x.coords[0] == 1:
                                        x.damage(4,15,'player')
                                        x.state = 'broken'

                                print('too far 1')
                                game.playertoofar = 0
                            #Or they get attacked for not moving
                        else:
                            for x in alltiles:
                                if x.coords[0] == player.currentpos[0]:   
                                    x.damagealert()
                                    x.damage(4,10,'player',['damageduration',10])
                            print('too far 2')
                                                
if __name__ == '__main__':
    print("This is enemy data. Run the battle system..")
   
   
    
    
