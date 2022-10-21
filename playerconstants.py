import random
import pygame
import copy
import pickle
class title:
    def __init__(self,name, desc1, desc2, desc3, effect):
        self.name = name
        self.desc1 = desc1
        self.desc2 = desc2
        self.desc3 = desc3
        self.effect= effect
gameevents = None
class bond:
    def __init__(self,name,description,image):
        self.name = name
        self.level = 1
        self.desc = description
        self.image  = image
    
        #Why? Why did you come back?
        #Don\'t you get that us talking like this...
        #It\'s only gonna make things hurt even more in the end.
        #But...
        #I guess it\'s nice to have someone to talk to...
        # I\'ve been stuck for a while.
    def call(self):
        #if gameevents:
        #    printdummy('yes')
        #printdummy('Design this already u frick',0,0,0,1)
        if self.name == 'Genmu':
            printdummy('"Number not found."')
            printdummy('It seems Genmu does not think phones\\are more important than swords.')
        if self.name == 'Gray':
            printdummy('Your phone begins to ring.')
            printdummy('Suddenly, it turns off!')
            printdummy('A voice speaks into your head.')
            printdummy('Don\'t even think about it.')
        if self.name == 'OFredrick':
            printdummy('Your phone shows an error...',0,0,0,1)
        if self.name == 'Percy':
            printdummy('The phone starts to ring.')
            printdummy('...')
            printdummy('H-hello?')
            printdummy('Oh, Fredrick? I\'m happy you called me...')
            printdummy('ignore what I just said I wasn\'t feeling well.')
        if self.name == 'Lucy':
            #when I talk about you with my brother...
            #He actually smiles for once.
            #it really creeps me out.
            printdummy('Your phone rings, but only for a moment.')
            printdummy('I thought you were dating my brother...?')
        #percival and lucille?
            
    def info(self):
        if self.name == 'Genmu':
            if self.level == 1:
                printdummy('He suddenly demanded you help him with his swords.',0,0,0,1)
                printdummy('You wonder about his social skills...',0,0,0,1)
            if self.level == 2:
                printdummy('You seem to have helped him resolve his salesman problem.',0,0,0,1)
                printdummy('If only the other ones were so easily solved.',0,0,0,1)
        if self.name == 'Percy':
            if self.level == 1:
                printdummy('He hates your guts.',0,0,0,1)
                printdummy('I think?',0,0,0,1)
                printdummy('Actually, you are probably exactly the person he needs...',0,0,0,1)
        if self.name == 'Gray':
            if self.level == 1:
                printdummy('He lazily started you off on your journey.',0,0,0,1)
                printdummy('Although he is probably more invested\\ in your success than his casual behavior implies.',0,0,0,1)
        if self.name == 'OFredrick':
            if self.level == 1:
                #printdummy('He really hates you.',0,0,0,1)
                printdummy("What is it that is linking you to him?",0,0,0,1)


    def effects(self):
        if self.name == 'Genmu':
            if self.level == 1:
                printdummy('Your strength increases.',0,0,0,1)
        if self.name == 'Gray':
                printdummy('You gain the ability to use magic...',0,0,0,1)
        if self.name == 'Percy':
                printdummy('Your magic increases.',0,0,0,1)
        if self.name == 'OFredrick':
                printdummy('Your SPmeter activates...',0,0,0,1)
    
       
class item:
    '''
    Consumables, plot stuff, etc.
    '''
    def __init__(self, name, image,itemtype,effect=None,line1='Laziness detected.',line2=None,line3=None):
        self.name = name
        self.image = image
        self.description = [line1,line2,line3]
        self.effect = effect
        self.itemtype = itemtype
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3

    def imageload(self):
    #This makes the class picklable, as loaded images cannot be pickled.
    # Use the function when you need to use the image of the item
    # ex. obj
        return pygame.image.load(self.image)

    def use(self,target):

        #The only way this could be exploited is
        #if someone puts in an instance of an item
        #with a malicious effect.
        #Kind of a lame way to hack.
        #Not very efficient.
        #  Or is it ingenious?
        #  Imagine getting a copy of that weird indie game
        #  and playing through, just to get bricked
        #  when you use a certain item?
        #  Don\'t pirate the game, I guess...?
        
        

        #looking back, i exerted way more effort defending this code than
        #I did writing it.
        exec(self.effect)
        
   
