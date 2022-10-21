import pygame
import sys
import random 
import copy
from pygame.locals import *
from playerconstants import *
import BattleEnemyData
import time

#cursor = pygame.mixer.Sound('cursor.wav')
fps = pygame.time.Clock()
global what
what = 0
global alertcounter
alertcounter = 0
global specialblits
specialblits = []
global alltiles 
alltiles = []
#heal = spell('Heal', 25,None, 'Healing',10, None)
heal = spell('Heal','Restores any small wounds','or injuries you may have sustained.','Manipulating life energy is draining...','', 25,'Healing',20,None,'creation')
print(heal.mpcost,'heal')
display = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Battle System, GO!')
pygame.init()
# 8x4 grid is where battles are conducted.5
# However, Players and enemies can get up close and personal, or attack
# from a distance, as the area is not divided.
#we should make corners able to be stood on.
grassbg = pygame.image.load('battlesprites/grassstagebackground.png')
grassbgrect = grassbg.get_rect()


class Game:
    '''Handles variables.
       Battle routine set.
       Execute!
       Uh, Lan, I think it's against copyright law to do this.
       You're right, Megaman.
       
       (I do not claim ownership of these characters.
        Heihachi and Akuma are copyright SNK and Hideo Kojima.)
        hideous kojimaaaaaaa
        gorgeous freemannnnnn
    '''
    def __init__(self,name):
        self.check1 = False
        self.check2 = False
        self.check3 = False
        self.check4 = False
        self.debug = None
        self.SPcheck = False
        self.SPattacked = False
        self.Ghealthcheck = False
        self.TooClose = False
        self.TooCloseCheck = False
        self.aggressivecheck = False
        self.aggressive = False
        self.playerhitcheck = False
        self.players = None
        self.enemies = None
        self.background = None
        self.alertinfo = None
        self.playerlastloc = None
        self.approachcounter = 0
        self.retreatcounter = 0
        self.playerretreating = None
        self.playerapproaching = None
        self.playervulnerable = None
        self.perfectblock = 0
        self.playertooclose = 0
        self.playertoofar = 0
        self.usedmagic = False
        self.usedsword = False
        self.difficulty = 1
        #player is used to quickly refer to current player
        self.player = None
        self.specialblits = specialblits
        self.specialintro = None
        self.moocounter = 0
        self.moo = 0
        self.moo2 = 0
        self.movecheck = False
        self.countdown = None
        self.countdownattribute = None
        self.countdownvalue = None
        self.countdownchar = None
        
global game
game = Game('name')
allowinput = True
battlebox = pygame.image.load('battlebox.png')
battleboxrect = battlebox.get_rect()
battleboxrect.midbottom = (320,480) 
cursorcleaner = pygame.image.load('cursorcleaner.png')
class choicepointer:
    '''
    Helps the player know what choice they're making.
    '''
    def __init__(self,rect,image, currentloc=0):
        self.rect = pygame.rect.Rect(rect)
        self.image = pygame.image.load(image)
        self.currentloc = currentloc
pointer = choicepointer((battleboxrect.topleft[0],300,15,15),'pointer.png')
def speak(moo,char):
    draw(moo,None,None,True,char)
def talkmenu(moo,choices,char):
    draw(moo,1,choices,1,char,1)
def triplequestion(choices,char):
    draw([],1,choices,1,char,1)
def itemmenu():
    #inherits info from gamedata
    #make sure to assign items to gamedata
    itemfont = pygame.font.Font('FreeSans.ttf',15)
    rendereditems = []
    currentitem = 1
    currentpointer = 1
    for i in game.gamedata.items:
        itemname = itemfont.render(i.name, True, (200,200,200),(255,255,255))
        itemrect = itemname.get_rect()
        itemrect.center = [200,360]
        if currentitem != 1:
            if currentitem % 2 == 0:
                itemrect.x += 100
            if currentitem % 2 == 1:
                itemrect.y += (50*((0.5 * currentitem) - 1))
        currentitem += 1
        print(itemrect)
        itemset = [itemname, itemrect,i]
        rendereditems.append(itemset)
    done = False
    while not done:
        display.blit(battlebox, battleboxrect)
        for i in rendereditems:
            display.blit(i[0],i[1])
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    currentpointer -= 1
                if event.key == pygame.K_RIGHT:
                    currentpointer += 1
                if event.key == pygame.K_UP:
                    currentpointer -= 2
                if event.key == pygame.K_DOWN:
                    currentpointer += 2
                if currentpointer <= 0:
                    currentpointer = 1
                if currentpointer >= len(rendereditems):
                    currentpointer = len(rendereditems)
                if event.key == pygame.K_z:
                    chosenitem = rendereditems[(currentpointer-1)]
                    chosenitem = chosenitem[2]
                    print(chosenitem)
                    done = True
                
        
        pointer.rect.center = copy.copy(rendereditems[(currentpointer-1)][1].center)
        pointer.rect.x -= 30
        display.blit(pointer.image,pointer.rect)
        pygame.display.update()
    
        
    print('My name jeff')
    
    if chosenitem.name in game.presentableitems:
        return chosenitem
        
    else:
        game.players[0].item = chosenitem
        return None
    #first item slot: 360,200
    
def draw(moo, choice=False, choices=None, talk=None, speaker=None,talkmenu=None):
    pygame.display.flip()
    for i in game.players:
        if not i.emoting:
            i.imagereset()
    for i in game.enemies:
        if not i.emoting:
            i.imagereset()
    displayupdate(game.players,game.enemies, game.background)
    if talk and not talkmenu:
        pass
    else:
        print(battleboxrect.x, battleboxrect.y)
        display.blit(battlebox, battleboxrect)
    currentlist = 0
    newline = 0
    dist_from_end = 0
    #print(moo)
    moo = list(moo)
    moo.append('\n')
    maxlist = (len(moo) - 1)
    if talk:
        textcolor = speaker.color
    else:
        textcolor = (0,0,0)
    mopen = False
    thinking = None
    for y in range(0,maxlist):
            font = pygame.font.Font('FreeSans.ttf',
                                    20)
            if talk:
                talkfont = pygame.font.Font('FreeSans.ttf',
                                    14)
            if moo == []:
                break
            z = moo[y]
            #print('current',z)
            #print('last',moo[y-1])
            
            #font.set_underline(1)
            #print('Font Linesize is :', font.get_linesize())
            if talk and not talkmenu:
                tso = talkfont.render(z,True, textcolor, (255,255,255))
            else:
                tso = font.render(z, True, textcolor, (255,255,255))
            tro = tso.get_rect()
            #print(tro.width)
            k = len(moo) -1
            # Let me explain;
            # the following code helps the text be displayed
            # without overlapping or clipping letters.
            # The copy functions track the location of the last letter
            # and assign the current ones location based on that previous letter.
            # Pygame only handles generation of entire sentences,
            # So... improvising
            # Isn't programming just improvisation?
            # Isn't LIFE just improvising?
            # i hoped you enjoyed the rarity that is me commenting on my code
            if moo[y-1] == moo[k]  or moo[y-1] == '\\':
                #print('yes')
                if talk and not talkmenu:
                    if speaker.isplayer:
                        tro.center = (speaker.rect.topright[0] + ((y- dist_from_end)*12)
                                      , speaker.rect.topright[1] + (10*newline) - 10)
                    if speaker.isenemy:
                        tro.center = (speaker.rect.topleft[0] + ((y- dist_from_end)*12 - 125)
                                    ,speaker.rect.topright[1] + (10*newline) - 30)
                else:
                    tro.center = (battleboxrect.topleft[0] + ((y- dist_from_end)*12)  + 15 ,
                              battleboxrect.topleft[1] + (20*newline) + 15)
                #tro.x = 97
                #print(moo[y], tro.midleft[0])
                #print(tro.center)
                lastletter = copy.copy(tro)
            else:
                tro.left = lastletter.right 
                tro.top = lastletter.top
                lastletter = copy.copy(tro)
##            if newline >= 1:
##                tro.centerx = 58 + ((y - dist_from_end)* 12) + 11
            
            if z == '\\':
                dist_from_end = y + 1
                newline += 1
                continue
            if z == '@':
                if moo[y+1] == '@':
                    moo[y+1] = ' '
                    time.sleep(0.5)
                    continue
            if z == '(':
                thinking = True
            if z == ')':
                thinking = False

            #if newline >= 1:
            tro.centery += (10*newline)
            if talk and not talkmenu:
                
                
                
                #thinking?
                if z != ' ' and z != ')':
                    if not mopen and not thinking:
                        speaker.image.scroll(-165,0)
                        mopen = True
                if z == ' ' or z == '.' or z == '!' or z == '?':
                    if not speaker.emoting:
                        speaker.image = speaker.imagedefault.copy()
                    else:
                        speaker.emote(speaker.emoting)
                    mopen = False
                chardraw(speaker)
##            if newline >= 2:
##                tro.centery += 20
##            if newline == 3:
##                tro.centery += 20
            #print(tro)
            display.blit(tso,tro)
            #if z != ' ':
            #    cursor.play()
                
            pygame.display.update()
            currentlist += 1
            if z == '.' or z == '?' or z == '!':
                time.sleep(0.15)
            if z == ',':
                time.sleep(0.1)
            else:
                time.sleep(0.03)
            
            fps.tick(60)
            for event in pygame.event.get():
                pygame.event.pump()
    choicelist = []
    if choice:
        #Change this for each enemy later.
        if not talkmenu:
            alert = font.render(game.alertinfo,True,(127,0,0),(255,255,255))
            alertrect = alert.get_rect()
            alertrect.center = copy.copy(battleboxrect.center)
            display.blit(alert,alertrect)
        font = pygame.font.Font('FreeSans.ttf',
                                    20)
        q1 = font.render(choices[0], True, (0,0,0), (255,255,255))
        qro1 = q1.get_rect()
        if talkmenu:
            qro1.center = copy.copy(battleboxrect.center)
            qro1.y -= 30
        else:
            qro1.center = (battleboxrect.topleft[0] + 70, battleboxrect.topleft[1] + 80)
            qro1.bottom = 476
        display.blit(q1, qro1)
        choicelist.append(qro1)
        if len(choices) >= 2:
            
            q2 = font.render(choices[1], True, (0,0,0), (255,255,255))
            qro2 = q2.get_rect()
            if talkmenu:
                qro2.center = battleboxrect.center
                qro2.y += 0 # for reference
            else:
                qro2.center = (qro1.right + 100, qro1.center[1])
                qro2.bottom = 476
            display.blit(q2,qro2)
            choicelist.append(qro2)
        if len(choices) >= 3:
            q3 = font.render(choices[2], True, (0,0,0), (255,255,255))
            qro3 = q3.get_rect()
            if talkmenu:
                qro3.center = battleboxrect.center
                qro3.y += 30
            else:
                qro3.center = (qro2.right + 100, qro2.center[1])
                qro3.bottom = 476
            display.blit(q3,qro3)
            choicelist.append(qro3)
        pygame.display.update()
        rightcheck = None
        leftcheck = None
        pointer.currentloc = 0
        answergiven = False
        #Efficient or lazy?
        if talkmenu:
            minus, plus = pygame.K_DOWN, pygame.K_UP
        else:
            minus, plus = pygame.K_RIGHT, pygame.K_LEFT
        for event in pygame.event.get():
            pygame.event.pump()
        for event in pygame.event.get():
            print(event)
        while not answergiven:
            for event in pygame.event.get():
##                if event.type == pygame.KEYDOWN:
##                    if event.key == pygame.K_RIGHT:
##                        rightcheck = 1
##                    if event.key == pygame.K_LEFT:
##                        leftcheck = 1
##                    if event.key == pygame.K_z:
##                        zcheck = 1
                if event.type == pygame.KEYUP:
                    
                    if event.key == minus:
                        pointer.currentloc += 1
                        if pointer.currentloc >= len(choicelist):
                            pointer.currentloc = (len(choicelist)-1)
                    if event.key == plus:
                        pointer.currentloc -= 1
                        if pointer.currentloc <= -1:
                            pointer.currentloc = 0
                    if event.key == pygame.K_z:
                        global chosenoption
                        chosenoption = choices[pointer.currentloc]
                        print(chosenoption)
                        
                        gaveananswer = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event)
                        
                        
            try:
                if pointer.currentloc != lastcurrentloc:
                    display.blit(cursorcleaner, lastcursor)
            except UnboundLocalError:
                pass
            try:
                if gaveananswer == True:
                    print(chosenoption + 'was chosen')
                    answergiven = True
                    chosenoption = copy.copy(pointer.currentloc) + 1
                    # my indexes start at 1
                    # That may make me "not a real programmer"
                    # but hey
                    # at least I'm making something...
                    print(chosenoption,'chosen')
                    pointer.currentloc = 0
                    return chosenoption
            except UnboundLocalError:
                pass  
            pointer.rect.midright = (choicelist[pointer.currentloc].midleft)
            #pointer.rect.x -= 30                   
                                              
            lastcursor = copy.copy(pointer.rect)
            lastcurrentloc = copy.copy(pointer.currentloc)
            
                
            display.blit(pointer.image, pointer.rect)
            pygame.display.update()
    if not choice:
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    done = True
    for event in pygame.event.get():
        pygame.event.pump()
    display.blit(battlebox, battleboxrect)
    displayupdate(game.players,game.enemies, game.background)
    
#allows usage of draw in battleenemydata module easily    
BattleEnemyData.draw = draw      
    
class battletile:
    def __init__(self, coords,tile,midtile):
        self.coords = coords # like [1,1], [2.3], etc. Not [100, 200].
        self.rect = pygame.Rect(self.coords[0] *60 + 20, (self.coords[1] * 60)+ 105 , 60,60)
        #Special Variables for decorative tiles.
        self.dummy = False
        self.spchanged = False
        if self.coords[1] == 1:
            self.rect.top += 27
        elif self.coords[1] == 2:
            self.rect.top += 18
        elif self.coords[1] == 3:
            self.rect.top += 9# self.coords[0] causes an effect
            #self.rect.top += 9
