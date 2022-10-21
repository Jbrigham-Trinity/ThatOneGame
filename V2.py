from ast import Try
import pygame
import pickle
import tmx
import random    
import sys
import copy
import time
from playerconstants import bond
import playerconstants as pc
import battleroutine as battle
from playerconstants import Fredrick, Genmu

DefFredrick = copy.copy(pc.Fredrick)
DefGenmu = copy.copy(pc.Genmu)
DefPercy = copy.copy(pc.Percy)
#understand yourself
#understand others
del Genmu

pygame.init()
global AllSprites
AllSprites  = []
global fps   
fps = pygame.time.Clock()

#make sure wavs are signed 16 bit 
cursor = pygame.mixer.Sound('cursor.wav')
footstep = pygame.mixer.Sound('footstep.wav')
goat = pygame.mixer.Sound('sounds/babygoat.mp3')
spdooropen = pygame.mixer.Sound('sounds/spdooropen.mp3')
global characters
characters = pygame.sprite.Group()
global allitems
allitems = pygame.sprite.Group()
global player
player = None




    

#global chosenoption
#chosenoption = None

# Sometimes I wonder (1/11/19)
# Someday, will someone use this code to make their own levels?
# Will someone have disassembled their copy of a game
# Just to let their creative desires run rampant?
# Or would have downloaded something off the internet?
# What will they make? Why will they make it?
# Will they make money from it (Not unless I get royalties)
# Will they have a story to tell?
# These are ambitious dreams, I know.
# (Especially because it involves someone who isnt me
# understanding my code.)
class dummypartymember():
    def __init__(self,name):
        self.name = name
        
class party:
    def __init__(self, money, items, player1,player2=None,player3=None,player4=None):
        self.money = money
        self.items = []
        self.equipment = []
        self.keyitems = []
        self.players = []
        self.equipment = []
        self.bonds = []
        self.zmoves = []
        self.xmoves = []
        self.cmoves = []
        self.spmoves = []
        
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.gold = 0
        #like, the amounting of typing i'm doing
        # that lampshades my laziness
        # would have been enough effort
        # to remove the attributes and everything related to them
        # but NoooOOOOOoooo
        
        for i in [player1,player2,player3,player4]:
            if i != None:
                self.players.append(i)
        print(self.players)

        #print('Party members are:',self.players)
    def addmember(self,arg):
        #Something about this feels stupid and wrong
        if self.player2 == None:
            self.player2 = arg
        elif self.player3 == None:
            self.player3 = arg
        elif self.player4 == None:
            self.player4 = arg
        self.players = []
        for i in [player1,player2,player3,player4]:
            if i != None:
                self.players.append(i)
    def printmembers(self):
        print(self.player1,self.player2, self.player3, self.player4)
    def __len__(self):
        
        moo = 1
        #print(self.player2.name, 'name')
        if self.player2 != None:
            if self.player2.name != 'None':
                moo += 1
            
        if self.player3 != None:
            if self.player3.name != 'None':
                moo += 1
                print('player3 found')
                moo += 1
        if self.player4 != None:
            if self.player4.name != 'None':
                moo += 1
                print('Player4 found')
                moo += 1
        print(game.currentplace)
        return moo


    

def findpreference():
    #dummied?
    print(game.player.color, 'current fredrick color')
    a, b, c = gamedata.emotionpoints, gamedata.logicpoints, gamedata.willpoints
    print('emotion',a)
    print('logic',b)
    print('will',c)
    if a > b and a > c:
        preference = 'emotion'
        game.player.color = (0,0,150)
    elif b > a and b > c:
        preference = 'logic'
        game.player.color = (0,0,100)
    else:
        preference = 'will'
        game.player.color = (0,0,50)
    gamedata.preference = preference
    game.preference = preference
def modecheck():
    x = game.player.player.zattack
    y = game.player.player.xattack
    print(x,y)
    print(x.ismagic,y.ismagic)
    if x.ismagic and y.ismagic:
        game.player.player.mode = 'magic'
    elif (not x.ismagic and y.ismagic) or (x.ismagic and not y.ismagic):
        game.player.player.mode = 'dual'
    elif not x.ismagic and not y.ismagic:
        game.player.player.mode = 'sword'
    print(game.player.player.mode)
        
global Party        
Party = party(0,[], Fredrick)
Party.printmembers()
print(Party.players)
#print(len(Party))
def getitem(item):
    global party
    #printstuff(item.name + ' obtained.')
    item2 = copy.copy(item)
    Party.items.append(item2)
def limitadd(x,amount,limit):
    x += amount
    if x > limit:
        x = copy.copy(limit)
def limitsubtract(x,amount,limit):
    print(x,'before')
    x -= amount
    if x < limit:
        x = copy.copy(limit)
    print(x,'after')
class dummycharacter:
    '''
    Much easier than adding if character.name == '' everywhere.
    Holds character spot and skips dialogue and stuff.
    I'm a genius!
    '''
    def __init__(self):
        self.name = 'None'
    def askandquestion(self,*args):
        pass
    def walk(self,*args):
        pass
    def talk(self,text, *args):
        pass
    def __eq__(self,other):
        if other == None:
            return True
        else:
            return self == other
    def __ne__(self,other):
        if other == None:
            return False
        else:
            return self != other
Noone = dummycharacter()
        

class item:
    '''
    Consumables, plot stuff, etc.
    '''
    def __init__(self, name, image,itemtype,effect=None,effectcode=None,line1='Laziness detected.',line2=None,line3=None, **kwargs):
        self.name = name
        self.image = image
        self.itemtype = itemtype
        self.description = [line1,line2,line3]
        print(self.name, self.itemtype)
        self.effect = effect
        self.effectcode = effectcode
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.specialproperties = {}
        self.charges = 1
        for i in kwargs:
            if 'charges' in i.keys():
                self.charges = i['charges']

    def imageload(self):
    #This makes the class picklable, as loaded images cannot be pickled.
    # Use the function when you need to use the image of the item
    # ex. obj
        return pygame.image.load(self.image)

    def use(self,target):
        
        #antipirating method:
        #distribute copy of ThatOneGame that
        #does something nastyyyyy upon item use  
        
        

        
        exec(self.effectcode)   
class equipment(item):
    """ up right down right 
    items equipped to increase stats for battle, and/or (in some cases) to apply special buffs
    """
    def __init__(self, name, image,effect,equiptext,statboost,line1='Laziness detected.',line2=None,line3=None,specialeffect=None):
        self.name = name
        self.image = image
        self.description = [line1,line2,line3]
        self.statboost = statboost
        self.effect = effect
        self.equiptext = equiptext
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.specialboost = specialeffect
        self.equipped = False
        self.specialproperties = []
        self.itemtype = 'equipment'

    def equip(self,player):
        for i in self.effect[0]:
            if i[0] == 'attack':
                player.equipboosts.add(i[1])

        self.equipped = True
        
##shield = equipment('Shield','items/sacredstick.png','Blocking becomes more effective','Fredric')
blade = equipment('Blade','items/sacredstick.png','Attack increases by 2 levels.','Equipping the blade is almost like habit for Fredrick.',
[['attack',2]],'A traditional blade.','Not stolen nor wooden, so an improvement.')
ring = equipment('Ring', 'items/sacredstick.png','Boosts magic recharge rate by 50%', 
'Fredrick is feeling sharper.', 'Boosts magic recharge ability.','Made of gold. No magic engravings, though.')
stick = equipment('Stick','items/stickimage.png','increases attack by one half of a level.\\That\'s all...?',
'Fredrick feels like a kid again.',[['attack',0.5],['luck',4]],'Neither heavy enough to crush things','or sharp enough to slice things.',None,[['luck','+5']])
firstsword = equipment('Lost Sword','items/sacredstick.png','Increases attack by one level.',
'Let\'s see how good\\floor weapons REALLY are.',[['attack',1]],'Pretty good for a sword','you randomly found on the ground.')
sharpfirstsword = equipment('Sharp Lost Sword','items/sacredstick.png',
'Increases attack by one and a half levels.\\Swordlovers are fanatic about it.','The sword is looking forward to\\ serving its purpose.',[['attack',1.5]],'Sharpened through the pain of rejection.')
genmusword = equipment('Genmu\'s Sword','items/genmusword.png','Increases attack by one level,\\and increases luck by two.','Anata no okasan doseiai-sai','Trades a social life for power.')
sacredstick = equipment('Stick?','items/sacredstick.png','Trust me, it\'s powerful','It\'s shining! SHINING WITH POWER!',[['attack',3],['luck',5]],'Oh yes.','You\'re both weird AND lucky.','Excessively so on both ends.')
angelfeather = item('Feather','items/angelfeather.png','consumable','Resurrect when hp = 0 one time.','Incredibly soft. Smells somewhat sweet.','May not be from an animal.')
#Items, not equipment, are defined here.
firstaidkit = item('First Aid Kit', 'items/firstaidimage.png','consumable','Slightly numbs pain and increases wellbeing,\\restoring 50 hp.','target.Chealth += 50', 'Chicks dig scars.','Not that you\'ll have them if you use this.')
#angelfeather = item('Feather','items/angelfeather.png','consumable','Resurrect when hp is 0 one time.','It\'s soft. Like REALLY soft.',' You could say divinely soft...')
tonic = item('Tonic', 'items/tonicimage.png', 'consumable',"Makes Fredrick more focused and determined,\\restoring 25 mp.",'target.Cmp += 25', 'Tastes bubbly and bland.','That\'s how you know it\'s quality.')
#stick = item('Stick', 'items/stickimage.png','equipment',"target.equippedweapon = self", 'Makes a good sword.','Actually, that depends on your definition of "good".','And sword.')
Hamburger = item('Hamburger','items/hamburgerimage.png','consumable',"0",'What? A burger?')
strengthbooster = item('StrengthPlus','items/strengthbooster.png','consumable','Raises attack stat by 1. Permanently.','target.attack += 1','It smells like victory.','And sweat.')
magicbooster = item('MagicPlus','items/magicbooster.png','consumable','Raises magic stat by 1. Permanently.','target.magic += 1','Holding it makes you feel','like overthinking..')
mpboost = item("MPBoost",'items/mpbooster.png','consumable','Raises Fredrick\'s desire, boosting MP by 5.','target.player.Mmp += 5','Emanates a destructive aura.','Holding it makes Fredrick feel decisive.')
hpboost = item("HPBoost",'items/hpbooster.png','consumable','Raises Fredrick\'s will, boosting HP by 10.','target.player.Mhp += 5','Emanates an aura of creation.','Holding it makes Fredrick feel steadfast.')
choiceboost = item("Choice Boost",'items/choicebooster.png','consumable','Allows Fredrick to pursue his preferred path,\\by increasing either his mp or his hp.','choicebooster()','Emanates a gray aura.','Holding it makes Fredrick feel confident in his abilties.')

############################

#Keyitems go here.

firstorb = item('Orb?','items/firstorbimage.png','None','None','None','Ooh, shiny...')
orb = item('Skill Orb','items/firstorbimage.png','None','None','None','Contains the abilities of a legendary warrior...')
hotelcard = item('Member Card','items/hotelcard.png','None','None','None','Lets the owner stay at any hotel','for the best possible price.')
#angelfeather = item('Feather','items/angelfeather.png','None','None','It\'s soft. Like REALLY soft.',' You could say divinely soft...')

genmucharm = item('Sword Catalogue','items/swordcatalog.png','None','None','Has all the coolest swords.')
percycharm = item("CEO's card",'item/ceocard.png','None','None','Allows access to the private room.')
#lucycharm = item("Ancient Technique")

class shopitems:

    '''
    This is where the items are stored for each shop.
    '''
    def __init__(self,items):
        self.items = items
        self.futureitems = []
def shopmenu(inventory):
    menutitletext = pygame.font.Font('FreeSansBold.ttf',30)
    titles = []
    titleloc = [185,310,430]
    index = 0
    pointer.currentloc = 1
    for i in ('Buy','Talk','Exit'):
        x = menutitletext.render(i,True,(127,127,127),(69,69,69))
        y = x.get_rect()
        y.center = (titleloc[index],420)
        titles.append((x,y))
        index += 1
        
    initialrectxs = [185,320,430]
    desctext = pygame.font.Font('FreeSansBold.ttf',14)
    itemtitletext = pygame.font.Font('FreeSansBold.ttf',20)
    Done = False
    mode = 'initial'
    while not Done:
        game.tilemap.draw(game.screen)
        game.screen.blit(shoptext.image,shoptext.rect)
        if mode == 'buy':
            for i in inventory.items:
                pass
        
        if mode == 'initial':
            for i in titles:
                game.screen.blit(i[0],i[1])
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        pointer.currentloc += 1
                        if pointer.currentloc > 3:
                            pointer.currentloc = 3
                        
                    if event.key == pygame.K_LEFT:
                        pointer.currentloc -= 1
                        if pointer.currentloc < 1:
                            pointer.currentloc = 1
                    if event.key == pygame.K_z:
                        if pointer.currentloc == 1:
                            mode = 'buy'
                        if pointer.currentloc == 2:
                            mode = 'talk'
                        if pointer.currentloc == 3:
                            Done = True
                    if event.key == pygame.K_RETURN:
                        Done = True
                          
        pointer.rect.center = (initialrectxs[(pointer.currentloc-1)]-50,420)
        game.screen.blit(pointer.image, pointer.rect)
            
        #185,422 310,420 430,420
        
        

        
                
                
                    
        pygame.display.update()   
            
class gameinfo:
    ''' Easily accesses save data information
        Attributes are read from the save file.
           '''
    def __init__(self):
        self.data = []
        self.nosave = True
        try:
            
            if __name__ == '__main__':
                
                file = pickle.load(open('save1.txt','rb'))
                #except:
                #    raise AttributeError
                print('loaded file')
                for i in file.keys():
                    newattr = 'self.{1} = file[i]'
                    print(file[i],'attr')
                    newattr = newattr.replace('{1}',i)
                    print(newattr)
                    exec(newattr)
                try:
                    if self.player2:
                        if not self.player2.name == 'None':
                            Party.player2 = self.player2
                except:
                    raise
                global Fredrick
                Fredrick = copy.copy(self.player1)
                Fredrick.imageload()
                Party.player1 = Fredrick
                if self.Genmu != None:
                    global Genmu
                    Genmu = copy.copy(self.Genmu)  
                    Genmu.imageload()
                Party.zmoves = copy.copy(self.zmoves)
                Party.xmoves = copy.copy(self.xmoves)
                Party.cmoves = copy.copy(self.cmoves)
                Party.spmoves = copy.copy(self.spmoves)
    
        except:
            self.nosave = True
            print('Huh? What\'d ya do to the file?')
            print('Great. Now I gotta make a new one.')
            print('Ya better save, or else I\'ll havta do this again.')
            self.currentplace = 'place_of_judgement.tmx'
##            try:
##                if self.player2:
##                    if self.player.name == 'None':
##                        self.player2 = None
##            except AttributeError:
##                pass
            self.emotionpoints = 0
            self.logicpoints = 0
            self.willpoints = 0
            self.items = []
            self.choices = []
            self.Genmu = DefGenmu
            self.Fredrick = DefFredrick
            #Party.items.append(firstaidkit)
            #Party.items.append(tonic)
            #Party.equipment.append(stick)
            self.items = Party.items
           # Party.player1.zattack = pc.slicer
           # Party.player1.xattack = pc.quickslice
           # Party.player1.spattack = pc.meteor
           # Party.zattacks = [pc.slicer]
           # Party.mattacks = [pc.quickslice]
           # Party.spattack = [pc.meteor]
           # Party.player1.equippedweapon = stick
            self.events = {}
            
             #'currentplace',game.currentplace],['emotionpoints',gamedata.emotionpoints],
            #    ['logicpoints',gamedata.logicpoints],['willpoints',gamedata.willpoints], ['items',Party.items]]
        
    def load(self):
        '''
        Reads the data from the save file
        and writes it to gameinfo for later use.
        Or, in other words, loads the save file.
        (Also, it just calls the init function again.)
        '''
        self.__init__()
gamedata = gameinfo()  
grasstownweaponshop = shopitems([[sacredstick,2000],[sacredstick,2000],[sacredstick,2000]])
class textbox:
    '''
    Where text is drawn to the screen.
    '''
    def __init__(self, rect, image):
        self.rect = pygame.rect.Rect(rect)
        self.image = pygame.image.load(image)
        print('rect center', self.rect.center)

text = textbox((50,350,450,100), 'textbox.png')
print(text.rect.center,'text center')
shoptext = textbox((0,0,530,200),'shopmenu.png')

class choicepointer:
    '''
    Helps the player know what choice they're making.
    '''
    def __init__(self,rect,image, currentloc=0):
        self.rect = pygame.rect.Rect(rect)
        self.image = pygame.image.load(image)
        self.currentloc = currentloc
global pointer
pointer = choicepointer((text.rect.topleft[0],300,15,15),'pointer.png')
cursorcleaner = pygame.image.load('cursorcleaner.png')
class menu:
    def __init__(self,image, icon1, icon2, icon3,icon4):
        #Items, equipmentstatus, settings.
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.icon1image = pygame.image.load(icon1)
        self.icon1rect = self.icon1image.get_rect()
        self.icon1default = self.icon1image.copy()
        self.icon1image = self.icon1default
        self.icon1rect.x = 90
        self.icon1rect.y = 15
        self.icon2image = pygame.image.load(icon2)
        self.icon2rect = self.icon2image.get_rect()
        self.icon2default = pygame.image.load(icon2)
        self.icon2rect.x = 175
        self.icon2rect.y = 15
        self.icon3image = pygame.image.load(icon3)
        self.icon3rect = self.icon3image.get_rect()
        self.icon3default = pygame.image.load(icon3)
        self.icon3rect.x = 260
        self.icon3rect.y = 15
        self.icon4image = pygame.image.load(icon4)
        self.icon4rect = self.icon4image.get_rect()
        self.icon4default = pygame.image.load(icon4)
        self.icon4rect.x = 345
        self.icon4rect.y = 15
        self.current_cursor = 1
        self.statusscreen = pygame.image.load('stats.png')
        self.statusrect = self.statusscreen.get_rect()
        self.itemscreen = pygame.image.load('Items.png')
        self.itemrect = self.itemscreen.get_rect()
        self.equipscreen = pygame.image.load('equipmenu.png')
        self.equiprect = self.equipscreen.get_rect()
        self.worldscreen = pygame.image.load('world.png')
        self.worldrect = self.worldscreen.get_rect()
        self.glove = pygame.image.load('glove.png')
        self.gloverect = self.glove.get_rect()
        self.gloveloc = 1
        self.quickstats = pygame.image.load('quickstats.png')
        self.quickstatsrect = self.quickstats.get_rect()
        self.quickstatsimagedefault = self.quickstats.copy()
        #print('Quick stats rect :', self.quickstatrect)
    def retract_menu(self):
        global game
        for i in range(1,17):
                #print(self.rect.bottomleft, 'V@')
                self.rect.y = 0 -(i*12)
                game.tilemap.draw(game.screen)
                #print(i, self.rect.y)
                game.screen.blit(self.image,self.rect)
                pygame.display.update()
                fps.tick(60)
        self.current_cursor = 1
                
    def menushow(self):
        global game
        done = False
        self.rect.bottomleft = (45,-200)#idk
        print(self.rect.y)
        for i in range(-15,1):
            self.rect.y = i*12
            print(i,self.rect.y)
            game.screen(self.image,self.rect)
            pygame.display.update()
            fps.tick(60)
        print(self.rect.y)
    def world_menu(self):
        done = False
        game.BlackOut()
        
        font = pygame.font.Font('FreeSans.ttf',18)
        levelfont = pygame.font.Font('FreeSansBold.ttf',20)
        bigfont = pygame.font.Font('FreeSansBold.ttf',30)
        mode = 'select'
        choice = 1
        currentloc = 1
        
        while not done:
            game.screen.blit(self.worldscreen,self.worldrect)
            #print(mode)
            #print(self.gloverect)
            if mode == 'select':
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_x):
                        done = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            choice -= 1
                            if choice <= 0:
                                choice = 1
                        if event.key == pygame.K_RIGHT:
                            choice += 1
                            if choice >= 4:
                                choice = 3
                        if event.key == pygame.K_z:
                            self.gloveloc = 1
                                
                            if choice == 1:
                                mode = 'bonds'
                            if choice == 2:
                                pass
                                #mode = 'messages'
                            if choice == 3:
                                pass
                                #mode = 'settings'
                        if event.key == pygame.K_x:
                            if mode == 'bonds':
                                mode = 'select'
                        
                if mode == 'select':
                    if choice == 1:
                        word = 'bonds'
                    if choice == 2:
                        word = 'messages'
                    if choice == 3:
                        word = 'settings'
                    current = bigfont.render(word,True,(127,127,127),(69,69,69))#ha funnee number
                    currect = current.get_rect()
                    currect.center = (315,65)
                    game.screen.blit(current,currect)
            
            if mode == 'bonds':
                x = 0
                for i in Party.bonds:
                    bondimage = pygame.image.load(i.image)
                    imagerect = bondimage.get_rect()
                    imagerect.center = [155,(145 + (67*x))]
                    bondtext = font.render(i.desc[(i.level-1)], True, (255, 255,255), (48,48,48))
                    textrect = bondtext.get_rect()
                    textrect.center = [360,(140 +(67*x))]
                    bondlevel = levelfont.render(str(i.level),True, (100,200,200),(48,48,48))
                    bondrect = bondlevel.get_rect()
                    bondrect.center = [360, (160+(67*x))]
                    game.screen.blit(bondtext,textrect)
                    game.screen.blit(bondimage,imagerect)
                    game.screen.blit(bondlevel,bondrect)
                    
                    x += 1
                
                for i in pygame.event.get():
                    if i.type == pygame.KEYUP:
                        
                        if i.key == pygame.K_z:
                            
                            if len(Party.bonds) > 0:
                                mode = 'bondselect'
                                if self.gloveloc == 1:
                                    chosenbond = Party.bonds[0]
                                if self.gloveloc == 2:
                                    chosenbond = Party.bonds[1]
                                if self.gloveloc == 3:
                                    chosenbond = Party.bonds[2]
                                if self.gloveloc == 4:
                                    chosenbond = Party.bonds[3]
                                assert chosenbond
                        if i.key == pygame.K_UP:
                            self.gloveloc -= 1
                            if self.gloveloc <= -1:
                                self.gloveloc = 0
                        if i.key == pygame.K_DOWN:
                            self.gloveloc += 1
                            if self.gloveloc >= 5 or self.gloveloc >= len(Party.bonds):
                                self.gloveloc = (len(Party.bonds))
                        if i.key == pygame.K_RETURN or i.key == pygame.K_x:
                            mode = 'select'
                #screen.blit(self.glove,self.gloverect)          
                #for z in [1,2,3,4]:
                #    print(self.gloveloc)
                ##    if self.gloveloc == z:
                #        self.gloverect.center = [95,(95+(50*z))]
                if self.gloveloc == 1:
                    self.gloverect.center = [95,145]
                if self.gloveloc == 2:
                    self.gloverect.center = [95,215]
                if self.gloveloc == 3:
                    self.gloverect.center = [95,280]
                if self.gloveloc == 4:
                    self.gloverect.center = [95,345]
                game.screen.blit(self.glove,self.gloverect)
                
                
                        
            if mode == 'bondselect':
                
                print(self.gloveloc)
                x = 0
                for i in Party.bonds:
                    bondimage = pygame.image.load(i.image)
                    imagerect = bondimage.get_rect()
                    imagerect.center = [155,(145 + (67*x))]
                    bondtext = font.render(i.desc[(i.level-1)], True, (255, 255,255), (48,48,48))
                    textrect = bondtext.get_rect()
                    textrect.center = [360,(140 +(67*x))]
                    bondlevel = levelfont.render(str(i.level),True, (100,200,200),(48,48,48))
                    bondrect = bondlevel.get_rect()
                    bondrect.center = [360, (160+(67*x))]
                    game.screen.blit(bondtext,textrect)
                    game.screen.blit(bondimage,imagerect)
                    game.screen.blit(bondlevel,bondrect)
                    x += 1
                x = 1
                for i in ['Info','Call','Effects']:
                    moo = font.render(i,True,(127,127,127),(0,0,0))
                    moorect = moo.get_rect()
                    moorect.center = [(50+135*x),420]
                    game.screen.blit(moo,moorect)
                    x += 1
                   
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_x or event.key == pygame.K_RETURN:
                            mode = 'bonds'
                            self.gloveloc = 1
                        if event.key == pygame.K_RIGHT:
                            self.gloveloc += 1
                            if self.gloveloc >= 4:
                                self.gloveloc = 3
                        if event.key == pygame.K_LEFT:
                            self.gloveloc -= 1
                            if self.gloveloc == 0:
                                self.gloveloc = 1
                        if event.key == pygame.K_z:
                            if self.gloveloc == 1:
                                chosenbond.info()
                            if self.gloveloc == 2:
                                chosenbond.call()
                            if self.gloveloc == 3:
                                chosenbond.effects()
                print(self.gloveloc)
                if self.gloveloc == 1:
                    self.gloverect.center = [120,422]
                if self.gloveloc == 2:
                    self.gloverect.center = [250,422]
                if self.gloveloc == 3:
                    self.gloverect.center = [380,422]
                    
                game.screen.blit(self.glove,self.gloverect)
                #pygame.display.update()
            pygame.display.update()
                
        game.BlackOut()
        screenupdate()
            
                    
                
                
           
    def show_menu(self):
        global game
        done = False
        self.rect.bottomleft = (45,-200)#idk
        print(self.rect.y)
        for i in range(-15,1):
            self.rect.y = i*12
            #print(i,self.rect.y)
            game.screen.blit(self.image,self.rect)
            pygame.display.update()
            fps.tick(60)
        #print(self.rect.y)

        print('okay')     
        while not done:
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    done = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.current_cursor -= 1
                        if self.current_cursor <= 0:
                            self.current_cursor = 1
                    if event.key == pygame.K_RIGHT:
                        self.current_cursor += 1
                        if self.current_cursor >= 5:
                            self.current_cursor = 4
                    if event.key == pygame.K_z:
                        if self.current_cursor == 1:
                            self.item_menu()
                        elif self.current_cursor == 2:
                            self.equip_menu()
                        elif self.current_cursor == 3:
                            self.status_menu()
                        elif self.current_cursor == 4:
                            self.world_menu()
                
        self.retract_menu()
        print('Should\'ve triggered.')
        
    def status_menu(self):
        '''
        Shows character status.
        Also makes sarcastic quips occasionally.
        '''
        global game
        global Party
        game.BlackOut()
        game.screen.blit(self.statusscreen, self.statusrect)
        pygame.display.update()
        finished = False
        titlefont = pygame.font.Font('FreeSansBold.ttf', 23)
        descfont = pygame.font.Font('FreeSansBold.ttf', 18)
        font = pygame.font.Font('FreeSans.ttf',14)
        current_character = 1
        last_character = 0
        
        while not finished:
            if current_character != last_character:
                if current_character == 1:
                    char = Party.player1
                elif current_character == 2:
                    char = Party.player2.character
            Name = titlefont.render(char.name, True, (255,255,255),(48,48,48))
            NameRect = Name.get_rect()
            NameRect.center = (426, 155)
            # I apologize for the repetitive typing. I'm just too lazy.

            # which is ironic.
            game.screen.blit(self.statusscreen, self.statusrect)
            game.screen.blit(Name, NameRect)
            #print(char.current_title)
            Title = titlefont.render(char.current_title.name, True, (223,223,223), (32,32,32))
            TitleRect = Title.get_rect()
            TitleRect.center =(422,204)
            game.screen.blit(Title, TitleRect)
            desc1 = descfont.render(char.current_title.desc1, True, (255, 255,255), (48,48,48))
            desc1Rect = desc1.get_rect()
            desc1Rect.center = (422, 230)
            game.screen.blit(desc1, desc1Rect)
            desc2 = descfont.render(char.current_title.desc2, True, (255, 255,255), (48,48,48))
            desc2Rect = desc2.get_rect()
            desc2Rect.center = (422, 255)
            game.screen.blit(desc2, desc2Rect)
            desc3 = descfont.render(char.current_title.desc3, True, (255, 255,255), (48,48,48))
            desc3Rect = desc3.get_rect()
            desc3Rect.center = (422, 280)
            game.screen.blit(desc3, desc3Rect)
            #250, 270
            Health = font.render('Health:' , True, (255, 255, 255), (32,32,32))
            HealthRect = Health.get_rect()
            HealthRect.center = (260, 325)
            game.screen.blit(Health, HealthRect)
            HStat = font.render(str(char.Chealth)+'/'+str(char.Mhealth), True, (0,0,0), (101,101,101))
            HStatRect = HStat.get_rect()
            HStatRect.center = (340, 325)
            game.screen.blit(HStat, HStatRect)
            MP = font.render('MP(???):' , True, (255, 255, 255), (32,32,32))
            MPRect = MP.get_rect()
            MPRect.center = (417, 325)
            game.screen.blit(MP, MPRect)
            MPStat = font.render(str(char.Cmp)+'/'+str(char.Mmp), True, (0,0,0), (101,101,101))
            MPStatRect = MPStat.get_rect()
            MPStatRect.center = (495, 325)
            game.screen.blit(MPStat, MPStatRect)
            Attack = font.render('Attack' , True,(255, 255, 255), (32,32,32))
            AttackRect = Attack.get_rect()
            AttackRect.center = (260, 356)
            game.screen.blit(Attack, AttackRect)
            if char.preference == 'strength':
                AStat = font.render(str(char.attack) , True, (130,0,255), (101,101,101))
            else:
                AStat = font.render(str(char.attack) , True, (0,0,0), (101,101,101))
            AStatRect = AStat.get_rect()
            AStatRect.center = (340, 356)
            game.screen.blit(AStat, AStatRect)
            Magic = font.render('Magic:' , True, (255, 255, 255), (32,32,32))
            MagicRect = Magic.get_rect()
            MagicRect.center = (417, 356)
            game.screen.blit(Magic, MagicRect)
            if char.preference == 'magic':
                MStat = font.render(str(char.magic) , True, (0,130,255), (101,101,101))
            else:
                MStat = font.render(str(char.magic) , True, (0,0,0), (101,101,101))
            MStatRect = MStat.get_rect()
            MStatRect.center = (495, 356)
            game.screen.blit(MStat, MStatRect)
            Defense = font.render('Defense:' , True, (255, 255, 255), (32,32,32))
            DefenseRect = Defense.get_rect()
            DefenseRect.center = (260, 387)
            game.screen.blit(Defense, DefenseRect)
            DStat = font.render(str(char.defense) , True, (0,0,0), (101,101,101))
            DStatRect = DStat.get_rect()
            DStatRect.center = (340, 387)
            game.screen.blit(DStat, DStatRect)
            MDefense = font.render('Magic Def :' , True, (255, 255, 255), (32,32,32))
            MDefenseRect = MDefense.get_rect()
            MDefenseRect.center = (417, 387)
            game.screen.blit(MDefense, MDefenseRect)
            MDStat = font.render(str(char.Mdefense) , True, (0,0,0), (101,101,101))
            MDStatRect = MDStat.get_rect()
            MDStatRect.center = (495, 387)
            game.screen.blit(MDStat, MDStatRect)
            Speed = font.render('Speed:'  , True, (255, 255, 255), (32,32,32))
            SpeedRect = Speed.get_rect()
            SpeedRect.center = (260, 418)
            game.screen.blit(Speed, SpeedRect)
            SStat = font.render(str(char.speed) , True, (0,0,0), (101,101,101))
            SStatRect = SStat.get_rect()
            SStatRect.center = (340, 418)
            game.screen.blit(SStat, SStatRect)
            Luck = font.render('Luck:' , True, (255, 255, 255), (32,32,32))
            LuckRect = Luck.get_rect()
            LuckRect.center = (417, 418)
            game.screen.blit(Luck, LuckRect)
            LStat = font.render(str(char.luck) , True, (0,0,0), (101,101,101))
            LStatRect = LStat.get_rect()
            LStatRect.center = (495, 418)
            game.screen.blit(LStat, LStatRect)
            Level = font.render('Level:'  , True, (255, 255, 255), (32,32,32))
            LevelRect = Speed.get_rect()
            LevelRect.center = (260, 449)
            game.screen.blit(Level, LevelRect)
            LvStat = font.render(str(char.level) , True, (0,0,0), (101,101,101))
            LvStatRect = LvStat.get_rect()
            LvStatRect.center = (340, 449)
            game.screen.blit(LvStat, LvStatRect)
            Exp = font.render('Exp to next:' , True, (255, 255, 255), (32,32,32))
            ExpRect = Exp.get_rect()
            ExpRect.center = (417, 449)
            game.screen.blit(Exp, ExpRect)
            EStat = font.render(str( char.exp), True, (0,0,0), (101,101,101))
            EStatRect = EStat.get_rect()
            EStatRect.center = (495, 449)
            game.screen.blit(EStat, EStatRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        current_character -= 1
                        if current_character <= 0:
                            current_character = 1
                    elif event.key == pygame.K_RIGHT:
                        current_character += 1
                        if current_character >= len(Party):
                            current_character = len(Party)
                    if event.key == pygame.K_RETURN or event.key == pygame.K_x:
                        finished = True
        game.BlackOut()
        screenupdate()
        
    
                
            
    def equip_menu(self):
        global game
        global party
        game.BlackOut()
        game.screen.blit(self.equipscreen,self.equiprect)
        finished = False
        selected = 'Zmoves'
        self.gloverect.center = (180,180)
        self.current_cursor = 1
        self.gloveloc = 1

        selecteditem = None
        itemset = None
        gesfont = pygame.font.Font('FreeSansBold.ttf',35)
        titlefont = pygame.font.Font('FreeSansBold.ttf', 20)
        
        descfont = pygame.font.Font('FreeSansBold.ttf', 12)
        font = pygame.font.Font('FreeSans.ttf',15)
        moveselect = False
        while not finished:
            game.screen.blit(self.equipscreen,self.equiprect)
            
            if game.player.player.mode ==  'sword':
                gestalt = 'Sword'
            elif game.player.player.mode == 'magic':
                gestalt = 'Magic'
            elif game.player.player.mode == 'dual':
                gestalt = 'Dual'
            gfont = gesfont.render(gestalt, True, (0,0,0), (101,101,101))
            grect = gfont.get_rect()
            grect.center = (332,100)
            game.screen.blit(gfont,grect)
            zmove = titlefont.render(Party.player1.zattack.name,True,(0,0,0),(101,101,101))
            zrect = zmove.get_rect()
            zrect.midleft = (210,180)
            game.screen.blit(zmove,zrect)
            xmove = titlefont.render(Party.player1.xattack.name,True,(0,0,0),(101,101,101))
            xrect = xmove.get_rect()
            xrect.midleft = (210,248)
            game.screen.blit(xmove,xrect)
            cmove = titlefont.render(Party.player1.cattack.name,True,(0,0,0),(101,101,101))
            crect = cmove.get_rect()
            crect.midleft = (210,316)
            game.screen.blit(cmove,crect)
            spmove = titlefont.render(Party.player1.spattack.name,True,(0,0,0),(101,101,101))
            sprect = spmove.get_rect()
            sprect.midleft = (210,385)
            game.screen.blit(spmove,sprect)
            #special info location center is 446 355
            
                                           
            for event in pygame.event.get():
                print('buttoncheck')
                menu_state = 'none'
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_x:
                        if menu_state == 'none':
                            finished = True
                       
                #print('mid loop')
               
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.gloveloc -= 1
                        if self.gloveloc <= 0:
                            self.gloveloc = 1
                    if event.key == pygame.K_DOWN:
                        self.gloveloc += 1
                        if not moveselect:
                            if self.gloveloc >= 5:
                                self.gloveloc = 4
                        else:
                            if self.gloveloc > len(itemset):
                                self.gloveloc = len(itemset)
                    if event.key == pygame.K_z:
                        try:
                            menu_state = 'moves'
                            if moveselect:
                            #print(selectedmove)
                                if selectedmove == None:
                                    raise UnboundLocalError
                                if selected == 'Zmoves':
                                    Party.player1.zattack = selectedmove
                                if selected == 'Xmoves':
                                    Party.player1.xattack = selectedmove
                                if selected == 'Cmoves':
                                    Party.player1.cattack = selectedmove
                                if selected == 'Special Moves':
                                    Party.player1.spattack = selectedmove
                            if not moveselect:
                                moveselect = True
                                if self.gloveloc == 1:
                                    
                                    itemset = Party.zmoves
                                if self.gloveloc == 2:
                                    
                                    itemset = Party.xmoves
                                if self.gloveloc == 3:
                                    
                                    itemset = Party.cmoves
                                if self.gloveloc == 4:
                                    itemset = Party.spmoves
                                
                                self.gloveloc = 1
                        except UnboundLocalError:
                            selectedmove = None
                        
                        
                    if event.key == pygame.K_x:
                        moveselect = False
                        self.gloveloc = 1
                        itemset = None
                        menu_state = 'none'
                    
            if moveselect:
                itemlist = []
                z = 1
                for i in itemset:
                    movename = font.render(i.name,True,(0,0,0),(101,101,101))
                    moverect = movename.get_rect()
                    moverect.midleft = (370,(140+(z*30)))
                    moveset = [moverect,i]
                    itemlist.append(moveset)
                    game.screen.blit(movename,moverect)
                    z += 1
            if finished == True:
                
                game.BlackOut()
                screenupdate()
                break
            if not moveselect:
                if self.gloveloc == 1:
                    self.gloverect.center = (180,180)
                    selected = 'Zmoves'
                if self.gloveloc == 2:
                    self.gloverect.center = (180,248)
                    selected = 'Xmoves'
                if self.gloveloc == 3:
                    selected = 'Cmoves'
                    self.gloverect.center = (180,316)
                if self.gloveloc == 4:
                    selected = 'Special Moves'
                    self.gloverect.center = (180,385)
                    
            if moveselect:
                for i in range(0,(len(itemset))):
                    print(i)
                    if (self.gloveloc-1) == i:
                        print(i)
                        self.gloverect.midright = copy.copy(itemlist[i][0].midleft)
                        self.gloverect.x -= 20
                        selectedmove = itemlist[i][1]
                        
            screen.blit(self.glove,self.gloverect)
            if not moveselect:
                if selected == 'Zmoves':
                    x = Party.player1.zattack.desc1
                    y = Party.player1.zattack.desc2
                    z = Party.player1.zattack.desc3
                    a = Party.player1.zattack.desc4
                    b = Party.player1.zattack
                if selected == 'Xmoves':
                    x = Party.player1.xattack.desc1
                    y = Party.player1.xattack.desc2
                    z = Party.player1.xattack.desc3
                    a = Party.player1.xattack.desc4
                    b = Party.player1.xattack
                if selected == 'Cmoves':
                    x = Party.player1.cattack.desc1
                    y = Party.player1.cattack.desc2
                    z = Party.player1.cattack.desc3
                    a = Party.player1.cattack.desc4
                    b = Party.player1.cattack
                if selected == 'Special Moves':
                    x = Party.player1.spattack.desc1
                    y = Party.player1.spattack.desc2
                    z = Party.player1.spattack.desc3
                    a = Party.player1.spattack.desc4
                    b = Party.player1.spattack
                
                
                desc1 = descfont.render(x,True,(0,0,0),(101,101,101))
                rect1 = desc1.get_rect()
                rect1.center = (433,180)
                screen.blit(desc1, rect1)
                desc2 = descfont.render(y,True,(0,0,0),(101,101,101))
                rect2 = desc2.get_rect()
                rect2.center = (433,210)
                screen.blit(desc2,rect2)
                desc3 = descfont.render(z,True,(0,0,0),(101,101,101))
                rect3 = desc2.get_rect()
                rect3.center = (433,240)
                screen.blit(desc3,rect3)
                desc4 = descfont.render(a,True,(0,0,0),(101,101,101))
                rect4 = desc2.get_rect()
                rect4.center = (433,270)
                screen.blit(desc4,rect4)
                if b.ismagic:
                    if b.alignment == 'creation':
                        descfont.render('Creation Magic',True,(200,200,200),(101,101,101))
                    if b.alignment == 'destruction':
                        descfont.render('Destruction Magic',True,(50,50,50),(101,101,101))
                
                
            pygame.display.update()
        if finished:
            modecheck()
            
            
            
        
    def item_menu(self):
        '''
        The items screen, obviously.
        Handles item management, with generous use of loops.
        But aren't most things a loop?
        '''
        global game
        global party
        self.current_cursor = 0
        self.gloveloc = 1
        self.gloverect.center = (85,95)
        game.BlackOut()
        game.screen.blit(self.itemscreen, self.itemrect)
        pygame.display.update()
        finished = False
        
        titlefont = pygame.font.Font('FreeSans.ttf', 25)
        descfont = pygame.font.Font('FreeSans.ttf', 18)
        font = pygame.font.Font('FreeSans.ttf',16)
        finished = False
        selected = None
        itemchosen = False
        
        while not finished:
            game.screen.blit(self.itemscreen, self.itemrect)
            for i in (['Items',157],['Equipment',325],['Key Items',494]):
               
                if i == selected:
                    color = (100,100,100)
                else:
                    color = (127,127,127)
                    
                title = titlefont.render(i[0],True, (color),(48,48,48))
                titlerect = title.get_rect()
                titlerect.center = (i[1],94)
                game.screen.blit(title,titlerect)
            for event in pygame.event.get():
                #print('mid loop')
                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    finished = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.gloveloc -= 1
                        if self.current_cursor <= 0:
                            self.current_cursor = 1
                        if self.gloveloc <= 0:
                            self.gloveloc = 1
                    if event.key == pygame.K_RIGHT:
                        self.gloveloc += 1
                        if self.current_cursor >= 4:
                            self.current_cursor = 3
                        if self.gloveloc >= 4:
                            self.gloveloc = 3
                    if event.key == pygame.K_z:
                        
                        if self.gloveloc <= 1:
                            selected = 'Items'
                            itemset = Party.items
                        if self.gloveloc >= 3:
                            selected = 'Key Items'
                            itemset = Party.keyitems
                        if self.gloveloc == 2:
                            selected = 'Special'
                            itemset = Party.equipment
                        
                        print(self.gloveloc)
                        index = -1
                        itemlist= []
                        itemreblit = []
                        pointloc = 0
                        itemselect = True
                        #First entry must be zero.
                        while itemselect:
                            game.screen.blit(self.itemscreen, self.itemrect)
                            for i in (['Items',157],['Equipment',325],['Key Items',494]):
                                if i == selected:
                                    color = (100,100,100)
                                else:
                                    color = (127,127,127)

                                title = titlefont.render(i[0],True, (color),(48,48,48))
                                titlerect = title.get_rect()
                                titlerect.center = (i[1],94)
                                game.screen.blit(title,titlerect)
                            for i in itemset:
                                #print(i.name)
                                index += 1
                               # print(index)
                                if i == Party.player1.equippedweapon:
                                    x = (250,250,250)
                                elif i == Party.player1.equippedarmor:
                                    x = (100,100,100)
                                elif i == Party.player1.equippedspecial:
                                    x = (250,250,250)
                                else:
                                    x = (127,127,127)                               
                                itemtitle = descfont.render(i.name,True, x,(48,48,48))
                                itemrect = itemtitle.get_rect()
                                #Excuse my hard coding for location of the words.
                                if index % 2 == 0:
                                    itemrect.left = 100
                                else:
                                    itemrect.left = 354
                                copyindex = (index // 2)
                                #print(copyindex, 'is copyindex.')
                                # Two items per line.
                                itemrect.centery = (30 * copyindex) + 150
                                moo = [copy.copy(index),copy.copy(itemrect),i]
                                itemlist.append(moo)
                                #print(itemrect)
                                itemreblit.append([itemtitle,itemrect])
                                game.screen.blit(itemtitle,itemrect)
                            index = -1
                            for event in pygame.event.get():
                                if event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_x):
                                    selected = None
                                    itemselect = False
                                if event.type == pygame.KEYUP:
                                    if event.key == pygame.K_LEFT:
                                        pointloc -= 1
                                        if pointloc <= -1:
                                            pointloc = 0
                                    if event.key == pygame.K_UP:
                                        lastpoint = copy.copy(pointloc)
                                        pointloc -= 2
                                        if pointloc <= -1:
                                            pointloc = lastpoint
                                    if event.key == pygame.K_RIGHT:
                                        pointloc += 1
                                        #print(pointloc, len(itemlist))
                                        if pointloc >= len(itemlist):
                                            pointloc = len(itemlist)-1
                                    if event.key == pygame.K_DOWN:
                                        lastpoint = copy.copy(pointloc)
                                        pointloc += 2
                                        if pointloc >= len(itemlist):
                                            pointloc = lastpoint
                                

                                        
                                    if event.key == pygame.K_z:
                                        #if selected == keyitems
                                        if itemset == Party.keyitems:
                                            pass
                                        else:
                                            itemchosen = True
                                    #if event.key == pygame.K_RETURN:
                                    #    itemselect = False
                            for i in itemlist:
                                #i is a list that contains the item's index, the items rect
                                # and the item itself, in that order.
                                if i[0] == pointloc:
                                    #print(i,'I?')
                                    if itemchosen:
                                        
                                        if i[2].itemtype == 'consumable':
                                            x = 'use'
                                        elif i[2].itemtype == 'equipment':
                                            x = 'equip'
                                        
                                        finished = 0
                                        y = 0
                                        choiceloc = 0
                                        choices = []
                                        while not finished:
                                            #print(finished,'?')
                                            y += 1
                                            print(x,'x?')
                                            choicelist = [x,'info','drop']
                                            #game.screen.blit(self.itemscreen, self.itemrect)
                                            game.screen.blit(self.itemscreen, self.itemrect)
                                            for q in (['Items',157],['Equipment',325],['Key Items',494]):
                                                print('drew titles')
                                                if q == selected:
                                                    color = (100,100,100)
                                                else:
                                                    color = (127,127,127)
                                                    
                                                title = titlefont.render(q[0],True, (color),(48,48,48))
                                                titlerect = title.get_rect()
                                                titlerect.center = (q[1],94)
                                                game.screen.blit(title,titlerect)
                                           
                                            for z in itemreblit:
                                               
                                                game.screen.blit(z[0],z[1])
                                                
                                            for h in choicelist:
                                                
                                                Choice = titlefont.render(h,True,(150,150,150),(0,0,0))
                                                Choicerect = Choice.get_rect()
                                                Choicerect.center = (170 + (y*100), 425)
                                                #print(Choicerect.center, 'H')
                                                screen.blit(Choice,Choicerect)
                                                choices.append([Choice,Choicerect])
                                                y += 1
                                            o = i[2].imageload()
                                            imgrect = o.get_rect()
                                            imgrect.topleft = (53, 392)
                                            screen.blit(o, imgrect)
                                            for event in pygame.event.get():
                                                if event.type == pygame.KEYUP:
                                                    if event.key == pygame.K_LEFT:
                                                        choiceloc -= 1
                                                        if choiceloc <= -1:
                                                            choice = 0
                                                        continue
                                                    if event.key == pygame.K_RIGHT:
                                                        choiceloc += 1
                                                        if choiceloc  >= 3:
                                                            choiceloc = 2
                                                        continue
                                                    if event.key == pygame.K_z:
                                                        #how deep can we go???
                                                        selchoice = choicelist[choiceloc]
                                                        #print(selchoice)

                                                        if selchoice == 'use':
                                                            i[2].use(Party.player1)
                                                            #print(i[2].effect)
                                                            #Item used
                                                            if i[2].itemtype == 'consumable':
                                                                for thing in Party.items:
                                                                    print(i[2],thing)
                                                                    if i[2] == thing:
                                                                        print('found')
                                                                        Party.items.remove(i[2])
                                                                        itemchosen = None
                                                                        finished = True
                                                                        #del x
                                                        if selchoice == 'equip':
                                                            printstuff(i[2].equiptext)
                                                            Party.player1.equippedweapon = i[2]
                                                            Party.player1.stat_recalculate()
##                                                            Party.players[0].equippedweapon = i[2]
##                                                            Party.players[0].stat_recalculate()
                                                            itemchosen = None
                                                            finished = True
                                                        if selchoice == 'drop':
                                                            if i[2].itemtype == 'consumable':
                                                                for thing in Party.items:
                                                                    print(i[2],thing)
                                                                    if i[2] == thing:
                                                                        print('found')
                                                                        Party.items.remove(i[2])
                                                                        itemchosen = False
                                                                        finished = True
                                                                        break
                                                            elif i[2].itemtype == 'equipment':
                                                                for thing in Party.equipment:
                                                                    print(i[2],thing)
                                                                    if i[2] == thing:
                                                                        print('found')
                                                                        Party.equipment.remove(i[2])
                                                                        itemchosen = False
                                                                        finished = True
                                                                        break
                                                                        #return
                                                            
                                                            
                                                        if selchoice == 'info':
                                                            printstuff(i[2].effect)
                                                            pygame.display.update()
                                                        
                                                                    
                                                                                        
                                                            
                                                                
                                                                
                                                            
                                                        
                                                    if event.key == pygame.K_RETURN or event.key == pygame.K_x:
                                                        finished = True
                                                        itemchosen = False
                                                        
                                                        
                                            currentchoice = choices[choiceloc][1]
                                            self.gloverect.center = currentchoice.center
                                            self.gloverect.x -= 50
                                            game.screen.blit(self.glove, self.gloverect)
                                            
                                            y = 0
                                            pygame.display.update()
                                            
                                            
                                            
                                        
                                    #else:
                                    #print(i)   
                                   # print(i[0], pointloc, 'item info')
                                    self.gloverect.x = i[1].x
                                    self.gloverect.y = i[1].y
                                    self.gloverect.left -= 30
                                    lines = [i[2].line1, i[2].line2,i[2].line3]
                                    
                                    if i[2].line3 != None:
                                        pass
                                    elif i[2].line2 != None:
                                        lines.pop() #removes last member of list
                                        #really? the only piece of code people probably understand is the one i comment on?
                                    m = 0
                                    for x in lines:
                                        #print(x,'x')
                                        if x == None:
                                            pass
                                        desc = font.render(x,True, (172,172,172), (32,32,32))
                                        descrect = desc.get_rect()
                                        descrect.center = (370, 410+(m*25))
                                        #desclist = 
                                        screen.blit(desc, descrect)
                                        m += 1    
##                                    desc = font.render(i[2].description,True, (172,172,172), (32,32,32))
##                                    descrect = desc.get_rect()
##                                    descrect.center = (370,423)
##                                    screen.blit(desc, descrect)
                                    #print(i[2].image,'moo')
                                    x = i[2].imageload()
                                    imgrect = x.get_rect()
                                    
                                    imgrect.topleft = (53, 392)
                                    
                                    screen.blit(x, imgrect)
                            screen.blit(self.glove, self.gloverect)
                            pygame.display.update()
                            #This prevents itemlist from having abnormal length.
                            itemlist = []
                                                                                                            
            if self.gloveloc == 1:
                self.gloverect.center = (85,95)
                selected = 'Items'
            elif self.gloveloc == 2:
                self.gloverect.center = (250,95)
                selected = 'Equipment'
            elif self.gloveloc == 3:
                self.gloverect.center = (419,95)
                selected = 'Key Items'
            #print(self.gloverect.width)
            game.screen.blit(self.glove, self.gloverect)
                    #if event.key == pygame.K_z:
            #53, 392
            pygame.display.update()
           # print('Loop again')
        game.BlackOut()
        screenupdate()
                    
        
        
    
    def update(self):
        #Just draw the normal menu.
        global game
        
        game.screen.blit(self.image, self.rect)
      #  print(self.icon1image == self.icon1default)
        
        if self.current_cursor == 1 and self.icon1image == self.icon1default:
             alertimage = copy.copy(self.icon1image).convert_alpha()
             alertimage.fill((255,255,0,200), special_flags=pygame.BLEND_RGBA_MULT)
             self.icon1image = alertimage    
        elif self.current_cursor != 1:
             self.icon1image = self.icon1default
        if self.current_cursor == 2 and self.icon2image == self.icon2default :
             alertimage = copy.copy(self.icon2image).convert_alpha()
             alertimage.fill((255,255,0,200), special_flags=pygame.BLEND_RGBA_MULT)
             self.icon2image = alertimage
        elif self.current_cursor != 2:
             self.icon2image = self.icon2default
        if self.current_cursor == 3 and self.icon3image == self.icon3default:
             alertimage = copy.copy(self.icon3image).convert_alpha()
             alertimage.fill((255,255,0,200), special_flags=pygame.BLEND_RGBA_MULT)
             self.icon3image = alertimage
        elif self.current_cursor != 3:
             self.icon3image = self.icon3default
        if self.current_cursor == 4 and self.icon4image == self.icon4default:
             alertimage = copy.copy(self.icon4image).convert_alpha()
             alertimage.fill((255,255,0,200), special_flags=pygame.BLEND_RGBA_MULT)
             self.icon4image = alertimage
        elif self.current_cursor != 4:
             self.icon4image = self.icon4default
        #454,47
        if self.current_cursor == 1:
            z = 'Items'
        elif self.current_cursor ==2:
            z = 'Skills'
        elif self.current_cursor == 3:
            z = 'Stats'
        elif self.current_cursor == 4:
            z = 'World'
        else:
            z = 'Items'
            self.current_cursor = 1
       # print(z)
        goldfont = pygame.font.Font('FreeSans.ttf',25)
        titlefont = pygame.font.Font('FreeSans.ttf',18)
        font = pygame.font.Font('FreeSans.ttf',12)
        tso = titlefont.render(z, True, (0,0,0), (101,101,101))
        tro = tso.get_rect()
        tro.center = [500, 47]
        screen.blit(tso, tro)
        areatitle = titlefont.render(game.areaname, True, (0,0,0),(101,101,101))
        arearect = areatitle.get_rect()
        arearect.center = [425,150]
        screen.blit(areatitle,arearect)
        #print(len(Party))
        moo = len(Party)
        #Handles data for multiple party members,
        #and doesn't cause interface spoilers.
        if moo == 1:
            locations = [(120,150)]
        if moo == 2:
            locations = [(120,150)]

       # elif moo == 2:
        self.quickstats.get_at((52,12))
        for i in Party.players:
            i = Party.player1
            #print(i, i.name)
            self.quickstatsrect.center = locations.pop(0)
            #Get at is nice for matching backgrounds.
            Name = titlefont.render(i.name,True, (0,0,0),self.quickstats.get_at((52,12)))
            Namerect = Name.get_rect()
            Namerect.center = (52,12)
            self.quickstats.blit(Name, Namerect)
            title1 = font.render('HP', True,(0,0,0), (self.quickstats.get_at((19,32))))
            title1rect = title1.get_rect()
            title1rect.center = (19,32)
            self.quickstats.blit(title1, title1rect)
            stat1 = font.render(str(i.Chealth) + '/' + str(i.Mhealth),True, (0,0,0), (self.quickstats.get_at((66,32))))
            stat1rect = stat1.get_rect()
            stat1rect.center = (66,32)
            self.quickstats.blit(stat1, stat1rect)
            title2 = font.render('MP', True,(0,0,0), (self.quickstats.get_at((19,57))))
            title2rect = title2.get_rect()
            title2rect.center = (19,57)
            self.quickstats.blit(title2, title2rect)
            stat2 = font.render(str(i.Cmp) + '/' + str(i.Mmp), True,(0,0,0), (self.quickstats.get_at((66,57))))
            stat2rect = stat1.get_rect()
            stat2rect.center = (66, 57)
            self.quickstats.blit(stat2, stat2rect)
            status = font.render(i.status,True, (0,0,0),(self.quickstats.get_at((52,81))))
            statsrect = status.get_rect()
            statsrect.center = (52,81)
            self.quickstats.blit(status,statsrect)
            
        
            game.screen.blit(self.quickstats, self.quickstatsrect)
            self.quickstats = self.quickstatsimagedefault.copy()
            
        # center of pt 2 is 270, 150
            #dont fcuk with the magic numbers for backcolor locations
        currentgold = goldfont.render(str(Party.money),True,(0,0,0),(self.image.get_at((175,145))))
        grect = currentgold.get_rect()
        grect.center = [230,160]
        game.screen.blit(currentgold,grect)
       
        game.screen.blit(currentgold,grect)
        game.screen.blit(self.icon1image, self.icon1rect)
        game.screen.blit(self.icon2image, self.icon2rect)
        game.screen.blit(self.icon3image, self.icon3rect)
        game.screen.blit(self.icon4image, self.icon4rect)

       
        pygame.display.update()

Menu = menu('menu.png','itemicon.png','equipment.png', 'status.png', 'settings.png')
#I kinda just define a bunch of function that are useful here.

def savegame():
    if Party.player2 == None:
        x = 'None'

    else:
        x = Party.player2.name
        print(x)
    try:
        Genmu.imagereset()
    except NameError:
        Genmu  = None
        pass
    Fredrick.imagereset()
    savedata = {'currentplace':game.currentplace,'emotionpoints':gamedata.emotionpoints,'logicpoints':gamedata.logicpoints,'willpoints':gamedata.willpoints,
                'items':Party.items,'equipment':Party.equipment,'zmoves':Party.zmoves,'xmoves':Party.xmoves,'cmoves':Party.cmoves,
                'spmoves':Party.spmoves,
                'keyitems':Party.keyitems,'choices':gamedata.choices,'events':gamedata.events,'bonds':Party.bonds,
                'player2':dummypartymember(x),'Genmu':Genmu,'Fredrick':Fredrick,'player1':Party.player1}
    #savedata = [['currentplace',game.currentplace],['emotionpoints',gamedata.emotionpoints],
    #            ['logicpoints',gamedata.logicpoints],['willpoints',gamedata.willpoints], ['items',Party.items],['equipment',Party.equipment],
    #            ['keyitems',Party.keyitems]]
    if gamedata.nosave == False:
        self.nosave = True
    pickle.dump(savedata,open('save1.txt','wb'))
##    try:
##        save = open('save1.txt','x')
##    except FileExistsError:
##        save = open('save1.txt','w')
##    save.write(game.currentplace)
##    
##    personalitydata = [gamedata.willpoint,gamedata.emotionpoint,gamedata.logicpoint]
##    x = str(personalitydata)



def screenupdate():
    '''
    Brings the screen back to normal
    It's a lot easier to write a function like this,
    rather than typing game.tilemap.draw() every time.
    '''
    global game
    game.findfocus()
    game.tilemap.draw(game.screen)
    if game.filter:
                if game.filter == 'dim':
                    blackRect = pygame.Surface(game.screen.get_size())
                    blackRect.set_alpha(100)
                    blackRect.fill((0,0,0))
                    game.screen.blit(blackRect, (0,0))  
                    pygame.display.flip()
    pygame.display.update()

def cleareventqueue():
    '''
    Clears pygame's event queue, so the game
    doesn't handle 50 inputs after some event finishes.
    they already have a function that does this
    why rename it
    Don\'t question me.
    '''
    pygame.event.pump()
    pygame.event.clear()
    #This function's not functioning properly
    for event in pygame.event.get():
        print('extra event')
        print(event)
        #the only important part of this function is pygame.event.pump()

def giveitem(moo,item):
    printstuff(moo,1)
    getitem(item)
    
def printstuff(moo, wait=0, creatormode=False, creatortalking=False,inmenu = False):
    text.rect.center = (275,400)
    #indentation bug is occurring
    if creatormode:
        textcolor = (255,255,255)
        backcolor = (0,0,0)
        invis = True
        centered = True
    else:
        textcolor = (0,0,0)
        backcolor = (255,255,255)
        invis = False
        centered = False
    if creatortalking:
        textcolor = (127,127,127)
    print(moo)
    maxlist = len(moo)
    currentlist = 0
    if centered:
        text.rect.center = (400,200)
    if not centered:
        text.rect.center = (275,400)
    if not invis:
        screen.blit(text.image, text.rect)
    newline = 0
    dist_from_end = 0
    needindent = False
    #print(moo)
    moo = list(moo)
    moo.append('\n')
    fast = None
    for y in range(0,maxlist):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    fast = True
                elif event.type == pygame.KEYUP and event.key == pygame.K_x:
                    fast = False
            #print('Fast?', fast)

            z = moo[y]
            #print('current',z)
            #print('last',moo[y-1])
            font = pygame.font.Font('FreeSans.ttf',18)
            #font.set_underline(1)
            #print('Font Linesize is :', font.get_linesize())
            tso = font.render(z, True, textcolor, backcolor)
            tro = tso.get_rect()
            #print(tro.width)
            k = len(moo) -1
            # the following code helps the text be displayed
            # without overlapping or clipping letters.
            # The copy functions track the location of the last letter
            # and assign the current ones location based on that previous letter.
            # Pygame only handles generation of entire sentences,
            # So...
            if moo[y-1] == moo[k]  or moo[y-1] == '\\' or needindent:
                #print('yes')
                tro.center = (text.rect.topleft[0] + ((y- dist_from_end)*12)   , text.rect.topleft[1] + (20*newline) + 15)               
                if not creatormode:
                    tro.left = 60
                #print(moo[y], tro.x)
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
        

            #if newline >= 1:
            tro.centery += (10*newline)
                
##            if newline >= 2:
##                tro.centery += 20
##            if newline == 3:
##                tro.centery += 20
            #print(tro)
            screen.blit(tso,tro)
            if z != ' ':
                cursor.play()
                
            pygame.display.update()
            currentlist += 1
            if z == '.' or z == '?' or z == '!':
                if fast:
                    time.sleep(0.1)
                else:
                    time.sleep(0.5)
            if z == ',':
                if fast:
                    time.sleep(0.1)
                else:
                    time.sleep(0.25)
            else:
                if fast:
                    pass
                else:
                    time.sleep(0.03)
            
            fps.tick(60)
    time.sleep(wait)
    cleareventqueue()
    #text.rect.center = (250,400)
    print(text.rect,'rect info') # 50 350
    revengeoftobias = False
    if fast:
        revengeoftobias = True
   
    while not revengeoftobias:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_z:
                revengeoftobias = True
    if not inmenu:
        screenupdate()
    print('finished!')


pc.printdummy = printstuff


def doublequestion(question, choice1,choice2):
#Take a third option.
    global pointer
    truemode = None
    rightcheck = 0
    leftcheck = 0
    zcheck = 0
    answergiven = False
    font = pygame.font.Font("FreeSans.ttf",17)
    maxlist = len(question)
    currentlist = 0
    newline = 0
    dist_from_end = 0
    thinking = 0
    screen.blit(text.image, text.rect)
    # No more than 75 characters, okay?
    for y in range(0,maxlist):
        global pointer
        z = question[y]
        font = pygame.font.Font('FreeSans.ttf',
                                    18)

       # print('Font Linesize is :', font.get_linesize())
        tso = font.render(z, True, (0,0,0), (255,255,255))
        tro = tso.get_rect()
        k = len(question) -1
        
        if question[y-1] == question[k]  or question[y-1] == '\\':
            tro.center = (text.rect.topleft[0] + ((y- dist_from_end)*12) + 15 , text.rect.topleft[1] + (20*newline) + 15)
            lastletter = copy.copy(tro)
        else:
            tro.left = lastletter.right 
            tro.top = lastletter.top
            lastletter = copy.copy(tro)

        
        if z == '\\' or z == '\n':
            dist_from_end = y + 1
            newline += 1
            continue
    

        tro.centery += (10*newline)

        screen.blit(tso,tro)
        if z != ' ':
            cursor.play()
##        if z == '(':
##            thinking = 1
##        elif z == ')':
##            thinking = 0
##        if z != ' ' and thinking == 0:
##            self.image.scroll(-120,0)
##        if z == ' ' or z == '.' or z == '!' or z == '?' and thinking == 0:
##            self.setSprite()
        global game
##        game.actors.draw(game.screen)
##        game.players.draw(game.screen)
        pygame.display.update()
        currentlist += 1
        
        if z == '.' or z == '?' or z == '!':
            time.sleep(0.5)
        if z == ',':
            time.sleep(0.25)
        else:
            time.sleep(0.03)

    currentchoice = None
    q1 = font.render(choice1, True, (0,0,0), (255,255,255))
    qro1 = q1.get_rect()
    qro1.center = (text.rect.topleft[0] + 200, text.rect.topleft[1] + 50) #was 80
    #qro1.left = 80
    screen.blit(q1, qro1)
    pygame.display.update()
    time.sleep(0.5)
    q2 = font.render(choice2, True, (0,0,0), (255,255,255))
    qro2 = q2.get_rect()
    qro2.center = (text.rect.topleft[0] + 200, text.rect.topleft[1] + 80)
    #qro2.left = 280
    screen.blit(q2,qro2)
    pygame.display.update()        
    time.sleep(0.5)
    gaveananswer = False
    rightcheck = None
    leftcheck = None
    pointer.currentloc = 0
    cleareventqueue()
    pygame.event.clear()
    
    while not answergiven:
        print(pointer.currentloc,'pointer location')
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and rightcheck == 1:
                    pointer.currentloc += 1
                    rightcheck = 0
                    if pointer.currentloc >= 2:
                        pointer.currentloc = 0
                if event.key == pygame.K_DOWN and leftcheck == 1:
                    leftcheck = 0
                    pointer.currentloc -= 1
                    if pointer.currentloc <= -1:
                        pointer.currentloc = 1
                if event.key == pygame.K_z and zcheck == 1:
                    #zcheck = 0
                    global chosenoption
                    #if not truemode:
                    print(pointer.currentloc,'current location')
                    
                    if pointer.currentloc == 0:
                        chosenoption = 1
                    elif pointer.currentloc == 1:
                        chosenoption = 2
                    else:
                        chosenoption = 3
                    print(chosenoption)
                    
                    gaveananswer = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rightcheck = 1
                if event.key == pygame.K_DOWN:
                    leftcheck = 1
                if event.key == pygame.K_z:
                    zcheck = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and rightcheck == 1:
                    pointer.currentloc += 1
                    rightcheck = 0
                    if pointer.currentloc >= 2:
                        pointer.currentloc = 0
                if event.key == pygame.K_DOWN and leftcheck == 1:
                    leftcheck = 0
                    pointer.currentloc -= 1
                    if pointer.currentloc <= -1:
                        pointer.currentloc = 1
                if event.key == pygame.K_z and zcheck == 1:
                    #zcheck = 0
                   
                    #if not truemode:
                    print(pointer.currentloc,'current location')
                    
                    if pointer.currentloc == 0:
                        chosenoption = 1
                    elif pointer.currentloc == 1:
                        chosenoption = 2
                    else:
                        raise UnboundLocalError('how u do dis no answer chosen')
                    print(chosenoption)
                    
                    gaveananswer = True
##                    if event.key == pygame.K_UP and choice3 != None:
##                        truemode = True
##                        print('third choice activated')
##                        q3 = font.render(choice3, True, (0,0,0), (255,255,255))
##                        qro3 = q3.get_rect()
##                        qro3.center = copy.copy(text.rect.center)
##                        screen.blit(text.image, text.rect)
##                        screen.blit(q3,qro3)
##                        currentchoice = qro3
                    
                    
                    
                    
        try:
            if pointer.currentloc != lastcurrentloc:
                #You want lazy? I'll show you lazy!
                #WHy redraw the screen when you can just
                #cover the last spot the cursor was?
                screen.blit(cursorcleaner, lastcursor)
        except UnboundLocalError:
            pass
        try:
            if gaveananswer == True:
                print(str(chosenoption) + 'was chosen')
                answergiven = True
                #pointer.currentloc = 0
                print(pointer.currentloc,'option number')
                return chosenoption
        except UnboundLocalError:
            raise
##                if not truemode:0
        if pointer.currentloc == 0:
            currentchoice = qro1
            chosenoption = 1
        else:
            currentchoice = qro2
            chosenoption = 1
        pointer.rect.midright = copy.copy(currentchoice.midleft)
        
        #pointer.rect.center = (text.rect.topleft[0] + (15 if pointer.currentloc == 0 else 215),
        #                       text.rect.topleft[1] + 80)
        lastcursor = copy.copy(pointer.rect)
        lastcurrentloc = copy.copy(pointer.currentloc)
        
            
        screen.blit(pointer.image, pointer.rect)
        pygame.display.update()

def triplequestion(choice1,choice2,choice3):
        game.tilemap.draw(game.screen)
        pygame.display.update()
        screen.blit(text.image, text.rect)
        global pointer
        truemode = None
        rightcheck = 0
        leftcheck = 0
        zcheck = 0
        answergiven = False
        #i messed something up regarding chosenoption
        # global variables are weird (i am also stupid)
        global chosenoption
        font = pygame.font.Font("FreeSans.ttf",17)
        
##        maxlist = len(question)
##        currentlist = 0
##        newline = 0
##        dist_from_end = 0
##        thinking = 0
##       
##        # No more than 75 characters, okay?
##        for y in range(0,maxlist):
##            global pointer
##            z = question[y]
##            font = pygame.font.Font('FreeSans.ttf',
##                                        18)
##    
##           # print('Font Linesize is :', font.get_linesize())
##            tso = font.render(z, True, (0,0,0), (255,255,255))
##            tro = tso.get_rect()
##            k = len(question) -1
##            
##            if question[y-1] == question[k]  or question[y-1] == '\\':
##                tro.center = (text.rect.topleft[0] + ((y- dist_from_end)*12) + 15 , text.rect.topleft[1] + (20*newline) + 15)
##                lastletter = copy.copy(tro)
##            else:
##                tro.left = lastletter.right 
##                tro.top = lastletter.top
##                lastletter = copy.copy(tro)
##
##            
##            if z == '\\' or z == '\n':
##                dist_from_end = y + 1
##                newline += 1
##                continue
##        
##
##            tro.centery += (10*newline)
##
##            screen.blit(tso,tro)
##            if z != ' ':
##                cursor.play()
##            if z == '(':
##                thinking = 1
##            elif z == ')':
##                thinking = 0
##            global game
##            game.actors.draw(game.screen)
##            game.players.draw(game.screen)
##            pygame.display.update()
##            currentlist += 1
##            
##            if z == '.' or z == '?' or z == '!':
##                time.sleep(0.5)
##            if z == ',':
##                time.sleep(0.25)
##            else:
##                time.sleep(0.03)

        currentchoice = None
        q1 = font.render(choice1, True, (0,0,0), (255,255,255))
        qro1 = q1.get_rect()
        qro1.center = copy.copy(text.rect.center)
        qro1.centery -= 30
        screen.blit(q1, qro1)
        pygame.display.update()
        time.sleep(0.5)
        q2 = font.render(choice2, True, (0,0,0), (255,255,255))
        qro2 = q2.get_rect()
        qro2.center = copy.copy(text.rect.center)
        screen.blit(q2,qro2)
        pygame.display.update()        
        time.sleep(0.5)
        q3 = font.render(choice3, True, (0,0,0), (255,255,255))
        qro3 = q3.get_rect()
        qro3.center =  copy.copy(text.rect.center)
        qro3.centery += 30
        screen.blit(q3,qro3)
        pygame.display.update()        
        time.sleep(0.5)
        
        rightcheck = None
        leftcheck = None
        pointer.currentloc = 1
        #pygame.event.pump()
        #cleareventqueue()
        pygame.event.clear(pygame.K_z)
        answergiven = False
        ztime = time.time()
        global chosenoption
        chosenoption = 1
        while not answergiven:
            print(pointer.currentloc,'pointer location')
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        rightcheck = 1
                    if event.key == pygame.K_UP:
                        leftcheck = 1
                    #Do I have to change more stuff? No?
                    #Then i\'m not gonna.
                    if event.key == pygame.K_z:
                        #hasty fix for weird glitch counting text advance z press as
                        #choice select z press
                        if time.time() -ztime >= 1:
                            
                            zcheck = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN and rightcheck == 1:
                        pointer.currentloc += 1
                        rightcheck = 0
                        if pointer.currentloc >= 4:
                            pointer.currentloc = 1
                    if event.key == pygame.K_UP and leftcheck == 1:
                        leftcheck = 0
                        pointer.currentloc -= 1
                        if pointer.currentloc <= 0:
                            pointer.currentloc = 3
                    if event.key == pygame.K_z and zcheck == 1:
                        zcheck = 0
                        #global chosenoption
                        #if not truemode:
                        if pointer.currentloc == 1:
                            chosenoption = 1
                        elif pointer.currentloc == 2:
                            chosenoption = 2   
                        elif pointer.currentloc == 3:
                            chosenoption = 3
                    
                        return chosenoption
                        gaveananswer = True
##                    if event.key == pygame.K_UP and choice3 != None:
##                        truemode = True
##                        q3 = font.render(choice3, True, (0,0,0), (255,255,255))
##                        qro3 = q3.get_rect()
##                        qro3.center = copy.copy(text.rect.center)
##                        screen.blit(text.image, text.rect)
##                        screen.blit(q3,qro3)
##                        currentchoice = qro3
                        
                        
                        
                        
                try:
                    if pointer.currentloc != lastcurrentloc:
                        #You want lazy? You opened up the right code.
                        #WHy redraw the screen when you can just
                        #cover the last spot where the cursor was?
                        screen.blit(cursorcleaner, lastcursor)
                except UnboundLocalError:
                    pass
                try:
                    if gaveananswer == True:
                        print(str(chosenoption) + 'was chosen')
                        answergiven = True
                        pointer.currentloc = 0
                        
                except UnboundLocalError:
                    pass
                
                if pointer.currentloc == 1:
                    currentchoice = qro1
                    chosenoption = 1
                elif pointer.currentloc == 2:
                    currentchoice = qro2
                    chosenoption = 2
                elif pointer.currentloc == 3:
                    currentchoice = qro3
                    chosenoption = 3
                pointer.rect.midright = copy.copy(currentchoice.midleft)
                #pointer.rect.center = (text.rect.topleft[0] + (15 if pointer.currentloc == 0 else 215),
                #                       text.rect.topleft[1] + 80)
                lastcursor = copy.copy(pointer.rect)
                lastcurrentloc = copy.copy(pointer.currentloc)
                
                    
                screen.blit(pointer.image, pointer.rect)
                pygame.display.update()
def showtitlecard(titlecard):
    title = pygame.image.load(titlecard).convert_alpha()
    rect = title.get_rect()
    title.convert_alpha()
    rect.x = 260
    rect.y = 100
    global game
    for i in range(1,25):
        i = (i*10) + 5
        title.fill((255,255,255,i), None, pygame.BLEND_RGBA_MULT)
        print(i)
        game.screen.blit(title, rect)
        pygame.display.update()
        fps.tick(30)
        title = pygame.image.load(titlecard).convert_alpha()
##    for i in range(1, 25):
##        i = (i*10) + 5
##        print(255 - i)
##        title.fill((255,255,255,(255-i)), None, pygame.BLEND_RGBA_MULT)
##        print(i)
##        game.screen.blit(title, rect)
##        pygame.display.update()
##        fps.tick(30)
##        title = pygame.image.load(titlecard).convert_alpha()
        
    time.sleep(1)
    print('yes')
class Player(pygame.sprite.Sprite):
    def __init__(self,player,location, orientation, cell,*groups):
        super(Player, self).__init__(*groups)
        self.player = player
        self.color = player.color
        self.image = pygame.image.load('sprites/player.png')
        self.imageDefault = self.image.copy()# Actual size is 28x56 #not anymore
        self.rect = pygame.Rect(0,0,40,80)# 32 60
        originalrect = pygame.Rect(cell.left,cell.top,32,32) #rect is always 32 by 32
        self.rect.midbottom = originalrect.midbottom
        #Collisionrect is the rect used to make collision detection seem more 
        #realistic (ex. Fredrick stops when his feet run into a wall, not when his head does.
        self.collisionrect = pygame.Rect((self.rect.x,self.rect.center[1]),(40,20))
        #self.rect.midbottom = location
        self.collisionrect.midbottom = copy.copy(self.rect.midbottom)
        self.averagewidth = copy.copy(self.rect.width)
        self.orient = orientation 
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.idletime = 0
        self.idlestart = 0
        self.coords = ((self.rect[0]//32)+1, (self.rect[1]//32)+2)
        self.emotion = None
        self.gamedata = {'is ready': None, 'Q1' : None, 'Q2' : None, 'Q3' : None, 'Q4' : None}
        self.zregister = 0
        self.xregister = 0
        self.truedx = 0
        self.name = 'Fredrick'
        self.moo = 0
        self.zcheck = None
        # Set default orientation
        self.setSprite()

    def animation(self,image,width,frames,mspf,dt):
        global game
        originalwidth = copy.copy(self.rect.width)
        Totaltime = frames*mspf
        time = 0
        framecount = 0
        self.rect.width = width
        self.image = pygame.image.load(image)
        done = False
        while not done:
            time += dt
            if time >= mspf:
                self.image.scroll(width*framecount*-1,0)
                time = 0
                framecount += 1
                if framecount == frames:
                    done = True
            game.tilemap.draw(game.screen)
            pygame.display.update()
        self.rect.width = originalwidth
        
            
                
    def talk(self,words, *args):
        text.rect.center = (275,400)
        wait = 0
        self.setSprite()
        screenupdate()
        self.walking = False
        lastletter = 0
        M_Open = 0
        print(self.name, ':',words)
        talking = 0
        thinking = 0
        font = pygame.font.Font("FreeSans.ttf",20)
        title = font.render(self.name, True, (0,0,0),(255,255,255))
        titlerect = title.get_rect()
        titlerect.bottomleft = copy.copy(text.rect.topleft)
        screen.blit(title,titlerect)
        screen.blit(text.image, text.rect)
        maxlist = len(words)
        currentlist = 0
        #screen.blit(text.image, text.rect)
        newline = 0
        dist_from_end = 0
        words = list(words)
        words.append('\n')
        fast = None
        letters = []
        for y in range(0,maxlist):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        fast = True
                    elif event.type == pygame.KEYUP and event.key == pygame.K_x:
                        fast = False
                z = words[y]
                #print('current',z)
                #print('last',moo[y-1])
                font = pygame.font.Font('FreeSans.ttf',
                                        18)
                
               # print('Font Linesize is :', font.get_linesize())
                tso = font.render(z, True, self.player.color, (255,255,255))
                tro = tso.get_rect()
                k = len(words) -1
                
                if words[y-1] == words[k]  or words[y-1] == '\\':
                    tro.center = (text.rect.topleft[0] + ((y- dist_from_end)*12) + 15 , text.rect.topleft[1] + (20*newline) + 15)
                    lastletter = copy.copy(tro)
                else:
                    tro.left = lastletter.right 
                    tro.top = lastletter.top
                    lastletter = copy.copy(tro)

                
                if z == '\\':
                    dist_from_end = y + 1
                    newline += 1
                    continue
            

                tro.centery += (10*newline)
                letters.append([tso,tro])
                
                if z != ' ':
                    cursor.play()
                if z == '(':
                    thinking = 1
                if z != ' ' and thinking == 0 and M_Open == 0:
                    self.image.scroll(-120,0)
                    M_Open = 1
                if z == ' ' or z == '.' or z == '!' or z == '?' and thinking == 0:
                    self.setSprite()
                    M_Open = 0
                global game
                game.actors.draw(game.screen)
                game.players.draw(game.screen)

                screen.blit(text.image, text.rect)
                for i in letters:
                    screen.blit(i[0],i[1])
                #make actor draw on talk box
                pygame.display.update()
                currentlist += 1
                if z == '-' and words[y-1] == '-':
                    self.setSprite()
                    wait = 0
                    sentenceinterrupt = True
                    break
                if z == ')':
                    thinking = 0
                if (z == '.' or z == '?' or z == '!') and thinking != 1:
                    if fast:
                        time.sleep(0.25)
                    else:
                        time.sleep(0.5)
                if z == ',':
                    if fast:
                        time.sleep(0.25)
                    else:
                        time.sleep(0.125)
                else:
                    if not fast:
                        time.sleep(0.03)
                
                fps.tick(60)
        done = False
        #time.sleep(wait)
       
        revengeoftobias = False
        while not revengeoftobias:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_z:
                    revengeoftobias = True

        screenupdate()
        cleareventqueue()
        


        '''
Fredrick: So, a trip?
Percy: Yeah, a trip.
Fredrick: Why?
Percy: Because why not? Who needs a reason to have fun?
Fredrick: I do. Dying doesn't sound appealing right now.
Percy: ... (I swear he'll never change.)
Percy: Come on. You're going.
Percy: Unless you wanna to spend the weekend with whatsherface.
Fredrick: (Dying would be better than that.)
Fredrick: Alright, fine.
       '''
    def imagereboot(self):
        self.image = self.originalimage.copy()
        self.imageDefault = self.originalimage.copy()
    def emote(self, emotion):
        '''call imagereboot after using this
        This function does not revert the image after using
        '''
        self.image = self.imageDefault.copy()
        
##        if emotion == 'shock':
##            self.image.scroll(0,-240)
##            game.screen.blit(pygame.image.load('sprites/exclamation.png'), (self.rect.centerx, self.rect.centery + 30))
##            pygame.display.update()
##            time.sleep(1)
        self.image = pygame.image.load(emotion)
        self.imageDefault = self.image.copy()
        if self.orient == 'down':
            pass
        elif self.orient == 'up':
            self.image.scroll(self.averagewidth*-1,0)
        elif self.orient == 'left':
            self.image.scroll(self.averagewidth*-2,0)
        elif self.orient == 'right':
            self.image.scroll(self.averagewidth*-3,0)
        screenupdate()
        cleareventqueue()
    def setSprite(self):
        # Resets the player sprite sheet to its default position 
        # and scrolls it to the necessary position for the current orientation
        # Lol shameless ripping
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -80)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -160)
        elif self.orient == 'right':
            self.image.scroll(0, -240)
        #self.image = pygame.transform.scale(self.image,(35,70))

    
        
    def coordsupdate(self):
        self.coords = [self.rect[0]//32, self.rect[1]//32]
        self.coords[0] += 1
        self.coords[1] += 2
        print(self.coords, 'coordinates')
    def getinfo(self, game,dt, cutscene=False):
        '''
        Handles inspecting things and talking to people.
        Also start cutscenes and stuff,
        Dialogue is handled here, so
        you can also change their dialogue so that they get into inane
        fights over monkeys and constellations, or have them scream about
        how much they HATE cabbage. 
        It's up to you.
        Maybe.
        Cutscene is used during a (yeah that's right, a) cutscene
        to initiate dialogue without player input.
        I made it go here in order to keep all dialogue
        in one easy to access area.
        this function is bloated 
        also buggy
        '''
        d_check = 0
        Not_A_Tile = None
        if cutscene:
            Not_A_Tile = True
        itemdetected = None
        #check if characters have moved
        #for i in characters:
        ##    for x in game.actors:
        #        print(i,x,i.name,x.name)
        #        if x == i:
        #            print('yes')
        #            i.rect = copy.copy(x.rect)
        ##print(cutscene,'Cutscene?')
        # This lets you interact with and inspect things.
        if self.orient == 'left':
            targetarea = copy.copy(self.coords)
            targetarea = list(targetarea)
            targetarea[0] -= 2
        # if occupied, etc...
        elif self.orient == 'right':
            targetarea = copy.copy(self.coords)
            targetarea = list(targetarea)
            targetarea[0] += 2
        elif self.orient == 'up':
            targetarea = copy.copy(self.coords)
            targetarea = list(targetarea)
            targetarea[1] -= 2
            #fixes rounding errors?
            #targetarea[0] -= 1
        elif self.orient == 'down':
            targetarea = copy.copy(self.coords)
            targetarea = list(targetarea)
            targetarea[1] += 2 
           
        print(targetarea,'checking for')
        
        x = (targetarea[0]//1) * 32
        y = (targetarea[1]//1) * 32
        Sprite_Area = list()
        Sprite_Area = [x,y]

        ##print(self.rect.center,'center')
        ##print(x,y,'Coords')
        #as if it wasn't clear enough already, this is a hack.
        if self.orient == 'left':
            Sprite_Area[0] += 32
        for i in characters:
            print('character =',i.coords,'self =', self.coords)
            print("Location being checked for sprite:",Sprite_Area,"Actual sprite location",[i.coords[0]*32,i.coords[1]*32],'checking for character')            
            if Sprite_Area == [i.coords[0]*32,i.coords[1]*32]:
                print(i.name,'found')
                Not_A_Tile = True
                moo = i.cell
                
                characterfound = True
                ##print('Character found.')
            else:
                characterfound = False
                print('No character found.')
        if self.orient == 'left':
            Sprite_Area[0] -= 32
        #if self.orient == 'up':
        #    Sprite_Area[0] -= 32
        for i in allitems:
            
            zx = copy.copy(Sprite_Area)
            #print(zx,'zx')
            Sprite_Area = pygame.rect.Rect(Sprite_Area[0],Sprite_Area[1], 1,1)
            Sprite_Area.centerx = (zx[0])
            Sprite_Area.centery = (zx[1])
            
            if i.rect.colliderect(Sprite_Area):
                Not_A_Tile = True
                ##print('There\'s an item.')
                moo = i.tile
                
                moocell = i
                
                #print(moo,'1')
                itemdetected = True
                
                #break
            else:
                ##print('Nope, no item.')
                if itemdetected == True:
                    pass
                else:
                    itemdetected = False
        ryan = game.tilemap.layers['Object Layer 1']
        if not cutscene and not itemdetected:
            Sprite_Area = pygame.rect.Rect(Sprite_Area[0],Sprite_Area[1], 64,64)

            for i in game.tilemap.layers['Object Layer 1'].find('description'):
                print(i.rect,Sprite_Area,'h')
                #print(i.rect.colliderect(Sprite_Area),'Collide')
                try:
                    if i.rect.colliderect(Sprite_Area):
                        
                        print(i.rect, Sprite_Area,'Collide')
                        moo = i
                        print('moo',4)
                        if 'orient' not in moo.properties:#only characters have orient
                            #this bug plagued me for longer than it shoudl have
                            Not_A_Tile = False
                        break
                except TypeError:
                    print('typeerror')
                    continue
            
        if cutscene:
            moo = cutscene[0]
        try:
            if moo:
                pass
        except UnboundLocalError:# here it is
            print('Moo undefined')
            moo = None

        print('Moo,Not a tile',moo,Not_A_Tile)      
        if moo != None and Not_A_Tile != True:

            try:
                ##print(3)
                if 'prohibitor' in moo.properties:
                    if moo.properties['prohibitor']  in game.gamedata.events:
                        pass
                
                else:
                    if 'nodesc' not in moo.properties:
                        printstuff(moo.properties['description'])
                if Party.player2 != None and Party.player2.name == 'Genmu':
                        gmode = True
                        char = Party.player2
                else:
                        gmode = False
                #print(dir(moo))
                
                if game.currentplace == 'itemplace.tmx':
                        self.talk('Well, i am hungry...')
                if 'MemoryPlace' in moo.properties:
                    if "Gray" in moo.properties:
                        printstuff('It looks like that weirdo from before.')
                        printstuff('There\'s a slot for those weird orbs near its feet.')
                        hasorb = False
                        for i in Party.keyitems:
                            if i.name == 'orb':
                                hasorb = True
                        if hasorb:
                            printstuff('Would you like to use an orb?')
                        else:
                            printstuff('If you had an orb, you could use it here.')
                if 'door' in moo.properties:
                    if game.currentplace == 'picnicarea.tmx':
                        printstuff("Before you lies the true final area of your journey.")
                        printstuff("In your current state, you would not\\ be able to handle what awaits you in there.")
                        printstuff("Perhaps that is because you have not\\ visited every other area in your journey yet.")
                        
                       
                    if game.currentplace == 'cave2.tmx':
                        if 'percyready' in game.gamedata.events:
                            spdooropen.play()
                            #printstuff("This place contains more difficult enemies than usual.")
                            printstuff("You cannot exit the area until you have finished it.")
                            doublequestion("Are you prepared to enter?","It's now or never.", "Not yet...")
                        else:
                            printstuff('This door is connected to Percy.')
                            printstuff("It seems he does not appreciate you enough yet.")
##                    if 'doorready' not in game.gamedata.events:
##                        printstuff('The door is firmly shut.')
##                        printstuff('Still, you feel drawn to it...')
##                        printstuff('You\'ll know when you need to come back here.')
##                        
##                    else:
                    elif game.currentplace == 'grasstowngiftshop3.tmx':
                        if 'genmuready' in game.gamedata.events:
                            spdooropen.play()
                            game.killtime(1.5)
                            printstuff('The door has unlocked...')
                            printstuff('You won\'t be able to return from this place easily.')
                            chosenoption = doublequestion('Are you sure you want to enter?', 'I\'m ready.','Not yet.')
                            if chosenoption == 1:
                                printstuff('WAIT, it opens?!? And you\'re going---')
                                game.fadeOut()
                                game.initArea('dungeonentrance.tmx')
                            if chosenoption == 2:
                                printstuff('Ugh, you too?\\Hmph, another satisfied customer...')
                        elif 'firstdoorready' not in game.gamedata.events and 'grayfirstdoor' not in game.gamedata.events:
                            game.initextras()
                            game.fadeOut()
                            for i in game.actors:
                                if i.name == 'Gray':
                                    char = i
                            char.rect.center = (544,288)
                            char.talk('Ugh, you found something important again?')
                            char.talk('I was about to get ready to bathe.')
                            char.talk('It\'s fortunate you didn\'t take any longer...')
                            char.talk('You remember how I told you to make friends, right?')
                            char.talk('Did you think I was making you do it\\for some mushy friendship related reason?')
                            chosenoption = triplequestion('That\'s usually how it goes.','I didn\'t really think about it.','I want to fight things.')
                            if chosenoption == 1:
                                char.talk('Well, it may be partially true, but...')
                                char.talk('It definitely doesn\'t cover the whole story.')
                            if chosenoption == 2:
                                char.talk('No one does.')
                                char.talk('Not that thinking about it would change anything.')
                            if chosenoption == 3:
                                char.talk('You remind me too much of an old friend...')
                                char.talk('But, you must be getting along well with Genmu.')
                                
                            char.talk('No, the real reason for your\\"friendship journey" was these doors.')
                            char.talk('Each of your friends is\\somehow connected to one of them.')
                            char.talk('When you "prove your worth" to a friend,\\the door will become unlocked.')
                            char.talk('Inside the doors...')
                            char.talk('Well, let\'s just say those waiting\\inside will see if you\'re a hero or not.')
                            char.talk('Which you should be if\\you have gotten that far, but...')
                            char.talk('Ugh, wait...')
                            char.talk('No, I forgot to feed them!')
                            char.talk('Sheesh, you threw off the\\momentum of my whole day.')
                            char.talk('See you around.')
                            #char.talk('I am unfortunately guaranteed to do so,\\even against my will...')
                            char.talk("Actually, wait a minute.")
                            char.talk('I do detect something on you.')
                            char.talk('You found one of those orbs, huh?')
                            char.talk('Hmmmmm.')
                            char.talk('These are the place to use those...')
                            char.rect.x += 2000
                            game.gamedata.events['firstdoorready'] = True
                        else:
                            printstuff('Genmu doesn\'t find you heroic yet.\\Neither goes the door.')
                            #printstuff('You\'ll know when you can enter it.')
                   
                        
               
                if 'gelevator' in moo.properties:
                    if 'hasroom' in game.gamedata.events:
                        chosenoption = doublequestion('Use the elevator?','Of course.','I just wanna loiter...')
                        if chosenoption == 1:
                            game.initArea('grasstownhotelhallway.tmx',False,1)
                    else:
                        printstuff('Have you considered buying a room first?')
                if 'question' in moo.properties:
                    if self.gamedata['is ready'] and game.currentplace == 'firstplace.tmx':
                        printstuff(' From nowhere, a blinding light appears!')
                        game.fadeOut()
                        game.initArea('place_of_decisions.tmx')
                if game.currentplace == 'grassstage3.tmx':
                    if moo.name == 'sign':
                        if gmode:
                            char.talk('Hmm, I wonder what\'s up ahead.')
                            self.talk('(Is this guy serious?)')
                
                if game.currentplace == 'grasstownweaponshop.tmx':
                    if Party.player2 != None and Party.player2.name == 'Genmu':
                        gmode = True
                        char = Party.player2
                    else:
                        gmode = False

                    if moo.name == 'sword1':
                        if gmode:
                            char.talk('...')
                            char.talk('WOAH!','bigtext')
                            char.talk('What is that?!?!?')
                            for i in game.actors:
                                if i.name == 'Yeah, Buddy':
                                    i.talk('Yeah, buddy.\\Took me forever to track it down...')
                            char.talk('oh my god...')
                            char.talk('(I need it...)')
                            
                            char.talk('SWORDSWORDSWORDSWORD...')
                            char.talk('Oh, It\'s perfect...')
                    if moo.name == 'sword2':
                        if gmode:
                            char.talk('The owner of this shop is truly a\\ connoisseur.')
                            for i in game.actors:
                                if i.name == 'Yeah, Buddy':
                                    i.talk('Yeah, buddy.')
                    if moo.name == 'logo':
                        self.talk('Tell me more about that man.')
                    if moo.name == 'Sign':
                        if gmode:
                            char.talk('(This place is amazing...\\\\Are they hiring?)')
                if game.currentplace == 'grasstownhotelhallway.tmx':
                    if moo.name == 'door':
                        if 'grasstownhotel' in game.gamedata.events:
                            if 'hasroom' in game.gamedata.events:
                                Party.player2.talk('Another eventful day of adventuring.')
                                Party.player2.talk("Who was that guy you fought earlier?")
                                printstuff("Fredrick is still wondering about that.")
                                #alt response?
                                
                                #Party.player2.talk('Uh.')
                                if game.genmuaffection >= 1:
                                    Party.player2.talk('Thanks a lot for helping me out.')
                                    Party.player2.talk("As a reward...")
                                    Party.player2.talk("I will pass on to you one of\\my amazing sword techniques.")
                                    printstuff("Time passes...")
                                    game.BlackOut()
                                    printstuff("Fredrick has learned how to handle a blade more efficiently!")
                                    printstuff("This is surprising given\\ Genmu\'s general lack of focus.")
                                    printstuff("Fredrick\'s strength has increased by half a level!")
                                    Party.player1.attack += 0.5
                                    Party.player2.talk("Good stuff, right???")
                                    Party.player2.talk("I will see you later, Fredrick.")
                                else:
                                    Party.player2.talk("Well, my faithful companion.")
                                    Party.player2.talk('For now, our journey draws to a close.')
                                    Party.player2.talk("I will see you tomorrow.")
                                    Party.player2.talk("Don\'t miss me TOO much until then.")
                                
                                #Party.player2.walkto()
                                Party.player2.walk('right',2)
                                Party.player2.walk('up',1)
                                
                                #when will he get over here?
                                Party.player2.rect.x += 900000
                                Party.player2.followmode = False
                                Party.player2.walkmode = False
                                Party.player2 = None
                            
                                printstuff("You should probably talk \\ to the concierge again.")
                                    
                                
                                
                                
                                del game.gamedata.events['grasstownhotel']
                                game.gamedata.events['percypizza'] = True
                                game.gamedata.events['percytalk'] = True
                            else:
                                Party.player2.talk('Why won\'t this door OPEN???')
                        else:
                            if 'hasroom':
                                chosenoption = doublequestion('Go to sleep?','I\'m so TIRED.','No! No.')
                                if chosenoption == 1:
                                    printstuff('Fredrick has had enough of today.')
                                    game.initArea('percydream.tmx')
                            else:
                                printstuff('Get a roomkey you Frick.')
                if 'temporary' in moo.properties:
                    moo.rect.x += 5000
                    
                    
                               
            except KeyError:
                print('something went wrong')
                raise
                pass
        elif moo != None and (Not_A_Tile == True or cutscene == True):
            print('It is a character, or a cutscene.')
            ##print(game.currentplace)
            ##print('Cutscene detected')
            #global characters
            ##print(moo,'Tile')
            ###print(moo.properties,'Properties')
            ##print(moo,'moo')
            ##print(moo.name)
            if cutscene:
                moo = cutscene[0].cell
            if itemdetected:
                print('Item detected')
                print(moo,'2')
                if 'kalpaspecial' in moo.properties:
                    if game.currentplace == '1stkalpa.tmx':
                        showtitlecard('abyss1.png')
                        for i in game.items:
                            if i.name == moo.name:
                                i.kill()
                                del i
                            
                       
                       
        
                if 'story' in moo.properties:
                    printstuff('The paper has a story written on it.')
                    chosenoption = doublequestion('It\'s not too long.','I guess I\'ll read it.','Nah...')
                    if chosenoption == 1:
                        printstuff('Once, there was a little boy who had a toy.')
                        printstuff('He loved his toy very much,\\and played with it all day, every day.')
                        printstuff('His parents thought he was a little strange.')
                        printstuff('Indeed, he was a little strange.')
                        printstuff('One day, the boy went to sleep,\\and his parents saw that his toy\\was nowhere to be found.')
                        printstuff('Knowing that the child would definitely\\not be able to handle the loss of his toy,\\his parents immediately replaced it.')
                        printstuff('The next morning, like he always would,\\he got up and played with his beloved toy.')
                        printstuff('He played with it like normal, none the wiser as to what had happened.')
                        printstuff('A while later, the boy\'s parents\\were about to take him out to play...')
                        printstuff('While he was getting prepared\\to leave, he found his old toy.')
                        printstuff('The boy was sharp,\\so he pieced together what had happened.')
                        printstuff('He was initially happy that he\\had two copies of his favorite toy, but...')
                        printstuff('His mood soured when he realized he\\could only bring one toy with him on the trip.')
                        printstuff('Should he bring his newer toy,\\or the original he held so dear?')
                        printstuff('The boy pondered this for a while.')
                        printstuff('Eventually, he decided to pick--')
                        printstuff('The rest of the story is missing...')
                    else:
                        printstuff('Reading is just so boring...')
                    
                if moo.name == 'flyer' or 'flyer' in moo.properties:
                    
                        
                    printstuff(moo.properties['description'])
                    if 'friendintro' in moo.properties:
                        if 'readthepaper' not in moo.properties:
                            printstuff('People have different personalities,\\and thus, different desires.')
                            printstuff('Some may have the same desires as you,\\others may not.')
                            printstuff('However, saying no to one person\\can mean saying yes to another.')
                            printstuff('Likewise, saying yes to someone\\can mean saying no to someone else.')
                            printstuff('Make sure you choose what you really want.')
                            printstuff('Making insincere choices may stop you\\from taking the path you would like the most.')
                    if game.currentplace == 'grassdungeon4a.tmx' and 'annoying' in moo.properties:
                        Party.player2.talk('That piece of paper is my soul mate.')
                    if game.currentplace == 'grassdungeon13.tmx':
                        
                        Party.player2.talk('Ugh!')
                        Party.player2.talk('What did I do to deserve all this grass?')
                        Party.player2.talk('What god have I angered to justify such torment?')
                        chosenoption = triplequestion('Genmu, it\'s just grass.','Is it my fault you look all slicey?','You must have done something HORRIBLE...')
                        if chosenoption == 1:
                            Party.player2.talk('It\'s the grass of my doom!')
                        if chosenoption == 2:
                            Party.player2.talk('How does all my sword-themed glory evoke the image of a landscaper?')
                            Party.player2.talk("That\'s not fair at all!")
                        if chosenoption == 3:
                            Party.player2.talk('...')
                            Party.player2.talk('I-I can\'t take it!')
                            Party.player2.talk('NOOOOOOOOOOOO')
                            printstuff('(You decide to calm him down, for the safety of all parties involved.)')
                    if game.currentplace == 'grassdungeon18.tmx':
                        Party.player2.talk('*sniff*,*sniff*')
                        Party.player2.talk('Finally, we escaped...')
                        Party.player2.talk('I was so scared.')
                        Party.player2.talk('It felt like I was trapped in a vegan nightmare.')
                        chosenoption = doublequestion('','Our freedom is so close...','OH NO MORE GRASS!!!')
                        if chosenoption == 1:
                            player.talk('Watch this.')
                            printstuff("Fredrick cuts all the grass.")
                            screenupdate()
                            Party.player2.talk('Fredrick...')
                            printstuff('Genmu\s mind has been blown.')
                        if chosenoption == 2:
                            Party.player2.talk('AHHHEAYUGHAYAYAAAA!')
                            #he pulls his bandana up, so it becomes a blindfold
                            Party.player2.talk('I can\'t look.')
                            printstuff('His hands shaking, Genmu grasps his sword.')
                            Party.player2.talk('Take this!')
                            printstuff('Genmu cuts all the grass.')
                        for i in allitems:
                            if i.name == 'cutgrass':
                                i.tangible = False
                                i.specialproperties['cut'] = True
                                i.image = pygame.image.load('grasscut.png')
                            
                                            
                        
                            
                    if 'controlnote' in moo.properties:
                        if 'allcut4' in game.gamedata.events:
                            printstuff('Woah. You cut all the grass...')
                        elif game.cutgrassnum == 0:
                            
                            printstuff('You have a limited number\\of cuts you can make.')
                            printstuff("Your remaining cuts are located at the top of the screen.")
                            
                            printstuff('This page will let you restore grass,\\should you make a mistake.')
                        else:
                            chosenoption = doublequestion('Do you wish to reset the grass?','Please...','I can live with my mistakes.')
                            if chosenoption == 1:
                                for i in allitems:
                                   
                                    if i.name == 'cutgrass':
                                        
                                        if 'cut' in i.specialproperties:
                                            del i.specialproperties['cut']
                                            
                                            i.image = pygame.image.load('cutgrass.png')
                                            i.tangible = True
                                            game.cutgrassnum = 0
                                            
                                            pygame.display.set_caption('Cuts left: 9')
                                Party.player2.talk("NO! WHY WOULD YOU MAKE IT GROW BACK!?!")
                if moo.name == 'cutgrass':
                    if 'cut' not in moocell.specialproperties:
                        print('cut')
                        print(moo.properties)
                        
                        if game.currentplace == 'grassdungeon7.tmx':
                             if 'path' not in moo.properties:
                                printstuff('You didn\'t listen...')
                                if 'maginyudone' in game.gamedata.events and 'genmugrassanger' not in game.gamedata.events:
                                    Party.player2.talk('No!')
                                    Party.player2.talk('DON\'t TOUCH ME!','bigtext')
                                    Party.player2.talk('GAAAAH!','bigtext')
                                   #bugged
                                    for i in allitems:
                                        i.tangible = False
                                        i.specialproperties['cut'] = True
                                    #Party.player2.talk('My VENGEANCE has been exacted.')
                                    game.gamedata.events['genmugrassanger'] = True
                                elif 'maginyudone' in game.gamedata.events and 'genmugrassanger'  in game.gamedata.events:
                                    Party.player2.talk('No way...')
                                else:
                                    game.initArea('grassdungeon7.tmx')
                        if game.currentplace == 'grassdungeon13.tmx':
                            if 'path' not in moo.properties:
                                printstuff('No! It\'s SO UNCRISP!')
                                Party.player2.talk('Who was that?')
                                Party.player2.talk('Don\'t touch us!')
                                printstuff('Or what?')
                                Party.player2.talk('I\'ll do something DANGEROUS!')
                                printstuff('Ooh, what are you going to do? Cut all the grass?')
                                Party.player2.talk('Yes.')
                                for i in allitems:
                                        i.tangible = False
                                        i.specialproperties['cut'] = True
                                        i.image = pygame.image.load('grasscut.png')
                                        
                                
                                #second time?
                                
                                
                                
                        if game.currentplace == 'grassdungeon18.tmx':
                            if 'reqgrass' in moo.properties:
                                game.cutgrassnum += 1
                                print('cutgrassnum')
                                if game.cutgrassnum == 3:
                                    game.gamedata.events['mincut'] = True
                                if game.cutgrassnum >= 4:
                                    game.gamedata.events['smileyfacecut'] = True
                                    del game.gamedata.events['mincut']
                                if game.cutgrassnum == 20:
                                    game.gamedata.events['allcut'] = True
                                    del game.gamedata.events['smileyfacecut']
                        if 'specialgrass' in moo.properties:
                            moocell.image = pygame.image.load('grasscutSP.png')
                        else:
                            moocell.image = pygame.image.load('grasscut.png')
                            if moo.properties['image'] == 'cutgrasssmall.png':
                                moocell.image = pygame.image.load('grasscutsmall.png')
                        
                        moocell.tangible = False
                        moocell.specialproperties['cut'] = True
                        if 'gold' in moo.properties:
                            if 'grassmoney' not in game.gamedata.events:
                                printstuff('There was $'+str(moo.properties['gold'])+' in the grass.')
                                Party.money += moo.properties['gold']
                                game.gamedata.events['grassmoney'] = True
                            else:
                                printstuff('Money doesn\'t grow on trees.\\Or in bushes...')
                        allcut = False
                        for i in allitems:
                            if i.name == 'cutgrass':
                                if 'cut' in i.specialproperties:
                                    
                                    allcut = True
                                else:
                                    allcut = False
                                    break
                        

                        if allcut:
                            if game.currentplace == 'grassdungeon2.tmx':
                                screenupdate()
                                time.sleep(1.5)
                                printstuff('What are you, a lawnmower?')
                                game.gamedata.events['allcut2'] = True
                            if game.currentplace == 'grassdungeon5.tmx':
                                screenupdate()
                                time.sleep(1.5)
                                printstuff('Why are you like this?')
                                game.gamedata.events['allcut5'] = True
                            if game.currentplace == 'grassdungeon6.tmx':
                                printstuff('???WHY???')
                                game.gamedata.events['allcut6'] = True
                            if game.currentplace == 'grassdungeon8.tmx':
                                #printstuff('A gentle, yet assertive voice calls out:')
                                printstuff('You couldn\'t even leave just one?')
                                game.gamedata.events['allcut8'] = True
                            if game.currentplace == 'grassdungeon10.tmx':
                                printstuff('You\'re bizarre.')
                                game.gamedata.events['allcut10'] = True
                            if game.currentplace == 'grassdungeon11.tmx':
                                printstuff('Oh, a path wasn\'t enough.')
                                printstuff('You need to cut ALL the grass, huh?')
                                gxame.gamedata.events['allcut11.tmx'] = True
                            if game.currentplace == 'grassdungeon12.tmx':
                                printstuff('How will you do the next puzzle now?')
                                printstuff('NICE GOING, STUPID.')
                                game.gamedata.events['allcut12'] = True
                            if game.currentplace == 'grassdungon13.tmx':
                                printstuff('Uh, I guess this will do.')
                                game.gamedata.events['allcut13'] = True
                            if game.currentplace == 'grassdungeon18.tmx':
                                printstuff('...')
                                printstuff('Unbelievable.')
                                game.gamedata.events['allcut18'] = True
                        if game.currentplace == 'grassdungeon7.tmx':
                            if 'specialgrass1' in moo.properties:
                                for i in allitems:
                                    if i.name == 'flyer1':
                                        i.rect.center = copy.copy(moo.rect.center)
                                        i.tangible = False
                                        moocell.rect.centerx += 10000
                            if 'specialgrass2' in moo.properties:
                                for i in allitems:
                                    if i.name == 'flyer2':
                                        i.rect.center = copy.copy(moo.rect.center)
                                        moocell.rect.centerx += 10000
                                        i.tangible = False
                            if 'specialgrass3' in moo.properties:
                                for i in allitems:
                                    if i.name == 'flyer3':
                                        i.rect.center = copy.copy(moo.rect.center)
                                        moocell.rect.centerx += 10000
                                        i.tangible = False
                            if 'specialgrass4' in moo.properties:
                                for i in allitems:
                                    if i.name == 'flyer4':
                                        i.rect.center = copy.copy(moo.rect.center)
                                        moocell.rect.centerx += 10000
                                        i.tangible = False
                            if 'specialgrass5' in moo.properties:
                                for i in allitems:
                                    if i.name == 'flyer5':
                                        i.rect.center = copy.copy(moo.rect.center)
                                        moocell.rect.centerx += 10000
                                        i.tangible = False
                            if 'path' not in moo.properties:
                               
                                game.initArea('grassdungeon7.tmx')
                            
                        if game.currentplace == 'grassdungeon4.tmx':
                            
                            game.cutgrassnum += 1
                            x = (9 - game.cutgrassnum)
                            game.grassdisplay = True
                            if x > 0:
                                pygame.display.set_caption('Cuts left: '+str(x))
                            if x <= 0:
                                pygame.display.set_caption('Cutting? I don\'t think so..')
                            if game.cutgrassnum >= 10:
                                moocell.tangible = True
                                moocell.image = pygame.image.load('cutgrass.png')
                                del moocell.specialproperties['cut']
                        
                                
                        if game.currentplace == 'grassdungeon2.tmx':
                        
                            if 'genmucut' in moo.properties and 'genmugrasstalk' not in game.gamedata.events:
                                
                                printstuff('Genmu begins to wince....')
                                Party.player2.talk('Oh, I HATE IT!')
                                Party.player2.talk("I hate it I hate it I HATE IT!")
                                game.gamedata.events['genmugrasstalk'] = True
                                
                           
                            if 'dog' in moo.properties and 'metdog' not in game.gamedata.events and 'grassdungeonround1done' not in game.gamedata.events :
                                game.initextras()
                                for i in game.actors:
                                    if i.name == 'Magidog':
                                        char = i
                                        char.rect.centerx = copy.copy(game.player.rect.centerx)
                                        char.rect.centery = copy.copy(game.player.rect.centery)
                                        char.rect.x += 50
                                char.orient = 'left'
                                screenupdate()
                                time.sleep(1)
                                screenupdate()
                                char.talk('Bark?')
                                
                                char.talk('Bark? BARK BARK!!!')
                                Party.player2.talk('Seriously?!?')
                                Party.player2.talk('How did you even fit in there?')
                                char.talk('BARK bark bark...')
                                
                                Party.player2.talk('What is that, a baseball cap???')
                                printstuff('The dog hands Fredrick a note.')
                                
                                
                                char.talk('"Hello. My name is Charles.\\I can understand human speech."')
                                Party.player2.talk('OH, CHARLES.\\That idiot saleman\'s mutt?')
                                char.talk('BARK BARK BARK BARK!?!?')
                                char.talk('"The man travelling with you\\has stolen my master\'s sword,\\and he wants it returned.')
                                Party.player2.talk('Hey, I borrowed it! I\'ll give it back eventually.')
                                

                                char.talk('Bark bark...')
                                char.talk('"We both already know you won\'t."')
                                char.talk('"The swordsman is probably resisting,\\so I have been authorized to use force..."')
                                
                                battle.Battle(Party.player1,[battle.fredrick],[battle.magicdog],'grass stage',None,(129,129,254),['Stick','First Aid Kit'],'Magic Dog Encounter',gamedata)
                                screenupdate()
                                char.talk('Bark?!?')
                                Party.player2.talk('Hey, mutt!\\Unless you want to deal with my\\friend again, tell me where your owner went.')
                                char.talk('BARK!?!?')
                                char.walk('right',30,1)
                                screenupdate()
                                printstuff('The dog left a note...')
                                char.talk('You are an unaccommodating brute!')
                                self.talk('...')
                                Party.player2.talk('Unbelievable. If the dog read my lips,\\ he would have known:')
                                Party.player2.talk("That sword is mine!")
                                
                                game.gamedata.events['metdog'] = True
                                Party.player2.chatready = True
                            allcut = False
                            for i in allitems:
                                if i.name == 'cutgrass':
                                    if 'cut' in i.specialproperties:
                                        
                                        allcut = True
                                    else:
                                        allcut = False
                                        break

                            
                        if moo.name == 'cutgrass6':
                           pass 

                                #battle.Battle(Party.player1,[battle.fredrick],[battle.ghostface],'gray area',None,(0,0,0),['Stick','First Aid Kit'],'First Battle (Starring Gray Cloak)',gamedata)
                                
                                        
                            
##                if moo.name == 'cutgrass2':
                        
##                    moo.item.image = pygame.image.load('grasscut.png')
                    
                if moo.name == 'chest':
                   
                    x = 'chest'
                    y = str(moo.properties['chestid'])
                    x += y
                    game.gamedata.events[x] = True
                    #print(type(moo.properties['opened']),'opened')
                    
                    if moo.properties['opened'] == 1:
                        
                        i = random.randint(0,1000)
                        print(i)
                        if i <= 333:
                            printstuff('There\'s nothing inside.\\You opened it, remember?')
                        if i >= 334 and i <= 667:
                            printstuff('Even though you wished there was,\\there was nothing inside the chest.')
                        if i >= 668 and i <= 997:
                            printstuff('There was something left inside.\\Until you took it.')
                        if i >= 998:
                            printstuff('You need to find a better way to use your time.')
                            printstuff('A special weapon was added to your inventory.')
                            Party.equipment.append(sacredstick)
                    if moo.properties['opened'] == 0:
                        printstuff('An item is held within.')
                        moo.item.image = pygame.image.load('chestopen.png')
                        if game.currentplace == 'grassstage.tmx':
                            printstuff("It was a strange tablet\\ with mystic writings engraved on it.")
                            printstuff("As Fredrick\'s eyes look over the tablet, suddenly...!")
                            choicebooster()
                            printstuff("The tablet disintegrates...")
                            printstuff("Fredrick is wondering why everything keeps affecting his mental state.")

                        if game.currentplace == "snowmountain4.tmx":
                            Party.player2.talk("Hm, more free stuff...")
                            Party.player2.talk("Who keeps putting those here?")
                            Party.player2.talk("I\'m glad we found it before someone else did.")
                            printstuff("Fredrick feels obligated to open the chest.")
                            printstuff("A ring was waiting inside.")
                            printstuff("Ring was added to your equipment.")
                        if game.currentplace == 'grassdungeon21.tmx':
                            Party.player2.talk("Hah! He dropped some merchandise on his way out...")
                            Party.player2.talk("Boy, I would love me a sword about now...")
                            printstuff('The chest contained a book\\ entitled "Memoirs of a Fencer".')
                            #bushido in the bedroom?
                            Party.player2.talk('Ugh, a book. What a waste of time...')
                            Party.player2.talk('BUT WAIT!','bigtext')
                            Party.player2.talk('Is it about SWORDS???','bigtext')
                            self.talk('Uh, yeah...')
                            self.talk('But i\'m reading it first.')
                            self.talk('...')
                            self.talk('...')
                            self.talk('...')
                            Party.player2.talk('Are you done yet???')
                            self.talk('...')
                            self.talk('...')
                            self.talk('...')
                            Party.player2.talk('COME ONNNNNNNNN--')
                            
                            printstuff('A new, nimbler slicing method\\was made clearer to Fredrick...')
                            printstuff('Quickslice was added to your zmoves.')
                            Party.zmoves.append(pc.quickslice)
                            
                            Party.player2.talk('Gimme the book!')
                            printstuff('Genmu grabs the book and starts reading.')
                            Party.player2.talk('Ugh, where are the pictures...?\\This book is horrible!')
                            printstuff('He throws the book away.\\\\At least someone got use of it...')

                            Party.player2.talk("I gotta go find that moron.")
                            Party.player2.talk("I\'ll get you a sword, too.")
                            Party.player2.talk('I won\'t keep you waiting TOO long.')
                            printstuff("Genmu has left the party.")
                    #if moo.name == 'flyer':
                    #    
                    #    self.talk('Someone dropped a flyer for a shop, it seems.')
                    #    Party.player2.talk('A shop!?! I sure hope they have swords.')
                    #    if game.gamedata.preference == 'will':
                    #        self.talk('It seems like there\'s a\\ good chance of that...')
                    #    if game.gamedata.preference == 'logic':
                    #        self.talk('I think we should go and see.')
                    #    if game.gamedata.preference == 'emotion':
                    #        self.talk('I don\'t think that\'s what\\ we should be worried about.')
                        moo.properties['opened'] = 1
                if moo.name == 'safe':
                    if moo.properties['opened'] == 0:
                        num = random.randint(1,5)
                        num = 1
                        if num == 1:
                            flavor = 'You found a safe.\\The lock on it is busted.'
                        printstuff(flavor)
                        
                        printstuff('You got $'+str(moo.properties['gold'])+'.')
                        Party.money += moo.properties['gold']
                        moo.properties['opened'] = 1
                        x = 'money'
                        y = str(moo.properties['moneyid'])
                        x += y
                        game.gamedata.events[x] = True
                        for i in allitems:
                            if 'moneyid' in i.tile.properties:
                                if i.tile.properties['moneyid'] == moo.properties['moneyid']:
                                    i.image = pygame.image.load('moneychestopen.png')
                    if game.currentplace == 'grassdungeon4.tmx':
                        if 'allcut4' not in game.gamedata.events:
                            printstuff('There was an extra piece of paper in the safe.')
                            printstuff('It is an incantation to remove all nearby grass.')
                            Party.player2.talk('Lemme see it.')
                            Party.player2.talk('Hmm.')
                            Party.player2.talk('Genmu mispronounces some mystic words...')
                            printstuff('All the grass vanishes.')
                            allcut = True
                            game.gamedata.events['allcut4'] = True
                        else:
                            printstuff('No, you can\'t use\\the spell anywhere else.')
                        
                    else:
                        num = random.randint(1,5)
                        num = 1
                        if num == 1:
                            flavor = 'It\'s empty, thanks to you.'
                        if num == 2:
                            flavor = 'You decide to lock the safe.'
                    
                if game.currentplace == 'place_of_judgement.tmx':
                    if moo.name == 'sword':
                        if 'denial' in moo.item.specialproperties:
                            self.talk('Nope, not interested.')
                            return
                        if moo.item.specialproperties['rejection']:
                             #printstuff('Are you going to take the sword, or not?')
                             chosenoption = doublequestion('Are you going to take the sword, or not?','Gimme that sword.','Nah...')
                             if chosenoption == 1:
                                 printstuff('Fredrick finally takes the sword.')
                                 printstuff('The sword feels happy...')
                                 gamedata.choices.append('swordreturner')
                                 
                                 Party.equipment.append(sharpfirstsword)
                                 for i in game.items:
                                    if i.name == moo.name:
                                        i.kill()
                                        del i
                                 del moo
                                 return
                                 
                             if chosenoption == 2:
                                 self.talk('Probably shouldn\'t touch it...')
                                 printstuff('The sword sinks into despair...')
                             return
                        printstuff(moo.properties['description'])
                        printstuff("Will you take it?")
                        game.gamedata.events['lookedatsword'] = True
                        chosenoption = triplequestion('Finders keepers.','But doesn\'t that belong to someone?','I don\'t want a sword.')
                       
                        if chosenoption == 1:
                            self.talk('(Wonder who left a sword just lying around...?)')
                            
                            printstuff('Fredrick awkwardly grabs the sword...')
                            gamedata.logicpoints += 1
                            Party.equipment.append(eval(moo.properties['itemid']))
                            
                           
                            for i in game.items:
                                if i.name == moo.name:
                                    i.kill()
                                    del i
                            del moo
                            return
                            #moo.kill()
                            #del moo
                            
                        elif chosenoption == 2:
                            self.talk('(Should I really just take random things?)')
                            #self.talk('(I don\'t need to risk angering\\one of this place\'s residents, as well.')
                            printstuff('The sword feels rejected...')
                            printstuff('Did it just get a little sharper?')
                            moo.item.specialproperties['rejection'] = True
                            moo.item.specialproperties['attackboost'] = 25
                            game.gamedata.emotionpoints += 1
                            #Through difficulty, we become stronger?
                        elif chosenoption == 3:
                            gamedata.willpoints += 1
                            self.talk("...")
                            game.gamedata.events['swordleaver'] = True
##                            gamedata.choices.append('swordreturner')
##                            self.talk('Weird. Who dropped this?')
##                            self.talk('Well, someone should get\\some use out of it.')
##                            printstuff('Fredrick just kinda grabs the sword.')
##                            Party.equipment.append(eval(moo.properties['itemid']))
##                            for i in game.items:
##                                if i.name == moo.name:
##                                    i.kill()
##                                    del i
##                            del moo
##                            return
                #if game.currentplace == 'grassstage.tmx':
                #    if moo.name == 'chest' and m
                if game.currentplace == 'grassstage2a.tmx':
                    if moo.name == 'flyer':
                        #printstuff(moo.properties['description'])
                        if 'grassstageflyer' not in game.gamedata.events:
                            printstuff("                        Fate's Salesman\\Everything you could ever want, at your fingertips.")
                            Party.player2.talk('Who writes like that?')
                            Party.player2.talk('Is it that guy over there?')
                            self.talk('Maybe..?')
                            game.gamedata.events['grassstageflyer'] = True
                            #printstuff('Fredrick grabs the flyer off the ground.')
                        else:
                            Party.player2.talk('I don\'t want to read it again.')
                    
                
                        
                        
                
                if game.currentplace == 'grassdungeon2.tmx' and 'nodesc' not in moo.properties:
                    findpreference()
##                    printstuff(moo.properties['description'])
##                    if game.gamedata.preference == 'will':
##                        self.talk('I don\'t think Genmu should know about this...')
##                    if game.gamedata.preference == 'logic':
##                        self.talk('Who is this guy?')
##                    if game.gamedata.preference == 'emotion':
##                        self.talk('Genmu, you should look at this...')
##                if game.currentplace == 'grassdungeon3.tmx':
##                    Party.player2.talk('*GASP*!!!')
##                    Party.player2.talk('My sword!!!')
##                    Party.player2.talk('REUNITED AT LAST!!!!!')
                    
                    
                    
                            
##                            self.talk('HEY! WHO LEFT A SWORD HERE?')
##                            self.talk('HELLOOOOOOOOOOOOOO!!!')
##                            printstuff('I did. Can you just take the sword already?',1,0,1)
##                            self.talk('Fine...')
                        
            for character in characters:
                print('checking characters')
                ##print(character.name,'Checking for')
                if character.name == moo.name:
                    ##print('character found')
                    if 'debug' in moo.properties:
                        for event in pygame.event.get():
                            pass
                        character.animation('armraise.png',35,4,200,dt)
                        break
                    if 'test' in moo.properties:
                        character.talk('ALEXANDERRRRRRRRR.')
                        chosenoption = character.askandquestion('Seeeeeeeeeed.','Fight me!','AAAAAA!')
                        if chosenoption == 1:
                            battle.Battle(Party.player1,[battle.fredrick],[battle.swordnyu],'grass stage',None,(89,89,204),[firstorb],'SwordNyu Battle',gamedata)
                        if chosenoption == 2:
                    
                            character.walkmode = True
                            character.followmode = True
                            Party.player2 = character

                    if 'graygoatexplain' in moo.properties:
                        character.talk('Oh, I really like goats.')
                        character.talk('Why is that important?')
                        character.talk('Well, there was a need for another race of people.')
                        character.talk('I have some authority over these matters, if you will.')
                        character.talk('So, naturally...')
                        character.talk('When the specifics of the race were decided...')
                        character.talk('One was chosen that I\\would feel motivated to watch over.')
                        character.talk('You can assume what that led to.')
                    if 'save' in moo.properties:
                        ##print('save detected'
                        if game.currentplace == 'grassstage.tmx':
                            findpreference()
                            game.gamedata.events['talkedtosaveguy'] = True

                            if Party.player2 != None:
                                if Party.player2.name == 'Genmu':
                                    character.talk('It seems that someone has made a friend...')
                                    Party.player2.talk('Heh, well...')
                                    Party.player2.talk('When you\'re a legend,\\ they just throw themselves at you...')
                                    chosenoption = character.askandquestion('Do you wish for me to save for you?','Yea.','Please help me.')
                                    if chosenoption == 1:
                                        character.talk('Very well.')
                                        savegame()
                                    if chosenoption == 2:
                                        character.talk('Alright...?')
                                        character.talk('Have you been the sword shop in town?')
                            else:
                                if character.talkedbefore == True:
                                    if character.name == 'Random Save Guy':
                                        chosenoption = character.askandquestion('Do you wish for me to save for you?','Do it, buddy.','Don\'t worry about it.')
                                        if chosenoption == 1:
                                            character.talk('That is my plan.')
                                            savegame()
                                            character.talk('It is done.')
                                        if chosenoption == 2:
                                            character.talk('But worrying about it is my job.')
                                            character.talk('There\'s something interesting to the east...')
                                    else:
                                        chosenoption = character.askandquestion('Do you wish for me to save for you?','Yeah.','Uh, not now.')
                                        if chosenoption == 1:
                                            if game.gamedata.preference == 'will':
                                                character.talk('If you didn\'t, why would you talk to me?')
                                                self.talk('Good point.')
                                                character.talk('I have my moments.')
                                                savegame()
                                            if game.gamedata.preference == 'emotion':
                                                character.talk('If you didn\'t, why would you talk to me?')
                                                character.talk('Because you seem interesting.')
                                                self.talk('I am flattered, but basic conversation\\is not what I am here to do.')
                                                savegame()
                                            
                                        if chosenoption == 2:
                                            character.talk('Then why are you here?')
                                            
                                            
                                if not character.talkedbefore:        

                                    if game.gamedata.preference == 'will' or 'emotion':
                                        self.talk('Hello.')
                                        character.nameless = True
                                        character.talk('Why are you talking to me?')
                                        character.talk('I was admiring the flower...')
                                        character.talk("Also I have no idea who you are.")
                                        character.talk('...')
                                        
                                        character.talk('(He\'s just standing there, staring at me.)')
                                        character.talk('(Wait, maybe he\'s the person\\I was told about...)')
                                        character.talk('So, ya gonna let me do my thing, or...?')
                                        chosenoption = triplequestion('Nah...','Go for it.','Who are you???')
                                        character.talkedbefore = True
                                        if chosenoption == 1:
                                            character.talk('Well, you might need to eventually.')
                                            character.talk('(But what if he\'s trying not to?)')
                                        if chosenoption == 2:
                                            character.talk('If you say so...')
                                            savegame()
                                            printstuff('Your adventure to this point has,\\ for lack of a better term, been saved.')
                                            self.talk('See you around, random save guy.')
                                            character.name = 'Random Save Guy'
                                            character.nameless = False
                                            character.talk('Until we meet again.')
                                            game.gamedata.events['saveguytrust'] = 1
                                        if chosenoption == 3:
                                            character.talk('Well, I\'m a person who\\ keeps track of people\'s journeys.')
                                            character.talk('I have been told to keep\\track of your adventure.')
                                            self.talk('Okay.')
                                            character.talk('So, we are going to save now.')
                                            self.talk('What exactly are we going to save?')
                                            character.talk('Just tell me everything\\that has happened to you so far.')
                                            self.talk('Everything?')
                                            character.talk('Well, all that\'s happened\\ in about the last 15 minutes...')
                                            self.talk('Well, it all started when I woke up\\in this weird kinda empty place...')
                                            game.BlackOut()
                                            printstuff('Your game has been...\\how do I put this...\\Saved.')
                                            savegame()
                                            character.talk('And then he did what with lasers?')
                                            character.talk('Man, whatever.')
                                            character.talk('I saw some weird guy over to the right.')
                                            character.talk('He seems to have a strange obsession with swords.')
                                            character.talk('Maybe he\'s what you\'re\\looking for?')
                                    elif game.gamedata.preference == 'logic':
                                        self.talk('Why are you just standing there?')
                                        character.talk('I am waiting for you.')
                                        self.talk('Why are you waiting for me?')
                                        character.talk('Because an acquaintance of mine told me to.')
                                        self.talk('Okay.')
                                        character.talk('Why?')
                                        self.talk('Because I am supposed to keep track of your journey.')
                                        character.talkedbefore = True
##                            if chosenoption == 1:
##                                character.talk('ALrighty then.')
##                                savegame()
##                                character.talk('That\'s all.')
##                                character.talk('Come back when ya need your actions saved.')
##                            elif chosenoption == 2:
##                                character.talk('Then why\'d ya talk to me?')
                                
                        
                            
                                

                                   
                            #break
                        if game.currentplace == 'grassdungeon19.tmx':
                            if "save" in moo.properties:
                                character.talk('Ah, you\'re almost done with this place.')
                                character.talk('But, as fate so decrees, a challenge awaits.')
                                character.talk('Hopefully it has been a learning\\experience for the both of you.')
                                character.talk('Well...?')
                                chosenoption = doublequestion('Should I save?','Yeah.','Well...')
                                if chosenoption == 1:
                                    savegame()
                                else:
                                    character.talk('Interesting.')
                                    character.talk('Well, it\'s not really interesting, but...')
                                character.talk("You look somewhat beat up.")
                                character.talk('Do you need some healing?')
                                chosenoption = doublequestion("Healing...?","Please fix me.","Really, I\'m fine.")
                                if chosenoption == 1:
                                    character.talk('Good, good.')
                                    printstuff("The man pulls something from somewhere...")
                                    character.talk("Drink this.")
                                    Party.player2.talk('Oh ho! A drink!\\And I was getting so thirsty...')
                                    printstuff("Genmu and Fredrick consume the drink.")
                                    game.player.player.Chealth = copy.copy(game.player.player.Mhealth)
                                    game.player.player.Cmp = copy.copy(game.player.player.Mmp)
                                    printstuff('The drink was somewhat sweet.')
                                    Party.player2.talk('What WAS that thing you gave us?')
                                    character.talk("Can't tell you.")
                                    
                            if "SPflag1" in moo.properties:
                                character.talk('Mister, you saved us!')
                                character.talk("You should adventure with us sometime!")
                                    
                        if game.currentplace == 'grasstownhotel.tmx':
                            if 'swordguytrust' in game.gamedata.events:
                                character.name = 'Random Save Dude'
                            character.talk('Hm. This hotel is just...')
                            character.talk('...')
                            character.talk('Oh yeah, you guys...')
                            chosenoption = doublequestion('Do you want to save?','Yes.','No.')
                            if chosenoption == 1:
                                savegame()
                                character.talk('It is done.')
                                character.talk('Perhaps you should write a memoir about your journey.')
                            if chosenoption == 2:
                                character.talk('That person at the front desk\\sure is something else, huh?')
                                character.talk('He has this look in his\\eyes that I can\'t describe.')
                                character.talk("He\'s also a sheeperson.")
                        if game.currentplace == 'grassdungeon8.tmx':
                            character.talk('It\'s getting rather cold up here...')
                            character.talk('Right?')
                            chosenoption = doublequestion('','I need you to save.','Yeah, it\'s freezing.')
                            if chosenoption == 1:
                                character.talk('Oh, whoops. Forgot that was my job.')
                                savegame()
                                character.talk('Alright, it is done.')
                                Party.player2.talk('WHO ARE YOU???')
                                character.talk('I am a person who helps your friend save.')
                                self.talk('He follows me everywhere.')
                                Party.player2.talk('But that\'s MY job...')
                                #Party.player2.talk('How are you EVERYWHERE we go???')
                                #character.talk('What? It\'s my job.')
                            if chosenoption == 2:
                                character.talk('I didn\'t know we were this close to the snow.')
                                character.talk('That village should be nearby...')
                                character.talk('You know, the one with all the sheep?')
                        if game.currentplace == '1stkalpabattle.tmx':
                            character.talk('How\'d you end up here?')
                            character.talk('I think I\'m in over my head with tracking you...')
                            character.talk('...')
                            self.talk('...')
                            character.talk('Hey, look.\\You need to be extremely careful.')
                            character.talk('You are in serious danger,\\if this place is what i think it is.')
                            character.talk('Also, no one will be able to save you here,\\so don\'t take any undue risks.')
                            character.talk('That being said...')
                            chosenoption = doublequestion('Do you want to save?','Yes.','No.')
                            if chosenoption == 1:
                                savegame()
                                character.talk('It is done.')
                                character.talk('I cannot stress being careful enough.')
                                character.talk('You have a nonzero chance of death here...')
                                
                            if chosenoption == 2:
                                character.talk('Wow, okay, you know what? Fine.')
                            
                    if game.currentplace == 'firstplace.tmx':
                        if tuple(targetarea) == tuple(character.coords):
                            ##print(moo.properties['specialtalk'], 'Hey')
                            if moo.properties['specialtalk'] == True:
                                ##print(moo.properties['specialtalk'], 'Thing')
                                character.talk('Hello.')
                                #self.talk('Uh, hello.')
                                self.talk('...')
                                character.talk('(Not much of a talker, are you?)',wait=1)
                                chosenoption = character.askandquestion('Do you know why you\'re here?','...','...','Yes, actually.')
                                if chosenoption == 'Yes, actually.':
                                    character.talk('Not your first time, is it?')
                                    self.talk('Nope.')
                                    self.talk('Also, can you hurry this up?\\I\'ve got places to be.')
                                    character.talk('Fine, fine.')
                                else:
                                    character.talk('This is the gray area.\\We will ask you questions, and you answer them.\\Simple, right?')
                                    self.talk('...')
                                    character.talk('Well, anyway...',wait=0)
                                    character.talk('Please be honest with us.\\Answer us the way you know you should.')
                                    character.talk('You\'ll find out more over there.')

                            elif moo.properties['specialtalk'] == 2:
                                character.talk('So...')
                                printstuff('...')
                                character.talk('Anyway, you\'re about to have a little adventure.')
                                character.talk('I bet you\'re wondering "Why am I here?"')
                                character.talk('Well, you\'re here to learn the basics\\of your upcoming journey.')
                                character.talk('You\'re also probably wondering\\"What are the basics, white cloak person?"')
                                character.talk('Well, lucky for you,\\you\'ll find out over there.')
                                printstuff('...')
                                character.talk('So, get over there.')
                                printstuff('...')
                                character.talk('Right. Now.')
                                killtime(1)
                                character.talk('Seriously?')
        ##                        self.talk('Okay, I walked a few feet. I want answers.'
                            elif moo.properties['specialtalk'] == 3:
                                character.talk('So,you walked ALL the way over here \\and held up your end of the bargain.')
                                character.talk('Now it\'s time for me to hold up mine.')
                                character.talk('This may sting a little bit...')
                                character.animation('armraise.png',35,5,200,dt)
                                game.BlackOut()
                                game.initArea('itemplace.tmx')
                                
                            if 'temporary' in character.cell.properties:
                                game.fadeOut()
                                character.kill()
                                del moo.properties['sprite']
                                del moo.properties['description']
                    if game.currentplace == 'place_of_judgement.tmx':
                        if 'SPflag2' in moo.properties:
                            character.talk('OH! An enemy?')
                            character.talk("Hee hee hee. This will be fun...")
                            battle.Battle(Party.player1,[battle.fredrick],[battle.darknyu],
                            'gray area',None,(0,0,0),['Stick','First Aid Kit'],'First Battle',gamedata)
                            character.talk("You meanie! I was supposed to win! Not you!")
                            character.talk("Someday, I will defeat you!")
                            printstuff("The creature has sworn a solemn oath against you.")
                            character.rect.x += 9999
                            

                        if (tuple(targetarea) == tuple(character.coords) or cutscene) and 'SPflag1' in moo.properties:
                           
                            
                            #Why did you leave that sword?
                            #Do you know what i went through to get it?
                            character.talk('Well, it\'s more like\\I summoned you here, but.')
                            if "secondtime" in game.gamedata.events:
                                printstuff("A knowing smirk falls upon Gray's face.")
                                character.talk("Fredrick...")
                                character.talk("It's rude to pretend you don't know me.")
                                character.talk('...')
                                character.talk("After going through all that, you're still playing coy?")
                                character.talk("I thought you'd be more excited\\to get back to your ladyfriend...")
                            character.talk('The specifics aren\'t too important...')
                            character.talk('Besides, you were probably just\\getting home from school or whatever.')
                            character.talk('But don\'t worry; you\'ll get back to\\your dorky school friends soon enough.')
                            
                            #self.talk('Wait!')
                            #character.talk('What?')
                            chosenoption = triplequestion('Who are you?','Where am I?','What\'s going on?')
                            if chosenoption == 1:
                                gamedata.logicpoints += 1
                                character.talk('Who am I?')
                                character.talk('Of course, the one person\\I cannot tell that to asks me that.')
                                character.talk('...')
                                character.talk('They usually call me "Gray".')
                                character.nameless = False
                                character.name = 'Gray'
                                character.talk('I am "in charge" of your world.')
                                character.talk('You are about to begin a journey;\\My job is to ensure you finish it.')
                                character.talk('So, now we begin.')
                                self.talk('Wait, I don\'t even know what\'s going on--')
                                #character.talk('You will after this.')
                                #self.talk('I\'m as ready as I\'ll ever be.')
                                #character.talk('That\'s not true.\\You\'ll be more ready after this.')
                                game.SPFade(game.dt)
                                battle.Battle(Party.player1,[battle.fredrick],[battle.ghostface],'gray area',None,(0,0,0),['Stick','First Aid Kit'],'First Battle (Starring Gray Cloak)',gamedata)

                                
                                               
                                
                                    
                            elif chosenoption == 2:
                                gamedata.emotionpoints += 1
                                character.talk('This place is known as the "Gray Area".')
                                character.talk('It is a place hidden between worlds.')
                                #character.talk('People like me keep your world going from here.')
                               
                                character.talk('It is functionally the heart of your world.')
                                
                                self.talk('Cool.')
                                character.talk('That is one way to look at it...')
                                character.talk('I am one of a select few\\who have control over this place.')
                                character.talk('Thus, I have called you here to \\start you off on your journey.')
                                
                                
                                game.SPFade(game.dt)

                                battle.Battle(Party.player1,[battle.fredrick],[battle.ghostface],'gray area',None,(0,0,0),['Stick','First Aid Kit'],'First Battle (Starring Gray Cloak)',gamedata)

                            elif chosenoption == 3:
                                gamedata.willpoints += 1
                                character.talk('A being which I have\\defeated before has returned.')
                                character.talk('Of course, you are the one who must defeat him.')
                                self.talk('Why me?')
                                character.talk('You really think I\'d just\\grab some random kid off the street for this?')
                                character.talk('Unfortunately, you\'re "special".')
                                character.talk('Hopefully.')
                                character.talk('I really hope you are actually special.')
                                
        
                                character.talk('Look, we don\'t have all day. Let\'s begin.')
                                

                                game.SPFade(game.dt)
                                battle.Battle(Party.player1,[battle.fredrick],[battle.ghostface],'gray area',None,(0,0,0),['Stick','First Aid Kit'],'First Battle (Starring Gray Cloak)',gamedata)
                            
                            #Rewrite for difficulty from here for cockiness?
                            
##                            for i in gamedata.data:
##                                if 'GCSkill' in i.keys():
##                                    x = i['GCSkill']
##                            assert x != None
##                            ##print(x,'Difficulty result')
                            x = gamedata.GCSkill
                            findpreference()
                            ##print(x,'battle difficulty result')
                            preference = gamedata.preference
                            
                            if  x == 2:
                                if preference == 'logic':
                                    self.talk('Was that supposed to be a challenge?')
                                    character.talk('Don\'t get TOO cocky.\\I was going easy on you.')
                                elif preference == 'emotion':
                                    
                                    character.talk('Very adequate.')
                                elif preference == 'will':
                                    self.talk('I think I\'m ready.')
                                    character.talk('Yes, I think so, too.')
                                    character.talk('Have you done this before?')
                                

                                
                            elif x == 1:
                                if game.gamedata.preference == 'logic':
                                    self.talk('Guess I did alright.')
                                    character.talk('Yes, "alright" is how I would describe it.')
                                if game.gamedata.preference == 'emotion':
                                    character.talk('Well, I guess that\'s good enough for now.')
                                    self.talk('So, does that mean I did well, or...?')
                                    character.talk('You did as well as I thought you would do.')
                                    self.talk('Which is?')
                                    character.talk('Eh, whatever.')
                                    
                                if game.gamedata.preference == 'will':
                                    print('whatever')
                            elif x == 0:
                                character.talk('Heh. Uh...')
                                character.talk('You\'ll get better eventually.')
                                self.talk('(Yikes.)')
                                character.talk('Maybe...')
                                self.talk('(Was I really THAT bad?')
                                character.talk("(Man, he was really bad.)")
                            elif x == 'ded':
                                character.talk('Please tell me you did that poorly on purpose.')
                            character.talk('Anyway, that\'s it.')
                            character.talk('You are now hopefully passable at fighting.')
                            
                            if game.gamedata.preference == 'logic':
                                self.talk('(Certainly took long enough...)')
                            
                                
                            #character.talk('Your chances of survival have hopefully increased.')
##                            character.talk('So, what are your thoughts on sheep?')
##                            if game.gamedata.preference == 'logic':
##                                #speak('Do you like sheep?',ghostface)
##                                self.talk('They\'re okay, I guess...')
##                                character.talk('Perhaps your opinion will change...')
##                                
##                                #character.talk('(Admittedly, not a sheep in the\\ traditional sense, but...)')
##                            if game.gamedata.preference == 'emotion':
##                                self.talk('I like them...')
##                                # so, i made a mistake where fredrick says the next line
##                                # instead of gray cloak
##                                # It gives it an entirely different meaning.
##                                character.talk('(If only he knew...)')
                                   #lol dummied out tho
##                            if game.gamedata.preference == 'will':
##                                self.talk('What kind of sheep?')
##                                character.talk('Heh heh heh. You will see.')
##                            character.talk('As I said earlier, You\'ve got a journey to go on.')
##                            character.talk('So, this is where you get off.')
##                            self.talk('How am I supposed to explain where I was to my friends?')
##                            character.talk('Don\'t worry about it. I\'ll take care of it.')
##                            #self.talk('So, how am I supposed to get home from...\\ whereever I am?')
                            
#                            character.talk('Like this.')
                            character.talk('One last thing, though...')
                            character.talk('In order for you to\\defeat that old acquaintance of mine,\\you must become stronger.')
                            character.talk('To gain that strength, you must master one of the\\scariest things people can offer:\\Relationships.')
                            #self.talk('Friendship? How does that help me kill things?')
                            #character.talk('Ugh, just listen...')
                            character.talk('I must unfortunately offer you an example.')
                            printstuff('You have established a bond\\with the Man in the Gray Cloak.')
                            Party.bonds.append(pc.GrayCloakBond)
                            for i in Party.bonds:
                                if i.name == 'Gray' and i.level == 1:
                                    #i.level += 1
                                    printstuff('A voice begins speaking into Fredrick\'s mind.')
                                    printstuff('You, the one whose path leads to the end...',0,1,1)
                                    printstuff('Let other\'s paths guide you to your own.',0,1,1)
                                    
                            printstuff('Gray has shared some of his power with Fredrick.')
                            printstuff('Fredrick learned the magic spell, Beam.\\Beam has been added to your Xmoves.')
                            printstuff('Your current xmove has also become beam.')
                            Party.xmoves.append(pc.laser)
                            game.player.xmove = pc.laser
                            printstuff('Your relationship with a person\\is shown through a bond,\\viewable in the world menu.')
                            
                            character.talk('For better or for worse,\\ you and I are now connected.')
                            character.talk('...')
                            self.talk('...')
                            character.talk('Once you make a bond, you can strengthen it.')
                            character.talk('You do this by getting to know a person,\\and showing that you understand them.')
                            character.talk('Strengthening a bond strengthens you,\\with unique benefits given\\when a bond reaches its limit.')
                            character.talk('Try to make as many friends as you can.')
                            character.talk('Well, actually, try to make the\\maximum number of friends possible.')
                            character.talk('But enough about your friends,\\and more about mine...')
                            
                            character.talk('In order for you to reach that enemy of mine,\\you must find my two partners.')
                            character.talk('They wear cloaks similar to mine,\\and are as unusual as I am.')
                            character.talk('It also seems that they have become\\something of a legend in your world.')
                            character.talk('Their locations are unfortunately\\unknown to me-- finding them falls on you.')
                            character.talk('But you aren\'t totally lost.\\When you return to you world,\\you will meet a swordsman.')
                            character.talk('Not only is he more powerful\\than his airheaded personality implies, but...')
                            character.talk('He seems to have some awareness\\of one of my friend\'s location.')
                            character.talk('It is important that you get to know him.')
                            character.talk('Normally, I\'d let you ask questions,\\but our precious time is dwindling.')
                            #questions here on second playthrough?
##                            if game.gamedata.preference == 'emotion':
##                                self.talk('No, not really...')
##                                character.talk('Are you sure about that?')
##                            if game.gamedata.preference == 'logic':
##                                self.talk('Seems like it.')
##                            if game.gamedata.preference == 'will':
##                                self.talk('That\'s what you\'ve been telling\\me the whole time.')
##                                character.talk('Touche.')
                            
                            character.animation('armraise.png',35,5,500,dt)
                            game.fadeOut()
                            self.rect.y += 10000 #Yep
                            character.setSprite()
                            game.killtime(2)
                            
                            lastspot = copy.copy(game.currentfocus)
                            done = False
                            theleaderofthebunch = 0
                            clock = pygame.time.Clock()

                            while not done:
                                theleaderofthebunch += 1
                                center = [character.rect.x,character.rect.y]#[(lastspot[0] + character.rect.x)/2,(lastspot[1] + character.rect.y)/2]
                                centerdiff = [(center[0] - lastspot[0])/30,(center[1] - lastspot[1])/30]
                                game.currentfocus = [lastspot[0] + (centerdiff[0]*theleaderofthebunch),lastspot[1] + (centerdiff[1]*theleaderofthebunch)]
                                screenupdate()
                                clock.tick(30)
                                if theleaderofthebunch == 30: #DK
                                    done = True
                            character.talk("He really is just like him.")
                            character.talk('I hope things go better this time...')
                            #character.talk('It really is beginning again.')
                            #character.talk('I hope he\'s strong enough.')
                            #character.talk('He wasn\'t before, but...')
                            #character.talk('No, I shouldn\'t talk like that.')

                            game.BlackOut()
                            
                            game.initArea('grassstage.tmx')
                            game.killtime(1)
                            printstuff("Pressing A will sometimes yield\\ valuable information.")
                            #why does screen glitch out if this next killtime is not active?
                            game.killtime(0.5)
                            printstuff("You must now press the A button.")
                            
                            return
                        

                            
                    if game.currentplace == 'grassstage.tmx':
                        if tuple(targetarea) == tuple(character.coords) and 'SPflag1' in moo.properties:
                            character.talk('You better find that swordsman.')
                            self.talk('Could you tell me where he is?')
                            character.talk('Somewhere. He\'s somewhere.')
                            
                            self.talk('Seriously?') 
                            character.talk('You\'ve gotta let me have \\some fun SOMEWHERE...')
                            character.talk('Anyway, I\'m sure you\'ll be seeing him\\soon enough.')
                            character.talk('Go look around for him.')
                            character.talk('He\'s not someone who\'s easy to miss.')
                    if game.currentplace == 'grassstage2.tmx':
                        if tuple(targetarea) == tuple(character.coords) and 'SPflag1' in moo.properties:
                            ###character.talk('Who are YOU supposed to be?')
                            ###self.talk('Uh, my name is--')
                            character.talk('HEEEEEY!!!','bigtext')
                            
                    if game.currentplace == 'grassstage2b.tmx':
                        if 'SPflag1' in moo.properties:
                            printstuff('The dog is sniffing around for something.')
                            character.walk('left',5)
                            character.talk('*Sniff*, *Sniff*')
                            character.talk('Bark!')
                            printstuff('Your existence has begun to anger the dog.')
                            character.talk('BARK BARK!')
                            character.walk('right',30,1)
                                                 
                    if game.currentplace == 'grassstage2a.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('I am sorry that we have\\been given these roles to play.')
                            character.talk('Who is it that will render their final judgment on us?')
                            
                            #character.talk('The burden of truth that you bear is heavy, indeed.')
                            character.talk('I trust that you will emerge victorious in the end.')
                            character.talk('Although, I admit those beliefs need testing.')
                            battle.Battle(Party.player1,[battle.fredrick],[battle.dark],'gray area',None,(89,89,204),[firstorb],'Dark Battle',gamedata)

                        if 'SPflag2' in moo.properties:
                            if character.talkedbefore:
                                if game.preference == 'will':
                                    character.talk('Are you enjoying your... thing?')
                                    self.talk('I probably would if I knew what it was...')
                                    character.talk('It\'s a mystical item said to contain\\ the essence of a\\ legendary hero.')
                                    self.talk('Wow.\\ \\How do I use it?')
                                    character.talk('Ah, it\'s simple, really.')
                                    character.talk('Or, at least that\'s what the guy who gave it to me said.')
                                    character.talk('It\'s a shame I didn\'t listen.')
                                    self.talk('...')
                                if game.preference == 'emotion':
                                    self.talk('Well, thank you for... whatever this is.')
                                    character.talk('Of course.')
                                    character.talk('If you ever need weird garbage,\\you know who to talk to.')
                                if game.preference == 'logic':
                                    self.talk('Thank you for giving me that orb.')
                                    character.talk('That\'s what I do.\\But only for people named "Fredrick".')
                                    character.talk('Aren\'t you lucky that\'s your name?')
                                    character.talk('Imagine someone gave you a far\\worse name that wasn\'t "Fredrick".')
                                    character.talk("That\'d really suck.")
                                    self.talk('Uh, yeah...?')
                            if not character.talkedbefore:
                                self.talk('Hey, is this you?')
                                printstuff('Fredrick shows the salesman the flyer.')
                                character.talk('"Fate\'s salesman?" Ugh...')
                                character.talk('You\'re kidding, right?\\I have enough self respect to\\not call myself that.')
                                character.talk('I saw some weird traveling merchant pass by though.\\Had a lot of swords.')
                                character.talk('Yeah, he looked like the sort who would call himself that...')
                                Party.player2.talk("Where\'d he go?")
                                character.talk('He went up into that forest over there...')
                               
                                self.talk('Anyway, can I buy something?')
                                character.talk('Who said I was selling anything?')
                                findpreference()
                                if 'secondtime' in game.gamedata.events:
                                    self.talk('Uh, maybe the sign that says "Stuff" on it.')
                                    character.talk('Who put that there?')
                                    character.talk('(Darn it...)')
                                    character.talk('All right, I suppose that means\\ I have to sell you something.')
                                    character.talk('Name your price.')
                                    chosenoption = triplequestion('$5', '$0','-$5')
                                    if chosenoption == 3:
                                        character.talk('What? You want $5 for it?')
                                        self.talk('I drive a hard bargain.')
                                        character.talk('You truly do.')
                                        printstuff('You got a great deal. And an orb.')
                                        Party.money += 5
                                        Party.keyitems.append(firstorb)
                                    if chosenoption == 2:
                                        character.talk('I should have seen that coming.')
                                        self.talk('There\'s no better price.')
                                        character.talk('Ah, but someone else would beg to differ.')
                                        self.talk('Who?')
                                        character.talk('Again, you really should know who they are.')
                                        printstuff('You got an orb.\\Seems there is such thing as free.')
                                        Party.keyitems.append(firstorb)
                                    if chosenoption == 1:
                                        character.talk('$5? Well, I\'ll take it.')
                                        printstuff('He hands you $5 and an orb.')
                                        character.talk('Ah, I\m finally free of that annoying thing.')
                                        self.talk('(This is a good result.)')
                                        character.talk('A pleasure doing business with you.')
                                        
                                        
                                else:
##                                    self.talk('Then what ARE you doing out here?')
##                                    character.talk('I am waiting for someone to show up.\\I am supposed to give them something.')
##                                    self.talk('Who are you looking for?')
##                                    character.talk('You should know that more than anyone else.')
##                                    character.talk('Just take the darn thing already....')
##                                    printstuff('The man hands you an orb.')
##                                    printstuff('You got a strange orb.')
##                                    printstuff('It was added to your Keyitems.')
##                                    Party.keyitems.append(firstorb)
##                                if game.gamedata.preference == 'emotion':
                                    self.talk('Is your store open?')
                                    character.talk('What store? I like to stand here\\ and get people\'s hopes up all day.')
                                    self.talk('Are you serious?')
                                    character.talk('Do I look serious?\\ I should, because I am.')
                                    character.talk('Well, here\'s something to cheer you up, anyway.')
                                    printstuff('The man shoves a strange orb at you.')
                                    Party.keyitems.append(firstorb)
                                character.talkedbefore = True
                                game.gamedata.events['metorbsalesman'] = True
                                    
                                    #character.talk('Sorry, you reminded me of someone I once knew.')
                                    
    ##                            character.talk('Yeah, I\'ve got this weird...\\whatever this thing is.')
    ##                            character.talk('You want it? It seems mysterious...')
    ##                            character.talk('(Heh heh heh...)')
    ##                            character.talk('(When he brings it to that tree...)')

                    if game.currentplace == 'grassstage4.tmx':
                        print('Current stage is gs4')
                        if 'SPflag1' in moo.properties:
                            if character.talkedbefore == True:
                                pass
                            #character.talk('You have not brought the sigil.')
                            
                            character.talk('Hey, pallie.\\Any chance ya got an orb on ya?')
                            self.talk('Well, i--')
                            hasorb = False
                            for i in Party.keyitems:
                                if i.name == 'Orb?':
                                    hasorb = True

                            if hasorb:
                                character.talk('Hold it...')
                                character.talk('Ah ha. Looks like we\'ve got a winner.')
                                if Party.player2:
                                    if Party.player2.name == 'Genmu':
                                        character.talkedbefore = True
                                        character.talk('Hey, sword guy?')
                                        Party.player2.talk('I like swords.')
                                        #fredrick is more aware as the true end is reached
                                        character.talk('If ya gimme this sharp eyed bloke\\for a while, I\'ll give ya a sword.')
                                        Party.player2.talk('YES.','bigtext')
                                        self.talk('He gave me up for a sword THAT easily?')
                                        character.talk('Hey, when someone wants something,\\they want something.')
                                        self.talk('So what do you want?')
                                        character.talk('To teach ya a lesson you won\'t forget.')
                                        
                                        game.SPFade(dt)
                                        time.sleep(1)
                                        Party.player2.talk('I have a question!')
                                        Party.player2.talk('So what kind of sword\\are we talking about here?')
                                        character.talk('You\'ll find out soon enough.')
                                        time.sleep(1)
                                        game.SPFade(dt)
                                        character.talk('No, I can\'t do it!\\He ruined all my momentum.')
                                        character.talk('Look, those orbs...')
                                        character.talk('They contain the battle\\ability of a legendary hero.')
                                        character.talk('I used to use these with my apprentice.')
                                        character.talk('Put simply, these things are amazing.')
                                        character.talk('Problem is, you have to find these weird doors\\ before you can use them.')
                                        character.talk('The first one is in your town somewhere.')
                                        character.talk('It should be pretty obvious, actually...')
                                        character.talk('I\'d crack it open for you,\\but I\'m too old for it.')
                                        
##                                        character.talk('They will let you enter places\\where you can fight to find greater power.')
##                                        character.talk('Find as many of them as you can.')
##                                        character.talk('It\'s REALLY important. Believe me.')
##                                        character.talk('You do not want to miss out on those opportunities.')
##                                        character.talk('The first door is in your town.\\Take the orb there...') 
                                        
                                        #battle.Battle(Party.player1,[battle.fredrick],[battle.ghostface],'grass stage',None,(129,129,254),[firstorb],'GrassStage Gestalt',gamedata)
                                        

                            else:
                                character.talk('Nah, you\'ve got nothin\'. Scram.')
                            #scharacter.talk('It is not time for me\\ to pass on my knowledge yet.')
##                            character.talk('Funny meeting you here...')
##                            self.talk('Hey, what does this have to do wi--')
##                            character.talk('Nope, no time for questions.')
##                            character.talk('Follow me.')
##                            self.talk('(Really? AGAIN?)')
##                            character.orient = 'right'
##                            character.distance = 7
##                            character.walkmode = True
                    if game.currentplace == 'grassdungeon15.tmx':
                        if  'SPflag1' in moo.properties:
                            game.gamedata.events['beatswordnyu'] = True
                            game.gamedata.events['swordnyudone'] = True
                            Party.player2.talk('Did you cut all this grass???')
                            character.talk('YES! I did it all!')
                            character.talk('I have to become stronger!')
                            character.talk('I want to be a powerful warrior!!!')
                            character.talk('Powerful warrior always cut grass!\\Always!!!')
                            character.talk('It\'s their duty!')
                            if 'maginyudone' in game.gamedata.events:
                                character.talk('And you like magic?')
                                character.talk('HARK! A powerful wizard has appeared!')
                                character.talk("I will cut you down as well!")
                                battle.Battle(Party.player1,[battle.fredrick],[battle.swordnyu],'grass stage',None,(89,89,204),[firstorb],'SwordNyu Battle',gamedata)
                                character.talk('...')
                                character.talk('I HATE mages...')
                                character.walk('right',20)
                            else:
                            
                            
                                Party.player2.talk('Every blossoming swordsman\\develops an urge for cutting grass.')
                                Party.player2.talk('It\'s a natural part of maturing\\as a young warrior.')
                                character.talk('I am MATURING!')
                                character.talk('aaaAAA!')
                                Party.player2.talk('aaaAAA!')
                                chosenoption = doublequestion('Do you join in the sword-oriented ritual?','aaaAAA!!!','...')
                                if chosenoption == 1:
                                    game.genmuaffection += 1
                                    character.talk('I like you! Teach me your ways!')
                                    Party.player2.talk('Oh, okay...')
                                    Party.player2.talk('Heh heh heh.')
                                    Party.player2.talk('There\'s just one rule...')
                                    character.talk('Fight every swordwielder in sight?')
                                    Party.player2.talk('Ooh! Someone has been studying!.')
                                    character.talk('ATTACK!')
                                    
                                    battle.Battle(Party.player1,[battle.fredrick],[battle.swordnyu],'grass stage',None,(89,89,204),[firstorb],'SwordNyu Battle',gamedata)
                                    character.talk('This stinks. I\'m going home.')
                                    character.walk('right',20)

                                    
                                    
                                if chosenoption == 2:
                                    game.percyaffection += 1
                                    character.talk('*GASP!!!*')
                                    character.talk('You didn\'t support my maturing!')
                                    character.talk('Your silence cuts my soul, you monster!')
                                    Party.player2.talk('It IS a rite of passage, Fredrick...')
                                    character.talk('And warriors always fight monsters!!!')
                                    game.SPFade(dt)
                                    character.talk('Prepare!!!')
                                    battle.Battle(Party.player1,[battle.fredrick],[battle.swordnyu],'grass stage',None,(89,89,204),[firstorb],'SwordNyu Battle',gamedata)
                                    
                                    character.talk('No! Not fair!')
                                    character.talk('You used magic! How is that fair?')
                                    character.walk('right',20)
                                

                                
                            
                            

                    if game.currentplace == 'grassdungeon10.tmx':
                        if  'SPflag1' in moo.properties:
                            game.gamedata.events['maginyudone'] = True
                            Party.player2.talk('Hey, you left your little friend all alone.')
                            character.talk('Huh?')
                            
                            if 'swordnyudone' in game.gamedata.events:
                                character.talk('NO! I\'m not talking to you!')
                                character.talk('You, you... SWORD LOVER!!!')
                                battle.Battle(Party.player1,[battle.fredrick],[battle.maginyu],'grass stage',None,(89,89,204),[firstorb],'MagiNyu Battle',gamedata)
                                character.talk('Grr...')
                                character.talk('GRR!!!!')
                                character.talk('GRRAAAAAAAAAHHH!')
                                character.walk('right',20,1)
                            else:
                                character.talk('I wanna play by myself.')
                                character.talk('He doesn\'t even know magic.')
                                character.talk('Boooooring.')
                                character.talk('All he does is talk about feelings.')
                                character.talk('Feelings aren\'t mystical and super cool.')
                                character.talk('Magic is.')

                                chosenoption = character.askandquestion('Magic is SOO cool.','The coolest.','No....')
                                if chosenoption == 1:
                                    character.talk('Yayyyyyy!')
                                    character.talk('You\'re cool too!')
                                    character.talk('I think i\'ll give you some magic...')
                                    
                                    character.talk('Okay! Here goes!')
                                                   
                                    character.walk('right',3)
                                    character.orient = 'left'
                                    character.talk('Abra cada--')
                                    printstuff('The creature throws a book at fredrick.')
                                    character.talk('Read a book!')
                                    self.talk('ow...')
                                    printstuff('The book is titled "Fire flingin\' for freakin\' fricks".')
                                    printstuff('Fredrick is offended, yet intrigued.')
                                    printstuff('Fredrick starts reading the book.')
                                    self.talk('It\'s pretty complex...')
                                    printstuff('Fredrick only partially understands the book.')
                                   
                                    character.talk('There! I found that cool book, but I couldn\'t figure it out.')
                                    character.talk('It\'s soooooo boring.')
                                    character.talk('I hope you like it.')
                                    character.talk('Now, play with me!')
                                    chosenoption = doublequestion('It seems the creature is challenging you to a fight.','Okay, I\'m down.','I don\'t wanna...')
                                    
                                    #make maginyu friendlier in this
                                    
                                    if chosenoption == 1:
                                        character.talk('Yayyy!\\I knew you were cool!')
                                        game.SPFade(dt)
                                        battle.Battle(Party.player1,[battle.fredrick],[battle.maginyu],'grass stage',None,(89,89,204),[firstorb],'MagiNyu Battle',gamedata)
                                        game.gamedata.events['maginyudone'] = True
                                        character.talk('You\'re too strong...')
                                        character.talk('I\'m tirrrrred.')
                                        character.talk('I\'m gonna go back now.')
                                        character.walk('right',7)
                                        character.talk('You better come back\\so we can play again...')
                                        
                                        
                                    else:
                                        character.talk('Really?')
                                        character.talk('Hmph. I\'m sad.')
                                        character.talk('But it\'s okay...')
                                        character.talk('Maybe we can play next time...')
                                        Party.player2.talk('Maybe you should go play with your first friend now.')
                                        character.talk('The boring one?')
                                        Party.player2.talk('Yes, the boring one.')
                                        character.talk('Ughhhhhhhh i don\'t wanna--')
                                        Party.player2.talk('Do it!\\Or else I\'ll make all the magic in the world disappear!')
                                        character.talk('*sniff*,*sniff*')
                                        character.talk('You\'re mean!')
                                        character.talk('Waaaaaaaaaaah!')
                                        character.walk('right',7)
                                        
                                        
                                        
                                if chosenoption == 2:
                                    Party.player2.talk('Pfft, magic is lame.')
                                    character.talk('*gasp*')
                                    character.talk('You\'re a meanie!')
                                    Party.player2.talk('Nuh uh!')
                                    character.talk('Yeah huh! Swords are for stupidheads.')
                                    Party.player2.talk('No they\'re not.\\They\'re for super cool warriors.')
                                    character.talk('No. They\'re not.')
                                    Party.player2.talk('Yes they are.')
                                    character.talk('NO. They\'re NOT.')
                                    Party.player2.talk('Okay, you\'re right. Magic is cool.\\ \\Ha! I lied! Magic sucks!')
                                    
                                    character.talk('...')
                                    character.talk('RRRRRAAAAWWWWWRRRRRRR!!!')
                                    character.talk('I\'LL KILL YOU!','bigtext')
                                    game.SPFade(dt)
                                    battle.Battle(Party.player1,[battle.fredrick],[battle.maginyu],'grass stage',None,(89,89,204),[firstorb],'MagiNyu Battle',gamedata)
                                    character.talk('I hate hate hate you!')
                                    character.talk('I hate you so much!')
                                    character.talk('HATE hate hate hate HATE!')
                                    character.talk('URRRRRRRRAAAAH!')
                                    character.walk('right',20)
                                    
                                    
                                
                            
                            #begin casting
##                            character.orient = 'left'
##                            character.talk('Abra cada--')
##                            printstuff('The creature throws a book at fredrick.')
##                            character.talk('Read a book you DUMMY!')
##                            self.talk('ow...')
##                            printstuff('The book is titled "Fire flingin\' for freakin\' fricks".')
##                            printstuff('Fredrick is offended, yet intrigued.')
##                            printstuff('Fredrick starts reading the book.')
##                            self.talk('It\'s pretty complex...')
##                            printstuff('Fredrick only partially understands the book.')
##                            printstuff('Despite this, he has learned a new attack!')
##                            printstuff('Laser was added to your xmoves.')
##                            printstuff('Your current xmove has also become laser.')
##                            Party.xmoves.append(pc.laser)
##                            game.player.xmove = pc.laser
##                            character.talk('Now, play with me!')
##                            game.SPFade(dt)
##                            battle.Battle(Party.player1,[battle.fredrick],[battle.maginyu],'grass stage',None,(89,89,204),[firstorb],'MagiNyu Battle',gamedata)
                            
                    if game.currentplace == 'grassdungeon6.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('I like swords.')
                            character.talk('My mommy said I\'ll be a powerful warrior someday...')
                            character.talk('But I wanna be one right now!')
                            character.talk('Are you a powerful warrior?')
                            chosenoption = triplequestion('I\'m powerful.','I\'m an okay warrior.','I\'m not powerful at ALL...')
                            if chosenoption == 1:
                                character.talk('Oh, wow!')
                                character.talk('Hee hee.')
                                character.talk('Hee hee hee.')
                                character.talk('Heh heh.')
                                character.talk('AHAHAHAHAH!')
                                character.talk('then FIGHT me in glorious battle.')
                            if chosenoption == 2:
                                character.talk('oh...')
                            if chosenoption == 3:
                                character.talk('I\'m not very powerful either...')
                                character.talk('Maybe we can practice together?')
                    
                    if game.currentplace == 'grassdungeon5.tmx':
                        if 'swordnyudone' not in game.gamedata.events and 'maginyudone' not in game.gamedata.events:
                            if 'SPflag1' in moo.properties:
                                
                                if not character.talkedbefore and ('swordnyudone' not in game.gamedata.events and 'maginyudone' not in game.gamedata.events) and 'metnyu' not in game.gamedata.events:
                                    game.gamedata.events['metnyu'] = True
                                    character.talk('Excuse me, Mister?')
                                    character.talk('Can you and your boyfriend help me?')
                                    
                                    Party.player2.talk('Hey, my only love is for swords.')
                                    character.talk('Hee hee, you\'re funny!')
                                    character.talk('Can you help me find my friends?')
                                    character.talk('I\'m not special like they are,\\so they left me all alone.')
                                    character.talk('If we don\'t get back soon,\\my parents will start worrying...')
                                    Party.player2.talk('Well, where did they go?')
                                    character.talk('My friend who likes swords went down,\\and the other who likes magic went up...')
                                    character.talk('My mommy is making dinner, and I\'m starving!')
                                    character.talk("Can you help me?")
                                    character.talk('Pleaseeeeeeeeee...!')
                                    printstuff("The creature makes a sad expression\\ that looks kind of silly.")
                                    character.talkedbefore = True
                                else:
                                    if character.talkedbefore:
                                        character.talk('Ohh, I\'m hungry...')
                                        character.talk('My mommy is making STEAK.')
                                        character.talk('MMM!')
                                        character.talk('MMM MMM MMM!')
                                        character.talk('Steak is so good!')
                                        Party.player2.talk('Yeah, well, can you\\fight people with steak???')
                                    elif 'metnyu' in game.gamedata.events:
                                        character.talk('I like steak so much!')
                                        character.talk('I think I love steak!')
                                        character.talk('I want to have a long happy life with steak!')
    ##                            character.talk('He\'s lucky. He has lots of friends.')
    ##                            character.talk('I wish I had friends like he does...')
    ##                            character.talk('Oh! I have a question for you.')
    ##                            character.talk('What makes you happy?')
    ##                            chosenoption = triplequestion('SWORDS!','Magic','Friends')
    ##                            if chosenoption == 1 or chosenoption == 2:
    ##                                character.talk('Why?')
    ##                            if chosenoption == 3:
    ##                                character.talk('Oh wow!')
    ##                                character.talk('Can you help me make friends, too?')
    ##                            printstuff('Your paths have become intertwined. You have made a new bond.')
                            
                            elif 'swordnyudone' and 'maginyudone' in game.gamedata.events:
                                printstuff('Ay, fonzi!')
                            elif 'swordnyudone' in game.gamedata.events:
                                if 'SPflag1' in moo.properties:
                                    if 'swordnyufriend' in game.gamedata.events:
                                        character.talk('LOOK! It\'s him...')
                                        character.talk('My master has returned...')
                                    else:
                                        character.talk('AAAAAAAAAAA NOOOOOOOOOO!')
                                        character.talk('I\'m sorry! I\'m sorry! I\'m sorry!')
                            elif 'maginyudone' in game.gamedata.events:
                                if 'SPflag1' in moo.properties:
                                    if 'maginyufriend' in game.gamedata.events:
                                        character.talk('Oh! It\'s my friend!')
                                        character.talk('Hiiiiii!')
                                    else:
                                        character.talk('...')
                                        character.talk('I hate you.')
                            elif 'metnyu' in game.gamedata.events:
                                character.talk('Ohhhhh, what\'s taking so long???')
                                character.talk('I don\'t want to be rude,\\but I am so hungry!')
                                character.talk('Pleaaaaaaaase find them!!!')
                        
                                    
                    if game.currentplace == 'grassdungeon9.tmx':
                        if 'SPflag1' in moo.properties:
                            if not character.talkedbefore:
                                character.talk('Hey, weirdos.')
                                character.talk('I\'ve got this cool thing you might find useful.')
                                character.talk('Some weird guy wearing a robe dropped this,\\and it seems like a potent healing item.')
                                character.talk('I picked up it up, but before I could give it back to him, he vanished.')
                                character.talk('I\'m not one of those violent types,\\so it\'s not likely to be useful for me.')
                                character.talk('However, I do like money, so I\'ll sell it to you.')
                                chosenoption = doublequestion('For the reasonable price of $15.','Yeah, alright.','I\'ll pass.')
                                if chosenoption == 1:
                                    if Party.money >= 15:
                                        character.talk('Of course...')
                                        character.talk('It smells divine; I\'m sure you\'ll enjoy it.')
                                        printstuff('AngelFeather was added to your items.')
                                        Party.items.append(angelfeather)
                                        character.talkedbefore = True
                                    else:
                                        character.talk('Um, you\'re broke.')
                                        character.talk('Well, that makes two of us...')
                                if chosenoption == 2:
                                    character.talk('Are you sure???')
                                    character.talk('It\'s literally a divine artifact...')
                                    character.talk('It only costs as much as a decent meal.')
                                    character.talk('You could probably cheat death with it.')
                            else:
                                character.talk('Believe me, it\'s a lifesaver.')
                    if game.currentplace == 'grassdungeon14.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('What? You guys again?')
                            character.talk('Are you two stalking me?')
                            chosenoption = doublequestion('','Giiiive me your items...','What? No. No we\'re not.')
                            if chosenoption == 1:
                                character.talk('Woah, okay buddy.')
                                character.talk('That\'s kinda weird...')
                                self.talk('I neeeeeed them.')
                                Party.player2.talk('Giiiiiiive them to us.')
                                character.talk('Ugh, what\'s going on?\\Is that cloak wearing jerk\\screwing with me again?')
                                character.talk('Who thought it was a good idea to\\give him those powers?')
                                character.talk('If you can hear me, this isn\'t funny!')
                                printstuff('Somewhere, someone laughed to themself...')
                                self.talk('Was I saying something?')
                                Party.player2.talk('Ow my legendary sword-wielding head.')
                                character.talk('Glad that\'s over...')
                            if chosenoption == 2:
                                character.talk('Hmm... That\'s not very convincing.')
                                character.talk('If you\'re not violating my privacy,\\then what are you doing?')
                                Party.player2.talk('We\'re looking for weird fluffy... things?')
                                character.talk('Sounds like those weird forest creatures.')
                                character.talk('Kinda looks like a mix of\\a rabbit and a sheep, you know?')
                                
                                character.talk('They have some kind of den\\hidden somewhere in this forest.')
                                character.talk('They\'re... strange.')
                            character.talk('Anyway, I\'m selling these special items.')
                            character.talk('It looks like they\\make you more powerful?')
                            character.talk('I really don\'t know about them...')
                            character.talk('It looks like one raises physical strength,\\while the other raises mental strength.')
                            character.talk('I\'ll sell you one of them for $15.')
                            chosenoption = triplequestion('Gimme the physical one.','I want the mind one, please','I\'ll pass.')
                            if chosenoption == 1:
                                character.talk('Alright, here you go.')
                                character.talk('These things seem pretty rare;\\you won\'t be able to find them easily.')
                                printstuff('You took the strengthbooster\\and placed it in your items.')
                                Party.items.append(strengthbooster)
                            if chosenoption == 2:
                                character.talk('Not the choice I was expecting from you,\\but still a choice nonetheless.')
                                printstuff('You placed the magicbooster in your items.')
                                Party.items.append(magicbooster)
                            if chosenoption == 3:
                                character.talk('Alright, I\'ll cut you a deal.')
                                character.talk('I\'ll give you both of them for $20.')
                                chosenoption = doublequestion('Deal?','Yeah, alright.','Nope nope nope.')
                                if chosenoption == 1:
                                    character.talk('Ugh, what a pain...')
                                    Party.items.append(strengthbooster)
                                    Party.items.append(magicbooster)
                                else:
                                    character.talk('Seriously?')
                    if game.currentplace == 'grassdungeon18.tmx':
                        if moo.name == 'Grassy Spirit':
                            if 'smileyfacecut' in game.gamedata.events:
                                character.talk('I am he who watches over the forest.')
                                character.talk('I am the one who has created the grass in this forest.')
                                character.talk('I appreciate you obediently participating in my games.')
                                chosenoption = triplequestion('Why would you do this?','It was SO boring.','Why so many path cutting puzzles?')
                                if chosenoption == 1:
                                    character.talk('Do you understand how boring forests are?')
                                    character.talk('Nothing happens, besides the odd idiot\\or child wandering through.')
                                    character.talk('You must forgive me. I desperately needed some entertainment...')
                                if chosenoption == 2:
                                    character.talk('Forgive me for that.')
                                    character.talk('Dealing with the NYU has dulled my awareness somewhat...')
                                if chosenoption == 3:
                                    character.talk('I must admit, carving those paths is a\\nuisance that even my own self cannot tolerate.')
                                    
                                    character.talk('I thank you for it.')
                                Party.player2.talk('WHY have you cursed me with all this grass?')
                                Party.player2.talk('Do you KNOW how much it hurts me?')
                                character.talk('The complaints of one peculiar swordwielder\\are nothing compared to joys of\\those who appreciate nature.')
                                character.talk('You may have disliked it, but others have enjoyed it.')
                                Party.player2.talk('...')
                                Party.player2.talk('I hate you.')
                                

                            elif 'mincut' in game.gamedata.events:
                                character.talk('Do you consider yourself efficient?')
                                character.talk('Paying no regard to an opportunity to leave one\'s mark...')


                               
                                character.talk('Perhaps someone else will make use of it...')
                                character.talk('How disappointing.')
                                character.talk('Still, to impede you would require an unfitting amount of effort...')
                                
                                
                            elif 'allcut' in game.gamedata.events:
                                character.talk('Why?')
                                character.takl('You have left no grass anywhere.')
                                character.talk('You have destroyed all potential for beauty.')
                                character.talk('You destroyed what little nature I left for embellishment.')
                                chosenoption == doublequestion('Why have you done this?','It\'s better like that.','My friend REALLY hates grass.')
                                if chosenoption == 1:
                                    Party.player2.talk('He\'s right, you know. Grass??? How horrifying.')
                                    character.talk('If I only I had detected the dark flame that had consumed your soul from the beginning...')
                                    #off is not my property. 
                                elif chosenoption == 2:
                                    game.genmuaffection += 2
                                    Party.player2.talk('I\'m touched, Fredrick.')
                                    character.talk('For friendship...')
                                    character.talk('Your intent isn\'t ignoble, but that doesn\'t make your actions any more acceptable.')
                                


                            else:
                                if character.talkedbefore:
                                    character.talk('Really, please cut it.')
                                    character.talk('It will only take a little bit.')
                                    character.talk('I know you have been through a lot, but...')
                                    character.talk('Please?')
                                else:
                                    character.talk('You would really ignore the grass?')
                                    character.talk('You have come this far...\\Finish the job.')
                                    character.talk('Please?')
                        
                    
                                    
                                
                            
                                
                                
                            
                                
                            
                            
                            
                    
                    if game.currentplace == 'grassdungeon20.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('Ohh, a customer?')
                            character.talk('Man, so much for me lounging around..')
                            
                            character.talk('Hey, wait a minute...')
                            #genmu fails at hiding
                            character.talk('You aren\'t slick, swordsman. I can see you.')
                            Party.player2.talk('No you can\'t!\\I\'m GREAT at hiding.')
                            character.talk('I guess it was just the wind, then...')
                            character.talk('Ah, so. Whaddya want?')
                            character.talk('I\'d sell you something,\\but my dogs are in charge of sales.')
                            character.talk('They went off to take care of some errands.')
                            character.talk('One should probably be getting back right about now...')
                            game.initextras()
                            for i in game.actors:
                                if i.name == 'WizDog':
                                    dog  = i
                            dog.talk('Wurf!')
                            character.talk('Yep, right on time.')
                            dog.walk('down',6)
                            dog.talk('Wurf wurf!')
                            character.talk('Did you get my sword back, pooch?')
                            
                            dog.walk('down',2)
                            #the dog approaches fredrick
                            dog.talk('...')
                            printstuff('The dog sniffs fredrick.')
                            dog.talk('WUUUUUUURF! WURF WURF!')
                            character.talk('Huh?')
                            character.talk('He smells like that bizarre swordthief?')
                            character.talk('You have to be more specific.\\There are a lot of thieves out there...')
                            dog.talk('Wurf wurf woof! WOOF WOOF.')
                            character.talk('Really? The scent of steel scraps and angst?')
                            character.talk('That swordsman...')
                            chosenoption = doublequestion('Do you know Genmu?','He likes swords. He\'s cool.','Not willingly.')
                            if chosenoption == 1:
                                game.genmuaffection += 1
                                character.talk('Well, your "friend" is a nutjob.')
                                character.talk('He stole my swords.')
                                character.talk('I was just about to gift them to my daughter.')
                                Party.player2.talk('WHAT!?!','bigtext')
                                Party.player2.rect.center = (448,864)
                                Party.player2.walk('right',6)
                                Party.player2.talk('How did this slimy salesman manage to reproduce???')
                                character.talk('Woah, ouch, buddy...')
                                character.talk('Yes, I have a daughter.\\She is also an excellent businesswoman.')
                                Party.player2.talk('NO! You can\'t let her sell those!')
                                Party.player2.talk("All she\'ll do is rip off some moron who'll\\just have them sit in a case for the rest of time.")
                                dog.talk("Wurf wurf wurf!!!")
                                character.talk('No, Alexander, attacking people isn\'t very--')
                                dog.talk('WURF!!!')
                                game.SPFade(dt)
                            else:
                                game.percyaffection += 1
                                character.talk('That definitely sounds like him.')
                                character.talk('Well, I guess it was just a weird coincidence.')
                                character.talk('I unfortunately definitely know him.')
                                character.talk('We traveled together for a while cause \\we both liked getting swords.')
                                character.talk('It worked fine for a while...')
                                character.talk('But he was so NEEDY!')
                                character.talk('Always asking if people liked him,\\and if he was "fulfilling the requirements necessary\\to become a legendary swordsman..."')
                                character.talk('Not to mention, some of my best swords kept "disappearing"...')
                                
                                
                                Party.player2.talk('HEY!','bigtext')
                                Party.player2.rect.center = (448,864)
                                Party.player2.walk('right',6)
                                Party.player2.talk('With how cheap you were selling them,\\you might as well have just given them away...')
                                Party.player2.talk('Was it my fault your greedy daughter\\suddenly demanded more money???')
                                Party.player2.talk('What did she even need all that money for???')
                                dog.talk("Wurf wurf wurf!!!")
                                Party.player2.talk('Really? "Investment opportunities"?')
                                Party.player2.talk('You can\'t fight people with those! Ridiculous!')
                                dog.talk('Wurf Wurf wurf wurf Wurf!')
                                game.SPFade(dt)
                            battle.Battle(Party.player1,[battle.fredrick],[battle.blackcloak],'grass stage',None, (0,0,0),['Stick','First Aid Kit'], 'WizDog Encounter',gamedata)
                            Party.player2.talk('HA! Your dog sucks!')
                            ###
                            character.talk('He still has a winning record over you, though...')
                            dog.rect.x += 9090909
                            character.rect.x += 199199199
                            game.gamedata.events['foughtthesalesman'] = True
                            dog.talk("...")
                            character.talk("Screw you guys!")
                            character.talk("I\'m going to the city.")
                            Party.player2.talk("Fredrick, you\'re amazing!")
                            Party.player2.talk("They weren\'t even invisible and you STILL beat them.")
                        
                            printstuff("Genmu holds a newfound respect for you.")
                            for i in Party.bonds:
                                if i.name == 'Genmu':
                                    #i.level += 1
                                    printstuff('A voice begins speaking into Fredrick\'s mind.')
                                    printstuff('You, the one whose path leads to the end...',0,1,1)
                                    printstuff('You tread the path of the warrior further still.',0,1,1)
                                    i.level += 1
                                    printstuff("Fredrick's bond with Genmu has strengthened!")
                                    printstuff("Fredrick can now slice one extra time when using sword attacks.")
                            
                            Party.player2.talk('That cowardly coward ran away like a coward again.')
                            Party.player2.talk('What cowardice!')
                            Party.player2.talk('...')
                            
                            self.talk('Maybe we should chase him?')
                            Party.player2.talk('LET\'S FREAKING DO IT!!!')
                            Party.player2.walkmode = True
                            Party.player2.followmode = True
                            game.gamedata.events['genmuswordsearch'] = True
                            game.gamedata.events['aftergrassdungeon'] = True

                            
                                
                                
                                
                            
                    if game.currentplace == 'grassdungeonsecret.tmx':
                        if 'SPflag1' in moo.properties:
                            if not character.talkedbefore:
                                character.talk("Oh! Mister! You\'re back!?")
                                character.talk("Wait, you\'re not Mister...")
                                character.talk('No, you\'re that meanie from earlier!')
                                character.talk("I don\'t want to fight you again.")
                                character.talk('...')
                                character.talk('Or maybe I do.')
                                character.talk('Hee hee hee.')
                                character.talk('I\'m so POWERFUL!')
                                character.talk('Hee hee hee hee HEE!')
                                character.talk('That guy gave me so much strength...')
                                character.talk('When I show nyu\'s friend how amazing I am...')
                                #character.talk('And then they\'ll ALL finally love me.')
                                character.talk('Finally! They will love me again!')
                                #character.talk('I\'ll be the one who FINALLY has friends.')
                                character.talk('After all, why should he have all the friends?')
                                #character.talk('His friends need someone who will\\ play with them the way I will.')
                                #character.talk('We\'ll have so much fun together...')
                                character.talk('Ohh, I love being powerful.')
                                character.talk('Are you powerful?')
                                chosenoption = doublequestion('','The most powerful.','I\'m not powerful at ALL...')
                                if chosenoption == 1:
                                    character.talk('Oh, wow!')
                                    character.talk('Hee hee.')
                                    character.talk('Hee hee hee.')
                                    character.talk('Are you really THAT powerful...?')
                                    #character.talk('Heh heh.')
                                    #character.talk('AHAHAHAHAH!')
                                    #character.talk('then FIGHT me in glorious battle.')
                                if chosenoption == 2:
                                    character.talk('Oh...')
                                    character.talk('I\'m sorry...')
                                    character.talk('Maybe you should go find the man I found.')
                                    character.talk('He can make you powerful, too!')
                                    #character.taxlk('I\'m not very powerful either...')
                                    #character.talk('Maybe we can practice together?')
                                character.talkedbefore = True
                            else:
                                printstuff("The nyu is contentedly chattering with himself.")
                                printstuff("Are you going to fight him?")
                            
                        if 'SPflag2' in moo.properties:
                            #character.talk('You\'ve tracked me down.')
                            character.talk('You ARE interrupting my training, you know.')
                            character.talk("It is good your friend isn\'t here.")
                            character.talk("His 'fated battle' would be a far worse interruption than you.")
                            #character.talk('A shame your friend isn\'t here.\\He\'s the one who really wants to see me.')
                            character.talk('Though, in his current state,\\his "dream" fight would prove a rude awakening...')
                            character.talk("So, that just leaves you.")
                            character.talk("...")
                            printstuff("The man shakes his head.")
                            character.talk("Strange to be put in this scenario again...")
                            
                            character.talk("You and I could spar.")
                            character.talk("Actually,\\you really should spar with me.")
                            character.talk('I need to get a sense of who you really are.')
                            ##character.talk("You are going to need help.")
                            ##character.talk('I will offer you some guidance.')
                            ##character.talk('To help me do so, tell me\\ what you want from this journey.')
                            ##chosenoption = doublequestion('...','Strength','Friends')
                            chosenoption = doublequestion('The man is waiting expectantly.','Let\'s do this...','No, not yet...')
                        
                            if chosenoption == 1:
                            
                                character.talk('I hope you are who Gray thinks you are.')
                                character.talk('Otherwise...')
                                battle.Battle(Party.player1,[battle.fredrick],[battle.blackcloak],'grass stage',None,
                                 (0,0,0),['Stick','First Aid Kit'], 'Black Cloak Battle',gamedata)
                                

                            if chosenoption == 2:
                                character.talk("Boring...")
                                character.talk("I won\'t be here for much longer.")
                                character.talk("Make sure you come back soon.")
                    if game.currentplace == 'picnicarea.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('You know what would be fun?')
                            character.talk("You and all your friends should\\get together here and have a picnic.")
                            character.talk("I have no ulterior motives whose\\ results would send you to the secret dungeon, I promise.")
                    
                    if game.currentplace == 'grasstown.tmx':
                        if 'friend' in moo.properties:
                            character.talk('Yo, how\'ve you been?')
                        if 'percival' in moo.properties:
                            if 'percystart' in game.gamedata.events:
                                #percy is very cleanly
                                if character.talkedbefore:
                                    character.talk('You\'re starting to irritate me.')
                                    character.talk('What could you possibly want from me?')
                                    character.talk('Actually, don\'t answer that.\\This conversation has gone on long enough already...')
                                    chosenoption = doublequestion('He seems both happy and\\ unhappy i\'m talking to him.','Do you like magic?','Is your job that hard?')
                                    if chosenoption == 1:
                                        printstuff("His eyes brighten.")
                                        character.talk("A little. Why do you ask?")
                                        character.talk("No, I\'m too tire to talk about that right now...")
                                        printstuff("The man cracks a small smile as he daydreams...")
                                        ##character.talk('Who are you to say that?')
                                        #character.talk('Are you looking for a fight?')
                                        #printstuff('A mischievous look falls upon his face.')
                                        #character.talk('I\'d be glad to give one to you...')
                                    if chosenoption == 2:
                                        character.talk("Not really.")
                                        character.talk("It\'s just so boring...")
                                        character.talk('I always feel like I\'m missing out on something.')
                                        
                                else:
                                    character.talk('What.')
                                    character.talk('This is a break. Leave me alone.')
                                    character.talk('I need it.')
                                    character.talk('I need it more than you could ever know.')
                                    character.talkedbefore = True
                                
                                        
                                
                         
                        
                            
                       
                    if game.currentplace == 'grasstowngiftshop.tmx':
                        if  'SPflag1' in moo.properties:
                            character.talk('Hello... and welcome to our exhibit.')
                            character.talk('Development has not finished yet,\\but we are still allowing a sneak peek\\for those who are interested.')
                            character.talk('Admission is $5 for a single,\\and $1000 for doubles.')
                            chosenoption = doublequestion('Are you going in?','Uh, I\'ll take two singles, please.','I\'ll pass.')
                            if chosenoption == 1:
                                if Party.money >= 10:
                                    character.talk('Wow, really? Finally! I can eat!')
                                else:
                                    character.talk('Hey, you\'re broke.')
                                    character.talk('Awkward...')
                            if chosenoption == 2:
                                character.talk('Rude...')
                    if game.currentplace == 'grasstowngiftshop3.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('Man, that door bugs me.')
                            character.talk('Everyone wants to look at it for SOME reason.')
                            character.talk('It\'s literally useless. It doesn\'t open!.')
                            character.talk('Door opens?\\No one cares, whatever, next.')
                            character.talk('But if it doesn\'t open?\\Ooh, I\'m interested!\\Whatever could be inside???')
                            character.talk('Why is my most successful\\attraction a freakin\' door?')
                    if game.currentplace == '1stkalpa.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('...')
                            character.talk('You look... familiar.')
                            character.talk('... ...')
                            character.talk('I remember someone like you.')
                            character.talk("But from where I don\'t remember...")
                            character.talk("Man, where did Genmu run off to again...")
                            #character.talk('He told me something that\\changed how I saw the world.')
                            #character.talk('It really felt like it opened doors for me.')
                            #character.talk('But I can\'t remember what it was...')
                            character.talk('...')
                            character.talk("You know, he probably couldn't have gotten too far from here..")
                        if 'SPflag2' in moo.properties:
                            character.talk('At its heart,\\ our world is ran by two powerful deities.')
                            character.talk('One is a being of creation, the other a being of destruction.')
                            character.talk('Neither of them are inherently good or bad.')
                            
                            character.talk('...')
                        if 'SPflag3' in moo.properties:
                            character.talk('Heeheeheeeee...')
                            character.talk("Everyone is so different...")
                            character.talk("But then, everyone is so similar...")
                            character.talk("It\'s all SO funny.")

                    
                        if 'lifequestion' in moo.properties:
                            character.talk('In this place you have stumbled into,\\the world is kept running.')
                            character.talk('The size of such a task leads\\those who inhabit this place to\\question their motivations for life.')
                            character.talk('Thus, it is only natural\\that your motivations should\\ be questioned, too.')
                            x = character.askandquestion('How should one live their life?','For yourself.','For others.')
                            if x == 1:
                                character.talk('We are not strong on our own...')
                                character.talk('Is something still beautiful if none see it?')
                                
                            if x == 2:
                                character.talk('You, who denies yourself for others...')
                                character.talk('What is it you can provide for them?')
                                
                        if 'deathquestion' in moo.properties:
                            character.talk('Another strange question...')
                            x = character.askandquestion('If life eventually ends, what is the point?','What point?','The point is that it ends.')
                            if x == 1:
                                character.talk('Maybe there isn\'t one.')
                            if x == 2:
                                character.talk('I don\'t get it.')
                            
                            
                    if game.currentplace == 'peteza.tmx':
                        
                        if 'SPflag1' in moo.properties:
                            character.talk('Man, I wonder if he\'ll come back again...')
                            #gray cloak eats at restaurants for fun
                            character.talk('Huh?\\You\'re...')
                            character.talk('No, nevermind.\\I thought you were someone else.')
                            character.talk('Where would you like to sit?')
                            chosenoption = triplequestion('A table.','Uhh, the bar?','The ground.')
                            if chosenoption == 1:
                                character.talk('Good, because one is all we got.')
                                #ugh, the pepperoni pizza is @11, but the cheese pizza is $10 and toppings cost $0.50
                                #What a ripoff!'
                                game.BlackOut()
                                game.player.rect.bottomleft = (516,288)
                                Party.player2.rect.bottomright = (716,288)
                                game.currentfocus = [617,250]
                                screenupdate()
                                
                                Party.player2.talk('Do you see this?')
                                Party.player2.talk('The cheese pizza is $10,\\and toppings are $0.50 each...')
                                Party.player2.talk('But they charge $11 for the pepperoni pizza?')
                                Party.player2.talk('What a cruel abuse of power!')
                                printstuff('The long awaited pizza finally arrives.')
                                Party.player2.talk('Hm...')
                                Party.player2.talk('No, too hot!')
                                Party.player2.talk('I will wait for my opportunity, then...')
                                printstuff('Genmu concentrates much more than\\is necessary, or even encouraged for eating pizza.')
                                Party.player2.talk('...')
                                Party.player2.talk('...')
                                
                                game.currentfocus = "Player"
                                
                            if chosenoption == 2:
                                character.talk('How old are you?')
                                character.talk('No, don\'t answer that.\\Lying would only make things worse.')
                            if chosenoption == 3:
                                character.talk('You don\'t need to come to\\ a restaurant to do that...')
                        if 'SPflag2' in moo.properties:
                            character.talk('Ah, that sword over there...')
                            character.talk('You know the old legend about\\the three heroes who saved the world?')
                            character.talk('It\'s said that that sword\\belonged to one of them.')
                            Party.player2.talk('AAA! AAAAaAaaAAAA!!!')
                            
                        
                            
                    if game.currentplace == 'grasstownweaponshop.tmx':
                        print(moo.properties)
                        if 'SPflag1' in moo.properties:
                            if 'firstswordshop' not in game.gamedata.events:
                                character.talk('Are you here to buy something?')
                                chosenoption = triplequestion('Why else would I be here?','You make swords?','What\'s your deal with swords?')
                                if chosenoption == 1:
                                    character.talk('Man, did you really have to put it like THAT?')
                                    shopmenu(grasstownweaponshop)
                                elif chosenoption == 2:
                                    character.talk("Yeah, buddy.")
                                    character.talk("It was just a hobby at first, but I got really good at it.")
##                                    character.talk("Oh, really...?")
                                    
##                                    character.talk('Then tell me who it is you think I am...?')
##                                    character.talk('Clearly you haven\'t finished the job.')
##                                    character.talk("We\'re all waiting on you...")
                                    #character.talk('Oh, you\'re just here to bask in my sword-oriented glory?')
                                    ##character.talk('yeahhhhhhhhh buddy.')
                                    #character.talk('If only you had your ninja friend with you...')
                                elif chosenoption == 3:
                                    character.talk('Man, what do you mean?')
                                    character.talk('I just think swords are cool.\\Stop acting like that\'s weird.')
                                    character.talk("You\'re acting like I have some ulterior motive...")
                                    character.talk('Okay, so it went down like this, alright?')
                                    character.talk('I nabbed a few swords over my travels,\\and some dudes starting hitting me up for swords.')
                                    character.talk('Then, it hit me.')
                                    character.talk('I could both collect swords\\ AND make money if I set up shop here.')
                                    character.talk('It was a pretty sick plan.')
                                    character.talk('So here I am.')
                                    #triplequestion
                            if 'firstswordshop' in game.gamedata.events:
                                
                                if Party.player2:
                                
                                    #Why are people missing stuff?
                                    #game.gamedata.choices['swordreturner']
                                    Party.player2.talk('Give me all of your swords.')
                                
                                    character.talk('That\'ll be $10,000.')
                                    Party.player2.talk('Okay, okay...')
                                    Party.player2.talk('psst, Fredrick...')
                                    self.talk('I\'m not giving you ten grand.')
                                    Party.player2.talk('WHAT? No.')
                                    Party.player2.talk('I don\'t need THAT much.')
                                    Party.player2.talk('Just a little over $9,000...')
                                    self.talk('I don\'t have $9000 for you.')
                                    Party.player2.talk('Curses. Foiled again.')
                                    Party.player2.talk('I won\'t be making a purchase today, it seems.')
                                    character.talk('Bummer, dude.')
                                    self.talk('Uh, we were looking for a sword.')
                                    self.talk('Specifically, some weird salesman\\had the sword we were looking for.')
                                    self.talk('Do you know the location of either of those?')
                                    character.talk('Duuuude.\\That salesbrah is a real pain\\in my behind, man.')
                                    character.talk('He sells all this weird stuff, and it\'s hurting demand for my swords.')
                                    character.talk('I think he\'s heading up to the north now.')
                                    character.talk('He should have what you\'re looking for.')
                                    character.talk('And if he doesn\'t, you can buy stuff from me.')
                                    game.gamedata.events['tohotel'] = True
                                    del game.gamedata.events['firstswordshop']
                                    
##                                    self.talk('Hey, my friend here lost one of his swords.')
##                                    
##                                    #i game.gamedata.preference == '
##                                    self.talk('And you seem like the kind of\\person who knows the location of\\every single sword within 5 miles.')
##                                    character.talk('Hey, watch it buddy.')
##                                    character.talk("I'm aware of every sword for up to 10 miles.")
##                                    character.talk('Could you describe the swords for me?')
##                                    Party.player2.talk('Well first, there was a weird silver one.' )
##                                    if 'swordleaver' in game.gamedata.choices:
##                                        character.talk('ugh, that one? It\'s all over the place')
##                                        character.talk('It keeps appearing in random spots just outside of town.')
##                                        character.talk('Maybe check the forest? I\'m not sure if there\'s more you can do.')
##                                    if 'swordreturner' not in game.gamedata.choices:
##                                        
##                                        
##                                        character.talk('Yes, I remember one like that.\\It disappeared sometime yesterday...')
##                                        Party.player2.talk('WHAT!?!','bigtext')
##                                        Party.player2.talk('Jus\' wait till I find out who did this...')
##                                        character.talk('Though, it returned just as suddenly.')
##                                        character.talk('I believe that it is somewhere within the forest just outside town.')
##                                        Party.player2.talk('Ah, to be reunited with my sword...')
##                                        self.talk('You don\'t know exactly where it is?')
##                                       
##                                        character.talk('Unfortunately, no. I have range, not precision.')
##                                        character.talk('Though, you should consider yourself lucky.\\If I knew exactly where it was,\\it doesn\'t seem like he would be pleased.')
##                                            
##                                        #if chosenoption == 2:
##                                        #    character.talk('Yeah, that you should.')
##                                        #    character.talk('I don\'t think that will take very long...')
##
##                                        #    character.talk('Or you could purchase a replacement sword...')
##                                        #    Party.player2.talk('I would much prefer to do both.')
##                                        #    character.talk('A fine choice that is.')
##                                        #    Party.player2.talk('Ha HA! Swords! Give them to ME!!!')
##                                            
##                                            
##                                            
####                                        if 'sharpfirstsword' in Party.equipment:
####                                            character.talk('But then it came back.')
####                                            character.talk('It\'s definitely somewhere around here.')
####                                            character.talk('I have a feeling that one of you knows\\ exactly where it is...')
####                                        character.talkedbefore = True
##                                            
##                                    else:
##                                        Party.player2.talk("Well, I had this long, sharp japanese sword.")
##                                        character.talk('Weeb...')
##                                        Party.player2.talk('Why you...')
##                                        character.talk('Hmm... \\it may take me a second to decipher it\'s location.')
##                                        character.talk('It\'s in the forest just outside of town.')
##                                        #character.talk('Yeah, it\'s located in a village located in the snow.')
##                                        self.talk('Huh...')
##                                        character.talkedbefore = True
                                else:
                                    
                                    shopmenu(grasstownweaponshop)

                                    
                                    
                                    #character.talk()

                    if game.currentplace == 'grasstownarmorshop.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk('HEY!')
                            character.talk('You look like a human who eats and drinks.')
                            character.talk('Are you a human who eats and drinks?')
                            
                            character.talk('If you are,\\then buy my food and drinks!')
                            character.talk('It\'s like they were made for you!')
                            character.talk('Please buy something.')
                            character.talk('I\'d have more stuff usually.')
                            character.talk('But my supplier raised prices!')
                            character.talk('She did it for NO reason at all!')
                            character.talk('She literally woke up one day and decided "i want more money"...')
                            character.talk('What a jerk!')
                            character.talk('Wanting more money is MY thing!')
                            shopmenu(grasstownweaponshop)
                            if talk:
                                character.talk('Ugh, my supplier...')
                                character.talk('He put his greedy daughter as head of marketing!')
                                character.talk('She\'s just another one of those\\ big city businesswomen.')
                                character.talk('I mean, Easton is the only city nearby,\\so I should say "Easton businesswomen"...')
                                character.talk('But a price-gouger by any other\\name is still just as annoying.')
                            #Northton
                            #Easton
                            #Westley
                            #Southlake
                            
                            #character.talk('If you become powerful, show me.')
                            #character.talk('It\'ll be worth your while.')
                        if 'SPflag2' in moo.properties:
                            character.talk('There\'s all this cool stuff here.')
                            character.talk('I can\'t decide what to get...')
                            character.talk('I keep thinking about how much\\I\'d like this thing...')
                            character.talk('But then I see something else and I like it just as much!')
                            for i in game.actors:
                                if i.name == 'Shopkeep':
                                    i.talk('You have been standing there for 2 hours.')
                                    i.talk('I have like 7 things available for sale.')
                                    i.talk('If nothing else, can you stop leaving\\fingerprints all over the merchandise?')
                    if game.currentplace == 'grasstownsmithing.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk("Incredible...")
                            character.talk("This is the metal necessary\\ for making impulse weaponry...") #desire?
                            character.talk("Don\'t mess this up...")
                                    
                    if game.currentplace == 'grasstownhotel.tmx':
                        #print(dir(moo))
                        
                        if 'SPflag2' in moo.properties:
                            if 'percytalk' in game.gamedata.events:
                                character.talk('What?')
                                character.talk('Are you gonna stay another night?')
                                character.talk('Why would you though?\\They\'re too cheap to even put a mint on your pillow here.')
                                chosenoption = doublequestion('','Why are you a goat?','Wow this place sucks.')
                                if chosenoption == 1:
                                    #character.talk('Baaa. Baaa.')
                                    character.talk('A goat? What\'s a goat?')
                                    character.talk('I have no idea what you\'re talking about.')
                                    #character.talk('But there\'s no one I like around here.')
                                    #character.talk('There was some in my village, which is not far from here...')
                                    character.talk("Anyway, looks like break time just started...")
                                
                                else:
                                    del game.gamedata.events['percytalk']
                                    character.talk('It\'s AWFUL.')
                                    character.talk('The hours are awful, the pay is awful,\\the people are awful...')
                                    character.talk('I seriously need a break.')
                                    character.talk('...')
                                    character.talk('Yeah, definitely a break.')
                                character.walk('right',6)
                                character.walk('down',20)
                                game.gamedata.events['percystart'] = True
                                
                                for i in game.actors:
                                    if i.name == 'Grey':
                                        char = i
                                char.rect.center = (352, 224)
                                printstuff('The elevator opens, and Grey walks out.')
                                char.orient = 'left'
                                char.talk('And so you found another one.')
                                char.talk('You seem to be on the right path...')
                                char.talk('That poor goat seems to be having a hard time.')
                                char.talk('Go make friends with him...')
                                char.talk('He really needs it.')
                                char.talk('Or maybe a rivalry would be more fitting..')
##                                    char.talk('Alright, a potential new friend!\\And he\'s powerful too!')
##                                    char.talk('What is your secret to always being\\able to stumble upon important weirdos?')
##                                    char.talk('That guy may seem dorky, but he\'s descended\\from a line of powerful mages.')
##                                    char.talk('And despite the depressive personality,\\he has some serious ambitions he wishes to fulfill.')
##                                    char.talk('Making friends is especially important for this one.')
##                                    char.talk('But, given that he isn\'t a social butterfly...')
##                                    char.talk('Play up his competitive side.')
##                                    char.talk('That will get your foot in the door.')
##                                    char.talk('Any questions?')
                                chosenoption = doublequestion('','What does he like?','Why is he a goat?')
##                                    char.talk('Anyway, you probably noticed\\his weird fluffy complexion.')
##                                    char.talk('He isn\'t a pureblooded human like you,\\but the difference is negligible.')
##                                    char.talk('Probably around 99.5% human?\\I think there\'s a little baa in there...')
##                                    #char.talk('Anyway, they are called "Sheeple". Even though they may not be truly sheep.')
##                                    doublequestion('','What do you mean by "baa"?','Where are the fluffy people.')
                                if chosenoption == 1: 
                                    char.talk('Hmm.')
                                    char.talk('Let me refer to my "records".')
                                    printstuff('You see him briefly concentrate...')
                                    
                                    char.talk('Magic...')
                                    char.talk('Ancestral magic? Hm...')
                                    char.talk('No...')
                                    char.talk('Urgh...')
                                    char.talk('Now, I see it...')
                                    char.talk('He considers himself a magic user.')
                                    char.talk('It seems to run in his family.')
                                    
                                if chosenoption == 2:
                                    char.talk('He\'s called a sheepperson.')
                                    char.talk('The plural is sheeple.')
                                    char.talk('Despite the name, he\'s part goat, i think?')
                                    char.talk('But it\'s only a cosmetic difference.')
                                    char.talk('I mean, the only true difference is his pale complexion.')
                                    char.talk("And is he slightly fluffy?")
                                    char.talk('Besides, he gets up, looks in the mirror,\\and feels disappointed just like a normal human would.')
                                    
                                    #char.talk('They\'re indistinguishable from humans in practically every way.')
                                    #char.talk('
                                    #char.talk('Oh, he\'s so fluffy!')
                                    #char.talk('I love fluffy goats so much.')
                            
                                
##                                        
                                #if chosenoption == 2:
##                                       char.talk('Oh, there\'s a whole town of them just north of here.')
##                                        char.talk('They look like this because of the cold climate they adapted to.')
##                                        char.talk('Heh, there are definitely sheeple in your future...')
                                char.talk('Now, shouldn\'t you get going?\\His break won\'t last forever.')
                                char.talk('Even though he wishes it would.')
                                char.talk('I have been watching over you closely recently, but...')
                                char.talk('I have been pushing the limit for how much I can interact with you.')
                                char.talk('If you do well, our paths will cross again.')
                                printstuff('Grey gets back in the elevator and leaves.')
                                char.walk('up',10)
                                
                                printstuff("You can either return to your \\hotel room and sleep until tomorrow's \\journey, or go mess around.")
##                                    character.walkmode = True
##                                    character.followmode = True
##                                    character.name = 'Percy'
##                                    Party.player2 = character
                                #oooh someone has a goatfriend.
##                                chosenoption = triplequestion('What are you doing here?','What\'s with the mask?','Why so depressive?')
##                                if chosenoption == 1:
##                                    character.talk('It\'s a bit of a long story...')
##                                    character.talk("I grew in a little village hidden away in the snow.")
##                                    character.talk('You know how small towns are.')
##                                    character.talk('Everyone knows each other,\\has the same routine everyday,\\ and so on.')
##                                    character.talk('They talk to the same old friends,\\and do the same old job\\until they die.')
##                                    character.talk('I just... didn\'t like it.')
##                                    character.talk('Having the same dull, boring plan\\for my life was not what I wanted.')
##                                    character.talk('So I left.\\I wanted to do something different\\with my l
##                                    character.talk('I wanted to take a chance, for better,\\or for worse.')
##                                    character.talk('And now I\'m stuck here,\\helping random people get hotel rooms.')
##                                if chosenoption == 2:
##                                    character.talk('Let\s just say I\'m "special".')
##                                if chosenoption == 3:
##                                    character.talk('Give me a reason not to be.')
                            else:
                                
                                #if game.gamedata.preference == 'logic':
                                #    self.talk('Ugh...')
                                #if game.gamedata.preference == 'will':
                                if 'aftergenmu' in game.gamedata.events:
                                    character.talk('What is it?')
                                    character.talkedbefore = True
                                elif 'grasstownhotel' in game.gamedata.events:
                                    if not character.talkedbefore:
                                        character.talk("(Ugh, another customer...)")
                                        ##self.talk('Can I get a room?')
                                        ##character.talk('Yeah, fine...')
                                        self.talk('Can I get two rooms, please?')
    ##                                    chosenoption = triplequestion('Don\'t know. That mask of yours didn\'t help.','Why work here if you hate it so much?','Can I *please* get a room?')
    ##                                    if chosenoption == 1:
    ##                                        character.talk('It wouldn\'t be any better if I took it off...')
    ##                                    if chosenoption == 2:
    ##                                        character.talk('Money.')
    ##                                        character.talk('It\'s the only reason.')
    ##                                    if chosenoption == 3:
                                        character.talk('Yeah, sure...')
                                        character.talk('That\'ll be $150...')
                                        printstuff("Fredrick shows the man his card.")
                                        #self.talk('I have a card.')
                                        character.talk('Alright, it\'s free then...')
                                        self.talk('What about the "thing"?')
                                        character.talk('Please don\'t do this to me.')
                                        Party.player2.talk("OOH, what\'s the thing???")
                                        chosenoption = doublequestion('Do I make him do the thing?','"You know you have to."','Show him mercy.')
                                        if chosenoption == 1:
                                            self.talk('You have to.')
                                            character.talk('...')
                                            character.talk('"Oh esteemed patron, we present you with a token\\of our favor: A complementary night\'s stay."')
                                            character.talk('"We wish you a most relaxing stay,\\and hope you will have many\\more with our company."')
                                            character.talk('...')
                                            Party.player2.talk("HAHA, yes! I feel like a KING!\\And not like a king of swords, my usual fantasy.")
                                            Party.player2.talk("Again!")
                                            character.talk('...')
                                            printstuff("The concierge is glaring at you.")
                                            character.talk('Here\'s your room key.')
                                            
                                            #genmu +2, percy -1?
                                        else:
                                            character.talk('Thank you so much...')
                                            character.talk('I really needed that.')
                                            character.talk('I don\'t know how much\\more of that I can take...')
                                            #percy + 1
                                            Party.player2.talk('Wait, what?! Why?')
                                            character.talk("Booo!")
                                            #Party.player2.talk("Now I'm REALLY curious!")
                                            character.talk('Here\'s your key.')
                                        game.gamedata.events['hasroom'] = True
                                        character.talkedbefore = True
                                        printstuff("Fredrick receives a room key.")
                                        character.talk("Take the elevator to get to your room.")
                                    else:
                                        character.talk("The elevator is directly to your right.")

                                else:
                                    character.talk('(I wish I had enough money to quit.)')
                                    
                                    
                            
##                            character.talk('Well...')
##                            character.talk('I should probably take you to your room.')
##                            character.walkmode = True
##                            character.followmode = True
##                            Party.player2 = character
                            #Party.addmember(percy)
                            #if game.gamedata.preference == 'emotion':
                            #    self.talk('I mean, may I have a room?')
                            #    character.talk('Uh, okay...')
                            #character.talk('You...')
                            #Party.player2.talk('What is that outfit you\'re wearing?\\What\'s with the mask you\'re wearing?')
                            #character.talk('You certainly have big talk for a person wearing two bandanas.')
                            #Party.player2.talk('Well, at least I\m not BLIND!')
                            
                    
                        
                    

                        
                        

    ##                    character.talk('The key.\\ You know what to do.')
  


                           
                    if game.currentplace == 'snowplace.tmx':
                        if tuple(targetarea) == tuple(character.coords) and 'SPflag1' in moo.properties:
                            ###character.talk('Who are YOU supposed to be?')
                            ###self.talk('Uh, my name is--')
                            character.talk('psst, Fredrick.')
                            character.talk('This question may be weird,\\but that hasn\'t stopped me before.')
                            chosenoption = doublequestion('Do you think the goat girl is hot?','Um. Yes...','*bleat mockingly*.')
                            if chosenoption == 1:
                                character.talk('Oh. Surprising. Deeply shocking.')
                                character.talk('Of course YOU would say that...')
                            if chosenoption == 2:
                                character.talk('Hm. I would say that is the normal opinion.')
                                character.talk('But normal is not a privilege we are allowed.')
                                character.talk('Hold this.')
                                printstuff('Gray gives fredrick a small stuffed goat.')
                                character.talk('Get ready...')
                                printstuff('Gray smacks fredrick.')
                                character.talk('Hah! Bingo! That must have done it.')
                                printstuff('Fredrick is having unusual feelings...')
                                printstuff('You can probably start a bond with Lucy now.')
                    if game.currentplace == '1stkalpabattle.tmx':
                        if 'SPflag1' in character.cell.properties:
                            character.talk('So you have found them.')
                            character.talk("You may be exactly what I am looking for.")
                            character.talk("I have a strange feeling about these places.")
                            character.talk('They are dark and mysterious,\\but familiar nonetheless...')
                            character.talk('However, they hide great secrets at their conclusions.')
                            character.talk("I pray you find them.")
                    if game.currentplace == 'snowplacecoffeeshop.tmx':
                        if 'SPflag1' in character.cell.properties:
                            character.talk('Are you going to buy a coffee, or...')
                            chosenoption = triplequestion('I\'m looking for a door.','Are you a goat too?','Yeah, coffee sounds nice.')
                            if chosenoption == 1:
                                character.talk('Why?')
                            if chosenoption == 3:
                                chosenoption = doublequestion('How do you like it?','The normal way.','Iced...')
                                if chosenoption == 1:
                                    character.talk('Yeah, alright.')
                                    character.talk('You and you friend should grab a seat.')
                                    self.walk('right',6)
                                    self.walk('up',4)
                                    self.walk('right',4)
                                if chosenoption == 2:
                                    character.talk('WHY???')
                                    character.talk('Only the locals drink it like that...')
                                    character.talk('You definitely do not look like a local.')
                                
                    if game.currentplace == 'snowplace2.tmx':
                        if 'SPflag3' in moo.properties:
                            #character.talk('Grrr! Grrr-grah! Rrrrrrrr...')
                            character.talk("Rrrrrrrr... ")
                            #character.talk('Graaaaah!?!')
                            character.talk("AAAAAAAAAAGH!")
                            printstuff('The being\'s eyes fill with more rage\\ than was already present.')
                            character.talk('You... stole... \\everything... from me...!')
                            #character.talk('GRRRRRAAAAAAAH!')
                            printstuff("The being draws into an attack position.")
                            #character.talk('GIVE IT BACK!')
                        if 'SPflag2' in moo.properties:
                            character.talk('...')
                            character.talk('Do you want to be friends?')
                            #chosenoption yes
                            character.talk('Oh, really?')
                            character.talk('I...')
                            printstuff('Percy seems somewhat grateful...')
                            character.talk('It\'s been a while since I\'ve done something like this...')
                            character.talk('I\'d like to visit the arcade.')
                            printstuff('Percy is traveling with you now.')
                            printstuff('I hope we don\'t see my sister, though.')
                            character.walkmode = True
                            character.followmode = True
                            Party.player2 = character
                    if game.currentplace == 'snowmountain2.tmx':
                        character.talk("Are you here to not ski?")
                        chosenoption = doublequestion('I don\'t know.','Yes?','No?')
                        if chosenoption == 1:
                            character.talk("This is clearly a ski resort. You\'re weird. ")
                            character.talk("Take the lift right behind me, then.")
                        else:
                            character.talk("Did you read the signs?")
                            character.talk('You can "not ski" all you want here.\\No actual skiing.')
                            character.talk("Take the lift behind me.")
                    if game.currentplace == 'snowmountain8.tmx':
                        if 'SPflag1' in moo.properties:
                            character.talk("Now pull your **** out of your prissy ****, ****.\\You and your pretty little **** goat buddy better listen up.")
                            character.talk("I\'m the **** who knows that ******* magic here,77 and you\'re the ***** who is begging for my scraps.")
                            character.talk("Let\'s ******** get going, *****.")
                    if game.currentplace == 'cave1.tmx':
                        if 'SPflag1' in moo.properties:
                            printstuff("The being seems to be amused by your presence.")
                            character.talk('Welcome to the end of your journey.')
                            character.talk("That man in the gray cloak...")
                            character.talk('You were instructed by him to defeat me, correct?')
                            character.talk("Well, here is your shining opportunity.")
                            character.talk("You may fight me now, if you wish.")
                            character.talk("But if you would instead opt to spare me, \\I would like to converse with you.")
                            character.talk("The choice is, as always, yours.")
                            chosenoption = doublequestion("...", "Fight", "Talk")
                            if chosenoption == 1:
                                printstuff("The being nods in acceptance.")
                                character.talk('It IS the path of your choosing...')
                            else:
                                printstuff("The being's expression lightens.")
                                character.talk("I am glad you see it my way.")
                                character.talk("The time to fight will come,\\ regardless of our desires.")
                                character.talk("It would be a shame to rush into it headfirst.")
                                character.talk("Follow me.")
                    if game.currentplace == 'cave2.tmx':
                        if 'SPflag1' in moo.properties:
                            printstuff("The being is gazing expectantly at you.")
                            character.talk('I take it you have become\\ acquanted with these doors.')
                            character.talk("I spoke to you the first\\ time you found one of these.") 
                            character.talk('You yourself must find out what we really are.')
                            character.talk("That man in the gray cloak\\ is not misleading you, but.")
                            character.talk("There are some things he hasn't told you of.")
                            character.talk("That is, of course, because he\\must not tell you of them.")
                            character.talk("This door, specifically,\\ holds some key information for you.")
                            character.talk('I will be at its end, anticipating your arrival.')
                            character.talk('Do not keep me waiting.')
                            game.fadeOut()
                            character.rect.x += 9999
                            game.gamedata.events['door2talkdone'] = True
 
                            
                    if game.currentplace == 'cityencounter.tmx':
                        if 'SPflag1' in moo.properties:
                            self.talk('Get out of my way.')
                            character.talk('You know I can\'t let you do this.') 
                            
                            """
                            character.talk("Why are you doing this?")
                            self.talk("I can\'t take this anymore.")
                            self.talk("I want my life back.")
                            self.talk('If you aren\'t going to do something about this, then I will.') 
                            character.talk('You think I like having things like this?')
                            character.talk("I\'m just as lost as you are.")
                            character.talk("Everything got so out of hand...")
                            character.talk('But I\'m trying. I\'m trying to track down the other god.)
                            character.talk("I\'m doing everything that I can.)
                            character.talk("But you can\'t just try to force your way through with a god.) 
                            character.talk("You know what will happen if you do.")
                            character.talk('You were wrong before.')
                            character.talk('Who says you won\'t be wrong again?') 
                            """
                                           
                    if game.currentplace == 'heaven.tmx':
                        if 'SPflag2' in moo.properties:
                            character.talk('Finally.')
                            character.talk('You have seen the world for how it is.')
                            character.talk("You have seen how people hurt.")
                            character.talk("You have seen how people rejoice.")
                            character.talk('You have seen the weaknesses people have.')
                            character.talk("You have seen the strengths people have.")
                            character.talk("You saw what it is to be human, and then...")
                            character.talk('You saw why those two deities were no longer necessary.')
                            character.talk('Your path has led you to me.')
                            character.talk('I am the original deity.')
                            printstuff('The being glances towards Gray.')
                            character.talk('He truly does remind me of you.')
                            character.talk('Even knowing his circumstances...')
                            character.talk('Moreso given how the other one differed...')
                            character.talk('It is strange to gaze upon it firsthand.')
                            character.talk('Our time has not yet arrived.')
                            character.talk('Go and enjoy the future which you fought for.')
                            character.talk('When you have seen enough...')
                            character.talk('Return to me.')
                        if 'reason' in game.gamedata.events:
                            character.talk("This is the end.")
                            character.talk("Whatever you are looking for lies behind me.")
                            character.talk("You must prove your worth to earn it, as you have done before.")
                            character.talk("But do you know why I have done these things?")
                            character.talk("I set these events in motion for the benefit of a certain person:")
                            character.talk("You.")
                            character.talk("Without me prompting your development,\\ the hero that was you would have never risen.")
                            character.talk('Imagine that those two deities never existed.')
                            character.talk('No great injustice needed resolution, and you never went on a journey to stop it.')
                            character.talk('All the lives you touched, all the people you came to understand...')
                            character.talk("None of them would have benefitted in any way.")
                            character.talk("Least of all yourself.")
                            character.talk("I created those beings to watch over you,\\ and to maintain your world so its inhabitants can live peacefully.")
                            character.talk("But people may not always know what is best for them.")
                            character.talk("People may only wish for what is easily achievable, not what may be truly beneficial to their goals.")
                            character.talk("Would Genmu have ever discovered\\that no sword would ever give him the strength \\he wanted had you not shown him otherwise?")
                            character.talk("Would Percy have ever learned what truly would have made him happy if you had not guided him?")
                            character.talk("Would Lucille have ever truly learned the real value of money without your insight?")
                            character.talk('Sometimes, people need someone who will guide them.')
                            character.talk('Someday, one who is strong would\\ slay those false arbiters of stability.')
                            character.talk("He would prove that he has exceeded their abilities.")
                            character.talk("That person would show that blindly following one path may not lead to happiness.")
                            character.talk("That knowledge and desire to achieve imbued\\ in that person would make him a hero unlike any other.")
                            character.talk("And he would create a world of happiness.")
                            #character.talk("That hero is you.")
                            character.talk("A few previous heroes attempted this same journey,\\ but most fell short of the ultimate goal.")
                            character.talk('The only one to perceive the true goal was the man in the gray cloak...')
                            character.talk('Ultimately, it could be argued that he did, in fact, achieve it.')
                            character.talk('Though, I believe you have proven why you are no one but yourself.')
                            character.talk("In fact, there were a few of you, were there not?")

                        if 'SPflag1' in moo.properties:
                            
                            character.talk('To use what opportunities we have been given to their fullest...')
                            character.talk('To let those close to us achieve their true desires...')
                            character.talk('We must defeat him.')
                            character.talk('You know, I always thought he was crazy for doing this...')
                            character.talk('But the only way for us to see our goal achieved...')
                            character.talk('Well, it was to do exactly as he had planned.')

                            
                            
                            
                            
                    if 'temporary' in character.cell.properties:
                        game.fadeOut()
                        character.kill()
                        del moo.properties['sprite']
                        #del moo.properties['description']
                    try:
                        if 'specialtalk' in moo.properties:
                            if moo.properties['specialtalk'] == 2:
                                killtime(1)
                                self.orient = 'down'
                                self.setSprite()
                                screenupdate()
                                killtime(1)
                                self.emote('sprites/angryfredrick.png')
                                killtime(2)
                                self.orient = 'right'
                                self.setSprite()
                                screenupdate()
                            if moo.properties['specialtalk'] == 3:
                                killtime(1)
                                self.talk('(Weird.)')
                    except AttributeError:
                        pass
                    
                                
                     
                        
    ##                if tuple(targetarea) == tuple(character.coords) and 'hasaquestion' in moo.properties and self.gamedata['is ready'] and game.currentplace == 'firstplace.tmx':
  
                        
                        pass
                    if tuple(targetarea) == tuple(character.coords) and 'SPflag' in moo.properties and game.currentplace == 'place_of_judgement.tmx' and d_check != 1:
                        time.sleep(1)
    ##                    character.talk(' I think, however, that i need to \\inform you of the true effects of \\those decisons you made. ')
  
                        character.talk(' Well, That\'s all for us. ')                   
            
                    elif tuple(targetarea) == tuple(character.coords) and 'hasaquestion'  in moo.properties and game.currentplace == 'firstplace.tmx' and chosenoption != True:
                        character.talk('So, now you know everything so far. ')
                        character.animation('removehood.png',30,5,200,dt)
                        character.imageDefault = pygame.image.load('uncloakedcreator.png')

                        ##print(character.image)
                        chosenoption = character.askandquestion('Have you made your choice yet?', 'Yes', 'No')
                        ##print('chosenoption')
                        if chosenoption == 'Yes':
                            character.talk('Then, you know what you have to do.')
                            self.talk('Wait a minute.')
                            self.talk('What AM i supposed to do?')
                            self.talk('You\'ve just been using weird \\metaphors the whole time and \\i\'m really confused.')
                            character.image = pygame.image.load('annoyedcreator.png')
                            character.imageDefault = character.image.copy()
                            character.talk('Look, You walk up to the sigil over\\there, and inspect it. The rest will\\soon be made clear to you.')
                            self.talk('Okay, Fine. Whatever.')
                            self.talk('But what is this place, anyway?')
                            character.talk('A special place. It is called the \\Gray Area. Didn\'t you see the sign?')
                            self.talk(' What sign? ')
                            character.talk('Never mind that. It\'s unimportant.\Just get going, already. ')
                            character.image = pygame.image.load('uncloakedcreator.png')
                            character.imageDefault = character.image.copy()
                            character.setSprite()                       
                            # Now , you know what to do.
                            self.gamedata['is ready'] = True
                            ##print(self.gamedata)
                        elif chosenoption == 'No':
                            character.talk(' You really don\'t have much of a \\choice, you know. ')
                    elif tuple(targetarea) == tuple(character.coords) and 'hasaquestion'  in moo.properties:
                        #character.askandquestion(character.cell.properties['description'], pointer, character.cell.properties['choice1'],character.cell.properties['choice2'])
                        if character.name == 'Lorei':
                            pass
    ##                        character.talk('Hello.')
    ##                        self.talk('(A girl?
                       
                        elif character.name == 'Percy':
                            self.talk('Percy! I wasn\'t expecting to see you here! What\'s up? ')
                            character.talk('Well, not much. \I have to ask you a question, though. ')
                            self.talk('Not you, too. Oh well. \Who put you guys up to this, anyway? \\I\'ve gotta know. ')
                            character.talk('Some dude in a cloak. Totally sketch.')
                            self.talk('Did the robe guy have long black hair? ')
                            character.talk('I dunno. His cloak covered everything.')
                            self.talk('Alright, then. \Don\'t you have a question to ask me?')
                            character.talk('Yep.')
                        elif character.name == 'Genmu':
                            self.talk(' Who are you? ')
                            character.talk(' My name is Genmu. ')
                            game.SPFade(dt)
                            character.image = pygame.image.load('sprites/genmu.png')
                            character.imageDefault = character.image.copy()
                            #Genmu casts the cloak away in an awesome manner
                            character.talk('I am here to kill you. ')
                            self.talk('...')
                            character.talk('Nah, I\'m jus\' messin with ya. ')
                            self.talk(' O-okay then...')
                            self.talk('So, you have a question for me?')
                            character.talk(' Yep.  ')         
                        chosenoption = character.askandquestion(character.cell.properties['description'],character.cell.properties['choice1'],character.cell.properties['choice2'])
                        if chosenoption == character.cell.properties['choice1']:
                            character.talk(character.cell.properties['response1'])
                            if character.cell.properties['answers']:
                                self.gamedata[character.cell.properties['answers']] = chosenoption
                        elif chosenoption == character.cell.properties['choice2']:
                            character.talk(character.cell.properties['response2'])
                            if character.cell.properties['answers']:
                                self.gamedata[character.cell.properties['answers']] = chosenoption
                        if character.name == 'Lorei':
                            character.talk('I have to leave now.')
                        if 'temporary' in character.cell.properties:
                            game.fadeOut()
                            character.kill()
                            del moo.properties['sprite']
                            del moo.properties['description']
                            
                        if character.name == 'Lorei':
                            self.talk('Hmph... ')
                    
                    
                            
                    else:
                        pass
                    pygame.event.pump()
            


    def update(self, dt, game):
        #cleareventqueue()
        for i in pygame.event.get():
            if i.type == pygame.KEYUP and i.key == pygame.K_z:
                self.getinfo(game,dt)
        if self.idletime != None:
            pass
        if self.walking == 'dummy':
            pass
        else:
            #who wrote this garbage?
           
                    
            key = pygame.key.get_pressed()#12x24
##            if key[300] == 1:
##                key[300] = 0
            if key[300] == 1 or key[301] == 1:
                #Caps/Num Lock?
                moo = list(key)                
                moo[301] = 0
                moo[300] = 0
                key = moo
              
            if 1 in key:
                self.idlestart = 0
                if not game.displaytalking and not game.grassdisplay:
                    pygame.display.set_caption('ThatOneGame')
            elif self.idlestart == 0:
                self.idlestart = time.time()
                pass
            ###print('Idle Time',self.idlestart)
            ###print('Current Time',time.time())
            # Setting orientation and sprite based on key input:
            lastrect = copy.copy(self.rect)
            if key[pygame.K_x]:
                running = True
            else:
                running = False
            if key[pygame.K_z]:
                self.zcheck = True
            else:
                if self.zcheck == True:
                   self.getinfo(game,dt)
                   self.zcheck = False
            if key[pygame.K_UP]:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                    self.dx = 0
                if not self.walking:
                    self.holdTime += dt
                    self.zregister = 0
                    self.xregister = 0
            elif key[pygame.K_DOWN]:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()
                    self.dx = 0
                if not self.walking:  
                    self.holdTime += dt
                    self.zregister = 0
                    self.register = 0
            elif key[pygame.K_LEFT]:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                    self.dx = 0
                if not self.walking:
                    self.holdTime += dt
                    self.zregister = 0
                    self.xregister = 0
            elif key[pygame.K_RIGHT]:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                    self.dx = 0
                if not self.walking:
                    self.holdTime += dt
                    self.zregister = 0
                    self.xregister = 0
            
##                self.zregister += 1
##                if self.zregister >= 10:

##                    self.zregister = 1
##                    pass
##                else:
##                    self.getinfo(game,dt)
##                    num = random.randint(1,100)
##                    if num % 7 == 0:
##                        self.zregister -= 2
                    
            
            elif key[pygame.K_q]:
                pass
            elif key[pygame.K_e]:
                pass
            elif key[pygame.K_a]:
                if Party.player2 != None:
                    z = Party.player2
                    if  z.rect.x <= self.rect.x: #and z.rect.y <= self.rect.y:
                        self.orient = 'left'
                    elif z.rect.x >= self.rect.y :
                        self.orient = 'right'
                    elif z.rect.y >= self.rect.y:
                        self.orient = 'up'
                    elif z.rect.y <= self.rect.y:
                        self.orient = 'down'
                if game.chatready == True:
                    game.chatready = False
                
                    game.chatholder.chatready = False
                    game.chatholder = None
                if game.currentplace == 'percydream.tmx':
                    printstuff('That\'s a lot of Percys.')
                if game.currentplace == 'place_of_judgement.tmx':
                    game.GAtalkcounter += 1
                    if game.GAtalkcounter == 1:
                        printstuff('You have no one to talk to.\\Sad!')
                    if game.GAtalkcounter == 2:
                        printstuff('Seriously, there is no one to talk to.\\ \\Maybe you should work on that?')
                    if game.GAtalkcounter == 3:
                        printstuff('Hey, quick question.\\What is wrong with you?\\You are still talking to no one.')
                    if game.GAtalkcounter == 4:
                        printstuff('...Did you want to talk to me?')
                    if game.GAtalkcounter == 5:
                        printstuff('Such a privilege may cost you...')
                    if game.GAtalkcounter == 6:
                        printstuff('I believe that a good price is $10.')
                    if game.GAtalkcounter == 7:
                        printstuff('That number has worked before, I believe...')
                    if game.GAtalkcounter == 8:
                        printstuff('Despacito')
                if game.currentplace == 'grassstage.tmx':
                    if Party.player2 == None:
                        printstuff('Fredrick has a slight headache.')
                        #printstuff("Fredrick begins to hear a voice.")
                        #printstuff('I shall guide you on your journey.')
                        #printstuff('No matter what you may believe, or choose...')
                        #printstuff("Your journey will lead to me.")
                        #printstuff('Find me.')
                        #printstuff("The voice fell silent...")
                            
                    if Party.player2 != None:
                        if Party.player2.name == 'Alexander Hamilton':
                            Party.player2.talk('\\                    Boob.         \\     ')
                        if Party.player2.name == 'Genmu':
                           Party.player2.talk('Hang on...')
                           printstuff('Genmu takes a deep breath.')
                           Party.player2.talk('aaaaaa.')
                           Party.player2.talk('aaaAAAA.')
                           Party.player2.talk('AAAAAAACHOOOOO!')
                           Party.player2.talk('Much better.')

                            
                if game.currentplace == 'grassstage2.tmx':
                    if Party.player2 == None:
                        printstuff('Wonder why the ground looks like that?')
                    elif Party.player2.name == 'Genmu' and not Party.player2.talkedbefore:
                        Party.player2.talk('You smell... strange.')
                        Party.player2.talk('...')
                        Party.player2.talk('Oooooh! A sword?')
                        chosenoption = Party.player2.askandquestion('You like swords too?','Who doesn\'t?','I kinda like magic...')
                        if chosenoption == 1:
                            game.genmuaffection += 1
                            Party.player2.talk('Heh heh, a man after my own heart!')
                            Party.player2.talk('Swords are so unbelievably cool.')
                            Party.player2.talk('I wish I had more arms\\so I could use all of my\\swords at the same time.')
                            Party.player2.talk('I would be an unstoppable warrior.')
                            
                            self.talk('(Who is this guy???)')
                        if chosenoption == 2:
                            Party.player2.talk('Hm?')
                            Party.player2.talk('Then why carry that blade around?')
                            Party.player2.talk('You could ALWAYS just give it to me...')
                            Party.player2.talk('I promise it\'ll be in good hands.')
                        Party.player2.talkedbefore = True
                if game.currentplace == 'grassstage2a.tmx':
                    if Party.player2 == None:
                        printstuff('I dropped my toy sword\\in the lake when I was little.')
                    elif Party.player2.name == 'Genmu':
                        Party.player2.talk('Why does this place look like this?')
                        self.talk('Like what?')
                        
                        Party.player2.talk('THE BRIDGE IS INEXPLICABLE.')
                        Party.player2.talk('Where did it come from?\\Why is it there?')
                        
                        
                if game.currentplace == 'grassstage3.tmx':
                    if Party.player2 == None:
                        printstuff('Boring.')
                    

                    elif Party.player2.name == 'Genmu':
                        findpreference()
                        self.talk('(Maybe I should get to know this guy\\ a little bit better.)')
                        character = Party.player2
                        if game.gamedata.preference == 'logic':
                            self.talk('Hey, Genmu.')
                            Party.player2.talk('What do you want?')
                        if game.gamedata.preference == 'will':
                            self.talk('Hey, Genmu.')
                            Party.player2.talk('What? This better be about swords...')
                            
                        if game.gamedata.preference == 'emotion':
                            self.talk('Can I ask you something, Genmu?')
                            Party.player2.talk('Only if it\'s interesting.')
                        chosenoption = triplequestion('What are your hobbies?','What is your deal with swords?','What do you want in a woman?')
                        if chosenoption == 2:
                            game.gamedata.willpoints += 1
                            character.talk('Really?\\You haven\'t figured it out by now?')
                            character.talk('My whole life,\\I have had only one desire.')
                            character.talk('I have been on a search to find the strongest sword.')
                            character.talk('At this moment,\\I am still awaiting a rival who I could\\hone my skills against...')
                            #self.talk('Then, maybe I\'ll fill that role.')
                            character.talk('Hmm...')
                            character.talk('Yes, you seem like a good rival.')
                            character.talk('Then, it is decided!')
                            character.talk('You will be my fated adversary.')
                            character.talk('Do you understand what that means?')
                            self.talk('Uh, no...')
                            character.talk('It means...')
                            game.SPFade(dt)
                            character.talk('I must defeat you!')
##                           
##                            if game.gamedata.preference == 'will':
                            
                            
                            self.talk('Usually, I wait until I really\\know a person before fighting them.')
                            character.talk('That is a good rule, I must admit.')
                            character.talk('I suppose that means we will\\have to save our fated duel\\for another day.')
##                                
##                                
##                            if game.gamedata.preference == 'logic':
##                                self.talk('Well, I have been raring for a fight...')
##                                character.talk('This will be a\\fight worthy of legend..')
##                                self.talk('...')
##                                character.talk('...')
##                                character.talk('No, I can\'t do it!')
##                                character.talk('You don\'t seem like\\you are ready to take me on\\quite yet.')
##                                self.talk('(Well, I have had a sword for about 15 minutes, so maybe he\'s right.)')
##                                self.talk('Then, we will fight later?')
##                                character.talk('Heh, I like your style, kid.')
##                                character.talk('Perhaps we will.')
##                                #Genmu liked that.
##                                
##                            if game.gamedata.preference == 'emotion':
##                                self.talk('Seriously!?!')
##                                character.talk('Well, actually...')
##                                character.talk('No, it doesn\'t have to be now.')
##                                character.talk('Perhaps later...')
##                                self.talk('Ok..')
##                                self.talk('(Easy come, easy go???)')
                        if chosenoption == 1:
                            character.talk('Swords are a gift from the heavens!\\Also, I am unable to focus\\on anything else!')
                            character.talk('I am unable to focus on anything else!')
                            character.talk('I love swords! They\'re neat, and easy to use!')
                            
##                            character.talk('Hmph.')
##                            character.talk('If I am to become the strongest swordsman,\\I will need the strongest sword.')
##                            character.talk('And that is why\\I am the man I am today.')
##                            self.talk('(A borderline obsessive manchild?)')
                            #if game.preference == 'Logic':
                            #    self.talk('
                        if chosenoption == 3:
                            character.talk('What\'s a woman?')
                            #if game.preference == 'emotion':
                            #    self.talk('
                if game.currentplace == 'grasstown.tmx':
                    if Party.player2 == None:
                        printstuff('The southern sea really does look nice from here...')
                    else:
                        if Party.player2.name == 'Genmu':
                            if 'FirstHometownTrip' in game.gamedata.events:
                                Party.player2.talk('You live in central town?')
                                Party.player2.talk('How could you?\\There\'s only ONE sword shop.')
                                Party.player2.talk('I would consider moving\\ somewhere not disappointing.')
                            elif 'AfterSwordShop' in game.gamedata.events:
                                Party.player2.talk('Why aren\'t we heading to the forest?')
                                self.talk('Do we have to do it now?')
                                Party.player2.talk('It is the only thing i have been thinking about for the past 3 months.')
                                Party.player2.talk('...')
                                Party.player2.talk('I neeeeeeed it!')
##                                Party.player2.talk("I wonder where my sword is.")
##                                self.talk('If you knew then I wouldn\'t have much of a point.')
##                                Party.player2.talk('...')
##                                Party.player2.talk('(I need my swords.)')                                
##                                Party.player2.talk('So where am I gonna sleep?')
##                                self.talk('On the ground.')
##                                Party.player2.talk('But that\'s awful!\\Besides, I did that yesterday...')
##                                self.talk('Well, there is a hotel.')
##                                self.talk('I heard someone special is staying there, as well.')
                if game.currentplace == 'grasstowngiftshop2.tmx':
                    Party.player2.talk('The dark swordsman is so cool...')
                if game.currentplace == 'grasstowngiftshop3.tmx':
                    Party.player2.talk('OOH! A door!')
                    Party.player2.talk('I must touch it.')
                    Party.player2.talk('Haha, YES! Door time!')
                    printstuff('Genmu attempts to open the door.')
                    Party.player2.talk('What? How could this be?')
                    Party.player2.talk('NO! Why can\'t I open it?')
                    Party.player2.talk("It's me-colored and everything!!!")
                    
                    
                if game.currentplace == 'grassdungeon1.tmx':
                    
                    Party.player2.talk('It\'s dim in here.')
                    Party.player2.talk('Can someone turn on the lights?')
                    Party.player2.talk('How can I clean my swords\\in this horrible darkness?')
                if game.currentplace == 'grassdungeon2.tmx':
                    if 'metdog' not in game.gamedata.events:
                        Party.player2.talk('URGH! The grass here is horrible!')
                        Party.player2.talk('All those memories about the\\ grass coming back as soon as you leave...')
                        Party.player2.talk('They\'re ALL coming back!\\And it\'s SCARING ME!')
                        Party.player2.talk('I don\'t want to be here...')
                        #Party.player2.talk('Gross.')
                        
                    elif 'metdog' in game.gamedata.events:
                        Party.player2.talk('Ugh, I hate that salesman so MUCH!')
                        Party.player2.talk('I almost hate him as much as I love swords!')
                        Party.player2.talk('It\'s really close. Unbelievably close.')
                if game.currentplace == 'grassdungeon4.tmx':
                    Party.player2.talk('That salesman has a pair\\of dogs he travels with.')
                    Party.player2.talk('They keep track of his inventory\\and even manage sales.')
                    Party.player2.talk('Even more annoying, they are also mages...')
                    Party.player2.talk('Even though they\'re so "perfect",\\they have their weaknesses.')
                    Party.player2.talk('One of them had serious self-doubt,\\and the other was too hotheaded.')
                    Party.player2.talk('I miss when dogs just ate food and barked at things...')
                    #Party.player2.talk('UGH! This is where i met that stupid salesman!')
                    ##Party.player2.talk('That jerk betrayed me!')
                    #Party.player2.talk('I placed the most solid of beliefs in him, and he ripped me off!')
                    #self.talk('What did he do?')
                    #Party.player2.talk('*sniff*')
                    #Party.player2.talk('He didn\'t give me a sword.')
                if game.currentplace == 'grassdungeon4a.tmx':
                    Party.player2.talk('Oh, about my backstory...')
                if game.currentplace == 'grassdungeon5.tmx':
                    if game.atalkedbefore == False:
                        Party.player2.talk('Ah, swords.')
                        Party.player2.talk('The power, and prestige they give...')
                        Party.player2.talk('Heh heh. Hahahahaha!')
                    else:
                        Party.player2.talk('Why are you looking at me like that?')
                if game.currentplace == 'grassdungeon6.tmx':
                    printstuff('Genmu looks unnerved...')
                    
                if game.currentplace == 'grassdungeon7.tmx':
                    if game.atalkedbefore == False:
                        Party.player2.talk('HOW? How can there be so much grass???')
                        Party.player2.talk('and READING!?!')
                        Party.player2.talk('AGH!')
                        Party.player2.talk('I need my swords...')
                    if game.atalkedbefore:
                        printstuff('Genmu is hyperventiliating.')
                if game.currentplace == 'grassdungeon8.tmx':
                    game.gamedata.events['grassskit1'] = True
                    if game.atalkedbefore == False:
                        Party.player2.talk('Have I told you of my\\deep disgust for grass yet?')
                        Party.player2.talk('Every leafy step I take fills me with hatred.')
                    else:
                        Party.player2.talk('Hate hate hate hate hate hate...')
                if game.currentplace == 'grassdungeon9.tmx':
                    Party.player2.talk('More grass!?!')
                    Party.player2.talk('EAaaaaghhhhh!!!!')
                    Party.player2.talk('I just wanna fight something already...')
                    Party.player2.talk('How can I become a great warrior\\if my skills are left to rust?')
                if game.currentplace == 'grassdungeon10.tmx':
                    Party.player2.talk('Someday, i want to defeat the man in the black cloak.')
                if game.currentplace == 'grassdungeon11.tmx':
                    Party.player2.talk('Yes, I am currently a sword collector.')
                if game.currentplace == 'grassdungeon12.tmx':
                    Party.player2.talk('Ask me a question, Fredrick.')
                if game.currentplace == 'grassdungeon13.tmx':
                    Party.player2.talk('Grass... Ughhhhhhh.')
                    Party.player2.talk('JUST LET ME FIGHT SOMETHING ALREADY!')
                    Party.player2.talk('...')
                    Party.player2.talk('Ooh, a sword would be nice right about now...')
                game.atalkedbefore = True
                if game.currentplace == 'grassdungeon14.tmx':
                    Party.player2.talk('One day, I met that salesman\\while looking for a certain sword.')
                if game.currentplace == 'grassdungeon15.tmx':
                    Party.player2.talk('Who\'s that over there?')
                    Party.player2.talk('OHH HE LIKES SWORDS!!!')
                if game.currentplace == 'grassdungeon18.tmx':
                    #Party.player2.talk("Eh.")
                    game.player.talk("Genmu, where do you live?")
                    Party.player2.talk("Not really anywhere. I just hunt down swords.")
                if game.currentplace == 'grassdungeon4b.tmx':
                    
                    #Party.player2.talk('Urrrrggggh....')
                    Party.player2.talk('My stomach hurts...')
                    Party.player2.talk('Something feels off right now.')
                    Party.player2.talk('Really off...')
                if game.currentplace == 'grassdungeon21.tmx':
                    Party.player2.talk('Finally! That grass, reduced to only a bad memory!')
                    Party.player2.talk('Hello SNOW!')
                    doublequestion('','It\'s really cold. REALLY cold.','You know, there\'s grass under the snow.')
                if game.currentplace == 'grassdungeonsecret.tmx':
                    Party.player2.talk("This place is out of the way...")
                    Party.player2.talk('...')
                    Party.player2.talk('I wonder if there are any swords here.')
                if game.currentplace == 'snowplace.tmx':
                    if Party.player2.name == 'Genmu':
                        Party.player2.talk('A coffee shop?')
                        Party.player2.talk('BUT coffee tastes so BAD!')
                        Party.player2.talk('They better have hot chocolate.')
                    if Party.player2.name == 'Percy':
                        Party.player2.talk('What.')
                        Party.player2.talk("I\'m not paid enough to be doing this...")
                        Party.player2.talk('...')
                        chosenoption = doublequestion("",'Do you always complain this much?', 'What would you rather do instead?')
                        if chosenoption == 1:
                            Party.player2.talk("Aren\'t WE friendly...")
                            Party.player2.talk("If you saw what they pay, you\'d complain too.")
                        else:
                            Party.player2.talk("Well, I\'ve always really wanted to become a good mage.")
                            Party.player2.talk("But I really need money...")
                        #if chosenoption
                        #printstuff("Percy seems to be thinking about something.")
                        
                        #Party.player2.talk('What, do you want to kiss or something?')
                if game.currentplace == 'snowplace2.tmx':
                        Party.player2.talk('Yes, the fountain is frozen.')
                        Party.player2.talk("I don\'t think it has ever not been frozen.")
                        #Party.player2.talk('You\'re... strong.')
                        #Party.player2.talk('Such a good mage, for a human.')
                        #Party.player2.talk('Are you sure you don\'t have any goat in you somewhere?')
                        #do you want some?
                        #percy would like some human in him...
                        #Party.player2.talk('(Finally, someone who likes what I like.)')
                        #but he has a serious side too
                      
                if game.currentplace == 'snowmountain1.tmx':
                        if Party.player2.name == 'Percy':
                            Party.player2.talk('Ugh, snow...')
                            Party.player2.talk('It just isn\'t my thing...')
                if game.currentplace == 'snowmountain2.tmx':
                        if Party.player2.name == 'Percy':
                            Party.player2.talk('No, this IS a ski area.')
                            Party.player2.talk("They act like it isn\'t\\so that only really motivated skiers show up.")
                if game.currentplace == 'snowmountain3.tmx':
                        if Party.player2.name == 'Percy':
                            Party.player2.talk('I haven\'t been here in a very long time...')
                if game.currentplace == 'snowmountain4.tmx':
                        if Party.player2.name == 'Percy':
                            Party.player2.talk("Unfortunately, I have to take you\\all the way to the top of the mountain.")
                            Party.player2.talk("That is where the resort is.")
                            Party.player2.talk('But there\'s something else there, too.')
                if game.currentplace == 'snowmountain8.tmx':
                        if Party.player2.name == 'Percy':
                            Party.player2.talk("The old shrine...")
                            Party.player2.talk("They say the heroes used this on their journey...")
                if game.currentplace == 'cave1.tmx':
                    Party.player2.talk("I used to sneak here and play when I was little...")
                if game.currentplace == '1stkalpa.tmx':
                    printstuff("This feels like that first place...")
                
                    

                            
                            
                    
                    
                    
            else:
            
                self.walking = False
                self.setSprite()
                self.holdTime = 0
                self.dx = 0
                if not game.displaytalking:
                    if self.idlestart != time.time():
                        self.idletime += time.time() - self.idlestart
                    if abs((self.idlestart - time.time())) >= 3 and abs((self.idlestart - time.time())) <= 3.04 and self.idlestart != 0:
                        self.image.scroll(-160,0)
                    if abs((self.idlestart - time.time())) >= 3.05  and abs((self.idlestart - time.time())) <= 3.09 and self.idlestart != 0:
                        self.image.scroll(-200,0)
                    if abs((self.idlestart - time.time())) >= 3.1 and abs((self.idlestart - time.time())) <= 3.14 and self.idlestart != 0:
                        self.image.scroll(-160,0)
                    if abs((self.idlestart - time.time())) >= 3.15 and abs((self.idlestart - time.time())) <= 3.19 and self.idlestart != 0:
                        self.image.scroll(0,0)
                    if abs((self.idlestart - time.time())) >= 3.2 and abs((self.idlestart - time.time())) >= 3.3 and self.idlestart != 0:
                        self.setSprite()
                    if abs((self.idlestart - time.time())) >= 6 and abs((self.idlestart - time.time())) <= 6.04 and self.idlestart != 0:
                        self.image.scroll(-160,0)
                    if abs((self.idlestart - time.time())) >= 6.05  and abs((self.idlestart - time.time())) <= 6.09 and self.idlestart != 0:
                        self.image.scroll(-200,0)
                    if abs((self.idlestart - time.time())) >= 6.1 and abs((self.idlestart - time.time())) <= 6.14 and self.idlestart != 0:
                        self.image.scroll(-160,0)
                    if abs((self.idlestart - time.time())) >= 6.15 and abs((self.idlestart - time.time())) <= 6.19 and self.idlestart != 0:
                        self.image.scroll(0,0)
                    if abs((self.idlestart - time.time())) >= 6.2 and abs((self.idlestart - time.time())) >= 6.3 and self.idlestart != 0:
                        self.setSprite()
                    if abs((self.idlestart - time.time())) >= 20.0 and abs((self.idlestart - time.time())) <= 59.9 and self.idlestart != 0:
                        self.image.scroll(-240,0)
                    if abs((self.idlestart - time.time())//1) == 20: #and abs((self.idlestart - time.time())) <= 29.9:
                        game.displaytalk('Are you just going to stand there and do nothing? ')
                    if abs((self.idlestart - time.time())//1) == 30: #and abs((self.idlestart - time.time())) <= 39.9 :
                        game.displaytalk('Seriously, get going!')
                    if abs((self.idlestart - time.time())//1) == 45: #and abs((self.idlestart - time.time())) <= 59.9:
                        game.displaytalk('Or just stand there, whatever.')
                    if abs((self.idlestart - time.time())//1) == 60: #and abs((self.idlestart - time.time())) <= 79.9:
                        game.displaytalk('...')
                    if abs((self.idlestart - time.time())//1) == 80: #and abs((self.idlestart - time.time())) <= 89.9:
                        game.displaytalk('Much power! Such programs! ')
                    if abs((self.idlestart - time.time())//1) == 90: #and abs((self.idlestart - time.time())) < 94.9:
                        pygame.display.set_caption('Now, how about I do nothing and you be impatient?')
                        game.BlackOut()
                        time.sleep(5)
                    if abs((self.idlestart - time.time())//1) == 95: #and abs((self.idlestart - time.time())) < 300:
                        game.displaytalk('Heh, I got you for a second.')
                    if abs((self.idlestart - time.time())//1) == 300: #and abs((self.idlestart - time.time())) <= 1000:
                        game.displaytalk('Idling is bad, you know. ')
                
                    
                    
            # Walking mode enabled if a button is held for 0.05 seconds
            if self.holdTime >= 50:
                self.walking = True
            lastRect = self.rect.copy()
            lastColRect = self.collisionrect.copy()
            # Walking at ? pixels per frame in the direction the player is facing
            speed = 4
            if running:
                #debug 36
                speed = 12
                
            if self.walking:
                if self.orient == 'up':
                   
                    self.rect.y -= speed
                    
                    self.collisionrect.y -= speed
                    
                elif self.orient == 'down':
                    self.rect.y += speed
                    self.collisionrect.y += speed
                elif self.orient == 'left':
                    self.rect.x -= speed
                    self.collisionrect.x -= speed
                elif self.orient == 'right':
                    self.rect.x += speed
                    self.collisionrect.x += speed
##                if self.dx == 0:
##                    self.dx += 8
                
                self.dx += 2
            # Collision detection:
            # Reset to the previous rectangle if player collides
            # with anything in the foreground layer
            if len(game.tilemap.layers['Tile Layer 1'].collide(self.collisionrect, 
                                                            'block')) > 0 or len(game.tilemap.layers['Object Layer 1'].collide(self.collisionrect, 
                                                            'block')) > 0:
                if not game.noclip:
                    self.rect = copy.copy(lastRect)
                    self.collisionrect = copy.copy(lastColRect)

            elif  len(game.tilemap.layers['Object Layer 1'].collide(self.rect, 'event')) > 0 and not game.debug:
                
               
                for cell in game.tilemap.layers['Object Layer 1'].collide(self.rect, 'event') :
                    if 'eventrequirement' in cell.properties:
                         if cell.properties['eventrequirement'] not in gamedata.events:
                             self.rect = copy.copy(lastRect)
                             self.collisionrect = copy.copy(lastColRect)
                         else:
                             continue
                             
                            
                    #print(cell.properties['event'],'Event value')
                    if game.currentplace == 'itemplace.tmx':
                        
                        self.talk('What is this gonna teach me?')
                    if game.currentplace == 'firstplace.tmx':
                        if cell.properties['event'] == 2:
                            self.talk('!')
                            self.walk('right',4)
                            self.getinfo(game,dt)
                        if cell.properties['event'] == 1:
                            print('Gray Cloak shows up?')
                    if game.currentplace == 'grassstage4.tmx':
                        game.fadeOut()
                        game.initextras()
                    if game.currentplace == 'grassdungeon1.tmx':
                        Party.player2.talk('UGH!')
                        Party.player2.talk('I HATE this place!')
                        Party.player2.talk('This is where I met that salesman...')
                        Party.player2.talk('What a weirdo he was!')
                        Party.player2.talk('The way he would get around money was horrifying.')
                        Party.player2.talk('He would get this weird look on his face,\\and pinch the money really tight...')
                        Party.player2.talk('Then, he would go "WEEEEEUEW!"\\Like a child riding a pig!')
                        Party.player2.talk('How could someone be so obsessed\\with something that\'s not a sword?')
                        game.gamedata.events['genmugrassintro'] = True
                        
                    if game.currentplace == 'grassdungeon4a.tmx':
                        pass                        
                        
                        
                        
                        
                    if game.currentplace == 'grassdungeon6.tmx':
                        Party.player2.talk('I have this sinking feeling, deep inside my stomach.')
                        Party.player2.talk('Initially, i thought I was hungry,\\but I ate something and IT\'S STILL THERE!')
                        Party.player2.talk('Obviously, my swordwielder\'s awareness\\is telling me that bizarre salesman is near.')
                        Party.player2.talk('...')
                        Party.player2.talk('PLEASE SAVE ME FROM HIM!')
                    if game.currentplace == 'grassdungeon18.tmx':
                        if 'aftergrassdungeon' not in game.gamedata.events:
                            Party.player2.talk('Finally!')
                            Party.player2.talk('WE\'RE FREE!')
                        
##                        Party.player2.talk('Uh, so what are you trying to do?')
##                        game.player.talk('What do you mean?')
##                        
##                        Party.player2.talk('Certainly you, a fellow swordwielder,\\must be on a journey your own?')
##                        game.player.talk('Well...')
##                        game.player.talk('I was supposed to help you.')
##                        Party.player2.talk('Huh.')
##                        Party.player2.talk('That means...')
##                        Party.player2.talk('Finally! My first fan!')
##                        
##                        Party.player2.talk('I have waited years for this day.')
##                        
##                        Party.player2.talk('I\'d cry if legends were able to.')
##                        Party.player2.talk('So tell me, how did word of my\\swordsmanship reach your ears?')
##                        game.player.talk('Uh, some guy told me to find you.')
##                        Party.player2.talk('TWO fans!?!')
##                        printstuff('This seems to be too much for Genmu...')
                    if game.currentplace == 'grassdungeon4b.tmx':
                        if 'event2' in cell.properties:
                    
                            Party.player2.talk("Fredrick?")
                            Party.player2.talk("You don\'t look so good.")
                            printstuff("Fredrick is still feeling off.")
                            Party.player2.talk("This adventure is starting to\\ weigh on this legendary swordsman.")
                            Party.player2.talk("We\'re not gonna find any swords\\with you zoning out like that...")
                            Party.player2.talk("We should get back to your village.")
                            game.gamedata.events['grassdungeonround1done'] = True
                            game.gamedata.events['grasstownhotel'] = True
                               
                            #if game.var == 1:
                            ##    Party.player2.talk("Ohh, I REALLY need to find some swords..")
                             #   Party.player2.talk("Fredrick! Stop tempting me!")
                                
                        else:
                            if 'ofredrickencounter' not in game.gamedata.events:
                            
                                printstuff('...')
                                printstuff('Fredrick is feeling strange.')
                                game.player.talk("Something's wrong.")
                                Party.player2.talk('NOOO! Not you, too!\\I blame the grass! It ruins EVERYTHING!')
                                #Party.player2.talk('AHHHHHHHHHHHH--')
                                #Party.player2.rect.x -= 20000
                                game.BlackOut()
                                game.initextras()
                                for i in game.actors:
                                    if i.name == '???':
                                        char = i
                                
                                char.talk('You...')
                                printstuff('A familiar voice calls towards the being.')
                                printstuff('You know what you\'re doing isn\'t right.')
                                char.talk('I\'m not listening to YOU anymore.')
                                char.talk('That cloaked scumbag...')
                                Party.player2.talk("Is someone there? I don't see anything...")
                                Party.player2.talk('Is something happening, Fredrick???')
                                char.talk('He can\'t even see me?')
                                #char.talk('You really took EVERYTHING from me.')
                                #printstuff("A somewhat wry grin appears on his face.")
                                char.talk("I can't even exist with you around...")
                                printstuff("The person points a sword at Fredrick.")
                                
                                ##chosenoption = doublequestion("He makes me feel off.",'Who are you?','You know Gray, too?')
                                ##if chosenoption == 1:
                                ##    char.talk('OH, of COURSE.')
                                ##   char.talk('You know what?\\Why don\'t you tell me?')
                                ##    char.talk('Hmph...')
                                ##    char.talk('I\'ll make it VERY clear just who I am.')
                                ##   #char.talk('What makes YOU so special, anyway?')
                                    
                                #else:
                                #    char.talk('Do I know him?')
                                #    char.talk("Do YOU know him?")
                                #    char.talk('Do you have any idea who he really is?')
                                #    char.talk('To think that dirtbag really started\\this garbage all over again...')
                                ##    printstuff('A look of disgust appears on his face,\\but only for a moment.')
                                 #   char.talk('No, that\'s not important right now.')
                                #    printstuff('He pulls out a weapon...?')
                                #    char.talk('I\'m not wasting any more time.')
                                #    char.talk('Show me why he picked you.')
                                
                                
                                
                                battle.Battle(Party.player1,[battle.fredrick],[battle.ofredrick],'grass stage',None, (100,100,200),[], 'Original Fredrick Encounter',gamedata)
                                #                                                                  ,'gray area',None, (0,0,0),['Stick','First Aid Kit'], 'FallenWarrior Battle',gamedata)
                                char.talk('W-what happened???')
                                char.talk('No! Not again! Why?!')
                                char.talk('...')
                                char.talk("Why does it have to be me?")
                                #printstuff('The person\'s face suddenly becomes determined.')
                                #char.talk('Next time...')
                                
                                #char.talk('I\'ll show you who\\I really am next time.')
                                char.rect.x += 90000
                                printstuff("As suddenly as he appeared, he vanishes.")
                                printstuff('Fredrick feels a strange connection to that person...')
                                Party.bonds.append(pc.OfredrickBond)
                                for i in Party.bonds:
                                    if i.name == 'OFredrick' and i.level == 1:
                                        #i.level += 1
                                        printstuff('A voice begins speaking into Fredrick\'s mind.')
                                        printstuff('You, the one whose path leads to the end...',0,1,1)
                                        printstuff('Let an alternate path guide your through your own.',0,1,1)
                                printstuff("Something has awakened inside Fredrick...")
                                printstuff('Fredrick\'s SPmeter activates.')
                                Party.player2.talk('Were you fighting an invisible person?')
                                Party.player2.talk('So much for ME being the legendary swordsman here.')
                                game.gamedata.events['ofredrickencounter'] = True                        
                        

                            
                        
                        
                    if game.currentplace == 'grassdungeon20.tmx':
                        Party.player2.talk('Th-that\'s...')
                        
                        Party.player2.talk('HIM!')
                
                        Party.player2.talk('Well, maybe he\'s just some peddler...')
                        Party.player2.talk('No, my senses never lie!\\He has the same smug look and everything....')
                        Party.player2.talk('Ohhhhh, you HAVE to get my sword from him.')
                        Party.player2.talk('I\'d go, but he\'d probably scream and run if he saw me.')
                        Party.player2.followmode = False
                        Party.player2.walkmode = False
                        Party.player2.walk('left',20)
                        del cell.properties['event']
                        game.killtime(1)
                        printstuff("You must interact with\\the salesman by yourself...")
                    if game.currentplace == 'snowplacetouristcenter.tmx':
                        if 'talkedtopercy' not in game.gamedata.events: 
                            for i in game.actors:
                                if i.name == 'Percy':
                                    percy = i
                            if 'PercyMercy' in game.gamedata.events:
                                percy.talk("Oh, you...?")
                            elif 'PercyMercy' not in game.gamedata.events:
                                percy.talk("Oh, YOU.")
                                percy.talk("What do YOU want?")
                            chosenoption = percy.askandquestion('Are you looking to book a room?', 'Might as well.','Not time yet.' )
                            if chosenoption == 1:
                                if 'percymercy' in game.gamedata.events:
                                    #friendly percy is polite?z
                                    percy.talk('The actual hotel is at the top of the mountain.')
                                    percy.talk("I will have to take you there...")
                                    percy.talk('It should not take too long.')
                                    percy.talk("In addition, there are a few landmarks you may want to see.")
                                else:
                                    percy.talk('.')
                                    percy.talk("The hotel itself is actually in another place.")
                                    percy.talk("It\'s ALL the way at the top of the mountain.")
                                    percy.talk("You should be very grateful \\ I am forced by company policy to do this.")
                                    percy.talk("You should be even more thankful \\ that I also already used all \\ my breaks for the day.")
                                printstuff("Percy has joined your party.")
                                percy.walkmode = True
                                percy.followmode = True
                                Party.player2 = percy
                                game.gamedata.events['talkedtopercy'] = True

                    
                        del cell.properties['event']
                            
                        #percy.talk('Step-fredrick I\'m stuck in the dryer again')
                    if game.currentplace == 'dungeonentrance.tmx':
                        if cell.properties['event'] == 2:
                            game.fadeOut()
                            game.initArea('1stkalpa.tmx')
                        if cell.properties['event'] == 1:
                            
                            #printstuff('They are not unfamiliar to me...',0,1)
                            printstuff('That man in the gray cloak...',0,1)
                            printstuff('Do you know where the path\\he has set you on will take you?',0,1)
                            printstuff('Your fate is not yet decided.',0,1)
                            printstuff('If you desire to truly\\understand the circumstances of your journey.',0,1)
                            printstuff('As well as find the way\\to navigate the path awaiting you...',0,1)
                            printstuff('Find every place like this,\\and venture in to each of them.',0,1)
                            printstuff('The way to grasp your fate\\with your own hands lies within...',0,1)
                            
                            del cell.properties['event']
                    if game.currentplace == '1stkalpa.tmx':
                        game.fadeOut()
                        game.initextras()
                        screenupdate()
                        printstuff('The being gazes eyelessly.')
                        game.initseconds()
                        printstuff('What is it that you want?')
                        printstuff('Can you tell us?')
                        printstuff("Show us that which you truly desire.")
                        del cell.properties['event']
                        chosenoption = doublequestion('','I want to be the strongest.', 'I want to be loved by all.')
                        if chosenoption == 1:
                            printstuff("Then show us the strength of your desire.")
                        if chosenoption == 2:
                            printstuff("Show us why you deserve that respect.")

                    if game.currentplace == '1stkalpabattle.tmx':
                        printstuff('...!')
                        game.fadeOut()
                        self.walk('up',3)
                        for i in game.actors:
                            if i.name == 'Warrior':
                                character = i
                        
                        character.talk('You know, there was once one like you.')
                        character.talk('It\'s not important for me to tell you, but...')
                        character.talk("You may find the path to the original one through this.")
                        character.talk("This entire conflict is both because of him and for him.")
                        character.talk("I can say no more, for he limits what one may say about him.")
                        #character.talk('If too much information about him is\\given to one undeserving of such knowledge...')
                        #character.talk('He may step in.')
                        character.talk("But enough of that.")
                        character.talk('You, who grasps the path of survival...')
                        character.talk("I will see for myself if you hold\\the strength necessary within you.")
                        character.talk("...")
                        #character.talk("Alriiiiight!")
                        character.talk("Man, I hate talking like that...")
                        character.talk("Now, that I've got the serious stuff out of the way...")
                        character.talk('Let\'s have some fuuuuuun!')
                        character.talk("You've worked hard to get here!")
                        character.talk('I\'ve got a little game for you...')
                        character.talk('You will have to fight me, AND\\I will also REALLY try to defeat you, but...')
                        character.talk('If you win, I\'ll give you something very special...')
                        character.talk("It\'s something only people like me can teach you.")
                        character.talk('Good deal, huh?')
                        character.talk('So, you ready?')
##                        character.talk('You...!')
##                        character.talk('Are you the one who will save us?')
##                        character.talk('I can\'t believe it\'s finally happening!')
##                        character.talk('But man, have I been bored...')
##                        character.talk('Just sitting here, waiting has worn me out.')
##                        character.talk('....')
##                        character.talk('Alright, fight first, questions later...')
                        game.SPFade(dt)#Party.player1,[battle.fredrick
                        battle.Battle(Party.player1,[battle.fredrick],[battle.fallenwarrior],'gray area',None, (0,0,0),['Stick','First Aid Kit'], 'FallenWarrior Battle',gamedata)
                        character.talk("Hmm, you are quite the fighter.")
                        character.talk("A deal IS a deal. You ARE still alive,\\ so I will give you something to keep you that way.")
                        printstuff("The orb in Fredrick's inventory is beginning to shake.")
                        printstuff('Suddenly, it shatters!')
                        character.talk("Alright, you ready?")
                        printstuff("The being's sword knowledge flows into Fredrick.")
                        printstuff("Fredrick learned a new SPMOVE.")
                        printstuff("Cleave was added to your SPmoves.")
                        Party.spmoves.append(pc.cleave)
                        character.talk('One last thing...')
                        character.talk('If you knew your journey\\would come to an end...')
                        chosenoption = character.askandquestion('How would you feel?','It won\'t end.','I\'ll treasure what I had.')
                        if chosenoption == 1:
                            character.talk('Heh, why did I even bother asking...')
                            character.talk("You wouldn't have come this far if that wasn't your mindset.")
                            character.talk("You will do anything, huh...?")
                            character.talk("But we wouldn't have it any other way, now, would we?")
                            character.talk('"Tomorrow."')
                            character.talk("There\'s a bit more to that word than you may think.")
                            character.talk('"I will see you tomorrow."')
                            character.talk('"Until tomorrow, then."')
                            character.talk('"I can\'t wait to see you tomorrow."')
                            character.talk("Every time you see hear those words...")
                            character.talk('Every time someone draws their eyes to a future with you...')
                            character.talk("Remember what you're here for.")
                            character.talk("Make sure you can give them that future.")
                            
##                            character.talk('Do you make the rules?')
##                            character.talk('Well, really, it\'s more like...')
##                            character.talk('Are you willing to pay the price to change the rules?')
                        if chosenoption == 2:
                            character.talk("Of course, of course.")
                            character.talk("How admirable.")
                            character.talk('You may be a true hero.')
                            character.talk("But true heroes are indeed the\\ones who deserve to continue on.")
                            character.talk('Maybe you got here too early, bud.')
                            character.talk("If you haven't seen your path yet...")
                            #character.talk('Stay strong.')
                        printstuff("An exit door appears from nowhere...")

                       
                        

                        del cell.properties['event']
                        
                        
                    if game.currentplace == 'place_of_judgement.tmx':
                        if cell.properties['event'] == 'titletalk1':
                    #elif game.displaytalking == True:

                            print('Triggered titletalking')
                            #game.displaytalk
                            printstuff('Run with X. Interact with Z.')

                            #game.displaytalk
                            #printstuff('Your adventure begins here.')
                            #game.displaytalk('See you soon.')
                            
                            #return
                            del cell.properties['event']
                            #that's right boiii bad programming
                            cell.px  += 10000
                        elif cell.properties['event'] == 'titletalk2':
                            #game.displaytalk('Oh wait, I almost forgot.')
                            #game.displaytalk
                            printstuff('Finally, access the menu by pressing Enter.')
                            #printstuff('Until we meet again.')
                            cell.px += 10000
                            

                        #printstuff('So, you\'ve finally arrived...',1,1)
##                        for i in game.actors:
##                            if i.name == 'Him':
##                                x = i
##                                x.rect.center = copy.copy(self.rect.center)
##                                x.rect.x += 32
##                                x.orient = 'left'
##                                x.setSprite()
##                        game.fadeOut()
##                        screenupdate()
##                        self.talk('How did you do that?')
                        elif cell.properties['event'] == 1:
                            self.setSprite()
                            screenupdate()
                            

                            #game.player.talk('???')
                            game.killtime(0.5)
                            printstuff("Fredrick feels slightly disoriented.")
                            game.killtime(0.5)
                            game.fadeOut()
                            print('Gray Cloak shows up?')
                            game.initextras()
                            for i in game.actors:
                                if i.name == 'Gray Cloak':
                                    character = i
                            screenupdate()
                            game.killtime(1)
                            character.nameless = True
                            character.talk('Oh, you showed up.')
                            done = False
                            theleaderofthebunch = 0
                            clock = pygame.time.Clock()
                            while not done:
                                theleaderofthebunch += 1
                                center = [(game.player.rect.x + character.rect.x)/2,(game.player.rect.y + character.rect.y)/2]
                                centerdiff = [(center[0] - game.player.rect.x)/20,(center[1] -game.player.rect.y)/20]
                                game.currentfocus = [game.player.rect.x + (centerdiff[0]*theleaderofthebunch),game.player.rect.y + (centerdiff[1]*theleaderofthebunch)]
                                screenupdate()
                                clock.tick(30)
                                if theleaderofthebunch == 20: #DK
                                    done = True
                            
                            game.player.getinfo(game,game.dt,[character])
                            game.currentfocus = "Player"
                        elif cell.properties['event'] == 2:
                            self.walk('right',2)
                            self.getinfo(game,dt)
                    if game.currentplace == 'grassstage.tmx':
                        print('found tile')
##                        for i in game.actors:
##                            
##                            if i.name == 'Save Guy':
##                                if i.talkedbefore == None:
##                                    i.talk('Hey, i\'m not gonna hurt you or anything...')
                    if game.currentplace == 'grassstage2b.tmx':
                        self.setSprite()
                        for i in game.actors:
                            if i.name == 'Dog':
                                character = i
                        printstuff('The dog is sniffing around for something.')
                        character.walk('left',5)
                        character.talk('*Sniff*, *Sniff*')
                        character.talk('Bark!')
                        printstuff('Something about your existence angers the dog.')
                        character.talk('BARK BARK!')
                        character.walk('right',30,1)
                        game.killtime(1)
                        printstuff("Fredrick considers the\\implications of the dog.")
##                        pygame.display.update()
##                        for i in game.actors:
##                            if i.name == 'Dog':
##                                char = i
##                        printstuff('The dog is sniffing around for something.')
##                        char.walk('left',5)
##                        char.talk('*Sniff*, *Sniff*')
##                        char.talk('Bark!')
##                        printstuff('The dog seems to have found something.')
##                        char.talk('BARK BARK!')
##                        
                        #battle.Battle('')
                        game.gamedata.events['metthewildanimal'] = True
                    if game.currentplace == 'grassstage2.tmx':
                        self.setSprite()
                        pygame.display.update()
                        for i in game.actors:
                            if i.name == 'Genmu':
                                character = i
                        character.talk('HEEEEEEY!!!','bigtext')
                        game.gamedata.events['FirstHometownTrip'] = True
                        character.talk('YOU!')
                        character.talk('YOU.')
                        character.talk('You.')
                        character.walk('left',6)
                        character.talk('Have you seen my swords?')
                        findpreference()
                        preference = gamedata.preference 
                        printstuff("Fredrick considers the implications of the swordsman.")
                        character.talk('I was just passing through,\\and I didn\'t feel my swords in my\\specially designed sword pouch!')
                        character.talk('I need those swords for\\my fated battle against\\the man in the black cloak!')    
                        character.talk('Where could they have gone???')
                        self.talk('What do they look like?')
                        character.talk('Oh, my darling swords...')
                        character.talk('The first one\'s a silver sword.\\It has these unusual markings\\on the blade.')
                        character.talk('It\'s by far the strongest sword I have.\\It is perfection, given stabby form.')
                        character.talk('I stole it from some guy.')
                        #character.talk('')
                        hassword = False
                        for i in Party.equipment:
                            if i.name == 'Lost Sword' or i.name == 'Sharp Lost Sword':
                                hassword = True
                        if not hassword:
                                character.talk('And the other one\'s a long, slender blade.\\ It\'s got more of an eastern design to it.')
                                character.talk('Anyway, I put them down somewhere,\\and then they disappeared!')
                                character.talk('That legendary hero\'s gonna think\\I\'m a nobody if I don\'t have cool swords!')
                                character.talk('Ya gotta help me find them!')                              
                                self.talk('Well, what\'s in it for me if I do?')
                                character.talk('The glory of traveling\\with an ace swordsman...')
                                self.talk('...')
                                character.talk('You have no choice but to\\enjoy my company.')                                   
##                                if game.gamedata.preference == 'logic':
##                                    self.talk('Maybe I will.')
##                                    character.talk('Then, maybe I\'l let you keep one of my sword\\ after we\'re done...')
##                                if game.gamedata.preference == 'emotion':
##                                    self.talk('Hmm, I don\'t know...\\I barely even know you.')
##                                    character.talk('Well, you\'re missing out.')
##                                    character.talk('100% of people who have gotten to\\know me rate me very highly on the \\"amazing swordsman" scale.')
##                                    character.talk('(100% of 0 is still 100%, right?\\I never was good with numbers...)')
##                                    self.talk('Maybe I\'ll see what all\\ those people are on about...')
##                                    character.talk('Maybe you will.')
                                printstuff('The swordsman has decided to\\travel with you for now...')
                                #printstuff('Your path has interwined with that of another.')
                                printstuff('You have been forced into a new bond.')
                                Party.bonds.append(pc.GenmuBond)
                                character.walkmode = True
                                character.followmode = True
                                Party.player2 = character
                                for i in Party.bonds:
                                            if i.name == 'Genmu' and i.level == 1:
                                            #i.level += 1
                                                printstuff('A voice begins speaking into Fredrick\'s mind.')
                                                printstuff('You, the one who carves his own path...',0,1,1)
                                                printstuff('Let other\'s paths give you the strength to change yours.',0,1,1)
                                            
                                            printstuff("Fredrick's strength increases by 1.")
                                            Party.player1.attack += 1
                                printstuff('"A" will let you talk to your friends.')
                                Party.player2.chatready = True
                                game.gamedata.events['mettheswordsman'] = True
                            
                        if hassword:
                            chosenoption = doublequestion('Does this guy need to know about your sword?','It belongs to him.','NoooooOOOOO???')
                            if chosenoption == 1:
                                gamedata.choices.append('swordreturner')
                                self.talk('You mean, like this sword?')
                                printstuff('Fredrick displays his newly found sword\\ to the strange sword person.')
                                character.talk('Yep, that\'s it!')
                                printstuff('Sword guy instinctively snatches it away.')
                                character.talk('My marvelous monster masher...')
                                character.talk('My supreme snake slicer...')
                                character.talk('My super useful can opener...')
                                character.talk('Oh, how I\'ve missed you.')
                                printstuff('Genmu begins to cry.')
                                
                                sharpsword = False
                                for i in Party.equipment:
                                    # i don't think anyones gonna have more than one instance
                                    # of the sword.
                                    if i.name =='Sharp Lost Sword':
                                        sharpsword = True
##                                            baa = i
                                        # i love goats
##                                    if 'attack+25' in baa.specialproperties:
                                        character.talk('*sniff*, *sniff*')
                                        character.talk('...hey, it\'s sharper than I remember...')
                                        character.talk('Have you been treating her right?')
                                        self.talk('("her?" Does he mean the sword?)')
                                        self.talk('Uh, I left her alone for a little bit...')
                                        character.talk('You\'re kidding me!\\No wonder she\'s so angry!')
                                        character.talk('I\'ve gotta teach you how to treat a sword properly!')
                                        character.talk('Alright, it\'s decided!')
                                        character.talk('I am traveling with YOU until\\ we find my other sword.')
                                        self.talk('Only if I get to keep the next sword.')
                                        character.talk('What!?!')
                                        character.talk('What kind of monster ARE YOU?')
                                        character.talk('I... I\'ll...')
                                        character.talk('(This guy runs a hard bargain...)')
                                        character.talk('I\'ll think about it!')
                                        printstuff('The swordsman begrudgingly agrees to\\travel with you.')
                                        character.walkmode = True
                                        character.followmode = True
                                        Party.player2 = character
                                        printstuff('Your path has interwined with that of another.')
                                        printstuff('You have made a new bond.')
                                        
                                
                                        Party.bonds.append(pc.GenmuBond)
                                        printstuff('"A" will let you talk to your friends.')
                                        Party.player2.chatready = True
                                        for i in Party.bonds:
                                            if i.name == 'Genmu' and i.level == 1:
                                            #i.level += 1
                                                printstuff('A voice begins speaking into Fredrick\'s mind.')
                                                printstuff('You, the one who carves his own path...',0,1,1)
                                                printstuff('Let other\'s paths give you the strength to change yours.',0,1,1)
                                            
                                            printstuff("Fredrick's strength increases by 1.")
                                            Party.player1.attack += 1
                                        printstuff('"A" will let you talk to your friends.')
                                        game.gamedata.events['mettheswordsman'] = True
                                        #character.talk('My sword! It\'s so ANGRY!')
                                        #character.talk('What\'d ya do to her?')
                                    
                               #elif 'swordreturner' not in gamedata.choices and firstsword in Party.equipment:
                                #    self.talk('deg')
                                if sharpsword == False:
                                    character.talk('Oh, how my heart has LONGED for this sword...')
                                    character.talk('*sniff*,*sniff*')
                                    character.talk('...')
                                    self.talk('...')
                                    character.talk('You HAVE to help me find the other one.')
                                    #screw you 
                                    self.talk('Uh, okay, I guess.')
                                    character.talk('Great.')
                                    character.talk('NOW! Our adventure BEGINS!!!')
                                    printstuff('The swordsman has decided \\to tag along with Fredrick\\ until his sword is found.')
                                    Party.player2 = character
                                    printstuff('Your path has interwined with that of another.')
                                    printstuff('You have made a new bond.')
                                    Party.bonds.append(pc.GenmuBond)
                                    character.walkmode = True
                                    character.followmode = True
                                    
                                    Party.player2.chatready = True
                                    game.gamedata.events['mettheswordsman'] = True
                                    for i in Party.bonds:
                                        if i.name == 'Genmu' and i.level == 1:
                                            #i.level += 1
                                            printstuff('A voice begins speaking into Fredrick\'s mind.')
                                            printstuff('You, the one who carves his own path...',0,1,1)
                                            printstuff('Let other\'s paths give you the strength to change yours.',0,1,1)
                            
                                    printstuff("Fredrick's strength increases by 1.")
                                    Party.player1.attack += 1
                                    printstuff('"A" will let you talk to your friends.')


                                

                            elif chosenoption == 2:
                                self.talk('(He seems like he has plenty of swords...)')
                                character.talk('And the other one\'s a long, slender blade.\\ It\'s got more of an eastern design to it.')
                                character.talk('Anyway, I put them down somewhere,\\and then they disappeared!')
                                character.talk('What kind of a jerk would take something\\that clearly doesn\'t belong to them?')
                                
                                self.talk('So, you left your swords somewhere,\\and now they\'re gone?')
                                character.talk('Yep, that\'s what happened.')
                                character.talk('Ya gotta help me find them!')
                                if game.gamedata.preference == 'will':
                                    self.talk('Well, what\'s in it for me if I do?')
                                    character.talk('Nothing besides the joy of\\traveling with the greatest swordsman\\ who ever lived.')
                                    self.talk('Well, when you put it like that...')
                                    character.talk('You have no choice but to\\enjoy my company.')
                                    
                                    
                                if game.gamedata.preference == 'logic':
                                    self.talk('Maybe I will.')
                                    character.talk('Thank you so much, random person I don\'t know...')
                                if game.gamedata.preference == 'emotion':
                                    self.talk('Hmm, I don\'t know...\\I barely even know you.')
                                    character.talk('Well, you\'re missing out.')
                                    character.talk('100% of people who have gotten to\\know me rate me very highly on the \\"amazing swordsman" scale.')
                                    character.talk('(100% of 0 is still 100%, right?\\I never was good with numbers...)')
                                    self.talk('You should find outall\\ those people are on about...')
                                    character.talk('Maybe you will.')
                                printstuff('The swordsman has decided to\\travel with you for now...')
                                character.walkmode = True
                                character.followmode = True
                                Party.player2 = character
                                printstuff('Your path has interwined with that of another.')
                                printstuff('You have made a new bond.')
                                Party.bonds.append(pc.GenmuBond)
                                
                                Party.player2.chatready = True
                                game.gamedata.events['mettheswordsman'] = True
                                for i in Party.bonds:
                                    if i.name == 'Genmu' and i.level == 1:
                                        #i.level += 1
                                        printstuff('A voice begins speaking into Fredrick\'s mind.')
                                        printstuff('You, the one who carves his own path...',0,1,1)
                                        printstuff('Let other\'s paths give you the strength to change yours.',0,1,1)
                                
                                printstuff("Fredrick's strength increases by 1.")
                                Party.player1.attack += 1
                                printstuff('"A" will let you talk to your friends.')

                                         
                                    
                                
                        
                            #Genmu describes two rather average swords that
                            #Fredrick finds later.
                            #He really pours his heart out about these two stabby pieces of metal...
##                                battle.Battle([battle.fredrick],[battle.Genmu],'grass stage', None, (129,129,254))
                    if 'onetime' in cell.properties:
                        del cell.properties['event']
                    if game.currentplace == 'grasstown.tmx':
                        for i in game.actors:
                           if i.name == 'Percy':
                               percy = i
##                        percy.talk('Hey, fried rice!')
##                        percy.walk('left',12)
##                        percy.talk('Uh, who\'s this ninja dude?')
                    if game.currentplace == 'grasstownhotel.tmx':
                        if 'percyintro' not in game.gamedata.events:
                            for i in game.actors:
                                if i.name == 'Fluffy Concierge':
                                    gray = i
                                if i.name == 'Weird Customer':
                                    customer = i

                            gray.talk('...Here\'s your room key.')
                            customer.talk('Yeah, took you long enough.')
                            customer.talk('Do they hire anyone who walks in here?')
                            customer.rect.x += 2000
                            #customer.walk('right',20)
                            gray.talk('...')
                            printstuff('The concierge stifles a grimace.')
                            game.gamedata.events['percyintro'] = True
                            del cell.properties['event']
                        else:
                            for i in game.actors:
                                if i.name == 'Weird Customer':
                                    i.rect.x += 20000
                    if game.currentplace == 'grassdungeon2.tmx':
                        game.player.talk('Hey, genmu.')
                        Party.player2.talk('What is it, and does it have to do with swords?')
                        game.player.talk('Nothing to do with swords.\\I have to split up with you temporarily to advance the plot.')
                        Party.player2.talk('Yeeto.')
                    if game.currentplace == 'grassdungeon3.tmx':
                        if Party.player2.name == 'Genmu' and Party.player2 != None and 'genmufoundsword' not in game.gamedata.events:
                            Party.player2.talk('No way...')
                            Party.player2.walk('right',20)
                            
                            for i in allitems:
                                if i.name == 'gsword':
                                    i.rect.center = copy.copy(Party.player2.rect.center)
                                    i.rect.centerx += 64
                            Party.player2.talk('...')
                            Party.player2.talk('...\\...\...')
                            Party.player2.talk('YES!','bigtext')
                            screenupdate()
                            
                            
                            lastspot = copy.copy([game.player.rect.x,game.player.rect.y])
                            done = False
                            theleaderofthebunch = 0
                            clock = pygame.time.Clock()
                            character = Party.player2

                            while not done:
                                theleaderofthebunch += 1
                                center = [character.rect.x,character.rect.y]#[(lastspot[0] + character.rect.x)/2,(lastspot[1] + character.rect.y)/2]
                                centerdiff = [(center[0] - lastspot[0])/30,(center[1] - lastspot[1])/30]
                                game.currentfocus = [lastspot[0] + (centerdiff[0]*theleaderofthebunch),lastspot[1] + (centerdiff[1]*theleaderofthebunch)]
                                screenupdate()
                                clock.tick(30)
                                if theleaderofthebunch == 30: #DK
                                    done = True
                            Party.player2.talk("Finally!")
                            Party.player2.talk('REUNITED!','bigtext')
                            Party.player2.followmode = False
    ##                        lastspot = copy.copy([game.player.rect.x,game.player.rect.y])
    ##                        done = False
    ##                        theleaderofthebunch = 0
    ##                        clock = pygame.time.Clock()
    ##                        character = Party.player2
    ##
    ##                        while not done:
    ##                            theleaderofthebunch += 1
    ##                            center = [character.rect.x,character.rect.y]#[(lastspot[0] + character.rect.x)/2,(lastspot[1] + character.rect.y)/2]
    ##                            centerdiff = [(center[0] - lastspot[0])/30,(center[1] - lastspot[1])/30]
    ##                            game.currentfocus = [lastspot[0] + (centerdiff[0]*theleaderofthebunch),lastspot[1] + (centerdiff[1]*theleaderofthebunch)]
    ##                            screenupdate()
    ##                            clock.tick(30)
    ##                            if theleaderofthebunch == 30: #DK
    ##                                done = True
                            game.currentfocus = "Player"
                            screenupdate()
                            
                            character = Party.player2
                            lastspot = copy.copy([character.rect.x,character.rect.y])
                            done = False
                            theleaderofthebunch = 0
                            clock = pygame.time.Clock()
                          

                            while not done:
                                theleaderofthebunch += 1
                                center = [game.player.rect.x,game.player.rect.y]#[(lastspot[0] + character.rect.x)/2,(lastspot[1] + character.rect.y)/2]
                                centerdiff = [(center[0] - lastspot[0])/30,(center[1] - lastspot[1])/30]
                                game.currentfocus = [lastspot[0] + (centerdiff[0]*theleaderofthebunch),lastspot[1] + (centerdiff[1]*theleaderofthebunch)]
                                screenupdate()
                                clock.tick(30)
                                if theleaderofthebunch == 30: #DK
                                    done = True
                            printstuff('Fredrick hears a familiar voice behind him...')
                            game.fadeOut()
                            game.initextras()
                            for i in game.actors:
                                if i.name == 'Gray Cloak':
                                    gray = i
                            gray.walk('right',7)
                            
                            game.player.orient = 'left'
                            gray.talk('Good. You found the swordsman...')
                            gray.talk('I was worried you wouldn\'t be able to find him.')
                            gray.talk('Sometimes when a person is teleported,\\they become a little... disoriented.')
                            gray.talk('When I first saw you, you had a distant look\\in your eyes that reminded me of that, but...')
                            gray.talk('I guess that blank stare\\is just how your face looks.')
                            gray.talk('...')
                            gray.talk('About the swordsman...')
    ##                        chosenoption = doublequestion('He\'s almost friendly sometimes, right?','Never a boring moment with him.','Maybe it would be better if I was a sword.')
    ##                        if chosenoption == 1:
    ##                            #gray.talk('Sunny D.')
    ##                            gray.talk('If you strengthened your friendship, it would be very beneficial for you.')
    ##                            gray.talk('I hope you haven\'t forgotten what that\\weird voice spoke into your head said.')
    ##                        if chosenoption == 2:
    ##                            gray.talk('I know. It\'s all he talks about...')
    ##                            gray.talk("Why is he so obsessed with them?")
                            gray.talk('During this little sword quest you\'re on...')
                            gray.talk('You should probably strengthen your relationship with him.')
                            gray.talk('Do you know what he desires?')
                            gray.talk('I mean, what he wants is no secret\\to anyone within earshot of him, but...')
                            gray.talk('Why does he want swords so bad??')
                            gray.talk('Mere appreciation can only drive a person so far...')
                            gray.talk("Try to find his real motivation,\\ then help him achive it.")
                            gray.talk("He will be nothing but grateful to you...")
                            ##gray.talk('I have to leave suddenly,\\as I remembered that I forgot to get food.')
                            gray.talk('Until we meet again.')

                            game.killtime(2)
                            printstuff('Fredrick wonders why the man keeps teleporting.')
                            #animation about open door here?
                            gray.rect.x -= 10000
                        

                            game.currentfocus = "Player"
                            game.player.walk('right',12)
                            
                            Party.player2.talk('This is the one.')
                            Party.player2.talk('Hah, you would think he would\\learn not to leave his swords out.')
                            Party.player2.orient = 'left'
                            Party.player2.talk('Yes, it...')
                            Party.player2.talk('No...')
                            Party.player2.emote('genmushocked.png')
                            Party.player2.talk("AGH!",'bigtext')
                            Party.player2.talk('I\'ve been had!','bigtext')
                            Party.player2.imagereboot()
                            Party.player2.talk('It\'s a fake!')
                            Party.player2.talk('A SHAM!','bigtext')
                            
                            Party.player2.talk('It doesn\'t have the same feel the other one has.')
                            Party.player2.talk('It\'s so unwieldy!')
                            Party.player2.talk('The amount of wield it has is ZERO!')
                            printstuff('Genmu throws the sword away...')
                            printstuff('Genmu proceeds to have a mental breakdown.')
                            for i in allitems:
                                if i.name == 'gsword':
                                    i.rect.center = copy.copy(Party.player2.rect.center)
                                    i.rect.centerx += 20000
                            
                            Party.player2.talk('Ugh, that weird dog, and then THIS?!?')
                            Party.player2.talk('It all reeks of that salesman\'s weird planning.')
                            Party.player2.talk('All this because of a few swords...')
                            Party.player2.talk('I am sorry that I got you involved in this.')
                            chosenoption = doublequestion('','I\'d feel better if I had a sword...','I\'m just here to fight things.')
                            if chosenoption == 1:
                                pass
                            if chosenoption == 2:
                                pass
                          
                            #Party.player2.talk('So I can beat him up\\and get my swords!')
                            #Party.player2.talk('Real men solve their problems in person.')
                            #Party.player2.talk('Not by sending their magical\\dog lackeys to beat up my friends.')
                            game.player.talk('So how are we going to find him?')
                            Party.player2.talk('Let\'s just wander around until he shows up.')
                            game.player.talk('I don\'t think that\'s gonna work.')
                            
                            Party.player2.talk('You may be right, but you being right is boring.')
                            Party.player2.talk('But...!')
                            Party.player2.talk('If I check the sword...')
                            game.fadeOut()
                            screenupdate()
                            Party.player2.talk('Some rust has built up on it, but not a noticable amount.')
                            Party.player2.talk('I would assume it was dropped three days ago.')
                            Party.player2.talk('I believe he dropped it on his exit trip...')
                            Party.player2.talk('He usually passes through the forest about twice per week.')
                            Party.player2.talk('So, this should be his entry trip.')
                            Party.player2.talk('We should be able to catch him\\if we get through this forest.')
                            Party.player2.talk('...')
                            Party.player2.talk('Let\'s get going!')
                            game.gamedata.events['genmufoundsword'] = True
                            
                            
    ##                        Party.player2.talk('Thinking?\\That has no place in MY brain...')
    ##                        game.player.talk('Just try it, okay?')
    ##                        Party.player2.talk('Alright...')
    ##                        Party.player2.talk('...')
    ##                        Party.player2.talk('...\\...\\...')
    ##                        Party.player2.talk('OW!','bigtext')
    ##                        Party.player2.talk('THE PAIN!','bigtext')
    ##                        Party.player2.talk('IT HURTS!!!','bigtext')
    ##                        Party.player2.talk('AAAAAAAAAA--','bigtext')
    ##                        game.fadeOut()
    ##                        Party.player2.talk('That\'s it! I got it!')
    ##                        game.player.talk('What!?')
    ##                        Party.player2.talk('An idea so brilliant you\'ll think\\i\'m the most interesting man who ever lived!')
    ##                        Party.player2.talk('We should wander around until he shows up.')
    ##                        game.player.talk('...')
    ##                        Party.player2.talk('At a loss for words due to my brilliance?')
    ##                        game.player.talk('I guess we don\'t have any other choice...')
                            #Let's go straight to the dungeon.
                            
                            
            
                            
                            
                            game.currentfocus = "Player"
                            Party.player2.followmode = True
                            game.gamedata.events['genmuswordsearch'] = True
                    

                        
                        
                        
            elif  len(game.tilemap.layers['Object Layer 1'].collide(self.collisionrect, 'sprite')) > 0:
                x  = game.tilemap.layers['Object Layer 1'].collide(self.collisionrect, 'sprite')
                global characters
                for z in x:
                    for i in characters:
                        if i.cell == z:
                            if self.collisionrect.colliderect(i.collisionrect):
                                 self.rect = lastRect
                                 self.collisionrect = lastColRect
                #self.rect = lastRect
                #self.collisionrect = lastColRect
                for event in pygame.event.get():
                    pass
                #Clear the event queue.
            elif  len(game.tilemap.layers['Object Layer 1'].collide(self.rect, 'blockSP')) > 0:
                for cell in game.tilemap.layers['Object Layer 1'].collide(self.rect, 'blockSP'):
                    print(self.gamedata)
                    print(cell.properties['requirement'])
                    if cell.properties['requirement'] in game.gamedata.events:#if self.gamedata.events[cell.properties['requirement']]:
                        #printstuff(' You may proceed. ')
                        del cell.properties['blockSP']
                        return
                    else:
                        if game.currentplace == 'place_of_judgement.tmx':
                            printstuff(cell.properties['blockSP'])
                        if game.currentplace == 'grassstage.tmx':
                            print('found tile')
                            for i in game.actors:
                                if i.name == 'Save Guy':
                                    if i.talkedbefore == None:
                                        i.talk('Really? You\'re just going to ignore me?')
                                        
                        if game.currentplace == 'grassstage2a.tmx':
                            if Party.player2:
                                Party.player2.talk('HEY!\\That\'s not north!')
                            else:
                                printstuff('How did you get here this early?')
                        if game.currentplace == 'grassdungeon4b.tmx':
                            if game.var == 1:
                                Party.player2.talk("Ohh, I REALLY need to find some swords..")
                                Party.player2.talk("Fredrick! Stop tempting me!")
                            if game.var == 0:
                                Party.player2.talk("No, you are NOT in adventuring condition.")
                                Party.player2.talk("Heh, maybe tomorrow...")
                                game.var += 1
                            
                        if game.currentplace == 'grassdungeon5.tmx':
                            printstuff('A voice calls out to you.')
                            printstuff('Don\'t be that guy.')
                        if game.currentplace == 'grassdungeon20.tmx':
                            Party.player2.talk('Wh-where are you going???')
                            Party.player2.talk('Don\'t leave me here with him!!!')
                        
                    #printstuff(cell.properties['description'])
                    self.xregister = 1
                    self.rect = copy.copy(lastrect)
                    self.walking = False
                    self.setSprite()
            elif  len(game.tilemap.layers['Object Layer 1'].collide(self.rect, 'NewArea')) > 0:
                for cell in game.tilemap.layers['Object Layer 1'].collide(self.rect, 'NewArea'):
                    print(self.gamedata)
                    print(cell.properties['area'])
                    if cell.properties['returnarea']:
                        print('triggered startarea')
                        game.initArea(cell.properties['area'],0,cell.properties['returnarea'])
                    else:
                        print('special entry not triggered')
                        game.initArea(cell.properties['area'])
            else:
                #global characters
                for i in characters:
                    if self.collisionrect.colliderect(i.rect):
                        print(' OOH A SPRITE ')
                        self.rect = lastRect
                        self.collisionrect = lastColRect
                
                for i in allitems:
                    if self.collisionrect.colliderect(i.rect):
                        if i.tangible:
                            print('Don\'t step on that!')
                            self.rect = lastRect
                            self.collisionrect = lastColRect
             
                
                
                    
            # Area entry detection:
##            elif len(game.tilemap.layers['Tile Layer 1'].collide(self.rect, 
##                                                            'entry')) > 0:
##                entryCell = game.tilemap.layers['triggers'].find('entry')[0]
##                game.fadeOut()
##                game.initArea(entryCell['entry'])
##                
##                return
            # Switch to the walking sprite after 32 pixels
            #print('Before evaluation', self.dx)
            if self.dx == 2 :
                self.setSprite()
                # Self.step keeps track of when to change the sprite so that
                # the character appears to be taking steps with different feet.
                # No it doesn't kill yourself
                footstep.play()
                self.image.scroll(-40,0)
                self.coordsupdate()
                #footstep.play()
            if self.dx == 8:
                self.setSprite()
                #if self.orient == 'down':
                #    self.image.scroll(-280,0)
                self.coordsupdate()
                
            if self.dx == 16:
                self.setSprite()
                self.image.scroll(-80,0)
                self.coordsupdate()
            #if self.dx == 18:
            #    footstep.play()
                
            # After traveling 32 pixels, the walking animation is done
            if self.dx == 24:
                footstep.play()
                #self.walking = False
                self.setSprite()
                #if self.orient == 'down':
                #    self.image.scroll(-280,0)
                self.coordsupdate()
                
            if self.dx == 32:
                self.dx = 0
                #footstep.play()
            #print(self.dx)
##            if game.screenshift:
##                game.tilemap.set_focus(self.rect.x + 30, self.rect.y)
##            else:
##                game.tilemap.set_focus(self.rect.x, self.rect.y)

    def walk(self,direction, distance, fast=None):
        print(self.rect)    
        if direction == 'up':
            if self.orient != 'up':
                self.orient = 'up'
                self.setSprite()

        elif direction == 'down':
            if self.orient != 'down':
                self.orient = 'down'
                self.setSprite()
                        
        elif direction == 'left':
            if self.orient != 'left':
                self.orient = 'left'
                self.setSprite()


        elif direction == 'right':
            if self.orient != 'right':
                self.orient = 'right'
                self.setSprite()
                
        lastRect = self.rect.copy()
        # Walking at ? pixels per frame in the direction the player is facing
        self.dx = 0
        self.truedx = 0
        speed = 8
        if fast:
            speed = 16
        while self.truedx < distance * 32:
            
            if self.dx < 32:
                if self.orient == 'up':
                    self.rect.y -= speed
                elif self.orient == 'down':
                    self.rect.y += speed
                elif self.orient == 'left':
                    self.rect.x -= speed
                elif self.orient == 'right':
                    self.rect.x += speed
                self.dx += speed
                self.truedx += speed
                
            # Switch to the walking sprite after 32 pixels 
            if self.dx == 8:
                # Self.step keeps track of when to change the sprite so that
                # the character appears to be taking steps with different feet.
                self.image.scroll(-40,0)
            if self.dx == 16:
                self.image.scroll(40,0)
            if self.dx == 24:
                self.image.scroll(-80,0)
            # After traveling 32 pixels, the walking animation is done
            if self.dx >= 32:
                self.walking = False
                self.setSprite()    
                self.dx = 0
                self.coordsupdate()
            if self.name == 'Fredrick':
                game.tilemap.set_focus(self.rect.x, self.rect.y)
            game.tilemap.draw(game.screen)
            pygame.display.update()
            fps.tick(30)
            #print(self.rect)
        else:
            if self.name != 'Fredrick':
                self.walking = 'dummy'
            self.truedx = 0
            self.dx = 0


        
class character(Player):
    ''' Computer controlled people who the player can interact with. '''
    def __init__(self, location, cell,orientation, *groups):
        super(Player, self).__init__(*groups)
        self.coords = ((cell.px//32)+1, (cell.py//32)+2) #coords are based off bottom half, not top half
        print(self.coords)
        self.image = pygame.image.load(cell.properties['image'])
        self.imageDefault = self.image.copy()# Actual size is 28x56 no its not 
        self.originalimage = self.image.copy()
        self.rect = pygame.Rect(location, (40,80))
        self.averagewidth = copy.copy(self.rect.width)
        self.rect.topleft = location
        self.collisionrect = pygame.Rect((0,0),(40,20))
        self.collisionrect.midbottom = copy.copy(self.rect.midbottom)
        self.orient = cell.properties['orient']
        self.walking = 'dummy'
        self.name = cell.name
        print('Character Name',self.name)
        self.cell = cell
        print(cell,'cell')
        self.dx = 0
        self.idletime = None
        self.blink = None
        self.waitcounter = 0
        self.xregister = 0
        self.truedx = 0
        self.walkmode = False
        self.direction = None
        self.distance = 0
        self.distancetraveled = 0
        self.nameless = None
        self.talkedbefore = None
        self.followmode = None
        self.pathtravel = None
        self.returntospot = None
        self.characterbehind = None
        self.chatready = None
        if self.name == 'Genmu':
            self.character = DefGenmu
        #self.coords = (self.rect[0]//32, self.rect[1]//32)
        # Set default orientation
        self.setSprite()
    def setSprite(self):
        # Resets the player sprite sheet to its default position 
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -80)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -160)
        elif self.orient == 'right':
            self.image.scroll(0, -240)
    def talk(self,words, *args):
        print(self.name, ':',words)
        bigtext = False
        sentenceinterrupt = False
        for i in args:
            if i == 'bigtext':
                bigtext = True
        text.rect.center = (275,400)
        
        wait = 0
        talking = 0
        thinking = 0
        m_open = 0
        font = pygame.font.Font('FreeSans.ttf',17)
        if not self.nameless:
            title = font.render(self.name, True, (0,0,0),(255,255,255))
            titlerect = title.get_rect()
            titlerect.bottomleft = copy.copy(text.rect.topleft)
            screen.blit(title,titlerect)
            screen.blit(text.image, text.rect)
        maxlist = len(words)
        words = list(words)
        words.append('\n')
        currentlist = 0
        
        newline = 0
        dist_from_end = 0
        #print(words)
        fast = None
        letters = []
        for y in range(0,maxlist):
                #for i in letters:
                #    print(i)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                        fast = True
                    elif event.type == pygame.KEYUP and event.key == pygame.K_x:
                        fast = False
                #print('Fast?', fast)
                z = words[y]
                #print('current',z)
                #print('last',moo[y-1])
                font = pygame.font.Font('FreeSans.ttf',
                                        18)
                if bigtext:
                     font = pygame.font.Font('FreeSans.ttf',
                                        50)
    
               # print('Font Linesize is :', font.get_linesize())
                tso = font.render(z, True, (0,0,0), (255,255,255))
                tro = tso.get_rect()
                k = len(words) -1
                
                if words[y-1] == words[k]  or words[y-1] == '\\':
                    if bigtext:
                        tro.midleft = copy.copy(text.rect.midleft)
                        #Lazy fix for letter location
                        tro.x += 80
                        tro.centery = copy.copy(text.rect.center[1])
                        lastletter = copy.copy(tro)
                    else:
                        #Magic numbers: tro.x has plus 80 (30 for edges, 50 for speaker pic
                        tro.center = (copy.copy(text.rect.topleft[0]) + ((y- dist_from_end)*12) + 80 , copy.copy(text.rect.topleft[1]) + (20*newline) + 15)
                        lastletter = copy.copy(tro)
                else:
                    tro.left = lastletter.right 
                    tro.top = lastletter.top
                    lastletter = copy.copy(tro)

                
                if z == '\\' or z == '\n':
                    dist_from_end = y + 1
                    newline += 1
                    continue
                if z != ' ':
                    cursor.play()
                if z == '(':
                    thinking = 1
                elif z == ')':
                    thinking = 0
                if z != ' ' and thinking == 0 and not m_open:
                    self.image.scroll(-120,0)
                    m_open = 1
                if z == ' ' or z == '.' or z == '!' or z == '?' and thinking == 0:
                    self.setSprite()
                    m_open = 0
                
               
                global game
                game.actors.draw(game.screen)
                game.players.draw(game.screen)
                if len(game.partymembers) >= 1:
                    game.partymembers.draw(game.screen)
                tro.centery += (10*newline)
                letters.append([tso,tro])
                #print(letters)
                screen.blit(text.image, text.rect)
                for i in letters:
                    screen.blit(i[0],i[1])
                
                #screen.blit(tso,tro)

                #This is how the character image is found and drawn to the screen
                #All emotes (save for special ones) are made for the
                #character to be facing down (toward the screen)
                speaker = self
                oldvalues = [copy.copy(speaker.orient),speaker.image.copy()]
                speaker.orient = 'down'
                speaker.setSprite()
                if m_open:
                    speaker.image.scroll(-120,0)
                speakerrect = self.image.get_rect()
                speakerrect.bottomleft = copy.copy(text.rect.bottomleft)
                speakerrect.x += 15
                a = copy.copy(text.rect.bottomleft[0] + 20)
                b = copy.copy(text.rect.y + 10)
                moo = pygame.Rect((0,0),(self.rect.width,self.rect.height))
                game.screen.blit(self.image,(a,b),moo)
                speaker.orient = oldvalues[0]
                speaker.image = oldvalues[1]
                pygame.display.update()
                currentlist += 1
                if z == '-' and words[y-1] == '-':
                    self.setSprite()
                    wait = 0
                    sentenceinterrupt = True
                    time.sleep(0.5)
                    break
                if z == '.' or z == '?' or z == '!':
                    if fast:
                        #time.sleep(0.25)
                        pass
                    else:
                        time.sleep(0.5)
                if z == ',':
                    if fast:
                        #time.sleep(0.125)
                        pass
                    else:
                        time.sleep(0.25)
                else:
                    if fast:
                        pass
                    else:
                        time.sleep(0.03)
                if not fast:
                    fps.tick(60)
                else:
                    #Best kill is overkill
                    fps.tick(900)
        
        time.sleep(wait)
        revengeoftobias = False
        if sentenceinterrupt:
            revengeoftobias = True
        while not revengeoftobias:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_z:
                    revengeoftobias = True
                    

                
        screenupdate()

    def askandquestion(self,question,choice1, choice2, choice3=None):
        #Take a third option.
        global pointer
        truemode = None
        rightcheck = 0
        leftcheck = 0
        zcheck = 0
        answergiven = False
        font = pygame.font.Font("FreeSans.ttf",17)
        title = font.render(self.name, True, (0,0,0),(255,255,255))
        titlerect = title.get_rect()
        titlerect.bottomleft = text.rect.topleft
        screen.blit(title,titlerect)
        maxlist = len(question)
        currentlist = 0
        newline = 0
        dist_from_end = 0
        thinking = 0
        screen.blit(text.image, text.rect)
        # No more than 75 characters, okay?
        for y in range(0,maxlist):
            global pointer
            z = question[y]
            font = pygame.font.Font('FreeSans.ttf',
                                        18)
    
           # print('Font Linesize is :', font.get_linesize())
            tso = font.render(z, True, (0,0,0), (255,255,255))
            tro = tso.get_rect()
            k = len(question) -1
            
            if question[y-1] == question[k]  or question[y-1] == '\\':
                tro.center = (text.rect.topleft[0] + ((y- dist_from_end)*12) + 15 , text.rect.topleft[1] + (20*newline) + 15)
                lastletter = copy.copy(tro)
            else:
                tro.left = lastletter.right 
                tro.top = lastletter.top
                lastletter = copy.copy(tro)

            
            if z == '\\' or z == '\n':
                dist_from_end = y + 1
                newline += 1
                continue
        

            tro.centery += (10*newline)

            screen.blit(tso,tro)
            if z != ' ':
                cursor.play()
            if z == '(':
                thinking = 1
            elif z == ')':
                thinking = 0
            if z != ' ' and thinking == 0:
                self.image.scroll(-120,0)
            if z == ' ' or z == '.' or z == '!' or z == '?' and thinking == 0:
                self.setSprite()
            global game
            game.actors.draw(game.screen)
            game.players.draw(game.screen)
            pygame.display.update()
            currentlist += 1
            
            if z == '.' or z == '?' or z == '!':
                time.sleep(0.5)
            if z == ',':
                time.sleep(0.25)
            else:
                time.sleep(0.03)

        currentchoice = None
        q1 = font.render(choice1, True, (0,0,0), (255,255,255))
        qro1 = q1.get_rect()
        qro1.center = (text.rect.topleft[0] + 70, text.rect.topleft[1] + 80)
        qro1.left = 80
        screen.blit(q1, qro1)
        pygame.display.update()
        time.sleep(0.5)
        q2 = font.render(choice2, True, (0,0,0), (255,255,255))
        qro2 = q2.get_rect()
        qro2.center = (text.rect.topleft[0] + 250, text.rect.topleft[1] + 80)
        qro2.left = 280
        screen.blit(q2,qro2)
        pygame.display.update()        
        time.sleep(0.5)
        
        rightcheck = None
        leftcheck = None
        pointer.currentloc = 0
        cleareventqueue()
        while not answergiven:
            print(pointer.currentloc,'pointer location')
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        rightcheck = 1
                    if event.key == pygame.K_LEFT:
                        leftcheck = 1
                    if event.key == pygame.K_z:
                        zcheck = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT and rightcheck == 1:
                        pointer.currentloc += 1
                        rightcheck = 0
                        if pointer.currentloc >= 2:
                            pointer.currentloc = 0
                    if event.key == pygame.K_LEFT and leftcheck == 1:
                        leftcheck = 0
                        pointer.currentloc -= 1
                        if pointer.currentloc <= -1:
                            pointer.currentloc = 1
                    if event.key == pygame.K_z and zcheck == 1:
                        #zcheck = 0
                        global chosenoption
                        #if not truemode:
                        print(pointer.currentloc,'current location')
                        if pointer.currentloc == 0:
                            chosenoption = 1
                        elif pointer.currentloc == 1:
                            chosenoption = 2
                        else:
                            chosenoption = 3
                        print(chosenoption)
                        return chosenoption
                        gaveananswer = True
##                    if event.key == pygame.K_UP and choice3 != None:
##                        truemode = True
##                        print('third choice activated')
##                        q3 = font.render(choice3, True, (0,0,0), (255,255,255))
##                        qro3 = q3.get_rect()
##                        qro3.center = copy.copy(text.rect.center)
##                        screen.blit(text.image, text.rect)
##                        screen.blit(q3,qro3)
##                        currentchoice = qro3
                        
                        
                        
                        
                try:
                    if pointer.currentloc != lastcurrentloc:
                        #You want lazy? I'll show you lazy!
                        #WHy redraw the screen when you can just
                        #cover the last spot the cursor was?
                        screen.blit(cursorcleaner, lastcursor)
                except UnboundLocalError:
                    pass
                try:
                    if gaveananswer == True:
                        print(str(chosenoption) + 'was chosen')
                        answergiven = True
                        #pointer.currentloc = 0
                        print(pointer.currentloc,'option number')
                       
                except UnboundLocalError:
                    pass
##                if not truemode:0
                if pointer.currentloc == 0:
                    currentchoice = qro1
                else:
                    currentchoice = qro2
                pointer.rect.midright = copy.copy(currentchoice.midleft)
                #pointer.rect.center = (text.rect.topleft[0] + (15 if pointer.currentloc == 0 else 215),
                #                       text.rect.topleft[1] + 80)
                lastcursor = copy.copy(pointer.rect)
                lastcurrentloc = copy.copy(pointer.currentloc)
                
                
                screen.blit(pointer.image, pointer.rect)
                pygame.display.update()
    def checkdistance(self):
        playerloc = [game.player.rect.x, game.player.rect.y]
        #print(playerloc,'Player coordinates')
        selfloc = [self.rect.x,self.rect.y]
        #print(selfloc,'Self coords')
        # I feel proud of this next line of code, for some reason
        self.xdistfromplayer, self.ydistfromplayer = (self.rect.x-game.player.rect.x),(self.rect.y-game.player.rect.y)
        distfromplayer = (abs(self.rect.x-game.player.rect.x)//36,abs(self.rect.y-game.player.rect.y)//36)
        # The efficiency is over, back to the usual dreck
        #print(distfromplayer)
        if distfromplayer[0] <= 5 and distfromplayer[1] <= 5:
            self.playerclose = True
            self.returntospot = False
        else:
            self.playerclose = False
        if self.xdistfromplayer >= 64 or self.ydistfromplayer >= 64:
            self.speedup = True
            self.returntospot = True
        #lse:
        #   self.speedup = False
        if self.returntospot:
            if self.xdistfromplayer <= 32 and self.ydistfromplayer <= 32:
                self.speedup = False
        
    def update(self,dt,game):
       
        #if game.counter // 3 == 0:
        #print('Waitcounter =', self.waitcounter, 'Gamecounter =', game.counter)
        #self.setSprite()
##        if game.counter == 61:
##            self.waitcounter += 1
##            game.counter = 0
##        if self.waitcounter == 3:
        self.cell.rect.bottomleft = copy.copy(self.rect.bottomleft)
        if self.walkmode or self.followmode:
            self.checkdistance()
            self.orient = copy.copy(player.orient)
            self.setSprite()
            if self.followmode:
               
                #if self.playerclose:
                if self.playerclose == False or self.returntospot:
                    speed = 12
                else:
                    speed = 4
                if self.rect.bottomleft[0] <= (player.rect.bottomleft[0] -72):
                    self.rect.x += speed
                if self.rect.bottomleft[0] >= (player.rect.bottomright[0] + 72):
                    self.rect.x -= speed
                if self.rect.bottomleft[1] <= (player.rect.bottomleft[1] +36):
                    self.rect.y += speed
                if self.rect.bottomleft[1] >= (player.rect.bottomleft[1] -36):
                    self.rect.y -= speed
            if self.pathtravel:
                if self.playerclose:
                    speed = 4
                    if self.orient == 'up':
                        self.rect.y -= speed
                    elif self.orient == 'down':
                        self.rect.y += speed
                    elif self.orient == 'left':
                        self.rect.x -= speed
                    elif self.orient == 'right':
                        self.rect.x += speed
                    self.distancetraveled += speed
                    
                    #36 is the pixel width of one tile
                    if self.distancetraveled == 36:
                        self.distancetraveled = 0
                        self.distance -= 1
                    print(game.tilemap.layers['Object Layer 1'].collide(self.rect,'direction'))
                    if len(game.tilemap.layers['Object Layer 1'].collide(self.rect, 'walkinfo')) > 0:
                        for cell in game.tilemap.layers['Object Layer 1'].collide(self.rect, 'direction'):
    ##                        try:
    ##                            if cell.properties['end']:
    ##                                self.direction = 0
    ##                                self.distance = 0
    ##                                self.walkmode = False
    ##                                break
    ##                        except KeyError:
    ##                            pass
                            self.direction = copy.copy(cell.properties['direction'])
                            self.orient = copy.copy(self.direction)
                            self.setSprite()
                            self.distance = copy.copy(cell.properties['distance'])
                        
                    
                if self.distance == 0:
                    walkmode = False
        self.collisionrect.midbottom = copy.copy(self.rect.midbottom)
        if game.counter == 40:
            x = random.randint(1,8008132)
            
            #print(x)
            if x > 4004066:
                self.blink = True
            else:
                self.blink = False
        if game.counter == 43 and self.blink:
            self.image.scroll(-160,0)
        if game.counter == 46 and self.blink:
            self.image.scroll(-200,0)
        if game.counter == 49 and self.blink:
            self.image.scroll(-160,0)
        if game.counter == 52 and self.blink:
            self.image.scroll(0,0)
        if game.counter == 55:
            self.setSprite()
        if game.player.rect.colliderect(self.rect):
            if game.player.rect.bottomleft[1] < self.rect.bottomleft[1]:
                self.playerbehind = True
               
                game.coverobjects.add(self)
            if game.player.rect.bottomleft[1] > self.rect.bottomleft[1]:
                self.playerbehind = False
                if self in game.coverobjects:
                    game.coverobjects.remove(self)
                
        else:
            self.playerbehind = False
            if self in game.coverobjects:
                game.coverobjects.remove(self)
        if self.chatready:
            game.chatholder = self
            exclamation  = pygame.image.load('sprites/exclamation.png')
            excrect = exclamation.get_rect()
            excrect.midbottom = copy.copy(self.rect.midtop)
            game.chatready = True
            
           
            game.specialblits.append([exclamation,excrect,'onetime'])
            
        self.cell.px, self.cell.py = self.rect.x, self.rect.y
##            if game.counter == 60:
##                self.waitcounter = 0
##       
        
class SpriteLoop(pygame.sprite.Sprite):
    """A simple looped animated sprite.
    
    SpriteLoops require certain properties to be defined in the relevant
    tmx tile:
    
    src - the source of the image that contains the sprites
    width, height - the width and height of each section of the sprite that
        will be displayed on-screen during animation
    mspf - milliseconds per frame, or how many milliseconds must pass to 
        advance onto the next frame in the sprite's animation 
    frames - the number individual frames that compose the animation
    """
    def __init__(self, location, cell, *groups):
        super(SpriteLoop, self).__init__(*groups)
        self.image = pygame.image.load(cell['src'])
        self.defaultImage = self.image.copy()
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width,self.height))
        self.frames = int(cell['frames'])
        self.frameCount = 0
        self.mspf = int(cell['mspf']) # milliseconds per frame
        self.timeCount = 0

    def update(self, dt, game):
        self.timeCount += dt
        if self.timeCount > self.mspf:
            # Advance animation to the appropriate frame
            self.image = self.defaultImage.copy()
            self.image.scroll(-1*self.width*self.frameCount, 0)
            self.timeCount = 0
            
            self.frameCount += 1
            if self.frameCount == self.frames:
                self.frameCount = 0
class spobject(Player):
    ''' Objects that the player can interact with
        or go in front of or behind.
    '''
    def __init__(self, location, tile, *groups):
        super(Player, self).__init__(*groups)
        print(tile.name)
        self.name = tile.name
        self.image = pygame.image.load(tile['image'])
        self.rect = pygame.Rect(location,(tile.width,tile.height))
        self.tile = tile
        self.image = pygame.image.load(tile['image'])
        self.rect = pygame.Rect(location,(tile.width,tile.height))
        self.tile = tile
        self.playerbehind = None
        self.characterbehind = None
        self.tangible = True

    def update(self,x,y):
        if game.player.rect.colliderect(self.rect):
            if game.player.rect.bottomleft[1] < self.rect.bottomleft[1]:
                self.playerbehind = True
               
                #game.coverobjects.add(self)
            if game.player.rect.bottomleft[1] > self.rect.bottomleft[1]:
                self.playerbehind = False
                #if self in game.coverobjects:
                #    game.coverobjects.remove(self)
        for i in characters:
            if i.rect.bottomleft[1] < self.rect.bottomleft[1]:
                self.characterbehind = True
                #game.coverobjects.add(self)

            if i.rect.bottomleft[1] > self.rect.bottomleft[1]:
                self.characterbehind = False
                #if self in game.coverobjects:
                #    game.coverobjects.remove(self)
        for i in game.actors:
            moo = i
            #print(type(moo))
            break
        if type(self) == type(game.player):
            pass#print('char')
        if self.playerbehind == True or self.characterbehind == True:
            game.coverobjects.add(self)
        else:
            if self in game.coverobjects:
                game.coverobjects.remove(self)
        #print(self.playerbehind,'Is player behind?')
        pass

        #print('grapes')
    
class worlditem(Player):
    def __init__(self, location, tile, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load(tile['image'])
        self.rect = pygame.Rect(location,(tile.width,tile.height))
        self.tile = tile
        self.image = pygame.image.load(tile['image'])
        self.rect = pygame.Rect(location,(tile.width,tile.height))
        self.tile = tile
        self.name = tile.name
        self.tile.item = self
        self.tangible = True
        self.specialproperties = {}
 
    def update(self,x,y):
        """
        This is a dummy function.
        I'm lazy, so the worlditem class
        inherits from the player class.
        This means that the game will treat it like a player,
        unless functions are designed explicitly for
        the worlditem class.
        So here it is.
        The update function for worlditems.
        """
        pass

    
        #print('grapes')

def choicebooster():
    chosenoption = doublequestion("Choose whether to increase your max hp or mp.",'HP.','MP.')
    x = random.randint(0,2)
    if chosenoption == 1:
        game.player.player.Mhealth += 10
        if x == 0:
            printstuff("Fredrick feels more calm.")
        if x == 1:
            printstuff("Fredrick feels more determined.")
        if x == 2:
            printstuff("A wave of relaxation washes over Fredrick...")
        printstuff("His health increases by 10.")
        x = random.randint(1,4)
        if x == 3:
            printstuff('You hear a goat bleating faintly...')
            printstuff("Fredrick's health further increases by 5.")
            game.player.player.Mhealth += 5
    if chosenoption == 2:
        game.player.player.Mmp += 5
        if x == 0:
            printstuff("Fredrick feels more focused.")
        if x == 1:
            printstuff("Fredrick feels sharper.")
        if x == 2:
            printstuff("Fredrick feels a desire to achieve.")
        x = random.randint(1,4)
        if x == 3:
            printstuff('You hear a goat bleating faintly...')
            printstuff("Fredrick's MP further increases by 3.") #I round up for the fans
            game.player.player.Mmp += 5
        
    
                                
class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.currentplace = None
        self.areaname = None
        self.currentmus = None
        self.backgroundcolor = (0,0,0)
        self.screenshift = False
        self.noclip = False
        self.playercontrol = False
        self.displaytalking = False
        self.displaysentence = 'I\'ve got nothing to say to you.'
        self.atalkedbefore = False
        self.grassdisplay = False
        self.currentsentence = ''
        self.currentletter = 0
        #lettercounter is 1 so that the title talks immediately.
        self.lettercounter = 1
        self.waitcounter = 0
        self.nextsentence = []
        self.GAtalkcounter = 0
        self.counter = 0
        self.currentfocus = 'Player'
        self.data = []
        self.gamedata = None
        self.currentscene = None
        self.chatready = None
        self.specialblits = []
        self.obstacles = []
        self.filter = None
        self.var = 0
        self.genmuaffection = 0
        self.percyaffection = 0
        self.debug = None
        self.chatholder = None
        self.nosave = False
        
    def killtime(self,seconds):
##    '''
##    Waste time without freezing everything, like
##    time.wait()
##    Updates and draws the game while waiting
##    for a set amount of seconds
##    '''
        clock = pygame.time.Clock()
        start = time.time()
        endtime = start + seconds
        done = False
        while not done:
            self.tilemap.draw(game.screen)
            pygame.display.update()
            clock.tick(30)
            if time.time() >= endtime:
                done = True
    def fadeOut(self):
        #Animate the screen fading to white for entering a new area
        # or just because.
        clock = pygame.time.Clock()
        whiteRect = pygame.Surface(self.screen.get_size())
        whiteRect.set_alpha(100)
        whiteRect.fill((255,255,255))
        # Continuously draw a transparent white rectangle over the screen
        # to create a fadeout effect
        for i in range(0,7):
            clock.tick(15)
            self.screen.blit(whiteRect, (0,0))  
            pygame.display.flip()
        clock.tick(15)
        screen.fill((255,255,255,50))
        pygame.display.flip()
        
    def displaytalk(self,words):
        if game.displaytalking == True:
            print('added to queue')
            #print(game.nextsentence,'before')
            game.nextsentence += [words]
            #print(game.nextsentence,'after')
        else:
            game.displaytalking = True
            game.displaysentence = words
    def displaytalkreset(self):
        game.displaytalking = False
        game.displaysentence = "I\'ve got nothing to say."
        game.lettercounter = 1
        game.currentsentence = ""
        game.currentletter = 0
        game.waitcounter = 0
    def BlackOut(self):
        #Animate the screen fading to black for entering a new area
        clock = pygame.time.Clock()
        blackRect = pygame.Surface(self.screen.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0,0,0))
        # Continuously draw a transparent black rectangle over the screen
        # to create a fadeout effect
        for i in range(0,5):
            clock.tick(15)
            self.screen.blit(blackRect, (0,0))  
            pygame.display.flip()
        clock.tick(15)
        screen.fill((0,0,0,50))
        pygame.display.flip()
    def SPFade(self,dt):
        clock = pygame.time.Clock()
        blackRect = pygame.Surface(self.screen.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0,0,0))
        # Continuously draw a transparent black rectangle over the screen
        # to create a fadeout effect
        for i in range(0,5):
            clock.tick(15)
            self.screen.blit(blackRect, (0,0))
            game.players.draw(game.screen)
            #if len(game.partymembers.sprites()) >= 0:
            #    game.partymembers.draw(game.screen)
            game.actors.draw(game.screen)
            pygame.display.flip()
        clock.tick(15)
        screen.fill((0,0,0,50))
        pygame.display.flip()
    def findfocus(self):
        if game.currentfocus == 'Player':
            game.tilemap.set_focus(game.player.rect.x,game.player.rect.y)
        elif type(game.currentfocus) == type([]):
            game.tilemap.set_focus(game.currentfocus[0],game.currentfocus[1])
        else:
            game.tilemap.set_focus(game.player.rect.x,game.player.rect.y)
        
    def initArea(self, mapFile, introsp=False, startarea=False):
        """Load maps and initialize sprite layers for each new area"""
        game.grassdisplay = False
        game.atalkedbefore = False
        game.filter = None
        game.var = 0
        global Party
        global characters
        global AllSprites
        Allsprites = []
        
        for i in allitems:
            i.kill()
        for i in characters:
            i.kill()
        print('Characters : ',characters)
        self.tilemap = tmx.load(mapFile, screen.get_size())
        self.currentplace = str(mapFile)
        print(self.currentplace)
        Menu.image = pygame.image.load('menu.png')
        for i in ('firstplace.tmx','place_of_decisions','place_of_judgement','itemplace.tmx'):
            if self.currentplace == i:
                Menu.image = pygame.image.load('menu.png')
        for i in ('grassstage.tmx','grassstage2.tmx','riverstart.tmx'):
            if self.currentplace == i:
                Menu.image = pygame.image.load('grassstagemenu.png')
        for i in ('snowplace.tmx','snowplace2.tmx'):
            if self.currentplace == i:
                Menu.image = pygame.image.load('snowplacemenu.png')
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.actors = tmx.SpriteLayer()
        self.items = tmx.SpriteLayer()
        self.spobjects = tmx.SpriteLayer()
        self.coverobjects = tmx.SpriteLayer()
        self.partymembers = tmx.SpriteLayer()
        game.tilemap.layers.append(self.coverobjects)
        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['Object Layer 1'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)
        try:
            #for cell1 in self.tilemap.layers['Object Layer 1'].find('sprite'):
             #   
             for cell1 in self.tilemap.layers['Object Layer 1'].objects:
                 if cell1.type == 'character':
                     if 'eventrequirement' in cell1.properties:
                         if cell1.properties['eventrequirement'] not in gamedata.events:
                             pass
                         else:
                             continue
                     character((cell1.px, cell1.py), cell1,cell1.properties['orient'], self.actors)
                     
                 
        except KeyError:
            print('No characters found.')
            raise
            #raise 
            pass
        try:
            for cell2 in self.tilemap.layers['Object Layer 1'].objects:
                if cell2.type == 'item':
                    #print('item found')
                    x = worlditem((cell2.px,cell2.py),cell2,self.items)
                    if 'noitem' not in cell2.properties:
                        x.item = eval(cell2.properties['itemid'])
                    self.items.add(x)
            self.tilemap.layers.append(self.items)
        except KeyError:
            print('No items?')
            
            pass

        try:
            for z in self.tilemap.layers['Object Layer 1'].objects:
                #print(z.type)
                if z.type == 'spobject':
                    #print('special object found')
                    x = spobject((z.px,z.py),z,self.spobjects)
                    self.spobjects.add(x)
            self.tilemap.layers.append(self.spobjects)
        except KeyError:
            print('No items?')
            raise
            pass
        try:
            #Levelinfo is an object in each map on object layer 1 that indicates (guess what) level info
            
            levelinfo = self.tilemap.layers['Object Layer 1'].find('levelinfo')[0]
            print(levelinfo)
            print(levelinfo.properties)
            game.areaname = levelinfo.properties['areaname']
            
            
            if 'music' in levelinfo.properties:
                #if levelinfo.properties['music'] != game.currentmus:
                pygame.mixer.music.load(levelinfo.properties['music'])
                pygame.mixer.music.play()
                #else:
                #    pygame.mixer.music.stop()
                #game.currentmus = levelinfo.properties['music']
            else:
                pygame.mixer.music.stop()
            if 'filter' in levelinfo.properties:
                game.filter = levelinfo.properties['filter']
            
        except:
            print('No level info found!')
            raise
        else:
            #global characters
            global AllSprites
            self.tilemap.layers.append(self.actors)
            for characterz in self.actors:
                characters.add(characterz)
                AllSprites.append(characterz)

            #
            for i in self.items:
                #print(i)
                allitems.add(i)
                
                         
                
            
                
        # Initializing player sprite
        if (startarea or startarea == 0):
            
            #links together certain entry and exit points with this variable
            #Or just makes special one time entry points
            #print(self.tilemap.layers['Object Layer 1'].objects, 'objects')
            for i in self.tilemap.layers['Object Layer 1'].objects:
                #print('Property check',i.properties['startarea'])
                
                try:
                    if 'startarea' in i.properties:
                        print(startarea,'looking for')
                        print(i.properties['startarea'], 'has')
                        if i.properties['startarea'] == startarea:
                            startCell = i
                except KeyError:
                    print('Keyerror for startarea linking')
                    pass
                        
        try:   
            assert startCell
        except UnboundLocalError:
            raise('Player needs a place to start! Don\'t you think that\'s kinda important?') from UnboundLocalError
        
            #startCell = self.tilemap.layers['Object Layer 1'].find('playerstart')[0]
        #It is out of place, but whatever
        if len(Party) == 1:
            Party.player2 = Noone
            Party.player3 = Noone
        if len(Party) >= 2:
            startCell.properties['image'] = 'graycloak.gif'
            #try:
##            if gamedata.player2:
##                Party.player2 = gamedata.player2
##                try:
##                    assert Party.player2.name != None
##                except:
##                    Party.player2.name == 'Genmu'
##            #except:
            #    print('Gameinfo has no player 2, or another error occured.')
            print(Party.player2.name, 'char name')
            
            if Party.player2.name == 'Genmu' or Party.player2.name == 'Alexander Hamilton':
                startCell.properties['image'] = 'sprites/genmu.gif'#.image = pygame.image.load('sprites/genmu.gif')
                startCell.name  = 'Genmu'
                inheritchar = DefGenmu
            if Party.player2.name == 'Percy':
                startCell.properties['image'] = 'sprites/percy.gif'
                startCell.name = 'Percy'
                inheritchar = DefPercy
            player2 = character((startCell.px, startCell.py), startCell,startCell.properties['orient'], self.partymembers)
            player2.character = inheritchar
            player2.followmode = True

            Party.player2 = player2
            self.tilemap.layers.append(self.partymembers)
            
        for i in game.tilemap.layers['Object Layer 1'].objects:
            i.assignobject(game)
        print(startCell.properties)
        self.player = Player(Party.player1,(startCell.left, startCell.top),
                             startCell.properties['orient'],startCell, self.players)
        if introsp:
            self.player.rect.center = (320,360) 
        global player
        print(player, 'Player?')
        assert self.player != None
        player = self.player
        #print(self.items.sprites(), 'items')
        self.tilemap.layers.append(self.players)
        self.tilemap.set_focus(self.player.rect.x, self.player.rect.y)
        
        if game.currentplace == 'grasstownweaponshop.tmx' and 'FirstHomeTownTrip' in game.gamedata.events:
            game.player.talk('So, here it is.')
            del game.gamedata.events['FirstHomeTownTrip'] 
            game.gamedata.events['AfterSwordShop'] = True
        if game.currentplace == 'grasstownweaponshop.tmx' and 'genmubondready' in game.gamedata.events:
            game.initextras()
        if game.currentplace == 'grassstage2a.tmx':
            if 'metorbsalesman' in game.gamedata.events:
                for i in game.spobjects:
                    if i.name == 'desk':
                        i.image = pygame.image.load('grassstageshopclosed.png')
            #if 'grassstageflyer' in game.gamedata.events:
            #    for i in game.gamedata.events:
            #        if i.name == 'flyer':
            #            i.rect.x += 8008132
            

        if game.currentplace == 'grasstown.tmx':
            if 'genmuswordsearch' in game.gamedata.events:
                game.player.talk('Don\'t you live somewhere?')
                Party.player2.talk('Well, I DO have a sword den.')
                Party.player2.talk('Its location is a secret to everyone.')
                Party.player2.talk('Even myself...')
                Party.player2.talk('Is there a hotel or something around here?')
                del game.gamedata.events['genmuswordsearch']
                game.gamedata.events['grasstownhotel'] = True
                game.gamedata.events['firstswordshop'] = True
                return
            elif 'percypizza' in game.gamedata.events:
                game.player.talk('(I\'m hungry...)')
            elif 'tohotel' in game.gamedata.events:
                Party.player2.talk('What do we do now?')
                game.player.talk('Wait until tomorrow...')
                Party.player2.talk('But that\'s so LONG!')
                Party.player2.talk('How will I become a great swordsman\\if I sit around and do nothing?')
                game.player.talk('You can stay at a hotel till then.')
                del game.gamedata.events['tohotel']
                game.gamedata.events['athotel'] = True
                
                pass
        if game.currentplace == 'grassdungeon2.tmx':
            if 'grassskit1' not in game.gamedata.events:
                
                Party.player2.chatready = True
                game.chatready = True
                game.gamedata.events['grassskit1'] = True
        if game.currentplace == 'grassdungeon3.tmx':
            if 'genmufoundsword' in game.gamedata.events:
                for i in allitems:
                    if i.name == 'gsword':
                        moo = i
                moo.rect.x += 9999
            
        if game.currentplace == 'grassdungeon4.tmx':
            game.cutgrassnum = 0
            
        if game.currentplace == 'grassdungeon5.tmx':
            if 'maginyudone' in game.gamedata.events and 'swordnyudone' not in game.gamedata.events:
                game.gamedata.events['maginyudone'] = True
                for i in game.actors:
                    if i.name == 'MagiNyu':
                        i.rect.bottomleft = (736,640)
                        
                    if i.name == 'Nyu':
                        i.rect.bottomleft = (672,640)
            elif 'swordnyudone' in game.gamedata.events and 'maginyudone' not in game.gamedata.events:
                game.gamedata.events['swordnyufirst'] = True
                for i in game.actors:
                    if i.name == 'Nyu':
                        i.rect.bottomleft = (736,640)
                    if i.name == 'SwordNyu':
                        i.rect.bottomleft = (672,640)
            elif 'swordnyudone' in game.gamedata.events and 'maginyudone' in game.gamedata.events:
                for i in game.actors:
                    if i.name == 'Nyu':
                        i.rect.bottomleft = (688,640)
                    if i.name == 'SwordNyu':
                        i.rect.bottomleft = (736,640)
                    if i.name == 'MagiNyu':
                        i.rect.bottomleft = (640,640)
        if game.currentplace == 'grassdungeon15.tmx':
            for i in allitems:
                if i.name == 'cutgrass':
                    i.tangible = False
                    i.specialproperties['cut'] = True
                    i.image = pygame.image.load('grasscut.png')
            game.gamedata.events['allcut15'] = True
        if game.currentplace == 'grassdungeonsecret.tmx':
            if 'blackcloakready' in game.gamedata.events: 
                game.initseconds()
            else:
                game.initextras()
        if 'grassdungeon' in game.currentplace:
            a = copy.copy(game.currentplace)
            a = a.strip('grassdungeon')
            a = a.strip('.tmx')
            a = 'allcut' + a
            print(a,'a')
            
            if a in game.gamedata.events:
                for i in allitems:
                    if i.name == 'cutgrass':
                        i.tangible = False
                        i.specialproperties['cut'] = True
                        i.image = pygame.image.load('grasscut.png')
        if game.currentplace == 'grassdungeon8.tmx':
            if 'grassskit2' not in game.gamedata.events:
                Party.player2.chatready = True
                game.chatready = True
                game.gamedata.events['grassskit2'] = True
        if game.currentplace == 'grassdungeon18.tmx':
            for i in allitems:
                if i.tile.properties['image'] == 'cutgrasssmall.png':
                    i.tangible = False
            game.cutgrassnum = 0
        if game.currentplace == 'grassdungeon19.tmx':
            if 'originalencounter' not in game.gamedata.events:
                Party.player2.chatready = True
                game.chatready = True
                game.gamedata.events['originalencounter'] = True
        if game.currentplace == 'grasstown.tmx':
            if 'percystart' in game.gamedata.events:
                game.initextras()
        if game.currentplace == 'grasstownhotel.tmx':
            if 'percypizza' in game.gamedata.events:
                printstuff("Fredrick is feeling hungry.")
                printstuff("Fredrick remembers that the pizza place\\ nearby has good lunch specials...")
                #game.player.talk('You know, I\'m kinda hungry...')
                #game.player.talk('Maybe I\'ll get pizza.')
        if game.currentplace == 'peteza.tmx':
            if 'percypizza' in game.gamedata.events:
                for i in game.actors:
                    if i.name == 'Percy':
                        char = i
                char.talk('Hey, Fredrick!')
                char.talk('I already ordered a pizza.')
                #that genmu guy...
                # we should all hang out together!
                #go pick up some chicks maybe??? Huh???
                #"He likes swords?", what?
        if game.currentplace == 'snowplace.tmx':
            if 'talkedtopercy' in game.gamedata.events and 'talkedtopercy2' not in game.gamedata.events:
                Party.player2.talk("Just go up from here and then to the right.")
                Party.player2.talk("That will take you to the foot of the mountain...")
                Party.player2.chatready = True
                game.gamedata.events['talkedtopercy2'] = True
        for i in allitems:
            if 'moneyid' in i.tile.properties:
                x = 'money'
                y = str(i.tile.properties['moneyid'])
                x += y
                if x in game.gamedata.events:
                    i.tile.properties['opened'] = 1
                    if i.tile.name == 'safe':
                        i.image = pygame.image.load('moneychestopen.png')
            if 'chestid' in i.tile.properties:
                x = 'chest'
                y = str(i.tile.properties['chestid'])
                x += y
                if x in game.gamedata.events:
                    i.tile.properties['opened'] = 1
                    if i.tile.name == 'chest':
                        i.image = pygame.image.load('chestopen.png')
            

        


    def initextras(self, everyone=None):
        '''
        Used to spawn characters at a certain time.
        Characters made this way must:
        1. must have type != character
        2. have sprite1 in their cell's custom properties.

        Also only works for one character at the time of writing.
        '''
        SpawnCell = self.tilemap.layers['Object Layer 1'].find('sprite1')[0]
        print(SpawnCell)
        
        global specialchar
        specialchar = character((SpawnCell.px, SpawnCell.py), SpawnCell,
            SpawnCell['orient'], self.actors)
        print(specialchar.name, specialchar)
        characters.add(specialchar)
        AllSprites.append(specialchar)
    def initseconds(self):
        '''
        Inits other special characters
        (lol plural it only works on one...)
        '''
        SpawnCell = self.tilemap.layers['Object Layer 1'].find('sprite2')[0]
        print(SpawnCell)
        global specialchar
        specialchar = character((SpawnCell.px, SpawnCell.py), SpawnCell,
            SpawnCell['orient'], self.actors)
        print(specialchar.name, specialchar)
        characters.add(specialchar)
        AllSprites.append(specialchar)
        
                        

            
        
    def intro(self):
        Font = pygame.font.Font('FreeSans.ttf',
                                        25)
        smallfont = pygame.font.Font('FreeSans.ttf',
                                        22)
        self.BlackOut()
        screen.fill((0,0,0))
        time.sleep(2)
        printstuff('Hmm.', 1,1)
        screen.fill((0,0,0))
        #if game.notfirsttime:
        #    printstuff('Were you unsatisfied with your outcome?\\It was the one most fitting for you.')
        
        printstuff('It has been a while\\since someone like you has come here.',1,1)
        screen.fill((0,0,0))
        printstuff('Before we begin,\\I would like to know your name.',1,1)
        name = []
        done = False
        shift = False
        keyboard = smallfont.render('Use the keyboard!',True, (200,200,200),(0,0,0))
        keyboardrect = keyboard.get_rect()
        keyboardrect.center = (320,460)
        while not done:
            game.screen.blit(keyboard,keyboardrect)
            print(name)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    shift = True
                if event.type == pygame.KEYUP:
                    print(event.key)
                    if event.key == pygame.K_BACKSPACE:
                            currentname.fill((0,0,0))
                            game.screen.blit(currentname, namerect)
                            if len(name)  > 0:
                                name.pop((len(name)-1))
                            else:
                                pass
                    if event.key == pygame.K_RETURN:
                        Name = ''
                        for i in name:
                            Name += i
                        done = True
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        shift = False
                    for i in ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'):
                        if len(name) <= 10:
                            if event.key == ord(i) and shift == True:
                                k = i.capitalize()
                                name.append(k)
                            elif event.key == ord(i) and shift == False:
                                name.append(i)
                        
            moo = ''
            for i in name:
                moo += i
           
            currentname = Font.render(moo,True, (255,255,255),(0,0,0))
            namerect = currentname.get_rect()
            namerect.center = (320,370)
            game.screen.blit(currentname,namerect)
            pygame.display.update()
            moo = ''
                        
                            
                    
        screen.fill((0,0,0))
        Name = Name.lower()
        playername  = copy.copy(Name)
        Name = Name.capitalize()
        
        if Name.lower() == 'nothanks':
            printstuff('Pfff, whatever.', 1, 1)
            return
        printstuff(Name+"...", 1, 1)
        screen.fill((0,0,0))
        if Name.lower() == 'genmu':
            printstuff('What are ya talking about?', 1, 1)
       
        screen.fill((0,0,0))
##        for i in ('So, i'):
##            'This story is unlike most others.', 'Choices you make will directly affect the story,\in ways both expected and unexpected.',
##                  'Also, as in real life, once a choice \\has been made, it cannot be undone.\\You can only move forward.',
##                  'Be cautious, but also trust your heart.', 'That being said...'):
##            printstuff(i,1,1)
        screen.fill((0,0,0))
        
      
        self.fadeOut()
        self.initArea('namingstage.tmx', True)
        screenupdate()
        printstuff('See this boy?',1,1)
        for i in (-160,-200,-160,0):
            self.player.image.scroll(i,0)
            self.player.setSprite()
            time.sleep(0.1)
            screenupdate()
        #He blinks.
        printstuff('Give him a name.',1,1)
        self.player.emote('sprites/angryfredrick.png')
        name = []
        done = False
        shift = False
        keyboard = smallfont.render('Again, keyboard.',True, (200,200,200),(0,0,0))
        keyboardrect = keyboard.get_rect()
        keyboardrect.center = (120,400)
        while not done:
            game.screen.blit(keyboard,keyboardrect)
            print(name)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    shift = True
                if event.type == pygame.KEYUP:
                    print(event.key)
                    if event.key == pygame.K_BACKSPACE:
                            currentname.fill((0,0,0))
                            game.screen.blit(currentname, namerect)
                            if len(name)  > 0:
                                name.pop((len(name)-1))
                            else:
                                pass
                    if event.key == pygame.K_RETURN:
                        Name = ''
                        for i in name:
                            Name += i
                        done = True
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        shift = False
                    for i in ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'):
                        if len(name) <= 10:
                            if event.key == ord(i) and shift == True:
                                k = i.capitalize()
                                name.append(k)
                            elif event.key == ord(i) and shift == False:
                                name.append(i)
            moo = ''
            for i in name:
                moo += i
           
            currentname = Font.render(moo,True, (255,255,255),(0,0,0))
            namerect = currentname.get_rect()
            namerect.center = (315,300)
            game.screen.blit(currentname,namerect)
            pygame.display.update()
            moo = ''
        self.player.setSprite()
        screen.fill((0,0,0))
        screenupdate()
        #printstuff((Name+'...'), 1, 1)
        screen.fill((0,0,0))
        screenupdate()
        #I'm sure you all are familiar with these words already...
        if Name.lower() in ['piss','shit','ass','dick','penis','fuck','asshole','bastard','tits','cunt','pussy','alexander hamilton' 
                            ,'damn','sans']:
            printstuff(('You must be joking.'),1,1)
            screen.fill((0,0,0))
            screenupdate()
            printstuff(('This will be a long journey\\for us, it seems...'),1,1)
            screen.fill((0,0,0))
            screenupdate()
        if Name.lower() == playername:
            printstuff('I do not think he would be happy with that.')
            printstuff('He is not a representation of yourself.')
            printstuff('It would be wise to remember that...')
            #printstuff('You and him are not the same.')
            #printstuff('He is a tool with which you impart your desires..')
            #printstuff('What he is not is a representation of yourself.')
        if Name.lower() == 'fredrick':
            printstuff('...',1,1)
            printstuff('So, you learned from your mistakes\\and made the right decision.',1,1)
            printstuff('Quite fitting.',1,1)
            #first time
            #Seriously? You already know whats going to happen?
            #R=
            
        else:
            printstuff((Name+'...'),1,1)
            screen.fill((0,0,0))
            screenupdate()
            printstuff(('What kind of a name is that?'),1,1)
            screen.fill((0,0,0))
            screenupdate()
            printstuff(('Too bad. His name\'s Fredrick now.'), 1,1)
            screen.fill((0,0,0))
            screenupdate()
            self.BlackOut()
            printstuff(('Unfortunately, a name is not\\what you have control over...'),1,1)
            #printstuff((''),1,1)
            #screenupdate()
        self.BlackOut()
        printstuff(('Now, you will decide what kind\\of person the boy will become.'),1,1)
        screen.fill((0,0,0))
        pygame.display.update()
       # screenupdate()
        #self.fadeOut()
        printstuff(('For this, there are some\\choices for you to make.'),1,1)
        screen.fill((0,0,0))
        printstuff(('Make sure your answers\\reflect that which you truly desire.'),1,1)
        screen.fill((0,0,0))
        #screenupdate()
        printstuff(('I assure you,\\I will be watching\\your decisions closely...'),1,1)
        self.fadeOut()
        #Where are the questions?

        
##        Name = 'Fredrick'
##        moo = ''
##        for i in name:
##            moo += i
##       
##        currentname = Font.render(moo,True, (255,255,255),(0,0,0))
##        namerect = currentname.get_rect()
##        namerect.center = (320,300)
##        game.screen.blit(currentname,namerect)
##        pygame.display.update()
##        moo = ''
        time.sleep(1)
        screen.fill((255,255,255))
        
    def main(self):
        
        #self.intro()
        #pygame.mixer.music.load('like9woodhills-01.ogg')
        #pygame.mixer.music.play(-1,0.0)
        title = pygame.image.load('title.png')
        titleimage = title.get_rect()
        self.fadeOut()
        BLACK = (0,0,0)
        z = time.time()
        for I in range(0,60):                                     #8.3 motherfuckers
            pygame.draw.line(screen, BLACK, (197,479),(197,479 - (I*8.3)))
            pygame.draw.line(screen, BLACK, (0,110),(0 + (I*11),110))
            pygame.draw.line(screen, BLACK, (442,0),(442,0 + (I*8.3)))
            pygame.draw.line(screen, BLACK, (639,190),(639 - (I*11), 190))
            pygame.display.update()
            fps.tick(30)
        print((time.time()-z), 'josh')
        #You mean joj?
        self.fadeOut()
        screen.fill((255,255,255))
        time.sleep(0.25)
        done = False
        Font = pygame.font.Font('FreeSans.ttf',
                                        25)
        smallfont = pygame.font.Font('FreeSans.ttf',
                                        22)
        titlepointer = choicepointer((0,0,32,32),'titlepointer.png',0)
        moo = 0
        # check for save file before allowing loading.
        #gamedata.loaddata()
        mainmenuselect(self)

def mainmenuselect(self):
        title = pygame.image.load('title.png')
        titleimage = title.get_rect()
        done = False
        Font = pygame.font.Font('FreeSans.ttf',
                                        25)
        smallfont = pygame.font.Font('FreeSans.ttf',
                                        22)
        titlepointer = choicepointer((0,0,32,32),'titlepointer.png',0)
        moo = 0
        while not done:
            print(moo)
            moo += 1
            if moo >= 51:
                moo = 1
            screen.blit(title,titleimage)
            begin = Font.render('Begin',True, (0,0,0), (255,255,255))
            beginrect = begin.get_rect()
            beginrect.center = (320,280)
            color = (0,0,0)
            if gamedata.nosave == False: 
                color = (180,180,180)
            cont = Font.render('Continue',True, (color),(255,255,255))
            contrect = cont.get_rect()
            contrect.center = (320,320)
            screen.blit(cont,contrect)
            screen.blit(begin, beginrect)
            # in case of more options
            
            choicemax = 2
            if gamedata.nosave == False: choicemax = 1
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        done = True
                        if titlepointer.currentloc == 0:
                            choice = 'Begin'
                            
                            game.gamedata.emotionpoints = 0
                            game.gamedata.logicpoints = 0
                            game.gamedata.willpoints = 0
                            game.gamedata.events = {}
                            
                            Party.player2 = None
                            #game.intro()
                            print('No intro')
                        elif titlepointer.currentloc == 1:
                            choice = 'Continue'
                    if event.key == pygame.K_UP:
                        titlepointer.currentloc -= 1
                        if titlepointer.currentloc <= -1:
                            titlepointer.currentloc = 0
                    if event.key == pygame.K_DOWN:
                        titlepointer.currentloc += 1
                        if titlepointer.currentloc >= choicemax:
                            titlepointer.currentloc -= 1
            if titlepointer.currentloc == 0:
                titlepointer.rect.center = copy.copy(beginrect.center)
                titlepointer.rect.x -= 50
            if titlepointer.currentloc == 1:
                titlepointer.rect.center = copy.copy(contrect.center)
                titlepointer.rect.x -= 70
                
##            if moo == 10:
##                titlepointer.rect.x += 2
##            elif moo == 20:
##                titlepointer.rect.x += 4
##            elif moo == 30:
##                titlepointer.rect.x += 6
##            elif moo == 40:
##                titlepointer.rect.x += 4
##            elif moo == 50:
##                titlepointer.rect.x += 2
            screen.blit(titlepointer.image, titlepointer.rect)
            pygame.display.update()
            fps.tick(30)

        #He squints.
        pygame.mixer.music.stop()
        if choice == 'Continue':
            Party.players = [game.gamedata.player1]
            game.BlackOut()
            
        clock = pygame.time.Clock()
        if choice == 'Begin':
            self.initArea('place_of_judgement.tmx')
            #game.initArea('grassstage.tmx', 0, 0)
            self.player.orient = 'down'
            self.player.setSprite()
            screen.fill((0,0,0))
            #printstuff('The quick brown fox\\jumped over the\\lazy dog.')
            #printstuff('This is a work in progress.\\Keep that in mind.')
            #killtime(1)
            Party.zmoves.clear()
            Party.xmoves.clear()
            Party.cmoves.clear()
            Party.spmoves.clear()
            Fredrick.get_title(pc.Fredrick_Archetype)
            Party.items.append(firstaidkit)
            Party.items.append(tonic)
            Party.equipment.append(stick)
            Party.zmoves.append(pc.slicer)
            Party.keyitems.append(hotelcard)
            Party.player1.zattack = pc.slicer
            Party.player1.xattack = pc.Noattack
            Party.player1.spattack = pc.Noattack
            Party.player1.cattack = pc.Noattack
            
            #game.displaytalk('Can you hear me?')
            #game.displaytalk('Move with the arrow keys.')
            Party.player1.Chealth = random.randint(95,98)
            
            
        elif choice == 'Continue':
##            try:
##                moo = open('save1.txt','r')
##            except FileNotFoundError:
##                print('didn\'t work.')
            Party.equipment = copy.copy(game.gamedata.equipment)
            Party.items = copy.copy(game.gamedata.items)
            Party.keyitems = copy.copy(game.gamedata.keyitems)
            Party.player1 = copy.copy(game.gamedata.player1)
            Party.bonds = copy.copy(game.gamedata.bonds)
            #
##            game.gamedata.player1 = Party.player1 
##            game.gamedata.items = Party.items 
##            game.gamedata.equipment = Party.equipment 
##            game.gamedata.keyitems = Party.keyitems 
            game.initArea(gamedata.currentplace)
            findpreference()
            print('Kewl, you loaded a file')
        intro = False
        while 1:
            dt = clock.tick(30)
            game.dt = dt
            self.counter += 1
            if self.counter >= 61:
                self.counter = 0
            #print(self.counter)
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    #printstuff('You\'ll be back.\\We\'re not finished yet.')
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    if game.currentplace == "place_of_judgement.tmx":
                        game.gamedata.events['openedmenu'] = True
                    Menu.show_menu()
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.main()
                if event.type == pygame.KEYUP and event.key == pygame.K_a:
                    pass
##                    if game.currentplace == 'grassstage.tmx':
##                        
##                        printstuff('You shouldn\'t be able to use that button yet.',0,0,1)
##                        game.player.talk('Then how did I, if I shouldn\'t be able to?')
##                        printstuff('...',0,0,1)
##                        printstuff('(Is he annoyed, or what?)')
####                    if game.place == 'grassstage.tmx':
####                        printstuff(
##                    #printstuff('Hint goes here. Maybe.')
                if event.type == pygame.KEYUP and event.key == pygame.K_F1:
                    self.BlackOut()
                    self.initArea('grassstage.tmx')#self.initArea('firstplace.tmx')
                if event.type == pygame.KEYUP and event.key == pygame.K_F2:
                    self.BlackOut()
                    self.initArea('grasstown.tmx')
                if event.type == pygame.KEYUP and event.key == pygame.K_F3:
                    self.BlackOut()
                    self.initArea('snowplace.tmx')
                if event.type == pygame.KEYUP and event.key == pygame.K_F4:
                    self.BlackOut()
                    self.backgroundcolor = [150,150,255]
                    game.initArea('grassdungeon8.tmx', 0, 0)
                if event.type == pygame.KEYUP and event.key == pygame.K_F5:
                    self.BlackOut()
                    battle.Battle(Party.player1,[battle.fredrick],[battle.ghostface],'gray area',None,(0,0,0),['Stick','First Aid Kit'],'First Battle (Starring Gray Cloak)',gamedata)
                    findpreference()
                    print(gamedata.preference)
##                    print(self.player.player.preference)
##                    self.player.player.stat_recalculate()
##                    for i in range(0,20):
##                        self.backgroundcolor = list(self.backgroundcolor)
##                        self.backgroundcolor[0] -= i
##                        if self.backgroundcolor[0] <= 0:
##                            self.backgroundcolor[0] = 0
##                        self.backgroundcolor[1] -= i
##                        if self.backgroundcolor[1] <= 0:
##                            self.backgroundcolor[1] = 0
##                        self.backgroundcolor[2] -= i
##                        if self.backgroundcolor[2] <= 0:
##                            self.backgroundcolor[2] = 0
##                        self.backgroundcolor = tuple(self.backgroundcolor)
##                        print(self.backgroundcolor)
##                        game.screen.fill(self.backgroundcolor)
##                        screenupdate()
##                        pygame.display.update()
                if event.type == pygame.KEYUP and event.key == pygame.K_F6:
                    game.screenshift = not game.screenshift
                    game.noclip = not game.noclip
                    if game.displaytalking == False:
                        game.displaytalk('What are you doing over there?')
                    elif game.displaytalking == True:
                        game.displaytalkreset()
                    game.debug = not game.debug
                    #game.player.animation('armraise.png',35,5,200,dt)
                    #battle.Battle([battle.fredrick],[battle.ghostface],'gray area',None)
                    #printstuff('Oho. Look who showed up.',1,1)
                    #print('Characters:')
                    #for i in characters:
                    #    print(i.name)
                    #    print(i.coords)
##                    game.BlackOut()
##                    game.initArea('firstbattle.tmx')
##                    game.player.talk('( ͡° ͜ʖ ͡°)')
                    #That's right. I went there.
##                    game.player.talk(' Okay, I went, now what?')
##                    print(AllSprites)
##                    print(characters)
##                    moo = len(AllSprites)
##                    character = AllSprites[moo-1]
                    #Hey, this is really on the nose, so it\'s scrapped.
                    #ALso, deez nutz ha gotteem
##                    character.talk('Sometimes, in life, you have to fight.')
##                    character.talk('There may be a reason to fight, \\or perhaps your reason is that there is none.')
##                    character.talk('Honestly, it doesn\'t matter.')
##                    game.player.talk('Do you ALWAYS have to be confusing?')
##                    character.talk('Yes. It\'s more fun that way.')
##                    character.talk('As I was saying...')
##                    character.talk('I will teach you how to fight now.')
##                    character.talk('When a fight is imminent, the world will darken around you.')
##                    self.SPFade(dt)
##                    
##                    character.askandquestion('Are you ready?','Ready as I\'ll ever be', 'Nope')
##                    if chosenoption == 'Ready as I\'ll ever be':
##                        character.talk('Good.')
##                        self.SPFade(dt)
##                        character.talk('Let\'s begin.')
##                    else:
##                        character.talk('That\'s unfortunate, but we will begin, anyways.')
##                        game.player.talk('Even though I don\'t want to?')
##                        character.talk('Especially because you don\'t want to.')
##                        self.SPFade(dt)
##                        character.talk('Get ready.')
                    
##                    self.player.setSprite()
##                    screenupdate()
##                    self.player.player.preference = 'strength'
##                    print(self.player.player.preference)
##                    self.player.player.stat_recalculate()
                    
                if event.type == pygame.KEYUP and event.key == pygame.K_F7:
                    #gamedata.emotionpoints += 1
                    #gamedata.emotionpoints = 0
                    shopmenu(grasstownweaponshop)
                    print(gamedata.choices)
                    #gamedata.choices = []
                    pygame.display.set_mode((700,600))
##                    game.initArea('GraveArea.tmx')
##                    killtime(1)
##                    for i in characters:
##                        moo = i
##                        i.talk('This is it. \This is the place.')
##                    global player
##                    player.orient = 'right'
##                    player.setSprite()
##                    player.talk('What do you mean, "it"?')
##                    moo.talk('The first place there was.\ The place of beginnings.')
##                    Show_tilecard('Whathesaid.png')
##                    player.talk('SO, we\'re going to fight to the end here? \That\'s rather ironic.')
##                    pygame.display.set_caption('Ugh, tactless as ever.')
##                    moo.talk('Yeah, well...')
##                    moo.talk('I didn\'t mean for it to turn out like this.')
##                    moo.talk('I just wanted my old life back. ')
##                    player.talk('Sorry.')
##                    moo.talk(' Save your sympathy for \someone who isn\'t about to kill you.')
##                    game.fadeOut()
##                    x =  game.tilemap.layers['Tile Layer 3'].find('hidden')
##                    for cell in x:
##                        if 'hidden' in cell.tile.properties:
##                            del cell.tile.properties['hidden']
##                        else:
##                            continue
##                    
##                    moo.image = pygame.image.load('First_Fredrick.png')
##                    moo.imageDefault = moo.image.copy()
##                    moo.orient = 'left'
##                    moo.setSprite()

                    game.SPFade(dt)
                    
                    
                if event.type == pygame.KEYUP and event.key == pygame.K_F8:
                    for char in game.actors:
                        print("Character",char,char.name,char.coords)
                    for i in game.tilemap.layers['Object Layer 1'].objects:
                        print("Object tile",i.properties)
                    for i in allitems:
                        print("Worlditems",i.rect)
                    #pygame.display.set_mode((800,600))
                    Party.player1.zattack = pc.slicer
                    Party.player1.xattack = pc.quickslice
                    Party.player1.cattack = pc.heal
                    Party.player1.spattack = pc.meteor
                    Party.zmoves.append(pc.quickslice)
                    Party.zmoves.append(pc.commandslice)
                    Party.xmoves.append(pc.laser)
                    Party.spmoves.append(pc.meteor)
                    Party.spmoves.append(pc.cleave)
                    Party.zmoves.append(pc.chargeslice)
                    Party.bonds.append(pc.GenmuBond)
                    Party.bonds.append(pc.GrayCloakBond)
                if event.type == pygame.KEYUP and event.key == pygame.K_e:
                    goat.play()
                    

                if event.type == pygame.KEYUP and event.key == pygame.K_F9:
                    try:
                        moo = input('Type a command.')
                        try:
                            
                            exec(moo)
                        except:
                            eval(moo)
                        
                    except:
                        
                        print('Nope')
                        
                        pass
                if event.type == pygame.KEYUP and event.key == pygame.K_F10:
                    pygame.mixer.music.load('dabbad.mp3')
                    pygame.mixer.music.play()

                    
                    
                    
                    #printstuff('Hello, my dear friends.')
                    #pygame.display.set_mode((900,1200))
##                    print(game.actors)
##                    pygame.display.toggle_fullscreen()
##                    x =  game.tilemap.layers['Tile Layer 3'].find('hidden')
##                    for cell in x:
##                        if 'hidden' in cell.tile.properties:
##                            del cell.tile.properties['hidden']
##                        else:
##                            continue

                
                
                
                        
                    

            
            self.tilemap.update(dt, self)
            screen.fill(self.backgroundcolor)
            game.findfocus()
            self.tilemap.draw(self.screen)
            #self.tilemap.layers[self.players].draw(dt)
            try:
                if self.tilemap.layers['Tile Layer 4'] != None:
                    self.tilemap.layers['Tile Layer 4'].draw(self.screen)
            except KeyError:
                pass
            if len(game.obstacles) > 0:
                pass
            if len(game.coverobjects) > 0:
                game.coverobjects.draw(game.screen)
            for i in game.coverobjects:
                if i.characterbehind == True and i.playerbehind == False:
                    game.players.draw(game.screen)
            if game.filter:
                if game.filter == 'dim':
                    blackRect = pygame.Surface(self.screen.get_size())
                    blackRect.set_alpha(100)
                    blackRect.fill((0,0,0))
                    self.screen.blit(blackRect, (0,0))  
                    pygame.display.flip()

            
            if game.currentplace == 'place_of_judgement.tmx' and intro == False:
                showtitlecard('Gray_Area_Title.png')
                printstuff('A voice calls out, urging those who\\hear it to move with the arrow keys.')
                printstuff('This confuses the boy,\\who does not know what the "arrow keys" are.')
                #game.speciablits.append('Move with arrow keys!','bottom')
                intro = True
            if game.displaytalking:
                length = len(self.displaysentence)
                if self.currentletter < length:
                    game.lettercounter += 1
                    if game.lettercounter  == 2:
                        self.currentsentence += self.displaysentence[self.currentletter]
                        game.currentletter += 1
                        self.lettercounter = 0
                if self.currentletter >= length:
                    game.waitcounter += 1
                    #print(game.waitcounter,'waitcounter')
                    #print(game.nextsentence)
                    if game.waitcounter == 60:
                        game.displaytalkreset()
                        if game.nextsentence:
                            self.displaytalk(game.nextsentence[0])
                            del game.nextsentence[0]
                pygame.display.set_caption(self.currentsentence)
                
            elif not game.displaytalking and not game.grassdisplay:
                pygame.display.set_caption('ThatOneGame')
            for i in game.specialblits:
                
                
                ox, oy = game.actors.position
                sx, sy = i[1].topleft
                area = pygame.Rect((0, 0),
                                                               (i[1].width,
                                                                    i[1].height))
               
                screen.blit(i[0], (sx-ox, sy-oy), area)
                if len(i) >= 3:
                    if i[2] == 'onetime':
                        game.specialblits.remove(i)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_icon(pygame.image.load('icon.png'))
    screen = pygame.display.set_mode((640,480))#full_screen()
    pygame.display.set_caption("Map Test")
    global game
    game = Game(screen)
    game.gamedata = gamedata
    pc.gameevents = game.gamedata.events
    #try:
    #if game.counter == 15:
    moo = 0
    if moo == 1:
        game.fadeOut()
        game.initArea('introconversation.tmx', True)
        screenupdate()
        game.player.rect.centerx += 10000 #get outta here
        for moo in game.actors:
            if 'SPflag1' in moo.cell.properties:
                blackcloak = moo
            if 'SPflag2' in moo.cell.properties:
                whitecloak = moo
        blackcloak.talk('Hmph. All that work to\\keep the world running smoothly\\and look where it got us...')
        whitecloak.talk('That\'s certainly unfortunate.\\What do you suppose we do about it?')
        blackcloak.talk('Man, I am beat.\\Can we get someone else to take care of things?')
        whitecloak.talk('You\'ll have to train someone up to do it.')
        blackcloak.talk('Hm. I think I know just who to pick...')
    game.main()
    #    cursor = pygame.mixer.Sound('cursor.wav')
    #except Exception as e:
    #    print(e)
    #    time.sleep(3)
   