Beta_Tester = title('Generic Hero', 'He has quite the blank ', 'look on his face...', '',  None)
Genmu_Default = title('Wandering Swordsman','He is at least a little interested in swords.','Sword attacks are stronger with him present.','',None)
Percy_Default = title('Sarcastic Mage','He seems to have a lot of ambitions to fulfill.','He somehow enhances your magic?','',None)
Gface_Default = title('Imitation Original','Do not forget your old friends.','','',None)
Genmu_Archetype = title('The Innocent','One who pursues happiness above all else.','','',None)
Percy_Archetype = title('The Explorer','One who journeys to realize','their deepest desires.','',None)
Fredrick_Archetype = title('The Self','A blank slate.','','',None)
Gface_Archetype = title('The Shadow','What you REALLY want...','','',None)


class Player:
    def __init__(self, name, level,battlesprite,statusboximage,
                 basehealth, basemp, baseattack,basedefense,basemagic,basemdefense,
                 basespeed,baseluck,spells, color,special=False):
        self.name = name
        self.level = level #??? useless !!!
        self.preference = None
        self.originalbattlesprite = battlesprite
        self.battlesprite = pygame.image.load(battlesprite)
        self.originalstatusboximage = None
        if statusboximage != 'None':
            self.originalstatusboximage = statusboximage
            self.statusboximage = pygame.image.load(statusboximage)
        self.titles = [Beta_Tester]
        self.current_title = Beta_Tester
        
        self.Mhealth = basehealth #+ (int(level)*10)
        self.Chealth = copy.copy(self.Mhealth)
        self.Mmp = basemp# + (int(level)*5)
        self.Cmp = copy.copy(self.Mmp)
        self.attack = baseattack #+ (int(level) * 4)
        if self.preference != None: #Huh? Preference? Bet ya didn\'t know this existed.
            #Preference is if a person likes strength, or if that person is an idiot.
            if self.preference == 'strength' and self.name == 'Fredrick':
                self.attack *= 1.5
        self.defense = basedefense #+ (int(level) * 2)
        self.speed = basespeed #+ int(level)
        self.magic = basemagic #+ (int(level) * 4)
        if self.preference != None: # How can you be that much of a moron
            #Preference is if a person likes using physical or magical attacks.

            #Despite the ramblings, preference wasn't relevant in the end.
            #Working hard can only be SO helpful...
            
            if self.preference == 'magic' and self.name == 'Fredrick':
                self.magic *= 1.5
        self.Mdefense = basemdefense# + (int(level) * 2)
        self.spells = []
        self.luck = baseluck #+ (int(level))
        self.exp = 1337 # why be pointless when you can be elitely pointless
        self.block = False 
        self.basestats = {'health':basehealth, 'mp' : basemp,'attack':baseattack,
                          'defense':basedefense,'magic':basemagic,'mdefense':basemdefense,
                          'speed':basespeed,'luck':baseluck}
        self.zattack = None
        self.mattack = None
        self.cattack = None
        self.status = 'Normal' 
        self.color = color
        self.equippedweapon = None
        self.equippedarmor = None
        self.equippedspecial = None
        self.mode = 'magic'
        self.item = None
        if special:
            self.SPmeter = 0
        else:
            self.SPmeter = None
    def imagereset(self):
        if self.originalstatusboximage != 'None':
            self.statusboximage = copy.copy(self.originalstatusboximage)
        self.battlesprite = copy.copy(self.originalbattlesprite)
    def imageload(self):
        self.battlesprite = pygame.image.load(self.originalbattlesprite)
        if self.originalstatusboximage != 'None':
            self.statusboximage = pygame.image.load(self.originalstatusboximage)
    def stat_recalculate(self):
        affectedstats = []
        if self.equippedweapon != None:
            affectedstats.append(self.equippedweapon.statboost)
            print('found weapon')
        if self.equippedarmor != None:
            affectedstats.append(self.equippedarmor.statboost)
        print(len(affectedstats))
        print(affectedstats,'stats bonuses')
        attackbonus = 0
        defensebonus = 0
        speedbonus = 0
        magicbonus = 0
        luckbonus = 0
        print(affectedstats[0])
        print(affectedstats[0][0])
        print(affectedstats[0][0][0])
        for i in affectedstats[0]:
            print(i,'i')
            if i[0] == 'attack':
                attackbonus += i[1]
            if i[0] == 'defense':
                defensebonus += i[1]
            if i[0] == 'speed':
                speedbonus += i[1]
            if i[0] == 'magic':
                magicbonus += i[1]
            if i[0] == 'luck':
                luckbonus += i[1]
        print(attackbonus,defensebonus,speedbonus,magicbonus,luckbonus,'adsml')
        self.attack = (self.basestats['attack'] + attackbonus)
        self.defense = (self.basestats['defense'] + defensebonus)
        self.speed = (self.basestats['speed'] + speedbonus)
        self.magic = (self.basestats['magic'] + magicbonus)
        self.luck = (self.basestats['luck'] + luckbonus)
        #Who has put all of this work towards nothing?
        #Perhaps this is what could have been?
        #level = self.level