##            if self.coords[1] == 1:
##                self.rect.top += 18
##            else:
##                self.rect.top += 9
        #print(self.rect.y)
        self.tile = tile
        self.state = 'normal'
        self.usable = True
        self.occupant = None
        self.playerisonit = None
        self.animinfo = None
        self.alertcounter = 0
        self.damageonframe = None
        self.damageamount = None
        self.damageelapsed = 0
        self.damageduration = 0
        if self.coords[1] < 4:
            self.defaultimage = midtile
        else:
            self.defaultimage = tile
        if self.coords[1] == 4:
            print(self.rect.y, 'Distance from top')
        
        # add more later...
    def tilechange(self):
        """
        Sets tiles to their proper image and usability if their state
        has been changed.
        """
        if self.spchanged != True:
          
            if self.state == 'normal' and type(self.tile) != type([]):
                self.image = pygame.image.load(self.defaultimage)
                self.usable = True
            if self.state == 'broken':
                if game.current_area == 'gray area':
                    x = 'grayareatilesbroken.png'
                else:
                    x = 'brokentile.png'
                self.image = pygame.image.load(x)
                self.usable = False
            if self.state == 'poison':
                self.image = pygame.image.load('poisontile.png')
                self.usable = True
            if self.state == 'damagealert':
                self.image = pygame.image.load(self.defaultimage)
                alertimage = copy.copy(self.image).convert_alpha()
                alertimage.fill((255,255,0,160), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = alertimage
                self.usable = True
            if self.state == 'damage':
                self.image = pygame.image.load(self.defaultimage)
                alertimage = copy.copy(self.image).convert_alpha()
                alertimage.fill((127,0,0,160), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = alertimage
                self.usable = True
            if self.state == 'Nil':
                self.dummy = True
                self.image = pygame.image.load(self.defaultimage)
                self.image.set_alpha(255)
                self.usable = False
            if type(self.tile) == type([]):
                #Loads a custom image if original image is a list.
                self.image = pygame.image.load(self.tile[0])
                self.usable = False
                self.spchanged = True
    def damagealert(self):
        #Make sure it doesn't cancel animations.
        if self.state != 'animation' and self.state != 'broken':
            self.state = 'damagealert'
    def damageflash(self):
        if self.state != 'animation' and self.state != 'broken':
            self.state = 'damage'
            self.alertcounter = 0
    def damage(self,amount, frame, damages,*args):#staggeronblock=None,damageduration=0, pierceinvis=0):
        '''
        Function for causing a tile to damage its occupants.
        Arguments are staggeronblock, damageduration, pierceinvis, stagger, etc...
        (More may be added.)
        Staggeronblock determines who will stagger if the attack is blocked (its weird, i know)
        Damageduration determines the amount of time the attack will last
        Pierceinvis determines if the attack ignores invincibility
        Stagger determines if the attack will knock the target back or cancel an attack
        Handles damage and stuff, basically.
        Actual damage is handled in updatebattlearea
        '''
    
        
        if self.state != 'broken':
            self.damagealert()
            self.damageonframe = frame
            self.damageamount = amount
            self.damages = damages
            self.staggeronblock = None
            #duration defaults to 1 frame
            self.damageduration = 1
            self.pierceinvis = None
            self.stagger = None
            self.hitstun = None
            for i in args:
                x = i[0]
                y = i[1]
                if x == 'staggeronblock':
                    self.staggeronblock = y
                if x == 'damageduration':
                    self.damageduration = y
                if x == 'pierceinvis':
                    self.pierceinvis = y
                if x == 'stagger':
                    #print('stagger assigned')
                    self.stagger = y
                if x == 'hitstun':
                    self.hitstun = y
                    
                
            
def Make_Tiles(place):
    print('place',place)
    if place == 'gray area':
        q1 = ['grayareaupperedge.png']
        q2 = ['grayareaedge.png']
        q3 = ['grayareaupperedge2.png']
        q4 = ['grayareaedge2.png']
        ab = 'grayareatiles.png'
        ac = 'grayareamidtiles.png'
        game.background == (0,0,0)
    if place == 'grass stage':
        q1 = ['grassstageupperedge.png']
        q2 = ['grassstageedge.png']
        q3 = ['grassstageupperedge2.png']
        q4 = ['grassstageedge2.png']
        ab = 'grassstagetiles.png'
        ac = 'grassstagemidtiles.png'
        game.background == (220,220,247)
        
        
    #else:
    #    raise TypeError('I\'m disappointed in you, Colonel. HUAAAAAAAAAAAHHH!!!')
    x = 0
    y = 0
    #Tiles with nil are blank spaces.
    #States in brackets are actually images, as you can tell.
    a = battletile([1,1],q1,ac)
    b = battletile([1,2],ab,ac)
    c = battletile([1,3],ab,ac)
    d = battletile([1,4],q2,ac)
    #print(d.rect.bottomleft)
    e = battletile([2,1],ab,ac)
    f = battletile([2,2],ab,ac)
    g = battletile([2,3],ab,ac)
    h = battletile([2,4],ab,ac)
    i = battletile([3,1],ab,ac)
    j = battletile([3,2],ab,ac)
    k = battletile([3,3],ab,ac)
    l = battletile([3,4],ab,ac)
    m = battletile([4,1],ab,ac)
    n = battletile([4,2],ab,ac)
    o = battletile([4,3],ab,ac)
    p = battletile([4,4],ab,ac)
    q = battletile([5,1],ab,ac)
    r = battletile([5,2],ab,ac)
    s = battletile([5,3],ab,ac)
    t = battletile([5,4],ab,ac)
    u = battletile([6,1],ab,ac)
    v = battletile([6,2],ab,ac)
    w = battletile([6,3],ab,ac)
    x = battletile([6,4],ab,ac)
    y = battletile([7,1],ab,ac)
    z = battletile([7,2],ab,ac)
    a1 = battletile([7,3],ab,ac)
    a2 = battletile([7,4],ab,ac)
    a3 = battletile([8,1],q3,ac)
    a4 = battletile([8,2],ab,ac)
    a5 = battletile([8,3],ab,ac)
    a6 = battletile([8,4],q4,ac)
    global alltiles
    alltiles = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a1,a2,a3,a4,a5,a6]
    return alltiles
def updatebattlearea():
    global alertcounter
    for x in alltiles:
            if x.state == 'damage':
                x.alertcounter += 1
                if x.alertcounter >= 5:
                    x.state = 'normal'
                    x.alertcounter = 0
            if x.state == 'damagealert' or (x.state == 'damage' and x.damageduration != 0):
                x.alertcounter += 1
                if x.damageonframe:
                    
                    #print(x.staggeronblock)
                    #print(x.alertcounter,x.damageonframe)
                    #Checking for x.damageelapsed helps duration attacks play out.
                    if x.alertcounter == x.damageonframe or x.damageelapsed >= 1:
                        x.state = 'damage'
                        x.alertcounter = 0
                        if x.occupied:
                            if x.occupant.isplayer:
                                if not (x.occupant.invincible and not x.pierceinvis) and (x.damages == 'player' or x.damages == 'all'):
                                    x.occupant.HitsTaken += 1
                                    x.occupant.invincible = 30
                                    if x.occupant.blocking:
                                        print('is blocking')
                                        print('stagger?',x.staggeronblock)
                                        if x.occupant.blockSP:
                                            #Can\'t regular attack, block perfectly and moderately increase SPmeter
                                            x.occupant.SPmeter += 20
                                            if game.perfectblock:
                                                print('perfect special block')
                                                x.occupant.SPmeter += 10
                                            x.occupant.burstready = True
                                            x.occupant.HitsTaken -= 1
                                        
                                        if x.staggeronblock:
                                            #breaks the attack, receiving no damage and staggering
                                            x.staggeronblock.stunned = 1
                                            x.staggeronblock.stunsp = 1
                                            x.occupant.HitsTaken -= 1
                                        
                                            
                                        elif game.perfectblock and not x.occupant.blockSP:
                                            print("Perfect block")
                                            x.occupant.SPmeter += 15
                                            #Why restructure the damage check sys
                                            #So that PerfectBlocking is checked for first
                                            #When you can subtract a hit if perfectblock is triggered?
                                            #Work smart, not hard
                                            #Or lazy, rather...
                                            x.occupant.HitsTaken -= 1
                                            x.occupant.Chealth -= 0
                                        else:
                                            if not x.occupant.blockSP:
                                                x.occupant.Chealth -= 1
                                    if not x.occupant.blocking:
                                        print(x.damageamount,'attack damage')
                                        
                                        damage = x.damageamount*(1-(0.05*x.occupant.defense))
                                        damage = int(damage)
                                        print(damage,'damage received',x.occupant.defense)
                                        x.occupant.Chealth -= damage
                                
                                    if x.occupant.quickcharging:
                                            x.occupant.Cmp *= 0.5
                                            x.occupant.Cmp = int(x.occupant.Cmp)
                                    #print(x.stagger)
                                    if x.stagger:
                                        if not x.occupant.blocking:
                                            x.occupant.stagger()
                                            if x.occupant.isplayer:
                                                x.occupant.stunned = 10
                                            else:
                                                x.occupant.stunned = 30
                                
                            elif x.occupant.isenemy and (x.damages == 'enemy' or x.damages == 'all'):
                                print(x.occupant.guard,'Occupant guarding?')
                                
                                if x.occupant.guard != True and not x.occupant.invincible:
                                    if game.debug:
                                        print(x.damageamount,'damage')
                                    if x.occupant.stunsp:
                                        x.damageamount *= 1.5
                                        x.damageamount = int(x.damageamount)
                                    if x.occupant.guard == False:
                                        x.occupant.Chealth -= x.damageamount
                                    if game.players[0].mode == 'Emotion':
                                        game.players[0].SPmeter += 10
                                    if x.hitstun:
                                        x.occupant.hitstun = copy.copy(x.hitstun)
                                    if x.stagger:
                                        x.occupant.stagger()
                                    print('damage enemy')
                                print('damage4')
                                
##                                if (not x.occupant.guard and x.occupant.isenemy) or (not x.occupant.invincible and x.occupant.isplayer):                                    
##                                    #guard means enemy is invincible for some reason
##                                    #weird glitch occurs when enemy is staggered and is in own attack
##                                    x.occupant.Chealth -= x.damageamount
##                                    
                                    
                        x.damageelapsed += 1
                        if x.damageelapsed >= x.damageduration:
                            x.damageonframe = None
                            x.damageamount = None
                            x.damageelapsed = 0
                            x.damageduration = 0
                        
                if x.alertcounter == 30:
                    x.state = 'normal'
                    x.alertcounter = 0
            if x.state == 'animation':
                x.image = pygame.image.load(x.animinfo['image'])
                x.image.scroll(x.animinfo['width']*x.animinfo['elapsedframes']-1)
                
                x.animinfo['elapsedframes']+= 1
                if x.animinfo['elapsedframes'] >= x.animinfo['frames']:
                    x.state = 'normal'
                    x.animinfo = None
                
                
    for x in alltiles:
        if x.dummy != True:
            x.tilechange()
            display.blit(x.image, x.rect)
#Make_Tiles()
def getlocation(self):
    for x in alltiles:
            if self.currentpos == x.coords and x.usable == True:
                self.rect.x = x.rect.centerx-25
                self.rect.y = x.rect.centery-65
            elif self.currentpos == x.coords and x.state == 'broken' and self.airshoes == True:
                return (x.rect.centerx -25, x.rect.centery - 65)

def specialdraw(pic, left,top):
    #Make something special for the background.
    image = pygame.image.load(pic)
    imagerect = image.get_rect()
    imagerect.left, imagerect.top = left, top
    moo = []
    moo.append(image)
    moo.append(imagerect)
    game.specialblits.append(moo)
    return image, imagerect
def choice():
    draw('Did this work?')
    time.sleep(3)
##    while True:
##        
##        display.blit(battlebox, battleboxrect)
##        pygame.display.update()
        
def eventcheck():
    global game
    weirdrects = None
    if game.scene == 'First Battle':
        dnyu = game.enemies[0]
        fredrick = game.players[0]
        if dnyu.Chealth >= 999 and game.check1 == False:
            
            game.alertinfo = 'An enemy?'
            draw('My first enemy! Some human guy! I\'m excited!',1,['Check','Talk','Item'])
            if chosenoption == 2:
                talkmenu('What is that thing and why does it want to hurt me?',['You think you can defeat me?', 'Why are you attacking me?'],fredrick)
                if chosenoption == 1:
                    speak('Hee hee hee!',dnyu)
                    speak('I don\'t know!',dnyu)
                    speak("But I want to find out!",dnyu)
                if chosenoption == 2:
                    speak('I... I don\'t know.',dnyu)
                    speak('I thought I was supposed to fight you?',dnyu)
                    draw("The creature is reevaluating its priorities...")
                    draw("Its attack drops!")
                game.check1 = True
        if dnyu.Chealth < 500 and game.check2 == False:
            game.alertinfo = 'The creature is rethinking fighting random people.'

    if game.scene == 'First Battle (Starring Gray Cloak)':
        fredrick = game.players[0]
    for i in game.players:
        if i.rect.width != i.defaultwidth or i.rect.height != i.defaultheight:
            #print('weird rect found')
            i.newwidth, i.newheight = copy.copy(i.rect.width),copy.copy(i.rect.height)
            i.rect.width , i.rect.height = copy.copy(i.defaultwidth),copy.copy(i.defaultheight)
            weirdrects = True
    for i in game.enemies:
        i.talkmode = True
    if game.scene == 'First Battle (Starring Gray Cloak)':
        if game.TooClose and game.TooCloseCheck == False:
            speak('Well punch my mother in the neck.',ghostface)
            #speak('Nice try, buddy.', ghostface)
            game.TooCloseCheck = True
        if game.player.Chealth <= 50 and game.Ghealthcheck == False:
            speak('Are you doing alright?',ghostface)
            speak('No.',fredrick)
            speak('Yeah, uh...',ghostface)
            speak('(He\'s gonna need some help.)',ghostface)
            speak('Here.',ghostface)
            game.player.cattack = heal
            speak('I gave you some healing magic.',ghostface)
            speak('Heal yourself with C.',ghostface)
            speak('What\'s "C"?',fredrick)
            speak('Oh, uh, nothing...',ghostface)
            game.Ghealthcheck = True
            
        if game.player.HitsTaken == 1 and game.playerhitcheck == False:

            speak('OWWW!',fredrick)
            #if gamedata.playerpreference == 'logic':
            speak('What were you expecting?\\Some vague awareness that you are now hurt?', ghostface)
            
            
##            speak('What was that?\\Are you trying to kill me?',fredrick)
##            speak('Uh, yeah.',ghostface)
##            speak('I\'d guess your enemies will do the same.',ghostface)
##            speak('My recommendation is that \\you should probably get used to it.',ghostface)
            #if game.gamedata.preference == 'logic':
            #    speak('(Jerk...)', fredrick)
            #if game.gamedata.preference == 'emotion':
            #    speak('(I feel personally attacked.)', fredrick)
            #if game.gamedata.preference == 'will':
            #    speak('(I guess he\'s right.)',fredrick)
            game.playerhitcheck = True
        if game.aggressivecheck == False and game.aggressive == True:
            #speak('Wait for an opening before making an attack.',ghostface)
            #speak('"The second player to make a mistake wins."',ghostface)
            #speak('But I always want to be first.',fredrick)
            #speak('First is the worst, man.',ghostface)
##            if game.debug:
##                return
##            speak('You\'re being too aggressive.',ghostface)
##            speak('You\'re supposed to hit me when my guard is down.',ghostface)
##            speak('Not the other way around.',ghostface)
##            if game.gamedata.preference == 'logic':
##                speak('But aren\'t you supposed to hit as much as possible?',fredrick)
##            if game.gamedata.preference == 'emotion':
##                speak('(But that\'s difficult...)',fredrick)
##            if game.gamedata.preference == 'will':
##                speak('So it\'s hit, but don\'t get hit?',fredrick)
##                speak('Of course. Why would you want to get hit?',ghostface)
            game.aggressivecheck = True
        
            
            game.playerhitcheck = True
        if game.SPattacked and game.SPcheck == False:
            fredrick.emote('displeased')
            speak('Are you serious?',fredrick)
            speak('Well I warned you, didn\'t I?',ghostface)
            if game.gamedata.preference == 'emotion':
                speak('No, you did not.',fredrick)
                speak('Well, I\'m sure you got the point, anyway.',ghostface)
            else:
                speak('But I didn\'t know it\\ would be THAT violent.',fredrick)
                speak('That is the point...',ghostface)
                      
##            speak('Heh, wasn\'t that a fun surprise.',ghostface)
##            ghostface.emote('condescension')
##            speak('Seems like you had some fun with it, huh?',ghostface)
##            fredrick.emote('hard squint')
##            speak('What WAS that?',fredrick)
##            speak('People tend to do interesting things when\\they\'re feeling cornered.',ghostface)
##            speak('I\'m sure you know this,\\but always keep on your guard...',ghostface)
##            speak('(You still didn\'t tell me what that was.)',fredrick)
            game.SPcheck = True

        #displayupdate(game.players,gameenemies)
        if ghostface.Chealth == 1500 and game.check1 == True:
            game.specialintro = True
        if ghostface.Chealth <= 1499 and game.check1 == True and game.specialintro == True:
            if game.debug:
                game.specialintro = False
                return
            game.moocounter += 1
            if game.moocounter == 15:
                speak('Good, you can follow basic commands.',ghostface)
                speak("Now then...",ghostface)
                #speak('Now, let\'s get in to the good stuff.',ghostface)
                game.specialintro = False
            
        if ghostface.Chealth >= 1001 and game.check1 == False:
            
            game.alertinfo = 'Show your skill (or lack thereof).'
            draw('This kid looks like he just woke up.',1,['Check','Talk','Item'])
            if chosenoption == 3:
                game.debug = True
            if chosenoption == 1:
                draw('The Man in the Gray Cloak@@\\A mysterious, cloaked, snarky individual.\\Begrudgingly teaches you things.\\Sword-oriented and Magic-oriented (showoff).')
                time.sleep(1)
                return
            if chosenoption == 2:
                
                findpreference()
                speak('Yes, this is battle. Exciting, right?',ghostface)
                speak('There was an important saying\\about battle that was\\passed down to me.',ghostface)
                speak('I hope it\'ll help you out...',ghostface)
##                if game.gamedata.preference == 'logic':
##                    speak('(Let\'s hear it, then...)',fredrick)
##                if game.gamedata.preference == 'emotion':
##                    speak('(I wonder what he\'s going to say?)',fredrick)
##                if game.gamedata.preference == 'will':
##                    speak('("Fighting knowledge?", huh?)',fredrick)
                
                findpreference()
                speak('"Z,S,C, Arrow keys!"', ghostface)
                #if game.gamedata.preference == 'will':
                speak('(Arrow keys? Sounds moving...)',fredrick)
                #if game.gamedata.preference == 'emotion':
                #    speak('What?',fredrick)
                speak('Do you feel fighty now?',ghostface)
                
                speak('Anyway, for your first lesson...',ghostface)
                speak('Just try to hit me a few times, okay?',ghostface)
                if game.gamedata.preference == 'emotion':
                    speak('But won\'t that hurt?', fredrick)
                    speak('It should.',ghostface)
                    speak("Not really, now that I think about it.",ghostface)
                    speak("You don\'t totally know how to fight yet...",ghostface)
                    #speak('That\'s the price I pay for your education.',ghostface)
                    #speak('Have you ever even really hit anything before?',ghostface)
                    
                elif game.gamedata.preference == 'logic':
                    speak('Whatever you say...',fredrick)
                

                #elif preference == 'will':
                
            
                # Logic, emotion, will
##                talkmenu('Who IS this guy?',['Who are you?', 'What\'s with the cloak?','What\'s going on?'],fredrick) #best dialogue choice
##                if chosenoption == 'Who are you?':
##                    game.gamedata.willpoints += 1
##                    speak('Uh, who are you, exactly?',fredrick)
##                    speak('Oh, just your average person of unfathomable power\\ wearing the usual mysterious cloak.',ghostface)
##                    ghostface.emote('morbid excitement')
##                    speak('Nothing special.', ghostface)
##                    speak('(???)',fredrick)
##                if chosenoption == 'What\'s with the cloak?':
##                    game.gamedata.emotionpoints += 1
##                    speak('What\'s that weird thing you\'re wearing?',fredrick)
##                    speak('Oh, this? It\'s a magical artifact with limitless power.',ghostface)
##                    speak('It gives me the ability to be condescending with people\\ who ask dumb questions.',ghostface)
##                    fredrick.emote('displeased')
##                    speak('(Is this guy serious?)',fredrick)
##                    speak('What\'s that look on your face?',ghostface)
##                    ghostface.emote('morbid excitement')
##                    speak('Do you honestly think I would LIE to you?',ghostface)
##                    speak('(Yes, actually...)',fredrick)
##                if chosenoption == 'What\'s going on?':
##                    game.gamedata.logicpoints += 1
##                    speak('Um, what\'s happening right now?',fredrick)
##                    speak('This is a battle. We\'re fighting.',ghostface)
##                    ghostface.emote('morbid excitement')
##                    speak('Any other tough questions?',ghostface)
##                    fredrick.emote('concern')
##                    speak('Well, it doesn\'t feel like we\'re fighting.',fredrick)
##                    #ghostface.emote('morbid excitement')
##                    speak('Oh, just give it a minute.',ghostface)
                    
                   
                
            if chosenoption == 'Check':
                print
                ('You win')
            if chosenoption == 3:
                chosenitem = itemmenu()
                if chosenitem != None:
                    if chosenitem.name in game.presentableitems:
                        if game.scene == 'First Battle (Starring Gray Cloak)':
                            if chosenitem.name == 'Stick':
                                speak('Hm. Wood. Interesting.',ghostface)
                                speak('And why did you feel like you should show me that?',ghostface)
                                speak('I don\'t know. I just felt like something told me to.',fredrick)
                                speak('You know, the other one was like this, too.',ghostface)
                            if chosenitem.name == 'First Aid Kit':
                                game.debug == True
                if not game.debug:
                     return
##                    speak('???',ghostface)
##                    speak('??? ??? ???',ghostface)
##                    speak('??????????????????\\??????????????????\\??????????????????',ghostface)
                #draw('Perhaps you should talk.',1,['Talk'])
    ##        if chosenoption == 'Talk':
    ##            speak('You\'re seriously trying to kill me?',fredrick)
    ##            speak('Yes. I seriously am.',ghostface)
                  #  I tried to make a dead serious joke, but the
                  #  only thing that was dead was the dialogue.
    ##            speak('You better get focused, otherwise "serious" won\'t \\be the kind of dead you are..', ghostface)
    ##            speak('So, if you end up in a battle against someone,\\ what should be your first priority?',ghostface)
    ##            #NO WAY!?! F-Bomb says a BAD WORD???
                  #I\'m telling MOM! You\'re getting kicked out of my birthday party!!!
                  #speak('Beating the crap out of them.',fredrick)
    ##            speak('No, that\'s priority number 2.\\ Number 1 is not getting hit.',ghostface)
    ##            speak('I\'m going to try to hit you.\\ Don\'t get hit and you\'ll be fine.',ghostface)
                # this stuff seemed funnier in my head
                
                
    ##            speak('', fredrick)
    ##            speak('Heh, you\'ll figure it out.', ghostface)
            if chosenoption == 'Pass':
                pass
            game.check1 = True
        elif ghostface.Chealth >= 501 and ghostface.Chealth <= 1000 and game.check2 == False:
            # if player is doing okay, took no damage, or took a lot, opponent reacts accordingly
            #if fredrick.Chealth >
            #Totally winged this part. Hope its accurate.
            if game.player.HitsTaken <= 5:
                thoughts = 'He is doing better than he should be...'
                snark = 'Seems you\'re doing well...'
                game.difficulty += 1
            elif game.player.HitsTaken >= 5 and game.player.HitsTaken <= 10 :
                thoughts = 'As expected...'
                snark = 'Is this your first time?'
            elif game.player.HitsTaken >= 11:
                thoughts = 'The other one was better at this.'
                snark = 'You suck a little bit...'
                game.difficulty -= 1
            game.alertinfo = snark
            draw(thoughts, 1, ['Check','Talk',])
            if chosenoption == 1:
                draw('He uses light and dark magic (the rarest types).\\Usually, he uses a sword...?')
                
            if chosenoption == 2:
                
                if game.difficulty == 2:
                    findpreference()
                    speak('You aren\'t leaving me much to teach you.',ghostface)
                    #speak('AHAHAHA! VIOLENCE!',fredrick)
                    #speak('Maybe you\'ll actually make it.',ghostface)
##                    if game.gamedata.preference == 'will':
##                        speak('Well, apparently it IS my job...',fredrick)
##                        speak('From a fighting standpoint,\\ you are the equivalent of a janitor.',ghostface)
##                        speak('However, you need to be at \\least management \\if you want to survive..',ghostface)
##                        speak('(Uh... okay.)',fredrick)
##                    if game.gamedata.preference == 'emotion':
##                        speak('I pride myself on having basic learning ability.',fredrick)
##                        speak('Don\'t give yourself a pat on the back just yet.',ghostface)
##                        speak('You still have more to learn...',ghostface)
##                    if game.gamedata.preference == 'logic':
##                        speak('I have to be strong.',fredrick)
##                        speak('Uh, yeah...',ghostface)
                        #speak('Good mindset, but you sound cliché.',ghostface)
                if game.difficulty == 1:
                    speak('Well, you\'re doing as well as I thought you would.',ghostface)
                    speak('And that is?',fredrick)
                    speak('Well...',ghostface)
                    speak('...',fredrick)
                    speak('Don\'t worry, you\'ll improve.',ghostface)
                    speak('(I really hope he does...)', ghostface)
##                    if game.gamedata.preference == 'logic':
##                        speak('Hey, I can only get better.',fredrick)
##                        speak('I can only hope.',ghostface)
##                    if game.gamedata.preference == 'will':
##                        speak('And that is?',fredrick)
##                        speak('Painfully average.',ghostface)
##                    if game.gamedata.preference == 'emotion':
##                        speak('In my defense, I\'ve never done this before.',fredrick)
##                        speak('I could tell.',ghostface)
                if game.difficulty == 0:
                    ghostface.emote('condescension')
                    speak('Wow, you are not doing so hot...', ghostface)
                    #speak('(Ehh.....)',fredrick)
                    ghostface.imagereset()
                    speak('(Maybe I should go easier on him.)',ghostface)
                #speak('Do you have any questions?',ghostface)
                #triplequestion('Do you have emotions or no.','Who are you really?','Ow this hurts.')
                
                speak('So, what should you do if you can\'t avoid an attack?',ghostface)
                
                speak('Put my hands in front of my face.',fredrick)
                speak('And what is that called..?',ghostface)
                speak('Cowering.',fredrick)
                speak('Is that based off of your prior experience?',ghostface)
                    #speak('Your grasp of basic knowledge is truly without rival...',ghostface)
                speak('Usually, if you can\'t avoid an attack, block it.',ghostface)
                speak('Use s to block.',ghostface)
                speak('Blocking certain attacks will leave\\ your opponent open for a counterattack.',ghostface)
                speak('As a wise man once said...',ghostface)
                speak('"If they can\'t stop ya, \\it\'s a lot easier to\\beat the CRAP outta them."',ghostface)
##                speak('Truly the wisdom of a sage.',ghostface)
##                
##                speak('What do you mean, "wise man?"', fredrick)
##                speak('A person who was to me what I am to you.', ghostface)
##                speak('A sarcastic pain in the neck?',fredrick)
##                speak('What? No.',ghostface)
##                speak('Well, actually that\'s dangerously close to the truth.',ghostface)
                #speak('So, blocking certain attacks\\ may cause their user to stagger.',ghostface)
                #speak('Basically, if you are stuck, try blocking.',ghostface)
                #speak('Now, let\'s get back down to business.',ghostface)
                
                
                    
##                fthoughts = 'What\'s that look on his face?'
##                # Black cloak, white cloak, grey cloak?
##                talkmenu(fthoughts,['Why areyou trying to kill me?','What am I supposed to do here?','Boy, you SURE seem like fun...'],fredrick)
##                if chosenoption == 'Why are you trying to kill me?':
####                    speak('Why?\\Because it\'s fun.',ghostface)
####    ##            speak('Ugh, so what\'s next, anyways?',fredrick)
####    ##            speak('Occasionally, your enemy may use a risky attack.',ghostface)
####    ##            speak('If you can block it, they\'ll be very vulnerable.',ghostface)
####    ##            speak('So I just block whatever move that you do?',fredrick)
####    ##            speak('Pretty much.',ghostface)
####                
##                    print('h')
##                if chosenoption == 'Why are you trying to kill me?':
##                    speak('Why are you trying to kill me?',fredrick)
##                    speak('The real question is why wouldn\'t i be trying to kill you?',ghostface)
##                    speak('The best way to learn something is to do it yourself.',ghostface)
##                    speak('So, this should teach you how to survive pretty fast.',ghostface)
##                    speak('How does that make any sense?',fredrick)
##                    speak('Don\'t knock it until you try it.',ghostface)
##                    speak('I AM trying it! It\'s terrible!', fredrick)
                game.check2 = True
        elif ghostface.Chealth >= 101 and ghostface.Chealth <= 500 and game.check3 == False:
            ghostface.emote('smirk')

            snark = 'An unusual smirk appears on the man\'s face...'
            if game.difficulty >= 2:
                x = 'He definitely has done this before...'
                #snark = 'Have you done this before?'
            elif game.difficulty == 1:
                x = 'He will improve with time. Maybe.'
                #snark = 'Yo yo yo you\re gonna double Mcdie yo'
            elif game.difficulty <= 0:
                ghostface.emote('concern')
                x = 'He should avoid violence whenever possible.'
                #snark = 'You may want to lower the difficulty...'
            
            game.alertinfo = snark
            
            draw(x,1,['Check','Talk'])
            if chosenoption == 1:
                draw('He doesn\'t seem to be using his usual attacks...')
            if chosenoption == 2:
                speak('Are we done yet?', fredrick)
                speak("Hmph, you\'re telling me...",ghostface)
                speak('You\'re almost finished.',ghostface)
                speak('When your opponent is in a pinch,\\they may use an exceedingly powerful move.',ghostface)
                speak('Usually, the attack\'s form is a\\reflection of its user\'s desires.',ghostface)
                #speak('You can\'t block these, you have to avoid them.',fredrick)
##                if game.gamedata.preference == 'logic':
##                    speak('Why do my enemies get \\something overpowered and I don\'t?',fredrick)
##                    speak('Oh, you have one.\\You just don\'t know how to use it yet.',ghostface)
##                    speak('How does someone not\\ know how to freak out?',fredrick)
##                    speak('I should be asking\\ you that question...',ghostface)
                speak('More often than not,\\blocking won\'t protect you.',ghostface)
                speak('However, this is usually your enemy\'s final attack.',ghostface)
##                if game.gamedata.preference == 'will':
##                    speak('So, it\'s both a good thing and\\ a bad thing when this happens?',fredrick)
##                    speak('Indeed.',ghostface)
##                if game.gamedata.preference == 'emotion':
                speak('Why\'d you bring that up?',fredrick)
                speak('Let\'s not spoil the surprise...',ghostface)
                 
                game.check3 = True
        elif ghostface.Chealth <= 100:
            speak('Yeah, I\'m beat. That\'s enough.',ghostface)
            ghostface.Chealth = 0
        
    elif game.scene == 'First Genmu Encounter':
        pass
    elif game.scene == 'WizDog Encounter':
        wizdog = game.enemies[0]
        fredrick = game.enemies[0]
        if not game.check1:
            game.check1 = True
            game.alertinfo = "This one is less persuadable."
            draw("There's another one?",1,['Check','Talk','Item'])
    elif game.scene == 'Magic Dog Encounter':
        magicdog = game.enemies[0]
        fredrick = game.players[0]
        if game.check0 != True:
            if game.debug:
                draw('During battle,\\you may have an opportunity to talk to your opponents.')
                draw('These opportunities appear if you fulfill\\varying requirements relevant to your opponents desires.')
                draw('Use check first to see any relevant\\information about your opposition.')
                draw('Then, Choose dialogue which you think will be\\persuasive or relevant to their personalities.')
                draw('If you are successful, something special may happen...')
            
            game.check0 = True
            
        if magicdog.Chealth == magicdog.Mhealth and game.check1 == False:
            game.alertinfo = "The dog is not firm in his resolve to fight."
            draw('What does this mutt want???',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('Charles@@\\A magical dog wearing a baseball cap and a bandana.\\Too kind to bargain, so keeps inventory instead.\\Magic oriented.')
            if chosenoption == 2:
                draw('A familiar voice begins speaking to Fredrick.')
                draw('This conversation will be pretty one-sided without this...')
                draw('Fredrick gains the ability to understand the dog.')
                talkmenu('Did he know we were coming?',['Why are you doing this?', 'What do you have against Genmu?'],fredrick)
                if chosenoption == 2:
                    speak('What is your problem???',fredrick)
                    speak('Bark bark bark bark bark bark bark\\bark bark bark bark bark\\ bark bark.',magicdog)
                    speak('(What was I expecting???)',fredrick)
                game.check1 = True
                if chosenoption == 1:
                    #rightchoice()!
                    speak('What did I even do to you?', fredrick)
                    #speak('Bark! BARKBARKBARK!',magicdog)
                    speak('Bark bark bark, bark... Bark?',magicdog)
                    speak('The dog is questioning its actions.',magicdog)
                    draw('The dog\'s will to fight wavers.')
                    draw("His attack drops...")
                    game.Mdogcheck1 = True
                game.check1 = True
                    
           
        if game.SPcheck == True and game.SPattacked == False:
            speak('Why does it know magic???',fredrick)
            speak('bark bark bark\\BARK BARK BARK\\BARK baBARK!!!',magicdog)
            speak('...',fredrick)
            game.SPattacked = True
        if (magicdog.Chealth < (magicdog.Mhealth*0.66) and magicdog.Chealth >= (magicdog.Mhealth*0.66)) and game.check2 == False:
            draw('If the dog cannot talk, how can it learn magic???',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('It seems Charles is of a more timid temperament.')
            if chosenoption == 2:
                talkmenu('...',['Why are you attacking me?','What\'s the big deal about his swords?'],fredrick)
                if chosenoption == 1:
                    pass
                    game.Mdogcheck2 = True
                    magicdog.Chealth = 0
                if chosenoption == 2:
                    pass
                game.check2 = True
        if (magicdog.Chealth < magicdog.Mhealth*0.33):
            if game.Mdogcheck1 and game.Mdogcheck2:
                draw('The dog is questioning its motives.')
                draw('Yes, attacking random people is weird...')

        if magicdog.SPevent :
            speak('Bark bark bark...', magicdog)
            #self.heal()
            magicdog.Chealth += 500
            magicdog.SPevent = False
            magicdog.strat = 'lightning'
    if game.scene == 'MagiNyu Battle':
        maginyu = game.enemies[0]
        fredrick = game.players[0]
        if maginyu.Chealth == maginyu.Mhealth and not game.check1:
            game.alertinfo = 'I wonder who taught her magic...'
            draw('She doesn\'t seem very happy...',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('A fluffy creature with an affinity for magic.\\She\'s young, and a bit bratty.\\Magic oriented.')
            if chosenoption == 2:
                speak('You meanies!',maginyu)
                speak('I\'ll show your jerk friend\\why magic rocks and swords... don\'t!',maginyu)
            game.check1 = True
        if maginyu.Chealth <= maginyu.Mhealth*0.75 and not game.check2:
    
            if game.usedmagic == False:
                game.alertinfo = "She\'s angry. Good job!"
                draw('Maginyu seems flustered.',1,['Check','Talk','Item'])
                if chosenoption == 1:
                    draw('Your opposition seems to have her disinterest in swords challenged.')
                if chosenoption == 2:
                    speak('Why? Why are you so mean to me?',maginyu)
                    speak('I hate swords! And you keep using them!',maginyu)
                    speak('I\'ve never been this mad before!',maginyu)
                    speak('Not even when they spilled juice on my magic book!',maginyu)
                    draw("Maginyu's focus has been affected.")
                    draw("Her magic power and defense decrease!")
                    #maginyu gets stronger
                    ##fight ends
                    #maginyu.Chealth = 0
                game.check2 = True
            else:
                game.alertinfo = "She has her usual smug look."
                draw('She is doing fine...',1,['Check','Talk','Item'])
                if chosenoption == 1:
                    draw('She has a little bit of magic knowledge.\\She usually has her nose in a book...')
                if chosenoption == 2:
                    speak('Heehee. I told you magic was cool.',maginyu)
                    #speak('I hate swords! And you keep using them!',maginyu)
                game.check2 = True
                
    if game.scene == 'SwordNyu Battle':
        swordnyu = game.enemies[0]
        fredrick = game.players[0]
        if swordnyu.Chealth == swordnyu.Mhealth and not game.check1:
            game.alertinfo = 'Using only magic will frustrate him...'
            draw('He seems intent on "training"?',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('A fluffy youth who dreams of heroism.\\Determined, but only to have fun.//Sword oriented.')
            if chosenoption == 2:
                speak('Yes! An opportunity for training!',swordnyu)
                speak('Prepare to taste my blade, fiend!',swordnyu)
            game.check1 = True
        if swordnyu.Chealth <= swordnyu.Mhealth*0.5 and not game.check2:
            if game.usedsword == False:
                game.alertinfo = "The thought of magic being useful scares him."
                draw('Swordnyu seems confused.',1,['Check','Talk','Item'])
                if chosenoption == 1:
                    draw('Your opposition now believes magic is not totally useless.')
                if chosenoption == 2:
                    speak('Ohhhh, I hate magic!',swordnyu)
                    speak('It\'s so cowardly and unfair!',swordnyu)
                game.check2 = True
            else:
                draw('He is starting to get frustrated...',1,['Check','Talk','Item'])
                if chosenoption == 2:
                    speak('You are a powerful fiend!',swordnyu)
                    speak('However, even though I want to stop,\\I won\'t!',swordnyu)
                    speak('Even though I am very hungry and tired,\\and want to play with my friends...',swordnyu)
                    speak('I will fight until I win!',swordnyu)
                game.check2 = True
                
                    
    if game.scene == 'Original Fredrick Encounter':
        ofredrick = game.enemies[0]
        fredrick = game.players[0]
        if ofredrick.Chealth == ofredrick.Mhealth and game.check1 == False:
            game.alertinfo = 'Show the proof of your worth.'
            draw('This guy really hates you.',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('??? \\Seriously hates Fredrick.\\An unstable energy is radiating from him.')
            if chosenoption == 2:
                speak('Don\'t try to talk to me.',ofredrick)
                draw("For some reason, the person's emotions\\ are resonating with Fredrick.")
                draw("Fredrick\'s health greatly increases!")
                fredrick.Chealth *= 1.5
                fredrick.Chealth = int(fredrick.Chealth)
                game.check1 = True
        if ofredrick.Chealth <= (ofredrick.Mhealth*0.5) and game.check2 == False:
            draw('The man\'s glare becomes somehow more hostile...',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw("Is he just a copy of you?")
            if chosenoption == 2:
                speak('I...!',ofredrick)
                speak('Grr!',ofredrick)
                speak('You scumbag!',ofredrick)
                speak('...',ofredrick)
                speak('Can\'t believe he was right...',ofredrick)
                game.check2 = True
        if ofredrick.Chealth <= (ofredrick.Mhealth * 0.3) and game.check3 == False:
            ofredrick.emote('turning')
            speak("U-uuugh...",ofredrick)
            speak('Everything\'s turning red...!',ofredrick)
            #speak("Y-you\'re making me..!",ofredrick)
            draw("The man is struggling to maintain control...")
            #speak('!',ofredrick)
            speak("NO! I don\'t want to--",ofredrick)
            speak('AAAAAAAAAGGGGHHHHH--',ofredrick)
            ofredrick.emote('desirous')
            draw("The man falls silent.")
            speak("...!",ofredrick)

            ofredrick.image = pygame.image.load('battlesprites/dfredrickbattlesprite.png')
            ofredrick.imagedefault = ofredrick.image.copy()
            game.check3 = True
        if ofredrick.Chealth <= (ofredrick.Mhealth * 0.1) and game.check4 == False:
            speak("K-KILL YOU...",ofredrick)
            speak("I.. WILL... BE... FREE...",ofredrick)
            draw("For a brief moment, the man looks utterly elated...")
            game.check4 = True
    if game.scene == 'Black Cloak Battle':
        bc = game.enemies[0]
        fredrick = game.players[0]
        if bc.Mhealth == bc.Chealth and game.check1 == False:
            draw('He even holds his sword\\the way the other one did....',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('Black Cloak.\\One of the three heroes, and the swordsman of the group.')
                draw('The only one who knows the greatest sword technique,\\ as a result of him creating it.')
            if chosenoption == 2:
                game.check1 = True
                speak("I hope you won\'t make me go easy on you.",bc)


        if game.SPcheck == True:
            draw('The man has prepared a powerful attack...')
            game.SPcheck = False
    if game.scene == 'FallenWarrior Battle':
        warrior = game.enemies[0]
        fredrick = game.players[0]
        if warrior.Chealth == warrior.Mhealth and game.check1 == False:
            draw('Fredrick feels concerned.',1,['Check','Talk','Item'])
            game.alertinfo = "This enemy is not persuadable."
            if chosenoption == 1:
                draw('Fallen Warrior\\Jovial dead guy.\\Is seriously powerful.\\Obviously sword oriented.')
            if chosenoption == 2:
                speak('Where are my clothes???',warrior)
                speak('This ALWAYS happens...',warrior)
                speak('Anyway, I feel like I lost some weight.',warrior)
                speak('You know, because I\'m ALL BONES.',warrior)
                talkmenu('That was bad.',['That pun was to die for.','You\'re not very "humerus".'],fredrick)
                if chosenoption == 1:
                    speak('Hehehe... I\'ve got more where that came from.',warrior)
                if chosenoption == 2:
                    speak('Yeah... Being dead ruined my social skills.',warrior)
                speak('You\'re one of us, right?',warrior)
                speak('That, of course,\\means our enemy is back.',warrior)
                speak('Which kinda negates my\\journey and subsequent death, but...',warrior)
                speak('Hey, I\'m dead.\\What can I do about it?',warrior)
                speak('On the other hand, you,\\who still clings to life...',warrior)
                speak('As the one who will finish the job,\\you will need great power.',warrior)
                #speak('"I am one of those who\\will ascertain your strength."',warrior)
                #speak('Ascertain...\\That\'s how you use that word, right???',warrior)
                speak('My job, specifically,\\is to fight you.',warrior)
                speak('Others may judge you in various ways,\\but not me.',warrior)
                speak('Violence really lets a person open up to you.',warrior)
                speak('Not that I\'m hiding anything.',warrior)
                speak('After all, you can probably see right through me.',warrior)
            
                
                game.check1 = True
            if chosenoption == 3:
                pass
                game.check1 = True
        if warrior.Chealth <= (warrior.Mhealth*0.66) and game.check2 == False:
            draw('I can see through his ribcage.',1,['Talk','Item'])
            if chosenoption == 1:
                speak('Heh heh, you\'re still alive! Sweet!',warrior)
                speak('You\'re doing better than the other guys...',warrior)#this line has no plot relevance
                speak('At this point,\\I hope you have met one of the previous warriors.',warrior)
                speak('They are three weirdos in pretty drab cloaks who,\\ for some reason, are super popular among the living...',warrior)
                speak('That one in the gray cloak is usually on top of things,\\but those other two, in the black and the white...',warrior)
                talkmenu('If that gray guy was "normal", then those two...',['Tell me about white cloak.','Who\'s black cloak?'],fredrick)
                if chosenoption == 1:
                    speak('She was a very decisive fellow.\\The only thing sharper than her tongue was her skill with magic...',warrior)
                    speak('She always wanted to do her own thing, too.',warrior)
                    speak('She is going to be a pain to track down;\\You won\'t find her unless she wants you to.',warrior)
                    
                if chosenoption == 2:
                    speak('Truly a legend with swords.. All swordsmen,\\from the amazing to the amazingly incompetent,\\hold him as the gold standard.',warrior)
                    speak('He seems to have gone into hiding...?',warrior)
                    speak('I doubt he\'s retired;\\he lived for and loved battle.',warrior)
                    speak('He\'s probably just gone undercover\\so he can fight people, free from fame\'s burden...',warrior)
                speak('...',warrior)
                speak('Somehow those three got together and\\finished the same journey you are beginning.',warrior)
                speak('They weren\'t able to end it permanently,\\but they were able to do it without the journey\'s downside.',warrior)
                speak('Yes, they cheated death. All of them.',warrior)
                speak('I\'d be jealous,\\but I\'m more busy being dead...',warrior)
                speak('I can\'t return to my rest\\until I have taught you enough, so...',warrior)
                speak('We should probably continue fighting.',warrior)
##                speak('As I said before, I undertook the same journey you did.',warrior)
##                speak('Ultimately, I gave my life so that I could finish it.',warrior)
##                speak('Every chosen before and after me has struggled with the same problem:',warrior)
##                speak('Is there a way for us to complete our journey without dying?',warrior)
##                speak('We have all tried everything we can, hoping and praying and bartering...',warrior)
##                speak('But, as my bones show, we have failed.',warrior)
##                speak('We have all turned our eyes and hopes to you...',warrior)
##                speak('If we can have at least one chosen saved, we will be able to rest.',warrior)
                
                #Gray cloak?
                    #He was the undisputed leader of the three.
                #No one ever really knew what he was thinking about.
                #He seemed very efficient and pragmatic, but...
                #...
                #
                
                game.check2 =True
                #who are you, why are you here?
                #(whya re you here?) We have been brought back for your journey.
        if warrior.Chealth <= (warrior.Mhealth*0.33) and game.check3 == False:
            draw('No bones about it, he is tough.',1,['Talk','Item'])
            if chosenoption == 1:
                speak('We, as people, are nothing more than the bonds we hold.',warrior)
                speak('The only way for us to truly exist\\is to be seen and heard by others.',warrior)
                speak('Which reminds me...',warrior)
                speak('That swordsman you put up with, Genmu...',warrior)
                speak('He takes after me for some reason.',warrior)
                speak('As a result,\\I can probably predict what problem he\'s dealing with...',warrior)
                speak('He can\'t deal with it on his own,\\so you\'ve gotta help him..',warrior)
                speak('Believe me, he will be eternally grateful to you for it.',warrior)
                speak('Now, figuring out the specifics of\\solving people\'s problems is your deal, but...',warrior)
                speak('I feel bad for that moron.',warrior)
                speak('After we finish fighting,\\I\'ll give you a map.',warrior)
                speak('It will lead you to something\\Genmu desperately needs.',warrior)
                speak('Find that sword-addled fool,\\and take him to where the map leads you.',warrior)
                speak('It will be lifechanging for both of you.',warrior)
                game.check3 = True
                
                
    elif game.scene == 'Light Battle':
        light = game.enemies[0]
        fredrick = game.enemies[0]
        if game.check1 == False:
            draw('He feels warm...?',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('Too powerful to decipher. Strong against Dark.')
            if chosenoption == 2:
                speak('I would assume you have met\\that being in the dark cloak.',light)
                speak('I am his counterpart.',light)
                speak('Do not let that knowledge restrict your actions.',light)
                speak('I would like to see what your journey has taught you...',light)
                speak('People are such contradictory creatures.',light)
                speak('They all act so different,\\and hold such variation in the\\way they live their lives.',light)
                speak('But they still have the\\same desires and values.',light)
                speak('I have seen your journey so far.',light)
                speak('Have you understood what it is\\that makes a person unique?',light)
                game.check1 = True
        if game.check2 == False:
            draw('His warmth hides a deep pain.',1,['Talk','Item'])
            game.check1 = True
            if chosenoption == 1:
                speak('The truth of your journey has been made apparent to you.',light)
                speak('You haven\'t been given the same agreement everyone else has.',light)
                speak('Yet, despite that knowledge,\\you utilize your remaining time to the fullest.',light)
                speak('Your resolve is truly admirable.',light)
                
                speak('Though, it would not be unwise\\to assume your true goal.',light)
                speak('Only by denying another\\a life can you regain yours.',light)
                speak('It must be done someway,\\but that does not lighten the choice.',light)
                speak('How is it you feel about this\\decision you have been burdened with?',light)
                talkmenu('...',['I\'ll choose what\'s best for all.','My fate is mine to decide.'],fredrick)

        if game.check3 == False:
            draw('The light is beginning to wear on you.',1,['Talk','Item'])
            game.check3 = True
            if chosenoption == 1:
                speak('It had always nagged at me.',light)
                speak('Despite you and him being the same in all ways,\\how could you have triumphed where he had failed?',light)
                speak('I suppose like you two, I must accept my situation.',light)
                speak('But still, I digress.',light)
                speak('You have seen what makes\\people hurt and what makes them happy.',light)
                speak('You have truly displayed your\\understanding of the human condition.',light)
                speak('That, and your decisiveness have proven your worth.',light)
                speak('It seems you are the\\one who will see tomorrow.',light)
                speak('We shall meet again.\\Our paths were created solely for that purpose.',light)
                speak('Until that time comes.',light)
                
        
    elif game.scene == 'Dark Battle':
        dark = game.enemies[0]
        fredrick = game.players[0] 
        if game.check1 == False:
            draw('A strange discomfort pulls at Fredrick.',1,['Talk','Item'])
            game.check1 = True
            if chosenoption == 1:
                speak('You, who has clung to light\\amidst the darkness.',dark)
                speak('You have done well until now.',dark)
                speak('Finding my true self was no small act, I must admit.',dark)
                speak('With that made clear: What are your intentions?',dark)
                
##                speak('But, the question still remains.',dark)
##                
##                speak('Those who came before you,\\and even you yourself have failed.',dark)
##                speak('Why is it that you will triumph when they have not?',dark)
##                speak('Are you different from them?',dark)
##                speak('Are you superior to them?',dark)
##                talkmenu('',['I am.','I am not.'],fredrick)
##                if chosenoption == 1:
##                    speak('This task you have is more than one can bear.',dark)
##                    speak('For your sake, I hope you are right.',dark)
##                if chosenoption == 2:
##                    speak('If you know you cannot,\\it is admirable that you still persevere.',dark)

            game.check1 = True
        if game.check2 == False:
            draw('Fredrick is feeling steadfast in his resolve.',1,['Talk','Item'])
            game.check2 = True
            if chosenoption == 1:
                speak('Of us two gods who maintain your world...',dark)
                speak('It is I who bears the brunt of the hatred.',dark)
                speak('My task is not a blessing by any means.',dark)
                speak('But beginnings are not valued without an ending.',dark)
                speak('It is I who brings about desire, and advancement.',dark)
                speak('And thus, I am also the god of such things.',dark)
                speak('However, do not let my words communicate lull you into a false sense of secuity.',dark)
                speak('Do not consider me your friend. Neither me or my counterpart.',dark)
##                speak('The One who I speak for...',dark)
##                speak('He is a being well deserving of the tales of death they tell.',dark)
##                speak('Knowing how many have tried, and still \\failed against this insurmountable opponent...',dark)
##                speak('Why is it that you believe you can defeat him?',dark)
##                talkmenu('',['I will defeat him.','I have to try.'],fredrick)
##                if chosenoption == 1:
##                    speak('Those who came before you held that belief.',dark)
##                    speak('Do you see how it served them?',dark)
##                if chosenoption == 2:
##                    speak('You accept your shortcomings.',dark)
##                    speak('You may be free from the blind\\pride which doomed your predecessors...',dark)
                game.check2 = True
        if game.check3 == False:
            draw('Fredrick is experiencing intense feelings...',1,['Talk','Item'])
            game.check3 = True
            if chosenoption == 1:
                speak('But the more pressing matter is your own.',dark)
                speak('You have an immense decision ahead of you.',dark)
                speak('The matter of that other "you".',dark)
                speak('What is it that you desire for your fates?',dark)
                talkmenu('...',['I will survive.','I don\'t know.'],fredrick)
                if chosenoption == 1:
                    speak('...',dark)
                    draw('A look of recognition spreads across his face.')
                    draw('The being seems pleased.')
                    #speak('HA HA HA!',dark)
                    speak('This desire to survive you have shown...',dark)
                    speak('The sanctity innate to it is what my existence was defined for.',dark)
                    speak('You have seen it: it IS you who would better use that life.',dark)
                    speak('Do what must be done.',dark)
                    speak('Once you have done so...',dark)
                    speak('Then you will be able to enjoy tomorrow.',dark)
                    
##                speak('We have dedicated our existences to maintaining yours.',dark)
##                speak('We keep your worlds in order, free from strife and chaos.',dark)
##                speak('Why do you reject our blessing?',dark)
##                talkmenu('',['It isn\'t a blessing.','This is what I believe in.'],fredrick)
##                if chosenoption == 1:
##                    speak('Have you seen that with your own eyes?',dark)
##                if chosenoption == 1:
##                    speak('Our purpose was to ensure human potential can be met.',dark)
##                    speak('If we are no longer able to fulfill that, then.',dark)

            
           
    elif game.scene == 'GrassStage Gestalt':
        oldcloak = game.enemies[0]
        fredrick = game.players[0]
        # You again?
        # What do you mean, "you again?" I've never met you before.'
        # Oh, right.
        # Heh heh heh.
        
        
        if oldcloak.Chealth == oldcloak.Mhealth and game.check1 == False:
            draw('Heh heh heh. Just like the old days...',1,['Check','Talk','Item'])
            if chosenoption == 1:
                draw('Reminds me of the man in the gray cloak.\\Though, it seems he possesses more emotions\\than just sarcasm...')
            if chosenoption == 2:
                speak('...',oldcloak)
                
                speak('Who\'dya think I am?',oldcloak)
                if 'secondplaythrough' in game.gamedata.events:
                    speak('You are some guy wearing a weird cloak\\who knows too much.',fredrick)
                    speak('Does that really narrow it down that much?',oldcloak) 
                else:
                    speak('I have no idea.',fredrick)
                    speak('I don\'t call anyone to your mind?',oldcloak)
                    speak('No.',fredrick)
                    speak('Heh heh heh. Is that so...',oldcloak)
                speak('Awright, let\'s get right down to business.',oldcloak)
                speak('When you build up enough flow during a battle,\\ a special move becomes available to you.',oldcloak)
                speak('How one builds up flow varies from person to person.\\But for you...',oldcloak)
                #You...
                #Don't you get it? Every step you take towards your end
                #is a day gone from our lives.
                #What you will find in the end IS the end.
                #One of us is going to meet our end.
                
                if game.gamedata.preference == 'logic':
                    speak('You build it up from damage being dealt, whether to your opponent or yourself.')
                if game.gamedata.preference == 'will':
                    speak('You make it manifest through sheer will.',oldcloak)
                speak('When your flow reaches its peak,\\you will have access to a power without rival.',oldcloak)
                speak('There are many forms to this power, you see.',oldcloak)
                speak('Your desires will shape the way it is expressed.',oldcloak)
                speak('However, you do not seem to know how to use this power yet...',oldcloak)
                speak('This is what these orbs are for...',oldcloak)
                speak('They will pass knowledge from previous warriors to you.')
                if game.gamedata.preference == 'logic':
                    battle.battle('GC SPatk transfer')
                elif game.gamedata.preference == 'Will':
                    battle.battle('BC SPatk transfer')
                elif game.gamedata.preference == 'Emotion':
                    battle.battle('WC SPatk transfer')
                
##                speak('Up to this point,\\ you have done things \\and have wanted to do things.',oldcloak)
##                speak('Because of those experiences,\you see the world differently.',oldcloak)
##                speak('This view of life you have\\ is known as a "Gestalt"',oldcloak)
##                speak('SO, I\'m gonna let you see\\ battle the same way you see life.',oldcloak)
                #game.fadeOut()
                
                #speak('The way I refer to the desires and experiences you\'ve had is to call it a "Gestalt".',oldcloak)
                #speak('The reason why you said that is\\due to the the experiences and desires\\that you have had so far.',oldcloak)
                #speak('That unique combination with which you\\see the world is known as a "Gestalt"',oldcloak)
                #speak('The unique worldview you have due\\ to your experiences and desires\\ thus far is known as a "Gestalt".',oldcloak)
                
                #speak('Now, I\'ll give ya a new viewpoint to see battle with.',oldcloak)
                if game.player.mode == 'Will':
                    game.player.mode = 'Emotion'
                #if fredrick.mode == 'emotion':
                #    fredrick.mode = 'logic'
                
                speak('Do ya feel it?',oldcloak)
                #if game.secondtimethrough:
                ##    speak('I think I have felt this before.',fredrick)
                ##    speak('You most likely have...',oldcloak)
                if game.gamedata.preference == 'logic':
                    speak('I feel like me, but... more.',fredrick)
                    speak('Guess that\'s one way to put it.',oldcloak)
                    #speak('Now your actions will truly reflect your intent...',oldcloak)
                if game.gamedata.preference == 'will':
                    speak('Kinda.',fredrick)
                    
                if game.gamedata.preference == 'emotion':
                    speak('I feel no different.',fredrick)
                    
                
            
                game.check1 = True
            if chosenoption == 3:
                itemmenu()
                print(game.player.mode)
                if game.player.mode == 'Will':
                    game.player.mode = 'Emotion'
                
                game.check1 = True
        if game.check1 == True and game.check2 == False and game.movecheck == False:
            #z check
            if game.moo >= 3:
                game.moo2 += 1
            if game.moo2 >= 60:
##                speak('What\'s the matter?\\What are you waiting for?',oldcloak)
##                speak('I..\\I don\'t know what I\'m doing!',fredrick)
##                speak('Huh...',oldcloak)
##                speak('I can\'t find my sword!',fredrick)
##                speak('You don\'t need a sword. You have magic now.',oldcloak)
##                speak('...Really?',fredrick)
##                speak('Hmm. Perhaps I should explain this better.',oldcloak)
                
                game.movecheck = True
        if oldcloak.Chealth <= (oldcloak.Chealth - 1000):
            draw('He\'s taking to it quite well...',1,['Talk','Item'])
            if chosenoption == 1:
                triplequestion(['What did you do to me?','Why are you doing this?','What\'s with the cloak?'],fredrick) #best dialogue choice
                if chosenoption == 1:
                    draw('You remind me of an old acquaintance.')
                    draw('That orb you had contained their "gestalt", if you will.')
                    draw('Now you see battle the way they did.')
                    
                if chosenoption == 2:
                    draw('It\'s a bit of a long story...',oldcloak)
                    draw('I take it you met some moron in a gray cloak?',oldcloak)
                    draw('Your task is to finish what he started...',oldcloak)
                if chosenoption == 3:
                    draw('It\s for special people.')
                    draw('I guess you could say that\\those "who run the place" get one.')
            
   
    else:
        pass
        #raise
        #print('You\'re battling Genmu, apparently.')
   

    if game.scene == 'Fateful Summon':
        print('Wait, you say? Do I look like a waiter?')
        '''
        There\'s no way!?!
        You summoned HIM???
        Yes, I did.
        He and I go WAAAAAY back.
        He owes me a few favors.
        Wiping you out will be one of them

        (YOU HAVE DRAWN YOUR FINAL BREATH)
        (THE END IS UPON YOU)



        Boy, that summoned monstrosity sure is great at parties
        (PLEASE HOLD MY BEVERAGE, I MUST DECIMATE A CIVILIZATION)

        '''
    if weirdrects:
        for i in game.players:
            i.rect.width, i.rect.height = i.defaultwidth,i.defaultheight
            i.talkmode = False
            i.emoting = False
    for i in game.enemies:
        i.talkmode = False
        i.emoting = False
        i.imagereset()
def intro():
    if game.scene == 'First Battle (Starring Gray Cloak)':
        speak('Alright, here we are.',ghostface)
        speak('Before we begin, there is an incantation that I must perform.', ghostface)
        speak('It is said to instantly bestow\\fighting knowledge upon those who hear it.',ghostface)
        speak('Cool, right?', ghostface)
        speak('Well, here goes.', ghostface)
        speak('Z, X, C, ARROW KEYS!',ghostface)
        speak('There it is.', ghostface)
        speak('Despite all this time, I still have no clue what it means.', ghostface)
    game.introed = True
class battleplayer:
    def __init__ (self, player,startpoint, emotions):
        self.player = player
        self.startpoint = startpoint
        self.currentpos = copy.copy(self.startpoint)
        self.image = player.battlesprite
        self.statusboximage = player.statusboximage
        self.imagedefault = self.image.copy()
        self.rect = pygame.Rect(0,0,55,85)#55 85
        self.defaultwidth = copy.copy(self.rect.width)
        self.defaultheight = copy.copy(self.rect.height)
        getlocation(self)
        self.name = player.name
        self.Mhealth = player.Mhealth
        self.Chealth = player.Chealth
        self.Mmp = player.Mmp
        self.Cmp = player.Cmp
        self.zattack = player.zattack
        self.xattack = player.xattack
        self.cattack = player.cattack
        self.spattack = player.spattack
        self.item = player.item
        if self.item != None:
            self.charges = copy.copy(player.item.charges)
        else:
            self.charges = 0
        self.SPmeter = 0
        self.spgain = 0
        self.spgaining = 0
        self.spcharging = None
        self.attack = player.attack
        self.defense = player.defense
        self.magic = player.magic
        #Do we really need speed and mdefense?
        self.speed = player.speed
        print('speed',self.speed)
        self.talkmode = None
        self.staggercounter = None
        self.isonpoison = None
        self.statuseffect = None
        self.airshoes = None
        self.stepslicecooldown = False
        self.stepcounter = 0
        self.timer = 0
        self.color = player.color
        self.playercontrol = True
        #assorted attack (or defense) variables
        self.blocking = None
        self.magicattacking = 0
        self.slicing = 0
        self.slicing2 = 0
        self.slicing3 = 0
        self.meteors = False
        self.meteorcount = 0
        #Just in case I need it
        self.moo = None
        self.debugcounter = 0
        self.isplayer = True
        self.isenemy= False
        self.emoting = None
        self.emotions = emotions
        self.HitsTaken = 0
        self.state = None
        self.guard = None
        self.attacking = False
        self.invincible = 0
        self.movementcooldown = 0
        self.staggercounter = 0
        #Boy, I wish ff13 didnt already use gestalt.
        # That would have fit so well, given the psychological overtones.
        #overtones? undertones?
        # well, maybe i can still use it.
        self.mode = copy.copy(player.mode)
        self.blockSP = 0
        self.equippeditem = None
        self.slideready = False
        self.quickcharging = None
        self.stuck = None
        self.quickslicing = 0
        self.quickslicing2 = 0
        self.nextslice = None
        self.burstready = None
        self.magicregen = False
        self.magicgain = 0
        self.magicgainrate = 1
        self.vulnerable = None
        self.stunned = None
       
        
        #self.idlestart = 0
        #self.idletime = 0

    def slide(self,direction):
        self.invincible = 30
        #ShineSlide
        if self.mode == 'Logic':
            if direction == 'right':
                for x in alltiles:
                    if x.coords[1] == self.currentpos[1]:
                        x.damagealert()
                        
                        x.damage(50,1,'enemy',['staggeronblock',self])
                        
        if direction == 'up':
            self.currentpos[1] -= 2
            if self.currentpos[1] <= 1:
                self.currentpos[1] = 1
                
        if direction == 'down':
            self.currentpos[1] += 2
            if self.currentpos[1] >= 8:
                self.currentpos[1] = 8#fieldheight
        if direction == 'left':
            self.currentpos[0] -= 2
            if self.currentpos[0] <= 1:
                self.currentpos[0] = 1
        if direction == 'right':
            self.currentpos[0] += 2
            if self.currentpos[0] >= 8:
                self.currentpos[0] = 8
        self.movementcooldown = 10


                
    def itemuse(self):
        if self.item != None:
            if self.item.charges:
                self.Cmp += 50
                self.item.charges -= 1
    def imagereset(self):
        self.image = self.imagedefault.copy()
        self.emoting = None
##        
    def rectreset(self):
        if self.rect.height != self.defaultheight:
             self.rect.height = copy.copy(self.defaultheight)
        

    def emote(self,emotion):
        self.imagereset()
        
        imageloc = copy.copy(self.emotions[emotion])
        self.image.scroll(imageloc[0],imageloc[1])
        self.emoting = emotion
    def statsimport(self, player):
            self.Mhealth = player.Mhealth
            self.Chealth = player.Chealth
            self.Mmp = player.Mmp
            self.Cmp = player.Cmp
            self.attack = player.attack
            self.defense = player.defense
            self.magic = player.magic
            self.speed = player.speed
            self.zattack = player.zattack
            self.xattack = player.xattack
            self.cattack = player.cattack
            self.spattack = player.spattack
            self.currentpos = copy.copy(self.startpoint)
        
    def update(self):
        #print(self.rect.width, self.rect.height, 'doot')
        if self.SPmeter > 100:
            self.SPmeter = 100

        if self.movementcooldown:
            self.movementcooldown -= 1
        if game.debug:
            self.debugcounter += 1
            if self.debugcounter == 60:
                print('Hits Taken:',self.HitsTaken)
                print('Location:', self.currentpos)
                for i in game.enemies:
                    print('Enemy Location:',i.currentpos)
                    print('Difficulty',game.difficulty)
                    print('Strategy',i.strat)
                print(ghostface.guard, 'Enemy Guard')
                self.debugcounter = 0

        if self.invincible:
            self.invincible -= 1
        
        if self.stepslicecooldown:
            self.vulnerable = True
            self.stepslicecooldown -= 1
        else:
            self.vulnerable = False
            #self.stepcounter += 1
            #if self.stepcounter == 10:
            #    self.stepslicecooldown = False
            #    self.stepcounter = 0
        if self.blocking or self.blockSP:
            isblocking = True
            self.blocking += 1
            if self.blocking == 21:
                self.blocking = False
                isblocking = False
                self.imagereset()
        else:
            isblocking = False

        
        if self.currentpos[1] <= 0:
            self.currentpos[1] = 1
        if self.currentpos[0] <= 0:
            self.currentpos[0] = 1
        if self.currentpos[1] >= 5:
            self.currentpos[1] = 4
        if self.currentpos[0] >= 9:
            self.currentpos[0] = 8
        getlocation(self)
        lastlocation = copy.copy(self.currentpos)
        if self.state == 'charge':
            self.charging += 1
            print(self.charging,'charge')
            if charging == 150:
                self.charging = False
                self.magicattack(self.chargingattack)
                self.chargingattack = None
        if self.stunned:
            print(self.stunned, 'player stun')
            self.stunned -= 1
            self.playercontrol = False
            if self.stunned == 0:
                self.playercontrol = True
        if self.staggercounter:
            
            self.staggercounter += 1
            self.playercontrol = False
            if self.staggercounter == 20:
                self.staggercounter = False
                self.playercontrol = True
        if self.spcharging:
            self.spgaining = True
            if self.SPmeter >= 120:
                self.spgaining = False
            else:
                self.spgaining = True
        
        self.magicregen = True
        if self.Cmp >= self.Mmp:
            self.magicregen = False
            
        if self.mode != 'Logic':
            self.spgaining = False
        if self.playercontrol:
            self.attacking = False
            key = pygame.key.get_pressed()#12x24
            
    ##            if key[300] == 1:
    ##                key[300] = 0
            if key[300] == 1 or key[301] == 1:
                    #Anti Caps/Num lock
               
                moo = list(key)                
                moo[301] = 0
                moo[300] = 0
                key = moo
            if 1 in key:
                self.timer = 0
                self.image = self.imagedefault.copy()
            else:
                self.timer += 1
                if self.timer >= 60:
                    self.timer = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:    
                        pygame.quit()
                        sys.exit()
                if event.type == KEYUP:
                    if event.key == K_s:
                        #self.blocking = False
                        pass
                        self.slideready = False
                        #if self.mode == 'Emotion':
                        #    self.slideready = False
                    if event.key == K_a:
                        if self.mode == 'Magic':
                            self.quickcharging = False
                   
                    if event.key == K_x and self.mode == 'Logic':
                        pass
                        #if self.SPmeter >= 100:
                        #    self.bigcast()
##                        self.blocking = False
##                        self.blockSP = False
                    if event.key == K_z and self.mode == 'Logic':
                        self.spcharging = False
                        self.quickcharging = False
                        self.spgaining = False
                        self.stuck = False
                    if event.key == pygame.K_F6:
                        game.debug = not game.debug
                    if event.key == K_q:
                        self.spgaining = False
                        self.SPmeter += 25
                    if event.key == K_e:
                        self.speed += 1
                        if self.speed >= 4:
                            self.speed = 1

                        print('current speed is ',self.speed)
                if event.type == KEYDOWN:
                    #print(self.movementcooldown, 'moving cooldown')
                    
                    if not self.movementcooldown and not self.stuck:                    
                            if event.key == K_UP:
                                if self.slideready:
                                    self.slide('up')
                                else:
                                    self.currentpos[1] -= 1
                                    self.movementcooldown = (self.speed*3)
                                    self.magicgain = -5
                                    if self.currentpos[1] <= 0:
                                        self.currentpos = lastlocation
                                        self.movementcooldown = 0
                                    if self.airshoes != True:
                                        for x in alltiles:
                                            if (x.usable == False or x.occupant != None) and fredrick.currentpos == x.coords :
                                                self.currentpos = lastlocation
                                                self.movementcooldown = 0
                               
                            if event.key == K_DOWN:
                               if self.slideready:
                                   self.slide('down')
                               else:
                                   self.currentpos[1] += 1
                                   self.movementcooldown = (self.speed*3)
                                   self.magicgain = -5
                                   if self.currentpos[1] >= 5:
                                        self.currentpos = lastlocation
                                        self.movementcooldown = 0
                                        
                                   if self.airshoes != True:
                                       for x in alltiles:
                                            if (x.usable == False or x.occupant != None) and fredrick.currentpos == x.coords:
                                                self.currentpos = lastlocation
                                                self.movementcooldown = 0
                            if event.key == K_LEFT:
                                if self.slideready:
                                    self.slide('left')
                                else:
                                    self.currentpos[0] -= 1
                                    self.movementcooldown = (self.speed*3)
                                    self.magicgain = -5
                                    if self.currentpos[0] <= 0:
                                        self.currentpos = lastlocation
                                        self.movementcooldown = 0

                                    if self.airshoes != True:
                                        for x in alltiles:
                                            if (x.usable == False or x.occupant != None) and fredrick.currentpos == x.coords :
                                                self.currentpos = lastlocation
                                                self.movementcooldown = 0


                            if event.key == K_RIGHT:
                                if self.slideready:
                                    self.slide('right')
                                else:
                                    self.currentpos[0] += 1
                                    self.movementcooldown = (self.speed*3)
                                    if self.currentpos[0] >= 9:
                                        self.currentpos = lastlocation
                                        self.movementcooldown = 0
                                    if self.airshoes != True:
                                        for x in alltiles:
                                            if (x.usable == False or x.occupant != None) and fredrick.currentpos == x.coords :
                                                self.currentpos = lastlocation
                                                self.movementcooldown = 0
                           


                    if event.key == K_p:
                        game.enemies[0].Chealth -= 300
                    if event.key == K_a:
                        if self.mode == 'Magic':
                            self.quickcharging = True
                    if event.key == K_z:
                        if self.zattack.ismagic:
                            self.magicattack(self.zattack)
                            game.usedmagic = True
                        else:
                            self.zattack.use(self)
                            game.usedsword = True

                            
                    if event.key == K_x:
                        if self.SPmeter >= 100 and self.spattack != None:
                            self.spattack.use(self)
                        else:
                            if self.xattack.ismagic:
                                self.magicattack(self.xattack)
                                game.usedmagic = True
                            else:
                                self.xattack.use(self)
                                game.usedsword = True

                    if event.key == K_c:
                        if self.cattack.ismagic:
                                self.magicattack(self.cattack)
                        else:
                                self.cattack.use(self)
                        
                    if event.key == K_w:
                        #print('Gestalt Switch')
                        #if self.mode == 'Will':
                        #    self.mode = 'Emotion'
                        #elif self.mode == 'Emotion':
                        #    self.mode = 'Logic'
                        #elif self.mode == 'Logic':
                        #    self.mode = 'Will'
                        pass
                    if event.key == K_a:
                        self.useitem()
                    if event.key == K_SLASH:
                        self.itemuse()
                    

                        #self.airshoes = not fredrick.airshoes
                    lastloc = fredrick.currentpos
                    if event.key == K_m:
                        self.meteors = True
                    if event.key == K_l:
                        self.lightning()
                    if event.key == K_F9:
                        try:
                            moo = input('Type a command.')
                            try:
                                
                                exec(moo)
                            except:
                                eval(moo)
                        
                        except:
                            
                            print('Nope')
                            
                            pass
                    if event.key == K_s:
                        self.blocking = 1
                        #if self.mode == 'Emotion':
                        #    self.slideready = True
                    if event.key == K_b:
                        print("detected")
                        for i in alltiles:
                            if i.coords[0] == 1:
                                print('found one')
                                i.state = 'broken'
                    #if event.key == K_q:
                        
                    
                    if event.key == pygame.K_RETURN:
                        #pause the game
                        #also allows pause scumming
                        # maybe anti pause scumming?
                        done = False
                        while not done:
                            
                            for event in pygame.event.get():
                                if event.type == KEYDOWN and event.key == K_F9:
                                    try:
                                        moo = input('Type a command.')
                                        try:
                                            
                                            exec(moo)
                                        except:
                                            eval(moo)
                                    
                                    except:
                                        
                                        print('Nope')
                                        
                                        pass
                                if event.type == KEYDOWN and event.key == K_RETURN:
                                    done = True
                    
                                
                            
        
        
        if self.timer != 0 :
            if self.timer == 47:
                self.image.scroll(-55,0)
                #print('one')
                #time.sleep(1)
            if self.timer == 49:
                self.image.scroll(-55,0)
                #print('two')
                #time.sleep(1)
            if self.timer == 51:
                self.image = self.imagedefault.copy()
                self.image.scroll(-55,0)
                #print('three')
                #time.sleep(1)
            if self.timer == 53:
                self.image = self.imagedefault.copy()
                #print('four')
                #time.sleep(1)
        if self.blocking or self.blockSP:
            if not isblocking:
                game.perfectblock = 10
            
            self.image = self.imagedefault.copy()
            self.image.scroll(-165,-170)

        if self.spgaining:
            self.spgain += 1
            if self.quickcharging:
                self.spgain += 2
                
            
            if self.spgain >= 8:
                self.spgain = 0
                self.SPmeter += 1
        if self.magicregen:
            self.magicgain += self.magicgainrate
            
            if self.magicgain >= 10:
                self.Cmp += 1
                if self.quickcharging:
                    self.Cmp += 1
                self.magicgain = 0
                

        if self.magicattacking:
            self.attacking = True
            if self.magicattacking < 5:
                self.imagereset()
                self.image.scroll(-165,-255)
                self.magicattacking += 1
            elif self.magicattacking >= 5:
                self.magicattacking = 0
        if self.quickslicing or self.quickslicing2:
            self.attacking = True
            if (self.quickslicing == 1 or self.quickslicing2 == 1):
                #This makes sure that the playersprite doesn't shift down
                self.moo = copy.copy(self.rect.bottomleft)
            self.stuck = True
            self.rect.width = 74
            self.rect.height = 94
            self.rect.bottomleft = self.moo
            if self.quickslicing:
                print('qs1',self.quickslicing)
                #print('slicing')
                
##                key = pygame.key.get_pressed()
##                if key[122]:
##                    self.slicing2 = 1
##                    print('next assigned')
                if self.quickslicing < 14:
                    self.imagereset()
                    #if self.slicing % 2 == 0:
                    self.image.scroll(74*(self.quickslicing//2)*-1,-340)
                    self.quickslicing += 1
                if self.quickslicing == 7:
                    damage = self.attack*5 + 30
                    area = [(1,0),(2,0)]
                    targetarea = self.currentpos.copy()
                    
                    for i in area:
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damagealert()
                            if x.occupant != None and x.coords == targetarea:
                                x.damagealert()
                                x.damage(damage,1,'enemy',['hitstun',15])
                        targetarea = self.currentpos.copy()

                    self.stepslicecooldown = 20
                elif self.quickslicing >= 14:
                    self.stuck = False
                    self.rect.width = 55
                    self.rect.height = 85
                    self.quickslicing = 0
                    if self.nextslice:
                        
                        self.quickslicing2 = 1
                        self.nextslice = 0
            if self.quickslicing2:
                
                if self.quickslicing2 < 12:
                    self.imagereset()
                    #if self.slicing % 2 == 0:
                    self.image.scroll(74*(self.quickslicing2//2)*-1,-340)
                    self.quickslicing2 += 1
                if self.quickslicing2 == 5:
                    damage = self.attack*5 + 40
                    targetarea = self.currentpos.copy()
                    area = [(1,0),(2,0)]
                    
                    
                    for i in area:
                        targetarea[0] += i[0]
                        targetarea[1] += i[1]
                        for x in alltiles:
                            if x.coords == targetarea:
                                x.damagealert()
                            if x.occupant != None and x.coords == targetarea:
                                x.damagealert()
                                x.damage(damage,1,'enemy', ['stagger',1])
                                x.occupant.stagger()
                                self.SPmeter += 10
                        targetarea = self.currentpos.copy()
##                    targetarea[0] += 1
##
##                    for x in alltiles:
##                        if x.coords == targetarea:
##                            x.damagealert()
##                        if x.occupant != None and x.coords == targetarea:
##                            x.damagealert()
##                            x.damage(damage,1,'enemy', ['stagger',1])
##    ##                        if x.occupant.invincible != True:
##    ##                            x.occupant.Chealth -= damage
##    ##                            #attacks break stun
                elif self.quickslicing2 >= 12:
                    self.stuck = False
                    self.imagereset()
                    self.rect.width = 55
                    self.rect.height = 85
                    self.quickslicing2 = 0
                    self.quickslicing = 0
                    self.stepslicecooldown = 40
        if self.slicing or self.slicing2 or self.slicing3:
            #print(self.slicing,self.slicing2,self.slicing3)
            self.attacking = True
            if (self.slicing == 1 or self.slicing2 == 1 or self.slicing3 == 1):
                #This makes sure that the playersprite doesn't shift down
                self.moo = copy.copy(self.rect.bottomleft)
            self.stuck = True
            self.rect.width = 74
            self.rect.height = 94
            self.rect.bottomleft = self.moo
            if self.slicing:
                #print('slicing')
                
##                key = pygame.key.get_pressed()
##                if key[122]:
##                    self.slicing2 = 1
##                    print('next assigned')
                if self.slicing < 14:
                    self.imagereset()
                    #if self.slicing % 2 == 0:
                    self.image.scroll(74*(self.slicing//2)*-1,-340)
                    self.slicing += 1
                if self.slicing == 7:
                    damage = self.attack*5 + 25
                    targetarea = self.currentpos.copy()
                    targetarea[0] += 1
                    for x in alltiles:
                        if x.coords == targetarea:
                            x.damagealert()
                        if x.occupant != None and x.coords == targetarea:
                            x.damagealert()
                            x.damage(damage,1,'enemy',['hitstun',12],['enemyreset',1])
                            #Combo starter, hard to find...
    ##                        if x.occupant.invincible != True:
    ##                            x.occupant.Chealth -= damage
    ##                            #attacks break stun
    ##                            x.occupant.stunned = 0
    ##                            x.occupant.stagger()
                    self.stepslicecooldown = 20
                elif self.slicing >= 14:
                    self.stuck = False
                    self.rect.width = 55
                    self.rect.height = 85
                    self.slicing = 0
                    if self.nextslice:
                        
                        self.slicing2 = 1
                        self.nextslice = 0
            if self.slicing2:
                #print('slicing2')
##                key = pygame.key.get_pressed()
##                if key[122]:
##                    self.slicing3 = 1
                if self.slicing2 < 12:
                    self.imagereset()
                    #if self.slicing % 2 == 0:
                    self.image.scroll(74*(self.slicing2//2)*-1,-340)
                    self.slicing2 += 1
                if self.slicing2 == 5:
                    damage = self.attack*5 + 30
                    targetarea = self.currentpos.copy()
                    targetarea[0] += 1
                    for x in alltiles:
                        if x.coords == targetarea:
                            x.damagealert()
                        if x.occupant != None and x.coords == targetarea:
                            x.damagealert()
                            x.damage(damage,1,'enemy',['hitstun',20])
    ##                        if x.occupant.invincible != True:
    ##                            x.occupant.Chealth -= damage
    ##                            #attacks break stun
                elif self.slicing2 >= 12:
                    self.stuck = False
                    self.rect.width = 55
                    self.rect.height = 85
                    self.slicing2 = 0
                    self.slicing = 0
                    if self.nextslice:
                        self.slicing3 = 1
                        self.nextslice = 0
            if self.slicing3:
                #print('slicing3')
                if self.slicing3 < 12:
                    self.imagereset()
                    #if self.slicing % 2 == 0:
                    self.image.scroll(74*(self.slicing3//2)*-1,-340)
                    self.slicing3 += 1
                if self.slicing3 == 10:
                    damage = self.attack*5 + 50
                    targetarea = self.currentpos.copy()
                    targetarea[0] += 1

                    for x in alltiles:
                        if x.coords == targetarea:
                            x.damagealert()
                        if x.occupant != None and x.coords == targetarea:
                            x.damagealert()
                            x.damage(damage,1,'enemy', ['stagger',1])
                            self.SPmeter += 10
    ##                        if x.occupant.invincible != True:
    ##                            x.occupant.Chealth -= damage
    ##                            #attacks break stun
                elif self.slicing3 >= 12:
                    self.stuck = False
                    self.rect.width = 55
                    self.rect.height = 85
                    self.slicing3 = 0
                    self.slicing2 = 0
                    self.slicing = 0
                    self.imagereset()
                    self.stepslicecooldown = (40- self.speed*5)
                
                    
                    
        
            
                
        if self.meteors:
            
            self.attacking = True
            ghostface.statuseffect = 'paralyzed'
            self.playercontrol = True
            self.meteorcount += 1
            if self.meteorcount % 2 == 0:
                damage = random.randint(self.magic*80, self.magic*100)
                restiles = copy.copy(alltiles)
                for i in restiles:
                    if i.coords[1] == 1 or i.coords[1] == 4:
                        restiles.remove(i)
                
                i = random.randint(0,(len(restiles)-1))
                x = i + 1
                if x >= len(restiles):
                    x -= 2
                targetarea = restiles[i].coords
                secondtarget = restiles[x].coords
                for x in restiles:
                    if x.coords == targetarea or x.coords == secondtarget:
                        x.damagealert()
                    if x.occupied == True and (x.coords == targetarea or x.coords == secondtarget) and x.occupant != self:
                        x.occupant.Chealth -= damage
            
            if self.meteorcount == 60:
                ghostface.statuseffect = 'normal'
                self.playercontrol = True
                self.meteors = False
                self.meteorcount = 0
                self.SPmeter = 0
##                for event in pygame.event.get():
##                    pass
            
        #print(self.blocking)


            
                
    def physicalattack(self):
        damage = random.randint(self.attack, self.attack*2)
        targetarea = self.currentpos.copy()
        targetarea[0] += 1
        for x in alltiles:
            if x.occupied == True and x.coords == targetarea:
                x.occupant.CHealth -= damage
    def meteor(self):
        self.meteors = True
    def stepslice(self):
        """
        Each attack function is actually a function
        that activates the variable connected to a certain attack.
        (Unless I wrote it up like a normal function.)
        The real attack is handled in player.update().
        This is the trigger function for the basic attack.
        (It's also a weird MMBN reference.)
        """
        if game.debug:
            for i in game.enemies:
                print(i.currentpos[0], i.currentpos[1])
        if not self.stepslicecooldown:
                if self.slicing < 1:
                    self.slicing = 1
                #self.stepslicecooldown = 5
                
##        if self.slicing != 0:
##            q = self.slicing
##        elif self.slicing2 != 0:
##            q = self.slicing2
##        else:
##            q = 0
##        if q < 12 and q >6:c
        
        if (self.slicing >= 2) or self.slicing2 >= 1:
            self.nextslice = True
        if self.burstready:
            self.slicing = False
            self.burst = 1
        else:
            pass
    #dashattack
    def quickslice(self):
        if not self.stepslicecooldown:
            if self.quickslicing <= 1:
                self.quickslicing = 1
        if self.quickslicing >= 2:
            self.nextslice = True
    def lightning(self):
        for x in alltiles:
            location = copy.copy(self.currentpos)
            location[0] += 2
            if x.coords == location:
                i = x
                
        moo = {'type':'animation','width':60,'frames':14,'elapsedframes':0,'image':'lightning.png','location':copy.copy(i.rect.midbottom),'damageframe':7,'tile':i,'damage':10,'damages':'enemy'}
        game.specialblits.append(moo)
    def commandsword(self):
        pass
            
    def strongblock(self):
        self.block = True
        self.blockSP = True
    def stepcircle(self):
        if self.SPmeter >= 30:
            #area = [(1,1),(1,0),(1,-1),(2,1),(2,0),(2,-1)]

            area = [(1,1),(1,0),(1,-1),(-1,1),(-1,0),(-1,-1),(0,1),(0,-1)]
            damage = random.randint(self.attack*10,self.attack*15)
            self.currentpos[0] += 2
            targetarea = self.currentpos.copy()
            self.SPmeter -= 30
            for i in area:
                targetarea[0] += i[0]
                targetarea[1] += i[1]
                for x in alltiles:
                    if x.coords == targetarea:
                        x.damagealert()
                    if x.occupant != None and x.coords == targetarea:
                        x.damagealert()
                        x.occupant.Chealth -= damage
                        x.occupant.stagger()
                targetarea = self.currentpos.copy()
            if self.SPmeter == 100:
                print('jeff')

    def cleave(self):
        area = [(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        targetarea = copy.copy(self.currentpos)
        damage = (250 + (self.attack*30))
        for i in area:
                targetarea[0] += i[0]
                targetarea[1] += i[1]
                for x in alltiles:
                    if x.coords == targetarea:
                        x.damagealert()
                    if x.occupant != None and x.coords == targetarea:
                        x.damagealert()
                        x.occupant.Chealth -= damage
                        x.occupant.stagger()
                targetarea = self.currentpos.copy()
        self.SPmeter = 0
    def salvation(self):
        for i in game.enemies:
            i.attack //= 1.3
            i.defense //= 1.3
        self.attack += 2
        self.defense  += 2
        self.autolife = True
        self.Cmp = copy.copy(self.Mmp)
        self.Cmp *= 2
        self.Chealth = copy.copy(self.Mhealth)
        self.Chealth *= 2
        
        self.SPmeter = 0
        
    def wideslice(self):
        print(self.SPmeter, "Special Meter")
        area = []
        if self.stepslicecooldown == False and self.SPmeter >= 25:
            waittimer = 0
            if self.SPmeter >= 100:
                #Unbelievably specific reference
                # this sword is my life
                damage = 400
                area = [(1,1),(1,0),(1,-1),(2,1),(2,0),(2,-1)]
                self.SPmeter = 0
            else:
                damage = 40
            targetarea = self.currentpos.copy()
            if area == []:
                area = [(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for i in area:
                targetarea[0] += i[0]
                targetarea[1] += i[1]
                for x in alltiles:
                    if x.coords == targetarea:
                        x.damagealert()
                    if x.occupant != None and x.coords == targetarea:
                        x.damagealert()
                        x.occupant.Chealth -= damage
                        x.occupant.stagger()
                targetarea = self.currentpos.copy()
            waittimer = 0
            stepslicecooldown = True
            self.SPmeter -= 25
            
                    
            
    
    def magicattack(self, magic,emotion=None):
##        if emotion:
##            if self.SPmeter >= magic.mpcost:
##                #if magic.specialeffect:
##                if magic.specialeffect == 'charge':
##                    self.state = 'charge'
##                    self.chargeattack = copy.copy(magic)
##                    #after the charge, do the normal attack
##                    self.chargeattack.specialeffect = None
##                    #charge info contains damage and area affected
##                    self.chargeinfo = [250,1]
##                    
##                else:
##                    damage = self.magic * (magic.basedamage//3)
##                    if magic.area == None:
##
##                        targetarea = self.currentpos.copy()
##                        targetarea[0] += magic.distance
##                        for x in alltiles:
##                            if x.coords == targetarea:
##                                    x.damagealert()
##                        
##                        for x in alltiles:
##                            if x.occupant != None and x.coords == targetarea:
##                                x.occupant.Chealth -= damage
##                self.SPmeter -= magic.mpcost
##                self.magicattacking = 1
##            else:
##                if game.scene == 'GrassStage Gestalt' and game.check1 == True and game.check2 == False:
##                    game.moo += 1
                
                
        if self.Cmp >= magic.mpcost:
            print(magic.element)
            if magic.element == "Healing":
                if self.Chealth >= self.Mhealth:
                    return
                else:
                    recovered = self.magic * magic.basedamage
                    self.Chealth += recovered
                    if self.Chealth >= self.Mhealth:
                        self.Chealth = copy.copy(self.Mhealth)
                    
                #return
            elif magic.element == 'Power Enhancement':
                self.attack += magic.basedamage
            elif magic.specialeffect:
                if magic.specialeffect == 'charge':
                    self.state = 'charge'
                    self.chargeattack = copy.copy(magic)
                    #after the charge, do the normal attack
                    self.chargeattack.specialeffect = None
                    #charge info contains damage and area affected
                    self.chargeinfo = [250,1]
                if magic.specialeffect == 'projectile':
                    x = ((10*(magic.basedamage + self.magic)))
                    damage = random.randint(x,x+2)
                    location = self.currentpos.copy()
                    print(location)
                    location[0] += 1

                    
                    for i in alltiles:
                        if i.coords == location:
                            targetarea = i
                            print(i.coords)
                    print(targetarea,'targetarea')
                    moo = {'type':'animation','width':60,'frames':2,'elapsedframes':0,
                           'image':'laser.png','location':copy.copy(targetarea.rect.midbottom),'coords':targetarea.coords,
                           'damageframe':'all','tile':targetarea,'damage':damage,'damages':'enemy','projectile':8,'onehit':1}
                    game.specialblits.append(moo)
                    
            else:
                damage = (self.magic * magic.basedamage)
                if magic.area == None:

                    targetarea = self.currentpos.copy()
                    targetarea[0] += magic.distance
                    for x in alltiles:
                        if x.coords == targetarea:
                            x.damagealert()
                    
                    for x in alltiles:
                        if x.occupant != None and x.coords == targetarea:
                            x.occupant.Chealth -= damage
                if magic.area:
                    pass
            
            self.Cmp -= magic.mpcost
            self.magicattacking = 1
        else:
            if magic.element == "Healing":
                if self.Chealth == self.Mhealth:
                    return
                else:
                    recovered = self.magic * magic.basedamage
                    self.Chealth += recovered
                    if self.Chealth >= self.Mhealth:
                        self.Chealth = copy.copy(self.Mhealth)
                self.Cmp = -15
                self.magicattacking = 1
    def useitem(self):
        if self.equippeditem != None:
            target = game.player
            exec(self.equippeditem.effect)
            #Multiple Uses?
            self.equippeditem = None
            #self.equippeditem.effect
    def meteors(self): 
        if self.Cmp > 0:
            waitime = 0
            for i in game.enemies:
                i.statuseffect = 'timestop'
                fredrick.statuseffect = 'timestop' 
            allowinput = False
            for x in (j,k,l,m,n,o,p,q,r):
                x.damagealert()
                time.sleep(0.05)
                displayupdate()
                
                if x.occupied == True:
                    x.occupant -= 300
                    self.Cmp -= 5

        else:
            pass
        
    def stagger(self):
        print('staggered')
        if self.isplayer:
            self.currentpos[0] -= 1
            self.staggercounter = True
        if self.isenemy:
            self.currentpos[0] += 1
            #self.guard = True
            self.battlecounter = 0
        if self.currentpos[0] <= 0:
            self.currentpos[0] = 1
        if self.currentpos[0] >= 8:
            self.currentpos[0] = 7

   
fredrick = battleplayer(Fredrick,[2,2],{'concern':[0,-85],'displeased':[0,-520],'hard squint':[0,-605],'shame':[0,-435]})
class enemy:
    def __init__(self,startpoint, player, emotions): #strategy
        self.player = player
        self.startpoint = copy.copy(startpoint)
        self.currentpos = copy.copy(self.startpoint)
        self.image = player.battlesprite
        #self.statussprite = player.statusboximage
        self.imagedefault = self.image.copy()
        self.rect = pygame.Rect(0,0,55,85)#55 85
        self.defwidth = copy.copy(self.rect.width)
        self.defheight = copy.copy(self.rect.height)
        getlocation(self)
        self.name = player.name
        self.Mhealth = player.Mhealth
        self.Chealth = player.Chealth
        self.Mmp = player.Mmp
        self.Cmp = player.Cmp
        self.attack = player.attack
        self.defense = player.defense
        self.magic = player.magic
        self.speed = player.speed
        self.talkmode = None
        self.staggercounter = 0
        #self.strategy = strategy
        self.battlecounter = 0
        self.statusboximage = pygame.image.load('Gstatusboxsprite.png')
        self.image.fill((255,0,0), special_flags=pygame.BLEND_RGB_ADD)
        self.staggerimage = self.image.copy()
        self.image = self.imagedefault.copy()
        self.statuseffect = None
        self.attacktimer = 0
        self.color = player.color
        self.magicattacking = None
        self.spattacking = None
        self.spattackpart = 1
        self.sptrigger = False
        self.isenemy = True
        self.isplayer = False
        self.invincible = None 
        self.sideswipe = None
        self.frontswipe = None
        self.animation = None
        self.emotions = emotions
        self.emoting = None
        self.stunned = None
        self.stunsp = None
        self.guard = None
        self.cooldown = 0
        self.aggrocounter = None
        self.movecounter = 0
        self.strat = 'intro'
        self.moveneeded = None
        self.moo = 0
        self.moo2 = 0
        self.attackready = False
        self.hit = None
        self.hitstun = 0
        self.leavehitstun = False
        self.chargecounter = 0
        self.midtransition = True
        self.finaltransition = False
        self.spattacked = False
        self.SPevent = False
        self.fast = False
        self.attackpattern = True
        self.prevcast = 1
        self.blockamount = 0
        self.weirdrects = None
        if self.player.SPmeter != None:
            self.SPmeter = self.player.SPmeter
        else:
            self.SPmeter = None
        
    def imagereset(self):
        if not self.weirdrects:
            self.rect.height = copy.copy(self.defheight)
            self.rect.width = copy.copy(self.defwidth)
        self.image = self.imagedefault.copy()
        self.emoting = None

    def emote(self,emotion):
        self.imagereset()
        
        imageloc = copy.copy(self.emotions[emotion])
        self.image.scroll(imageloc[0],imageloc[1])
        
        self.emoting = emotion
        print(self.emoting)
    def playerinfocheck(self, player):
        #print('check info')
        #Check horizontal position vs self
        if game.playerlastloc == None:
            game.playerlastloc = copy.copy(player.currentpos)
        if player.vulnerable == True:
            game.playervulnerable = True
        else:
            game.playervulnerable = False
        #print(game.playerlastloc, player.currentpos)
        if game.playerlastloc != player.currentpos:
            #check if approaching
            if game.playerlastloc[0] < player.currentpos[0]:
                game.playerapproaching = True
                game.playerretreating = False
                game.approachcounter = 0
            if game.playerlastloc[0] > player.currentpos[0]:
                game.playerretreating = True
                game.playerapproaching = False
                game.retreatcounter = 0
        
                

        else:
            game.approachcounter += 1
            game.retreatcounter += 1
            #because frame perfect inputs usually don't happen
            if game.approachcounter >= 10:
                game.playerapproaching = False
            if game.retreatcounter >= 10:
                game.playerretreating = False
                
            
        if player.currentpos[0] < self.currentpos[0]:
            playerinfront = True
            playerbehind = False
            playerinsamecolumn = False
            distancefromplayer = self.currentpos[0] - player.currentpos[0]
        if player.currentpos[0] > self.currentpos[0]:
            playerbehind = True
            playerinfront = False
            playerinsamecolumn = False
            distancefromplayer = player.currentpos[0] - self.currentpos[0]
        if player.currentpos[0] == self.currentpos[0]:
            playerinsamecolumn = True
            playerinfront = False
            playerbehind = False
            distancefromplayer = 0
        #check vertical position
        #print(self.currentpos[1], player.currentpos[1])
        if player.currentpos[1] > self.currentpos[1]:
            playerisabove = True
            playerisbelow = False
            playerinsamerow = False
        if player.currentpos[1] < self.currentpos[1]:
            playerisbelow = True
            playerisabove = False
            playerinsamerow = False
        if player.currentpos[1] == self.currentpos[1]:
            playerinsamerow = True
            playerisabove = False
            playerisbelow = False
        if player.attacking:
            playerattacking = True
        else:
            playerattacking = False
        
        game.playerisabove= playerisabove
        game.playerisbelow = playerisbelow
        game.playerinfront = playerinfront
        game.playerbehind = playerbehind
        game.playerinsamerow = playerinsamerow
        game.playerinsamecolumn = playerinsamecolumn
        game.playerattacking = playerattacking
        game.distancefromplayer = distancefromplayer
       # print(game.playerinsamerow,game.playerinsamecolumn)
        game.playerlastloc = copy.copy(player.currentpos)
    def strategy(self):
        player = game.player
        #print(self.invincible,'invincible')
        #print(self.staggercounter,'staggering')
        if self.staggercounter:
            self.staggercounter += 1
            self.invincible = 30
            if self.staggercounter >= 25:
                self.staggercounter = 0
                self.invincible = False
        if self.hitstun:
            self.hitstun -= 1
            self.imagereset()
        
            
            self.image.scroll(0,-85)
            self.leavehitstun = True
        if not self.hitstun and self.leavehitstun:
            game.player.currentpos[0] = 1
            self.leavehitstun = False
            
        if self.stunned:
            self.guard = False
            self.imagereset()
            self.image.scroll(0,-85)
            #scroll to stunned face
            self.stunned += 1
            if self.stunned == 60:
                self.stunned = 0
                self.stunsp = 0
        if self.strat == 'blocking':
            self.imagereset()
            self.image.scroll(60,-85)
            
            self.blockamount += 1
            if self.blockamount >= 10:
                self.strat = 'reset'
                self.blockamount = 0
                #define reset for all characters
                #assigns strategy after being staggered
            
        
        #print(self.battlecounter)
        self.playerinfocheck(game.player)
##        #print(game.playerinsamerow)
##        #if game.playerapproaching:
##        #    print('approaching')
##        #if game.playerretreating:
##        #    print('retreating')
##
        if self.statuseffect != 'K.O' and not self.animation and not self.stunned and not self.hitstun:
            # and  self.statuseffect != 'SPattack'
            # self.statuseffect != 'paralyzed' or self.statuseffect == 'timestop' or
            
            lastarea = copy.copy(self.currentpos)
            if self.name == 'Gray Cloak':
                if game.scene == 'First Battle (Starring Gray Cloak)':
                    if game.specialintro:
                        pass
                    else:
                        BattleEnemyData.GrayCloakStrategy(self, fredrick, game, alltiles)
            if self.name == 'Dark Nyu':
                BattleEnemyData.DarkNyuStrategy(self,fredrick,game,alltiles)
            if self.name == 'Genmu':
                 BattleEnemyData.GenmuStrategy(self, fredrick, game, alltiles)
            if self.name == 'MagicDog':
                BattleEnemyData.MagicDogStrategy(self,fredrick,game,alltiles)
            if self.name == 'MagiNyu':
                BattleEnemyData.MagiNyuStrategy(self,fredrick,game,alltiles)
            if self.name == 'SwordNyu':
                BattleEnemyData.SwordNyuStrategy(self,fredrick,game,alltiles)
            if self.name == 'OFredrick':
                BattleEnemyData.OFredrickStrategy(self,fredrick,game,alltiles)
            if self.name == 'FallenWarrior':
                BattleEnemyData.FallenWarriorStrategy(self,fredrick,game,alltiles)
            if self.name == 'Black Cloak':
                BattleEnemyData.BlackCloakStrategy(self,fredrick,game,alltiles)
        

                #BattleEnemyData.GenmuStrategy(self,game.player,game,alltiles)

    def stagger(self):
        self.currentpos[0] += 1
        if self.currentpos[0] >= 9:
            self.currentpos[0] = 8
        self.staggercounter += 1
        self.battlecounter = 0


def healthcheck(players,enemies):
    for i in players:
        if i.Chealth <= 0:
            i.Chealh = 0
            i.statuseffect == 'K.O'
    for i in enemies:
        if i.Chealth <= 0:
            i.Chealth = 0
            i.statuseffect == 'K.O'


 


    
class Playerinfobox:
    def __init__(self, player, location):
        self.player = player
        self.location = location
        self.rect = pygame.rect.Rect(150, 405, 100,75)
        self.image2 = pygame.image.load('playerstatusbox.png')
        self.Mhealth = player.Mhealth
        self.Chealth = player.Chealth
        self.Mmp = player.Mmp
        self.Cmp = player.Cmp
        self.SPmeter = player.SPmeter
        #spcenter is 92, 50
        self.status = player.statuseffect
        self.image = player.statusboximage

class Enemyinfobox:
    def __init__(self, enemy, location):
        self.enemy = enemy
        self.location = location
        self.rect = pygame.rect.Rect(300, 405, 150,75)
        self.image2 = pygame.image.load('enemystatusbox.png')
        self.Mhealth = enemy.Mhealth
        self.Chealth = enemy.Chealth
        self.hasSPmeter = False
        if self.enemy.SPmeter != None:
            self.SPmeter = enemy.SPmeter
            self.hasSPmeter = True
        
        self.Mmp = enemy.Mmp
        self.Cmp = enemy.Cmp
        self.status = None
        self.image = enemy.statusboximage
def epoisoncheck():
    if e.state == 'poison' and e.playerisonit == True:
        fredrick.isonpoison = True
    else:
        fredrick.isonpoison = False
def displaystatusbox(player):
    Finfo = Playerinfobox(player, (300,250))
   
    Hobj = pygame.font.Font('FreeSans.ttf', 14)
    htso = Hobj.render(str(Finfo.Chealth)+'/'+str(Finfo.Mhealth)+'HP', True, (0,0,0), None)
    htro = htso.get_rect()
    htro.center = (45,20)


    Mobj = pygame.font.Font('FreeSans.ttf', 14)
    Mtso = Mobj.render(str(Finfo.Cmp)+'/'+str(Finfo.Mmp)+'MP', True, (0,0,0), None)
    mtro = Mtso.get_rect()
    mtro.center = (45,40)
    
    if Finfo.SPmeter == 100:
        spcolor = (255,0,0)
    else:
        spcolor = (0,0,255)
    linelength = (48 + (Finfo.SPmeter * 0.85)//1)
    #print(Finfo.SPmeter)
    
    stso = Mobj.render('SP',True,spcolor,None)
    stro = stso.get_rect()
    #48,59 is beginning of sp meter
    #Spmeter is 8 px tall, first segment is 6 px.
    stro.center = ((Finfo.rect.x + 92,Finfo.rect.y + 50))   
    display.blit(Finfo.image2, Finfo.rect)
    display.blit(htso, (Finfo.rect.centerx-10, Finfo.rect.centery-30))
    display.blit(Mtso, (Finfo.rect.centerx-10,Finfo.rect.centery-10))
    display.blit(stso,stro)
    display.blit(Finfo.image, Finfo.rect.topleft)
    Finfo.image.blit(stso,stro)
    if Finfo.SPmeter > 0:
        pygame.draw.line(display, (127,127,255),(Finfo.rect.x + 48,Finfo.rect.y + 59),(Finfo.rect.x + linelength,Finfo.rect.y + 59),6)


def displayenemystatusbox(enemy):
    Ginfo = Enemyinfobox(enemy, (400,250))
    GHobj = pygame.font.Font('FreeSans.ttf', 16)
    Ghtso = GHobj.render(str(enemy.Chealth)+'/'+str(enemy.Mhealth)+'Hp', True, (0,0,0), None)
    Gtro = Ghtso.get_rect()
    Gtro.center = (45,20)
    display.blit(Ginfo.image2, Ginfo.rect)
    display.blit(Ghtso, (Ginfo.rect.centerx - 25,Ginfo.rect.centery -10))
    display.blit(Ginfo.image, Ginfo.rect.topleft)
xcounter = 0
timecounter = 0
timecounter2 = 0
ist = 0
alertcounter = 0
imcounter = 0
specialdraw('grayareabottom.png',80,405)
def displayupdate(players, enemies,background):
        #if background is a color or an image
        
        
        #If type == type(str)
        #display.fill((0,0,0))
        #global specialblits
        #screen.fill(background)
        
        if type(background) == type((0,0)):
            display.fill(background)
        
        updatebattlearea()

        if type(background) == type(pygame.image.load('sprites/player.png')):
            display.blit(game.background, grassbgrect)
        
        
        for i in specialblits:
            if type(i) == type({}):
                #Special restrictive draw technique.
                #jk its bad coding
                if i['elapsedframes'] >= i['frames']:
                    
                    if 'projectile' in i.keys() and i['coords'][0] <= 8 :
                        #Object termination handled here
                        
                        moo = copy.copy(i)
                        moo['elapsedframes'] = 0
                        if 'initalframes' in moo.keys():
                            moo['elapsedframes'] = copy.copy(moo['initialframes'])
                        newloc = list(copy.copy(moo['tile'].coords))
                        #print(list(copy.copy(moo['tile'].coords)),'moo')
                        if 'direction' in i.keys():
                            if i['direction'] == 'left':
                                newloc[0] -= 1
                            if i['direction'] == 'up':
                                newloc[1] -= 1
                            if i['direction'] == 'right':
                                newloc[0] += 1
                            if i['direction'] == 'down':
                                newloc[1] += 1
                            if newloc[0] == 0 or newloc[0] >= 9 or newloc[1] <= 0 or newloc[1] >= 5:
                                game.specialblits.remove(i)
                                break
                        else:
                            newloc[0] += 1
                            if newloc[0] == 9:
                                game.specialblits.remove(i)
                                break
                        #special enemy projectiles
                        if 'splitlightning' in i.keys():
                            i = 1
                            while i <= 2:
                                if i == 1:
                                    newloc[1] -= 1
                                if i == 2:
                                    newloc[1] += 2
                                    
                                for z in alltiles:
                            
                                    if z.coords == newloc:
                                            #print('found')
                                            moo['tile'] = z
                                            moo['location'] = copy.copy(z.rect.midbottom)
                                            moo['coords'] = copy.copy(z.coords)
                                if i != 2:
                                    game.specialblits.append(moo)
                                if i == 2:
                                    i = 0

                        
                        
                        for z in alltiles:
                            
                            if z.coords == newloc:
                                #print('found')
                                moo['tile'] = z
                                moo['location'] = copy.copy(z.rect.midbottom)
                                moo['coords'] = copy.copy(z.coords)
                                
                        
                        
                       
                        #print(dir(moo))
                        game.specialblits.append(moo)
                    if 'projectile' in i.keys() and (i['coords'][0] >= 9):
                        del i
                    
                    game.specialblits.remove(i)
                    continue
                x = pygame.image.load(i['image'])
                
                x.scroll(60*i['elapsedframes']*-1,0)
                y = x.get_rect()
                y.width = copy.copy(i['width'])
                #print(i.keys())
                #print(i.items())
                y.midbottom = i['location']
                #excuse the magic number, but it fixes the animation location
                y.y -= 8
                a,b = y.topleft
                moo = pygame.Rect((0,0),
                                       (y.width,
                                            y.height))
                display.blit(x,(a,b),moo)
                if i['elapsedframes'] == i['damageframe'] or i['damageframe'] == 'all':
                    i['tile'].damageflash()
                    if i['damages'] == 'player':
                        if i['tile'].occupied == True and i['tile'].occupant.isplayer and not i['tile'].occupant.invincible:
                            if i['tile'].occupant.blocking or i['tile'].occupant.blockSP:
                                i['tile'].occupant.Chealth -= 1
                                i['tile'].occupant.SPmeter += 5
                                if game.perfectblock:
                                    i['tile'].occupant.SPmeter += 5
                                    i['tile'].occupant.Cmp += (i['tile'].occupant.Mmp*.3//1)
                                if 'reflectable' in i.keys():
                                    i['direction'] = 'right'
                                    i['damages'] = 'enemy'
                                    i['elapsedframes'] = copy.copy(i['frames'])
                                i['tile'].occupant.invincible = 30
                            else:
                                damage = int(i['damage'] *(1-(0.05*i['tile'].occupant.defense)))
                                i['tile'].occupant.Chealth -= damage
                                i['tile'].occupant.invincible = 30
                            
                            if 'stagger' in i.keys():
                                i['tile'].occupant.stagger()
                                
                    if i['damages'] == 'enemy':
                        if i['tile'].occupied == True and i['tile'].occupant.isenemy and not i['tile'].occupant.guard == True and not i['tile'].occupant.invincible:
                            i['tile'].occupant.Chealth -= i['damage']
                            i['tile'].occupant.hit = True
                            #i['tile'].occupant.invincible = 30
                            #print(i.keys())
                            #time.sleep(0.5)
                            if 'stagger' in i.keys():
                                i['tile'].occupant.stagger()
                            if 'strong' in i.keys():
                                #i['tile'].occupant.guard = True
                                i['tile'].occupant.invincible = 30
                            if 'onehit' in i.keys():
                                i['elapsedframes'] = (i['frames'] - 1)
                            if 'enemyreset' in i.keys():
                                i['tile'].occupant.stratpause = True
                        if i['tile'].occupied and i['tile'].occupant.guard:
                            if 'projectile' not in i.keys():
                                i['tile'].occupant.Chealth -= (i['damage']*0.1)//1
                                i['tile'].occupant.hit = True
                                i['tile'].occupant.strat = 'blocking'
                            else:
                                i['tile'].occupant.Chealth -= i['damage']
                                
                                
                    
                        
                #display.blit(x,y)
                i['elapsedframes'] += 1
            else:
                display.blit(i[0],i[1])
        
        for i in range(1,5):
            for x in game.allchars:
                  if x.currentpos[1] == i:
                      chardraw(x)
##        if fredrick.currentpos[1] < ghostface.currentpos[1]:
##            chardraw(fredrick)
##            chardraw(ghostface)
##        else:
##            chardraw(ghostface)
##            chardraw(fredrick)
        
        for i in players:
            displaystatusbox(i)
        for i in enemies:
            displayenemystatusbox(i)
        #Makes characters 'in front' draw first.

        
def chardraw(char):
    sx, sy = char.rect.topleft
    # Only the sprite's defined width and height will be drawn
    area = pygame.Rect((0, 0),
                                       (char.rect.width,
                                            char.rect.height))
    display.blit(char.image,(sx,sy), area)

pygame.display.update()

stepcounter = 0
allowinput = True
def occupantcheck():
     for x in alltiles:
            if game.player.currentpos == x.coords:
                x.occupied = True
                x.occupant = game.player
            elif game.player.currentpos != x.coords:
                if x.occupant != game.enemy:
                    x.occupied = None
                    x.occupant = None
            if game.enemy.currentpos == x.coords:
                x.occupied = True
                x.occupant = game.enemy
            elif game.enemy.currentpos != x.coords:
                if x.occupant != game.player:
                    x.occupied = None
                    x.occupant = None
    
def Battle(playerdata,players, enemies, place, music, background,presentableitems, scene=None,gamedata=None):
    #print(playerdata)
    ##print(playerdata)
    #print(playerdata)
    #print('playerdata=',playerdata,players,enemies,place,music,background,scene,gamedata)
    
    print(background,'background')
    print(scene,'Scene')
    Make_Tiles(place)
    if scene == 'Magic Dog Encounter':
        game.check0 = False
        game.Mdogcheck1 = False
        game.Mdogcheck2 = False
    #reset all vars here
    
    game.alertinfo = None
    game.check1 = False
    game.check2 = False
    game.check3 = False
    game.current_area = place
    game.players = players
    game.player = game.players[0]
    game.player.HitsTaken = 0
    game.enemies = enemies
    game.enemy = game.enemies[0]
    game.allchars = game.players + game.enemies
    game.gamedata = gamedata
    game.presentableitems = presentableitems
    print(game.allchars)
    game.background = background
    if game.current_area == 'grass stage':
        game.background = grassbg
    game.scene = scene
    # Change if you want an intro!
    introed = True
    game.player.statsimport(playerdata)
    #reset battlefield
    game.specialblits.clear()
    
    while True:
        #print(game.players[0].mode)
        #print(game.enemies[0].stunned)
        healthcheck(players,enemies)
        if game.perfectblock:
            game.perfectblock -= 1
        if game.countdown:
            game.countdown -= 1
            if game.countdown == 0:
                moo = 'countdownchar.attr = val'
                if game.countdownchar != None:
                    moo = moo.replace('countdownchar',game.countdownchar)
                else:
                    moo = moo.replace('countdownchar','game')
                moo =  moo.replace('attr',game.countdownattribute)
                moo = moo.replace('val',game.countdownvalue)
                print(moo)
                exec(moo)
                game.countdownattribute = None
                game.countdownvalue = None
                game.countdownchar = None
            
        for i in game.enemies:
            
            if i.invincible:
                print(i.name)
                i.invincible -= 1
        if enemies[0].Chealth <= 0:
            if game.scene == 'First Battle (Starring Gray Cloak)':
                difficultyresult = copy.copy(game.difficulty)
                print(difficultyresult)
                game.gamedata.GCSkill = difficultyresult
            return
        #print(players[0].Chealth)
        if players[0].Chealth <= 0:
            if game.scene == 'First Battle (Starring Gray Cloak)':
                result = 'ded'
                game.gamedata.GCSkill = result
            return

        
        occupantcheck()
        if enemies[0].currentpos[0] > 8:
            enemies[0].currentpos[0] = 8
        if enemies[0].currentpos[0] < 0:
            enemies[0].currentpos[0] = 0
        if enemies[0].currentpos[1] < 0:
            enemies[0].currentpos[1] = 0
        if enemies[0].currentpos[1] > 4:
            enemies[0].currentpos[1] =4
            
        game.enemy.strategy()
        game.player.update()
        for i in game.enemies:
            getlocation(i)
        displayupdate(players,enemies, background)
        
        if not introed:
            intro()
            introed = True
        eventcheck()
        pygame.display.update()
        fps.tick(30)
        
def findpreference():
    print(game.player.color, 'current fredrick color')
    a, b, c = game.gamedata.emotionpoints, game.gamedata.logicpoints, game.gamedata.willpoints
    if a > b and a > c:
        preference = 'emotion'
        game.player.color = (20,20,50)
    elif b > a and b > c:
        preference = 'logic'
        game.player.color = (0,0,50)
    else:
        preference = 'will'
        game.player.color = (40,40,50)
    print(preference, 'preference')
    game.gamedata.preference = preference
ofredrick = enemy([6,2],OriginalFredrick,{'turning':[0,-170],'desirous':[0,-255]})    
ghostface = enemy([6,2], GrayCloak, {'condescension':[0,-85],'concern':[0,-510],'smirk':[0,-170]})
darknyu = enemy([5,2],DarkNyu,{})
blackcloak = enemy([6,2],BlackCloak,{})
genmu = enemy([6,2],Genmu,{})
magicdog = enemy([6,2],MagicDog,{})
wizdog = enemy([6,2],WizDog,{})
maginyu = enemy([6,2],MagiNyu,{})
swordnyu = enemy([6,2],SwordNyu,{})
fallenwarrior = enemy([6,2],FallenWarrior,{})
dark =  enemy([6,2],Dark,{})
light =  enemy([6,2],Light,{})

if __name__ == '__main__':
    alertcounter = 0
    #Do not try to import gameinfo, __init__ will fail
    #I had to improvise a dummy gameinfo for debug purposes
    from V2 import firstaidkit,stick,tonic
    
    class dummygameinfo:
        def __init__(self):
            self.items = [firstaidkit, stick,tonic]
            self.equipment = [stick]
            self.keyitems = [tonic]
            self.emotionpoints = 1
            self.logicpoints = 0
            self.willpoints = 0
            self.preference = 'logic'
            self.data = {}
    
    x = dummygameinfo()  
    global gamedata
    gamedata = x
    #Battle(Fredrick,[fredrick],[blackcloak],'grass stage',None, (0,0,0),['Stick','First Aid Kit'], 'Black Cloak Battle',x)
    #Battle(Fredrick,[fredrick],[darknyu],'gray area',None,(0,0,0),None,'First Battle',x)
    #Battle(Fredrick,[fredrick],[wizdog],'grass stage',None, (100,100,200),['Stick','First Aid Kit'], 'WizDog Encounter',x)
     #Battle(Fredrick,[fredrick],[magicdog],'grass stage',None, (100,100,200),['Stick','First Aid Kit'], 'Magic Dog Encounter',x)
    Battle(Fredrick,[fredrick],[ofredrick],'grass stage',None, (100,100,200),[], 'Original Fredrick Encounter')

    #Battle(Fredrick,[fredrick],[genmu],'grass stage',None, (100,100,200), 'First Genmu Encounter')

    #Battle(Fredrick,[fredrick],[ghostface],'grass stage',None, (129,129,254),['Stick','First Aid Kit'], 'GrassStage Gestalt',x)

    #Battle(Fredrick,[fredrick],[ghostface],'gray area',None, (0,0,0),['Stick','First Aid Kit'], 'First Battle (Starring Gray Cloak)',x)
   
    #Battle(Fredrick,[fredrick],[maginyu],'grass stage',None, (100,100,200),['Stick','First Aid Kit'], 'MagiNyu Battle',x)
    #Battle(Fredrick,[fredrick],[swordnyu],'grass stage',None, (100,100,200),['Stick','First Aid Kit'], 'SwordNyu Battle',x)
    #Battle(Fredrick,[fredrick],[fallenwarrior],'gray area',None, (0,0,0),['Stick','First Aid Kit'], 'FallenWarrior Battle',x)
    #Battle(Fredrick,[fredrick],[dark],'gray area',None, (0,0,0),['Stick','First Aid Kit'], 'Dark Battle',x)
    Battle(Fredrick,[fredrick],[light],'gray area',None, (0,0,0),['Stick','First Aid Kit'], 'Light Battle',x)


    #'grass stage', 129,129,254