##        self.Mhealth = self.basestats['basehealth'] + int((level)*10)
##        self.Mmp = self.basestats['basemp'] + (int(level)*5)
##        self.attack = self.basestats['baseattack'] + (int(level)*4)
##        self.defense = self.basestats['basedefense'] + (int(level)*2)
##        self.magic = self.basestats['basemagic'] + (int(level)*4)
##        self.Mdefense = self.basestats['basemdefense'] + (int(level)*2)
##        self.speed = self.basestats['basespeed'] + int(level)
##        self.luck = self.basestats['baseluck'] + int(level)
##        #Wonder who did this?
        ##if self.preference == 'magic':
         ##   self.magic *= 1.5
        ##elif self.preference == 'strength':
          ##  self.attack *= 1.5
        

    def get_title(self, title):
        self.titles.append(title)
        self.current_title = title


class spmove:
    def __init__(self,name,function,desc1,desc2,desc3,desc4,basedamage,element=None):
        self.name = name
        self.function = function
        self.desc1 = desc1
        self.desc2 = desc2
        self.desc3 = desc3
        self.desc4 = desc4
        self.basedamage = basedamage
        self.element = element
        self.ismagic = False
        

    def use(self,player):
        if self.function == 'stepslice':
            player.stepslice()
        if self.function == 'quickslice':
            player.quickslice()
        if self.function == 'meteor':
            player.meteor()
        if self.function == 'None':
            pass
        if self.function == 'cleave':
            player.cleave()
        if self.function == 'salvation':
            player.salvation()
        
        
class spell:
    def __init__(self, name,desc1,desc2,desc3,desc4,basedamage, element,
                 mpcost, effect,alignment, specialeffect=None):
        self.name = name
        self.desc1 = desc1
        self.desc2 = desc2
        self.desc3 = desc3
        self.desc4 = desc4
        self.basedamage = basedamage
        self.element = element
        self.mpcost = mpcost
        self.effect = effect
        self.specialeffect = specialeffect
        self.alignment = alignment
        self.ismagic = True


    def use(self):
        pass
    def specials(spell):
        self.mpcost = None
        self.damage = player.attack * self.basedamage
##class ENEMY:
##    def __init__(self, name, health
##    #maybe later
##        self.resist = resist
        #lol defined elsewhere
#Fire, Lightning are Creation
#Ice, Ground are Destruction
holy = spell('Holy','Attack your enemies','with a beam of pure energy','Has a large radius.','Costs 25 mp',
 25, 'Light', 25,None,'creation','charge')
doubleholy = spell('Light Fusillade','Repeatedly press the button to','assail your enemies with light magic.',
'Requires laser to be equipped.','Costs 10 mp', 2,'None',5,None,'creation','projectile')
laser = spell('Gleam','Shoots a small beam of light','at your enemies.','Beginner\'s magic.','Costs 5 mp.',
1,'None',5,None,'creation','projectile')
chargelaser = spell('Ray','Charge to max power','to fire a burst of light.','Can be held indefinitely.','Costs 30 mp.'
,10,'Light',30,'Projection','Creation')
strengthen = spell('Strengthen','Allows a person to channel more energy','by adding some magic energy.',
'Feels weirdly energizing.','',1,'Power Enhancement',10,'creation',None)
pinnacle = spell('Pinnacle','Summons a powerful beam of energy','after a successful block.',
'Only activates on block.','Range:Circle (radius of 1)',75,'Light', 25,None,'creation','onespot')
devitalize = spell('Devitalize','Reduces your opponent\'s','ability to focus,',
'making them easier to hurt.','',1,'destruction',10,None,'destruction')
heal = spell('Heal','Restores minor wounds or injuries.','Basic healing magic.',
'','Costs 10 mp', 25,'Healing',10,None,'creation')
#MagicBooster = spell('Magic Mastery','Magic
#SwordBooster = spell('Sword Mastery'
slicer = spmove('Slice','stepslice','Slice with your sword.','Can do up to three','hits in a row.','Range: 1',50)
commandslice = spmove('Command Slice','commandslice','Use special inputs to',' use different moves.','Masters can make','great use of it...',50)
quickslice = spmove('Quick Slice','quickslice','Thrust forward with your sword.','Can do two hits in a row.','Range: 2','',30)
Noattack = spmove('None','None','There is no move equipped here.','well, technically there is, but...','','',0)
meteor = spmove('Meteors','meteor','Summon meteors to kill everything.','Charges faster than other moves.','Stronger if you\'re lucky...','',150)
death = spmove('Purify','purify','Instantly defeats your foe.','Makes SPmeter much more difficult to charge.','','','ALL')
chargeslice = spmove('Chargeslice','chargeslice','Charge up and slice','in front of yourself.','Makes meter charge differently.','Fiercely powerful at full charge.',10)
cleave = spmove('Cleave','cleave','Unleash a powerful slice','on a large area ahead of you.','Can finish off enemies whose health','is at 1/4 or less of maximum.',200)
SP_aura = spmove('Aura','auraburst','Your attack increases relative','to SP meter fullness.','Damage reduces your meter, however.','',0)
SP_trueaura = spmove('Emanation','auraburst','Your attack and speed increases relative','to SP meter fullness.','Damage still reduces your meter, however.','You can use full meter for an attack, too.',0)
Salvation = spmove('Salvation','salvation','Heat Riser, Debilitate, Autolife.','And of course, Salvation.','Ultimate Light Move.','Switches to backup spmove after use.',100)
Fredrick = Player('Fredrick', 1, 'battlesprites/Fredricktruebattle.png','Fstatusboxsprite.png',
                  100, 35,1,1,1,1,1,1, [], (0,113,113))
OriginalFredrick = Player('OFredrick', 1,'battlesprites/ofredrickbattlesprite.png','battlesprites/HimBattleSprite.gif',
                  1000, 350,1,1,1,1,1,1, [], (0,60,60),True)
Fredrick.spells.append(holy)
Fredrick.zattack = slicer
Fredrick.xattack = laser
Fredrick.cattack = heal
Fredrick.spattack = Salvation
Fredrick.mode = 'sword'
#atk def mag mdef spd lck
GrayCloak = Player('Gray Cloak', 1, 'battlesprites/HimBattleSprite.gif','None',1500,100,3,3,3,3,3,3,None,(127,127,127))
DarkNyu = Player('Dark Nyu',1,'battlesprites/dnyubattlesprite.gif','None',1000,25,2,2,2,2,2,2,None,(100,100,100))
BlackCloak = Player('Black Cloak',1,'BlackCloakBattleSprite.gif','None',2500,50,4,4,1,1,3,3,None,(50,50,50))
Dark = Player('Dark', 1, 'battlesprites/DarkBattleSprite.gif','None',1500,100,5,5,0,0,5,0,None,(0,0,0))
Light = Player('Light', 1, 'LightBattleSprite.gif','None',1500,100,0,0,5,5,5,0,None,(127,127,127))
Genmu = Player('Genmu',1,'GenmuBattleSprite.png','genmustatusboxsprite.png',4000,10,8,8,2,2,5,10,None,(100,100,100))
Genmu.get_title(Genmu_Default)
Percy = Player('Percy',1,'GenmuBattleSprite.png','genmustatusboxsprite.png',3000,200,4,4,7,7,2,7,None,(200,200,200))
#he wants to be special???
Percy.get_title(Percy_Default)
MagicDog = Player('MagicDog',1,'magicdog.png','genmustatusboxsprite.png',2000,500,1,1,2,2,3,2,None,(100,100,100))
WizDog = Player('WizDog',1,'magicdog.png','genmustatusboxsprite.png',2500,500,2,2,3,3,4,3,None,(125,125,125))
MagiNyu = Player('MagiNyu',1,'MagiNyubattlesprite.gif','genmustatusboxsprite.png',1250,250,1,1,2,2,3,5,None,(70,70,70))
SwordNyu = Player('SwordNyu',1,'SwordNyubattlesprite.gif','genmustatusboxsprite.png',1500,15,2,2,1,1,3,5,None,(100,100,100))
FallenWarrior = Player('FallenWarrior',1,'FallenWarriorbattlesprite.gif','genmustatusboxsprite.png',2000,100,2,2,2,2,2,2,None,(150,150,150))
GenmuBond = bond('Genmu',['Idiot Swordsman','You have become closer ultimately due to swords.'],'genmustatusboxsprite.png')
OfredrickBond = bond('OFredrick',['Indignant Being','What is going on with him?'],'Gstatusboxsprite.png')
GrayCloakBond = bond('Gray',['Sarcastic Ex-hero','You understand his motivations.'],'graystatusboxsprite.png')
#(self,name,description,image,character)
#NyuBond = bond
##Percy = Player('Percy',1,'','percystatusboxsprite.png'
##Lucy = Player('Lucy',1,'','lucystatusboxsprite.png',
##Lorei = Player('Lorei',1,'','loreistatusboxsprite.png'
