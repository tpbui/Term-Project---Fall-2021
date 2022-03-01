#Tra Bui - 15112 TP03
#Due date: November 26nd, 2021

import pygame
import os
import random, string
import math
import numpy as np
import socket

############################ CLASS DECLARATION #################################

################################################################################

class App(object):
    '''I creat a class App and create an instance app = App() to define variables
        outside the class. CA Huda Baig has given me this idea to start with'''
    
    def __init__(self, width = 1100, height = 700, title = "Space Typing Game"):
        self.width = width
        self.height = height
        self.title = title

class Word(object):
    '''This is a class that controls states relate to word including
        randomly generating, and word comparing'''
    
    def __init__(self):
        #new word that is going to be created 
        self.newWord = ""
        
        #a list that keep track of all words appear on the screen
        self.wordList = []
        
        #a dictionary that match the word to its starting letter
        #to know which word the player is aiming for
        self.startingLetter = dict()
        
        #word that is being targeted
        self.original = ""
        
        #dynamic version of targeted word to use in comparing functions
        self.current = ""
        
        #index of current word in wordList
        self.currentIndex = None
        
        #range of targeted word that is being colored
        self.colored = ""
        
    def __repr__(self):
        return self.newWord
    
    def __eq__(self, other):
        return isinstance(other, list) and self.wordList == other
    
    def randomWord(self):
        #use random twice in this functions to:
        #(1) decide which word pool (easy, medium, hard) to look at
        #(2) generate random word from that pool
        
        #decide the ratio of easy over hard words
        #the ratio will change based on the stage (level) of the game
        lst = [1,2,3]
        dif = np.random.choice(lst, 1, p = app.prob)
        
        #generate random word
        if dif == 1:
            self.newWord = random.choice(easyWord)
        if dif == 2:
            self.newWord = random.choice(mediumWord)
        if dif == 3:
            self.newWord = random.choice(hardWord)
        
    def createWord(self):
        """Create new word so that each word in the word list has different
            starting letter."""
        
        #maximum number of words appear
        #on the screen is 26
        if len(self.wordList) < 26:

            #generate random word
            self.randomWord()
            
            #make sure that every word has different starting letter
            #by checking whether the first letter is in the dictionary or not
            if len(self.wordList) != 0:   
                while self.newWord[0] in list(self.startingLetter.values()):
                    self.randomWord()
           
            #add new word to current word list
            self.wordList.append(self.newWord)
            
            #update the dictionary based on current word list
            self.startingLetter = {}
            
            for word in self.wordList:
                self.startingLetter[word] = word[0]
                  
    def checkFirst(self, app):
        #check if the typer is aiming for any of the word
        #that appears on the screen
        
        if app.startGame == True and app.startWord == False:
            #if in the player's type list
            #there are any letter that matches the first letter
            #of existing words in word list,
            #mark that letter
            for i in range(len(app.typeList)):
                if app.typeList[i] in list(self.startingLetter.values()):
                    app.firstLetter = app.typeList[i]
                    app.startWord = True
                    self.original = self.getKey(app)    
            return False
    
    def getKey(self, app):
        #from the first letter that the player is aiming for
        #return the word that has that first letter inside the word dictionary
        
        if app.startGame == True:
            for key, value in self.startingLetter.items():
                if value == app.firstLetter:
                    self.current = key
                    return self.current
                
    def compare(self, app):
        '''This function is only called when the user pressed a new key
        (conditions in the main loop). It will compare user's latest key
        with existing character in the targeted word'''
        
        if app.startGame == True:
            #when the user successfully targets a word
            if len(self.current) > 0:
                #start comparing characters
                
                #if the typed characters match the current letter
                if app.typeList[-1] == self.current[0]:
                    
                    #the current letter will be shifted to the right by one
                    self.current = self.current[1:]
                    
                    #bullets will be fired
                    app.isFired = True
                
                #if the typed character and current character are not matching
                else:
                    #counted as a mistake
                    app.wrong += 1
            
            #keep checking until the word is being typed completely
                    
            #if the word is finished --> return
            if len(self.current) == 0:
                return True
            
            #if the word is not yet finished --> mark the position of current
            #letter to use for coloring characters
            if len(self.current) != 0:
                #because Python sometimes do not distinguish between
                #"1" and "True" or "0" and False
                #I tried to return the results in this form
                return False, len(self.current)
        
    def compareWord(self, app):
        '''This function takes all the comparison and processing from previous functions
        and decides the result'''
        
        #once detect a word
        if app.startGame == True and app.startWord == True:
            #determine the word index in the whole word list
            self.currentIndex = self.wordList.index(self.original)

            #if there is a bullet created
            if app.isFired == True:
                #determine the position of targeted asteroids and shoot
                pos = app.asteroid[self.currentIndex]
                shoot = Bullet(pos.x, pos.y)
                app.bullets.append(shoot)
                
                #add sound effect for bullet
                bulletSound.play()
                
                if type(app.asteroid[self.currentIndex]) == BadAsteroid:
                    app.typeList = []
                    app.stringTypeList = ""
                    
                    #add explosion effect
                    explosion = BigExplosion(pos.x, pos.y, "bad")
                    app.explosions.append(explosion)
                    
                    #and sound effect
                    explodeLarge.play()
                    
                    #get rid of the asteroid, the word in related structure
                    app.asteroid.pop(self.currentIndex)
                    self.wordList.remove(self.original)
                    del computerWord.startingLetter[self.original]
                    
                    #there is no word being targeted at the moment the player finishes
                    app.startWord = False
                    
                #return the normal state
                app.isFired = False
                
            #If there are still some words need to be typed
            #Color the words that have been typed
            if app.result != True:
                self.colored = self.original[: len(self.original) - app.result[1]]
                return False
            
            #If the player finish one eligible word
            if app.result == True and (self.original in self.wordList):    
                #return the values back to empty 
                app.typeList = []
                app.stringTypeList = ""
                
                #determine the position of the asteroid carrying that word
                pos = app.asteroid[self.currentIndex]
                
                #add explosion effect
                explosion = Explosion(pos.x, pos.y)
                app.explosions.append(explosion)
                
                #and sound effect
                explodeSmall.play()
                
                #get rid of the asteroid, the word in related structure
                app.asteroid.pop(self.currentIndex)
                self.wordList.remove(self.original)
                del computerWord.startingLetter[self.original]
                
                #there is no word being targeted at the moment the player finishes
                app.startWord = False

            return True

class Spaceship(object):
    '''Spaceship class: The spaceship will have its fixed (x,y) position'''
    
    def __init__(self):
        self.content = pygame.transform.scale(pygame.image.load(
                os.path.join("Items", 'spaceship2.png')), (200, 150))
        self.x = app.width / 2
        self.y = app.height - 200
    
    def draw(self, screen):
        screen.blit(self.content, (self.x - 200 / 2, self.y))

class Bullet(Spaceship):
    '''Spaceship subclass: Bullet. The bullets will inherit the starting point
    from its parent class Spaceship, and will be modified to target asteroids'''
    
    def __init__(self, tx, ty):
        #inherit the starting point
        super().__init__()
        
        #position of target
        self.targetX = tx
        self.targetY = ty
        
        self.content = pygame.transform.scale(pygame.image.load(
                os.path.join("Items", 'bullet.png')), (30, 30))
        
        #create index for tasks that only need to complete once in the while loop
        self.count = 0
    
    def getAngle(self):
        #Calculate the angle to shoot the bullet
        line1 = [(app.width / 2, app.height - 200),(self.targetX, self.targetY)]
        a = line1[0][0] - line1[1][0]
        b = line1[0][1] - line1[1][1]
        
        #the original direction of this image is to the right
        #that's why I need to + 90 in the formula
        self.angle = 90 + math.degrees(math.atan(a/b))
    
    def changeAngle(self):
        #after getting the angle
        self.getAngle()

        #rotate the bullet image based on the angle
        if self.count < 1:
            self.count += 1
            self.content = pygame.transform.rotate(self.content, self.angle)
        
        #if the bullet is still shooting
        #add velocity to it
        if self.y > self.targetY:
            self.y -= (app.height - 150 - self.targetY) / 5
            self.x -= (app.width / 2 - self.targetX) / 5
        
        #once the bullet hits the asteroid
        #remove the bullet from shooiting list
        if self.y <= self.targetY:
            app.bullets.remove(self)
        
    #draw all the changes onto screen
    def draw(self, app, screen):
        screen.blit(self.content, (self.x, self.y))
            
class Asteroid(object):
    '''Citation: I create this Asteroid class based on the 15-112 Demo Code
    Link: https://github.com/CMU15-112/lecture_demos_qatar/blob/F21/week10/square_dot_game.py'''
    
    '''An asteroid will have position (x,y), velocity (dx,dy), size (sizeX, sizeY)
    to start with'''
    
    def __init__(self, x, y, dx, dy, sizeX = 30, sizeY = 30):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.dx = dx
        self.dy = dy
        
        #resize the image to fit the screen
        self.content = pygame.transform.scale(pygame.image.load(
                os.path.join("Items", 'asteroid1.png')), (self.sizeX, self.sizeY))
        
    def __repr__(self):
        return f"A({int(self.x)}, {int(self.y)})"
    
    def draw(self, app, screen):
        screen.blit(self.content, (self.x, self.y))

class BadAsteroid(Asteroid):
    def __init__(self, x, y, dx, dy, sizeX = 30, sizeY = 30):
        super().__init__(x, y, dx, dy, sizeX = 30, sizeY = 30)
        
        self.content = pygame.transform.scale(pygame.image.load(
                os.path.join("Items", 'red_asteroid.png')), (self.sizeX, self.sizeY))

class Explosion(object):
    '''Class Explosion: Control the states of explosions occur in the game'''
    
    def __init__(self, x, y):
        #add all the states of the explosion from the image source
        self.states = []
        for i in range(5, 21):
            img = pygame.image.load(os.path.join("Items/explosion", f'{i}.png'))
            img = pygame.transform.scale(img, (50, 50))
            self.states.append(img)
        
        #get the size of the image
        self.width = self.states[0].get_width()
        self.height = self.states[0].get_height()
        
        #an index that will be looped on
        #this index represents the state of the explosion
        self.index = 0
        self.state = self.states[self.index]
        
        #postion that the explosion occurs
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Explosion({self.x}, {self.y})"
    
    def changeState(self):
        #once their is an explosion
        #continuously change the image of the explosion
        if self.index < len(self.states) - 1:
            self.index += 1
            self.state = self.states[self.index]
        
        #when reach the end
        #remove explosion from the list
        if self.index >= len(self.states) - 1:
            app.explosions.remove(self)
    
    def draw(self, screen):
        screen.blit(self.state, (self.x, self.y))

class BigExplosion(Explosion):
    '''A subclass of explosion. Distinguish between explosion for word completion
    and explosion for hitting the spaceship. Change the size of the explosion'''
    
    def __init__(self, x, y, p):
        #inherit all basic properties from parent class
        super().__init__(x, y)
        
        self.states = []
        for i in range(5, 21):
            img = pygame.image.load(os.path.join("Items/explosion", f'{i}.png'))
            
            #make the size of each explosion larger
            img = pygame.transform.scale(img, (100, 100))
            self.states.append(img)
        
        self.prop = p
    
    def draw(self, screen):
        screen.blit(self.state, (self.x - self.width / 2 , self.y - self.height / 2))
        
class BlackHole(object):
    def __init__(self):
        img = pygame.image.load(os.path.join("Items", 'blackhole.png'))
        img = pygame.transform.scale(img, (200, 200))
        self.content = img
        self.x = app.width / 2
        self.y = 30 + 100
    
    def draw(self, screen):
        screen.blit(self.content, (self.x - self.content.get_width() / 2,
                                   self.y - self.content.get_height() / 2))


############################ DECLARE INIT VARIABLES ############################
        
################################################################################
        
#create an instance of app and computerWord
app = App()
computerWord = Word()

#start the program
pygame.init()
app.running = True

#measure and keep track of the time in the game main loop
app.clock = pygame.time.Clock()

#Create game screen
screen = pygame.display.set_mode((app.width, app.height))
pygame.display.set_caption(app.title)

#Word list from computer
f = open("Word_List/easy.txt", "rt")
a = f.read()
easyWord = a.split("\n")
easyWord = easyWord[:-1]

f = open("Word_List/medium.txt", "rt")
a = f.read()
mediumWord = a.split("\n")
mediumWord = mediumWord[:-1]

f = open("Word_List/hard.txt", "rt")
a = f.read()
hardWord = a.split("\n")
hardWord = hardWord[:-1]

#Image for background and objects
backgroundImage = pygame.transform.scale(pygame.image.load(
                os.path.join("Items", 'space.png')), (app.width, app.height))

heartImg = pygame.transform.scale(pygame.image.load(
                os.path.join("Items", 'heart2.png')), (30, 30))

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GRAY = (125,125,125)
BEIGE = (249, 228, 183)

#text design and font
app.menuHeaderFont = pygame.font.Font(os.path.join('Items','PixelEmulator-xq08.ttf'), 80)
app.menuChoiceFont = pygame.font.Font(os.path.join('Items','PixelEmulator-xq08.ttf'), 25)
app.margin = 3
    
#Sound effect and music
explodeSmall = pygame.mixer.Sound(os.path.join('Sound_Effect', 'explodeSmall.wav'))
explodeLarge = pygame.mixer.Sound(os.path.join('Sound_Effect', 'explodeLarge.wav'))
bulletSound = pygame.mixer.Sound(os.path.join('Sound_Effect', 'bulletSound.wav'))

#Leaderboard
app.leaderboard = ["user1: 0", "user2: 0" , "user3: 0"]


##################### GAME BEGINNING FUNCTIONS AND MODELS ######################

################################################################################

def connectServer(app):
    '''This server is created by Professor Saquib (CMUQ). I have gained his
    permisison to use the server to support my Term Project'''
    
    '''First connect to the server to update the leaderboard'''
    
    '''I have created this function based on 15112 Demo Note for networking.
    Link: https://github.com/CMU15-112/lecture_demos_qatar/blob/F21/week11/echo_client.py '''
    
    HOST = '86.36.42.136'  # The server's hostname or IP address
    PORT = 15112        # The port used by the server
     
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    #get the stored information form the server
    client_socket.sendall("get\n".encode())
    response = client_socket.recv(1024)
    
    #if the server is used for the first time (empty information)
    #then format the return structure of the server
    if len(response.decode()[:-1]) == 0:
        message = "update:" + "user1: 0,user2: 0,user3: 0\n"
        client_socket.sendall(message.encode())
    
    #for the next time
    #update the leaderboard based on current server
    if len(response.decode()[:-1]) != 0:
        received = response.decode()[:-1]
        app.leaderboard = received.split(",")

def initGame(app, computerWord):
    '''This function stores the original state of important variables of the game.
    Whenever the player is not playing, all these values will reset'''
    
    #first screen
    app.currentScreen = "menuScreen"
    
    #starting condition of the typer
    computerWord.__init__()
    
    #time indicator
    app.blip = 0
    app.timer = 0
    app.interval = 60
    
    #game state
    app.gameMode = None
    app.pause = False

    app.startGame = False
    app.gameOver = False
    app.result = None
    
    #word state
    app.startWord = False
    app.firstLetter = None

    #User's type list and word count
    app.typeList = []
    app.stringTypeList = ""
    app.specialWord = ""

    #Asteroid list
    app.asteroid = []
    app.isExplode = True
    app.explosions = []

    #Bullet
    app.isFired = False
    app.bullets = []

    #Blackhole
    app.blackHole = BlackHole()

    #Point counter
    app.wrong = 0
    app.charCount = 0
    app.grossWPM = 0
    app.accuracy = 0
    app.avgWPM = 0
    app.health = 400
    app.score = 0
    
    #Levels and difficulty
    app.stage = 1
    app.prob = [0.90,0.10,0.0]

    #extra position variables for drawing profile screen
    app.profilePos = []
    app.leaderboardPos = []
    app.userName = ""
    app.waitForLogin = True
    
    #call the function to connect to server
    connectServer(app)

initGame(app, computerWord)
        
########################### GAME CONTROLLER ####################################

################################################################################

def createTextMenu(app):
    #Helper function to generate text for the menu screen
    if app.currentScreen == "menuScreen":
        
        #game header
        app.gameHeader1 = app.menuHeaderFont.render("SPACE", True, WHITE)
        app.gameHeader2 = app.menuHeaderFont.render("TYPING", True, WHITE)
        
        #four buttons
        app.button1 = app.menuChoiceFont.render("START", True, WHITE)
        app.button2 = app.menuChoiceFont.render("MY PROFILE", True, WHITE)
        app.button3 = app.menuChoiceFont.render("LEADERBOARD", True, WHITE)
            
        app.boxWidth1 = (max(app.button1.get_width(), app.button2.get_width(),
                             app.button3.get_width()) * 0.7)
            
        app.boxHeight = (app.button1.get_height() / 2)
        
        app.textWC1 = app.width/ 2 - app.boxWidth1
        app.textHC1 = app.height * 3 / 5 - app.boxHeight
    
#Helper function to generate text for the game mode screen
def createTextGameModes(app):
    if app.currentScreen == "gameModeScreen":
        
        app.mode1 = app.menuChoiceFont.render("Normal mode", True, WHITE )
        app.mode2 = app.menuChoiceFont.render("Endless mode", True, WHITE)
        app.mode3 = app.menuChoiceFont.render("Python mode", True, WHITE)
            
        app.boxWidth2 = max(app.mode1.get_width(), app.mode2.get_width(),
                            app.mode3.get_width()) * 0.7
        
        app.boxHeight = app.mode1.get_height() / 2
        
        app.textWC2 = app.width/ 2 - app.boxWidth2
        app.textHC2 = app.height * 2 / 5 - app.boxHeight
 
def createProfile(app):
    '''This function creates/updates user profile when they log in.'''
    
    #If there profile exists on the local computer, keep updating information to the file.
    #If it is a new player, create a file with the player's username
    f = open(f'Users/{app.userName}.txt', 'a')
    f.close()
    
    #update the player's profile
    with open(f"Users/{app.userName}.txt", "r") as f:
        app.myProfile = f.read()
        
        lines = app.myProfile.split("\n")
        app.myProfileList = []
        
        for line in lines:
            b = line.split(" ")
            app.myProfileList.append(b)
            
        f.close()
    
    #only choose the player most recents score
    app.myProfileList = app.myProfileList[-11:-1]
        
def createMyRecord(app):
    #function that calculate the position to put text in on MyProfile Screen
    L = ["No.", "Total Keys", "Mistakes", "WPM", "Accuracy", "Time"]
    startingX = 0
        
    for i in range(len(L)):
        s = app.menuChoiceFont.render(L[i], True, WHITE)
        #the starting position for the first row
        pos =  (50 + startingX + 50 * i, 60)
        #add white space between words
        startingX += s.get_width()
        
        #mark the position
        app.profilePos.append(pos)

def createleaderboardPos(app):
    L = ["Rank", "Username", "Score"]
    startingX = 0
        
    for i in range(len(L)):
        s = app.menuChoiceFont.render(L[i], True, WHITE)
        pos =  (300 + startingX + 100 * i, 100)
        startingX += s.get_width()
        app.leaderboardPos.append(pos)

def keyPressed(app, event):
    '''#Function that takes user's input from keyboard and decide the output'''
    
    #If during the game play player presses "TAB", then game is Paused
    if event.key == 9:
        if app.startGame == True:
            app.pause = True
            app.startGame = False
    
    #If game is paused and player presses "2" --> continue playing
    if event.unicode == "2":
        if app.pause == True and app.startGame == False:
            app.pause = False
            app.startGame = True
            
    #if player presses "1"        
    if event.unicode == "1":
        #if it is not during the game
        if app.startGame == False:
            #when the game is finished
            if app.gameOver == True:
                #update player's personal score
                with open(f"Users/{app.userName}.txt", "a") as f:
                    f.write(app.myProfile)
                    f.close()
                    
                controlLeaderBoard(app)
                
                #reset values and return to menu
                initGame(app, computerWord)
            
            #if it is during the game is Paused
            #then return to menu
            #this means that if the play press "1" before pressing "TAB",
            #the player won't return
            elif app.currentScreen == "startGameScreen":
                if app.pause == True:
                    initGame(app, computerWord)
            else:
                initGame(app, computerWord)
                               
    else:
        #a dictionary that maps key (str) to their code (int)
        #input characters will be limited to letters, numbers, punctuation
        #and white space, backspace, and bit mark
        d = {}
        isModsPressed = pygame.key.get_mods()
        
        for char in string.ascii_lowercase + string.punctuation + string.digits + " " + "\r" + '\b':
            d[char] = pygame.key.key_code(char)
        
        #detemine which key is pressed
        if pygame.key.get_pressed()[event.key] == True and event.key in list(d.values()):
            #during the login
            if app.currentScreen == "menuScreen" and app.waitForLogin == True:
                #if player presses "ENTER"
                #then logged in
                if event.key == 13:
                    app.waitForLogin = False
                    createProfile(app)
                
                #if player presses backspace
                #delete one character from the player's name
                elif event.key == 8:
                    app.userName = app.userName[:-1] + ""
                
                #maxium length for name is 20
                elif len(app.userName) <= 20:
                    app.userName += event.unicode
            
            #during the game
            elif app.currentScreen == "startGameScreen" and app.startGame == True:
                #type list will be updated
                #counted towards number of keys typed
                app.typeList.append(event.unicode)
                app.charCount += 1
        
    #make type list into a string to print this on screen more easily
    app.stringTypeList = "".join(app.typeList)

def mousePressed(app, event):
    '''Function that takes input from player's mouse and return output'''
    
    #check if the mouse is being pressed
    isMousePressed = pygame.mouse.get_pressed()
    
    #get mouse tuple (x,y) position
    mouseKey = pygame.mouse.get_pos()
    
    #if "left" mouse is not being pressed --> then do nothing
    if isMousePressed[0] == False:
        return
    
    #based on the mouse position
    #decide which button on the menu and game mode screen is pressed
    #and move to the next screen
    if app.currentScreen == "menuScreen" and app.waitForLogin == False:
        if (app.textWC1 <= mouseKey[0] <= app.textWC1 + app.boxWidth1 * 2) and \
            (app.textHC1 <= mouseKey[1] <= app.textHC1 + app.boxHeight * 2):
            
            app.currentScreen = "gameModeScreen"
               
        if (app.textWC1 <= mouseKey[0] <= app.textWC1 + app.boxWidth1 * 2) and \
            app.textHC1 + 70 <= mouseKey[1] <= app.textHC1 + app.boxHeight * 2 + 70:
            
            app.currentScreen = "myProfileScreen"
        
        if (app.textWC1 <= mouseKey[0] <= app.textWC1 + app.boxWidth1 * 2) and \
            app.textHC1 + 140 <= mouseKey[1] <= app.textHC1 + app.boxHeight * 2 + 140:
            
            app.currentScreen = "leaderboardScreen"
        
    elif app.currentScreen == "gameModeScreen":
        if (app.textWC2 <= mouseKey[0] <= app.textWC2 + app.boxWidth2 * 2) and \
            (app.textHC2 - 70 <= mouseKey[1] <= app.textHC2 + app.boxHeight * 2 - 70):
            
            app.gameMode = "normal"
        
        if app.gameMode != None:
            app.startGame = True
            app.currentScreen = "startGameScreen"
   
def controlLeaderBoard(app):
    '''This function gets the result from the server and update the player's
    current score to the server'''
    
    HOST = '86.36.42.136'  # The server's hostname or IP address
    PORT = 15112        # The port used by the server
     
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
#     resetServer(app)
    
    client_socket.sendall("get\n".encode())
    response = client_socket.recv(1024)
    
    #the last character of response is "\n" --> formating
    if len(response.decode()[:-1]) == 0:
        message = "update:" + "user1: 0,user2: 0,user3: 0\n"
        client_socket.sendall(message.encode())
    
    if len(response.decode()[:-1]) != 0:
        received = response.decode()[:-1]
        app.leaderboard = received.split(",")
    
    #compare player's score with users in the leaderboard
    compareScore(app)
    
    #determine new ranks
    firstPlace = app.leaderboard[0]
    secondPlace = app.leaderboard[1]
    thirdPlace = app.leaderboard[2]
    
    #update to the server
    message = "update:" + f"{firstPlace},{secondPlace},{thirdPlace}"
    client_socket.sendall(message.encode())
    received = response.decode()[:-1]

def compareScore(app):
    '''Compare the player current score to user in the leaderboard'''
    
    #Suppose the player is not in TOP 3
    currentIndex = 3
    
    #formatting
    currentPlayer = f"{app.userName}: " + f"{app.score}"
    info = currentPlayer.split(':')
    
    #get the info from the current leaderboard
    firstPlayer = app.leaderboard[0]
    secondPlayer = app.leaderboard[1]
    thirdPlayer = app.leaderboard[2]
    
    infoFirst = firstPlayer.split(':')
    infoSecond = secondPlayer.split(':')
    infoThird = thirdPlayer.split(':')
    
    #compare the player's score
    #if the current player score is higher or equal to any of the player
    #then the old achievements will be replaced
    
    if int(info[1]) >= int(infoFirst[1]):
        currentIndex = 0
    elif int(info[1]) >= int(infoSecond[1]):
        currentIndex = 1
    elif int(info[1]) >= int(infoThird[1]):
        currentIndex = 2
    else:
        currentIndex = 3
    
    #extract only the top three players from to put on the leaderboard
    if currentIndex != 3:
        app.leaderboard.insert(currentIndex, currentPlayer)
        app.leaderboard = app.leaderboard[:3]
             
def createAsteroid(app, computerWord):
    #create the word that will be carried
    computerWord.createWord()
    
    #and new asteroids that carry the word
    x = random.choice([app.width / 2 - 50, app.width / 2, app.width / 2 + 50])
    y = 150
    dx = 0.5
    dy = 0.5
    app.asteroid.append(Asteroid(x,y,dx,dy))

def createAsteroidLine(app, computerWord):
    #create an asteroid line
    pos = [app.width / 2 - 50, app.width / 2, app.width / 2 + 50]
    for i in range(3):
        computerWord.createWord()
        app.asteroid.append(Asteroid(pos[i], 150, 0.5, 0.5))

def createBadAsteroid(app, computerWord):
    computerWord.createWord()
    
    #and new asteroids that carry the word
    x = random.choice([app.width / 2 - 50, app.width / 2, app.width / 2 + 50])
    y = 150
    dx = 0.5
    dy = 0.5
    app.asteroid.append(BadAsteroid(x,y,dx,dy))
    
def createGameElement(app, computerWord):
    '''Take in the player's input and time to control the movement of game elements'''
    
    if app.startGame == True:
        if app.charCount > 0:
            #calculate player's statistics
            app.grossWPM = (app.charCount / 5) / (app.blip / 40) * 60
            app.accuracy = (1 - app.wrong / app.charCount)
            app.avgWPM = int(app.grossWPM * app.accuracy)
            
            #the time between asteroid generator
            #is based on the player's WPM
            #and it is shortened as the player types faster
            if app.avgWPM < 10:
                app.interval == 60
            
            elif app.avgWPM < 20:
                app.interval == 30
                
            elif app.avgWPM < 30:
                app.interval == 20
                
            elif app.avgWPM < 40:
                app.interval == 15
                
            else:
                app.interval == 10
        
        #after a certain amount of time
        #create an asteroid line to generate more words on the screen
        if app.blip % (10 * app.interval) == 0 and len(computerWord.wordList) < 22:
            createAsteroidLine(app, computerWord)
        
        elif app.blip % (8 * app.interval) == 0 and len(computerWord.wordList) < 26:
            createBadAsteroid(app, computerWord)
            
        #else, only create one at a time
        elif app.blip % (app.interval) == 0 and len(computerWord.wordList) < 26:
            createAsteroid(app, computerWord)
        
        #this is equivalent to one second has passed
        if app.blip % 40 == 0:
            app.timer += 1
            
def controlAsteroid(app, computerWord):
    if app.startGame == True:
        #change the asteroids position as they move
        for item in app.asteroid[:]:

            if app.avgWPM > 0:
                item.dx = 1.5 * app.avgWPM / 40
                item.dy = 1.5 * app.avgWPM / 40
            
            if item.dx <= 0.5 or item.dy <= 0.5:
                item.dx = 0.5
                item.dy = 0.5
               
            if item.x == app.width / 2:
                item.y += item.dy
                
            elif item.x < app.width / 2:
                item.x -= item.dx * 0.65
                item.y += item.dy 
                
            else:
                item.x += item.dx * 0.35
                item.y += item.dy 
            
            # if the asteroid reaches the end of the screen
            if item.y > app.height - 225:
                index = app.asteroid.index(item)
            
                #remove the word on that asteroid from the word list
                deletedWord = computerWord.wordList[index]
                
                computerWord.wordList.pop(index)
                del computerWord.startingLetter[deletedWord]
                    
                #Explosion will be bigger
                
                if type(item) == Asteroid:
                    explosion = BigExplosion(item.x, item.y, "bad")
                    app.explosions.append(explosion)
                    explodeLarge.play()
                    
                if type(item) == BadAsteroid:
                    explosion = BigExplosion(item.x, item.y, "good")
                    app.explosions.append(explosion)
                    explodeLarge.play()

                #remove the asteroid 
                app.asteroid.remove(item)
                
                #if the player has not finished the word
                #but the asteroid disappears
                #reset the player's type list
                if deletedWord[0] == app.firstLetter:
                    app.typeList = []
                    app.stringTypeList = ""
                    app.startWord = False

def controlBullet(app):
    #change bullet's angle
    for item in app.bullets:
        item.changeAngle()

def calculateHealth(app):
    #calculate player's health
    #health is deducted every time the asteroid hits the spaceship
    
    for item in app.explosions:
        if type(item) == BigExplosion and item.prop == "bad" and item.index == 1:
            damage = 25
            app.health = (app.health - damage)
    
    #if health < 0 --> game over
    if app.health <= 0:
        app.gameOver = True
        app.startGame = False

def controlLevel(app, computerWord):
    '''This functions control the level of the game (including the word difficulty)
    based on the number of correct keys that the user has pressed'''
    
    if app.startGame == True:
        if app.gameMode == "normal":
            num = app.charCount - app.wrong
            if num < 50:
                app.stage = 1
                #change the ratio of words based on level
                app.prob = [0.90, 0.10, 0.0]
            elif num < 100:
                app.stage = 2
                app.prob = [0.75, 0.25, 0.0]
            elif num < 150:
                app.stage = 3
                app.prob = [0.60, 0.25, 0.15]
            elif num < 200:
                app.stage = 4
                app.prob = [0.45, 0.30, 0.25]
            elif num < 300:
                app.stage = 5
                app.prob = [0.30, 0.45, 0.25]
            elif num < 400:
                app.stage = 6
                app.prob = [0.20, 0.50, 0.30]
            elif num < 500:
                app.stage = 7
                app.prob = [0.10, 0.60, 0.30]
            elif num < 600:
                app.stage = 8
                app.prob = [0.10, 0.55, 0.35]
            else:
                #once finish all levels --> win!
                app.gameOver = True
                app.startGame = False

        
################################ GAME VIEW #####################################
        
################################################################################
        
def drawMenuScreen(app, screen):
    #Draw starting menu screen
    if app.currentScreen == "menuScreen":
        
        #set space image as background image
        screen.blit(backgroundImage, (0, 0))
        
        for i in range(3):
        #draw buttons: the last layer is white and the upper layer is gray
            pygame.draw.rect(screen, WHITE, (app.textWC1 - app.margin,
                                             app.textHC1 - app.margin + 70 * i,
                                             app.boxWidth1 * 2 + 2 * app.margin,
                                             app.boxHeight * 2.3 + 2 * app.margin))
            
            pygame.draw.rect(screen, GRAY, (app.textWC1, app.textHC1 + 70 * i,
                                                 app.boxWidth1 * 2, app.boxHeight * 2.3))
        
        #draw game header text
        screen.blit(app.gameHeader1, (app.width / 2 - app.gameHeader1.get_width() / 2,
                            app.height * 1 / 4 - app.gameHeader1.get_height() / 2))
        
        screen.blit(app.gameHeader2, (app.width / 2 - app.gameHeader2.get_width() / 2,
                            app.height * 1 / 4 + 80 - app.gameHeader2.get_height() / 2))
        
        #draw text on top of the buttons
        screen.blit(app.button1, (app.width / 2 - app.button1.get_width() / 2,
                            app.height * 3 / 5 - app.button1.get_height() / 2))
        
        screen.blit(app.button2, (app.width / 2 - app.button2.get_width() / 2,
                            app.height * 3 / 5 + 70 - app.button2.get_height() / 2))
        
        screen.blit(app.button3, (app.width / 2 - app.button3.get_width() / 2,
                            app.height * 3 / 5 + 140 - app.button3.get_height() / 2))

def drawUserBox(app,screen):
    #Draw User log in box
    if app.currentScreen == "menuScreen" and app.waitForLogin == True:
        pos1 = (50,50,300,25)
        pos2 = (50,75,300,100)
        
        pygame.draw.rect(screen, GRAY, pos1)
        pygame.draw.rect(screen, WHITE, pos2)
        
        pygame.draw.rect(screen, GRAY, pygame.Rect((pos2[0] + pos2[2]) / 2 - 10,
                                            pos2[1] + 10, pos2[2] / 2 + 10, 30),  2)

        wordFont = pygame.font.SysFont('Helvetica', 16)
        text1 = wordFont.render("Login Window", True, BLACK)
        text2 = wordFont.render("User name: ", True, BLACK)
        text3 = wordFont.render("Press Enter to Log in", True, BLACK)
        name = wordFont.render(app.userName, True, BLACK)
        
        screen.blit(text1, (pos1[0] + pos1[2] / 2 - text1.get_width() / 2,
                            pos1[1] + pos1[3] / 2 - text1.get_height() / 2))
        
        screen.blit(text2, (pos2[0] + 20, pos2[1] + 20))
        
        screen.blit(text3, (pos2[0] + pos2[2] / 2 - text3.get_width() / 2,
                            pos2[1] + 75 - text3.get_height() / 2))
        
        screen.blit(name, ((pos2[0] + pos2[2]) / 2 - 5, pos2[1] + 20))
        
def drawGameModes(app,screen):
    #Draw game mode screen
    if app.currentScreen == "gameModeScreen":
        screen.blit(backgroundImage, (0, 0))
        
        #draw game buttons
        for i in range(-1, 0):
            pygame.draw.rect(screen, WHITE, (app.textWC2 - app.margin,
                                        app.textHC2 - app.margin + 70 * i,
                                        app.boxWidth2 * 2 + 2 * app.margin,
                                        app.boxHeight * 2.3 + 2 * app.margin))
            
            pygame.draw.rect(screen, RED, (app.textWC2, app.textHC2 + 70 * i,
                                        app.boxWidth2 * 2, app.boxHeight * 2.3))
        
        #add text on top of buttons
        screen.blit(app.mode1, (app.width / 2 - app.mode1.get_width() / 2,
                            (app.height * 2 / 5) - 70 - (app.mode1.get_height() / 2)))
        
def drawInstruction(app,screen):
    #Draw Instruction screen
    if app.currentScreen == "instructionScreen":
        
        screen.blit(backgroundImage, (0, 0))
        
        InstructionFont = pygame.font.SysFont('Helvetica', 30)
        
        textIntro = InstructionFont.render("WELCOME TO INSTRUCTIONS!", True, WHITE)
        textPara = InstructionFont.render("Press 1 to return to menu", True, WHITE)
        
        screen.blit(textIntro, (app.width / 2 - textIntro.get_width() / 2,
                    (app.height * 1 / 5) - 70 - (textIntro.get_height() / 2)))
        
        screen.blit(textPara, (50,100))
            
def drawMyProfile(app, screen):
    #Draw Player's Personal Profile
    if app.currentScreen == "myProfileScreen":
        
        screen.blit(backgroundImage, (0, 0))
        
        L = ["No.", "Total Keys", "Mistakes", "WPM", "Accuracy", "Time"]
        
        for i in range(len(L)):
            s = app.menuChoiceFont.render(L[i], True, WHITE)
            screen.blit(s, app.profilePos[i])
               
        for i in range(len(app.myProfileList)):
            totalKey =  app.menuChoiceFont.render(app.myProfileList[i][0], True, WHITE)
            mistake = app.menuChoiceFont.render(app.myProfileList[i][1], True, WHITE)
            wordPerMin = app.menuChoiceFont.render(app.myProfileList[i][2], True, WHITE)
            accuracy = app.menuChoiceFont.render(app.myProfileList[i][3] + "%", True, WHITE)
            recordNum = app.menuChoiceFont.render("#" + f"{i+1}", True, WHITE)
            
            num = app.myProfileList[i][4]
            timePassed = app.menuChoiceFont.render(f"{(int(num) // 60):02} : {(int(num) % 60):02}", True, WHITE)

            instruction = app.menuChoiceFont.render("Press 1 to return to menu", True, WHITE)
            
            screen.blit(recordNum, (app.profilePos[0][0], 100 + 50 * i))
            screen.blit(totalKey, (app.profilePos[1][0], 100 + 50 * i))
            screen.blit(mistake, (app.profilePos[2][0], 100 + 50 * i))
            screen.blit(wordPerMin, (app.profilePos[3][0], 100 + 50 * i))
            screen.blit(accuracy, (app.profilePos[4][0], 100 + 50 * i))
            screen.blit(timePassed, (app.profilePos[5][0], 100 + 50 * i))
    
            screen.blit(instruction, (app.width / 2 - instruction.get_width() / 2, app. height - 50))
    
def drawBackground(app,screen):
    #Draw Game Main background and objects
    if app.currentScreen == "startGameScreen" and app.startGame == True:
        
        #add background image
        screen.blit(backgroundImage, (0,0))
        
        #add spaceship
        Spaceship().draw(screen)
        
        #draw lines to create perspective lane
        pygame.draw.line(screen, WHITE, (app.width / 2 - 70, app.height / 4),
                         (0 + 100, app.height), width=2)
        
        pygame.draw.line(screen, WHITE, (app.width / 2 + 70, app.height / 4),
                         (app.width - 100, app.height), width=2)
        
        pygame.draw.line(screen, WHITE, (app.width / 2 - 20, app.height / 4),
                         (0 + 400, app.height), width=2)
        
        pygame.draw.line(screen, WHITE, (app.width / 2 + 20, app.height / 4),
                         (app.width - 400, app.height), width=2)

def drawBlackHole(screen):
    app.blackHole.draw(screen)
    
def drawAsteroids(app, screen):
    if app.currentScreen == "startGameScreen" and app.startGame == True:
        for item in app.asteroid:
            item.draw(app, screen)

def drawComputerWord(app,screen):
    #draw computer words on the screen
    if app.startGame == True:
        wordFont = pygame.font.SysFont('Helvetica', 16)
        
        #attach the word to the asteroid
        for i in range(len(computerWord.wordList)):
            a = wordFont.render(computerWord.wordList[i], True, WHITE)
            screen.blit(a, (app.asteroid[i].x , app.asteroid[i].y - 10))
        
        #add colored letters
        if app.startWord == True:
            b = computerWord.currentIndex
            coloredWord = wordFont.render(computerWord.colored, True, RED)
            screen.blit(coloredWord, (app.asteroid[b].x , app.asteroid[b].y - 10))
           
def drawTypingKeys(app, screen):
    #Make typing key appear on the screen 
    if app.startGame == True:
        typerFont = pygame.font.SysFont('Helvetica', 20)
        
        #take the string of the type list
        inputKey = typerFont.render(app.stringTypeList[-10:], True, WHITE)
        
        #and print that on the screen
        screen.blit(inputKey, (app.width / 2 - 50, app.height - 50))
        
        #Draw Type Box
        pygame.draw.line(screen, WHITE, (app.width / 2 - 70, app.height - 60),
                         (app.width / 2 + 70, app.height - 60), width = 3)
         
        pygame.draw.line(screen, WHITE, (app.width / 2 - 70, app.height - 60),
                         (app.width / 2 - 70  , app.height - 20), width = 3)
        
        pygame.draw.line(screen, WHITE, (app.width / 2 - 70, app.height - 20),
                         (app.width / 2 + 70, app.height - 20), width = 3)
         
        pygame.draw.line(screen, WHITE, (app.width / 2 + 70, app.height - 60),
                         (app.width / 2 + 70  , app.height - 20), width = 3)

def drawControlBox(app, screen):
    #Draw Control box on the top right corner
    if app.startGame == True:
        pygame.draw.rect(screen, GRAY, (app.width - 300, 30, 280, 130))
        
        timePasses = app.menuChoiceFont.render("Time: " + f"{(app.timer // 60):02} : {(app.timer % 60):02}", True, WHITE)
        screen.blit(timePasses, (app.width - 280, 60))
        
        level = app.menuChoiceFont.render(f"Stage : {app.stage} / 8", True, WHITE)
        screen.blit(level, (app.width - 280, 90))
        
def drawHealthBar(app, screen):
    if app.startGame == True:
        screen.blit(heartImg, (app.width / 2 - 250, 20))
        pygame.draw.rect(screen, RED, (app.width / 2 - 200, 30, 400 * (app.health / 400), 10))
        
def drawExplosion(app, screen):
    for item in app.explosions:
        if app.blip % 1 == 0:
            item.draw(screen)
            item.changeState()
            
def drawBullet(app, screen):
    if app.startGame == True:
        for item in app.bullets:
            item.draw(app,screen)
            
def drawScore(app, screen):
    #Draw the score on game over screen
    if app.gameOver == True:
        totalKey =  app.menuChoiceFont.render(f"Keys typed: {app.charCount}", True, WHITE)
        mistake = app.menuChoiceFont.render("Mistakes: " + str(app.wrong), True, WHITE)
        wordPerMin = app.menuChoiceFont.render("Word/Minute: " + str(app.avgWPM), True, WHITE)
        accuracy = app.menuChoiceFont.render("Accuracy: " + str(int(app.accuracy * 100)) + "%", True, WHITE)
        
        num = app.timer
        timePassed = app.menuChoiceFont.render("Time Passed: " +
                            f"{((num) // 60):02} : {(num % 60):02}", True, WHITE)

        instruction = app.menuChoiceFont.render("Press 1 to save and return to menu", True, WHITE)
        
        screen.blit(totalKey, (200, 250))
        screen.blit(mistake, (200, 300))
        screen.blit(wordPerMin, (200, 350))
        screen.blit(accuracy, (200, 400))
        screen.blit(timePassed, (200, 450))
        
        screen.blit(instruction, (app.width / 2 - instruction.get_width() / 2, app. height - 150))
        
def drawGameOver(app, screen):
    if app.gameOver == True:
        screen.blit(backgroundImage, (0,0))
        
        #Draw big white rectangle
        
        pygame.draw.line(screen, WHITE, (100, 100),
                         (app.width - 100, 100), width = 3)
         
        pygame.draw.line(screen, WHITE, (100, 100),
                         (100, app.height - 100), width = 3)
        
        pygame.draw.line(screen, WHITE, (100, app.height - 100),
                         (app.width - 100, app.height - 100), width = 3)
         
        pygame.draw.line(screen, WHITE, (app.width - 100, 100),
                         (app.width - 100, app.height - 100), width = 3)
         
        #Generate different text for two possible outcomes
        if app.health <= 0:
            title = app.menuHeaderFont.render("Game Over", True, WHITE)
            screen.blit(title, (app.width / 2 - title.get_width() / 2, 120))
        
        if app.health > 0:
            title = app.menuHeaderFont.render("Victory!", True, WHITE)
            screen.blit(title, (app.width / 2 - title.get_width() / 2, 120))

def drawLeaderBoard(app,screen):
    #Draw leaderboard ranking screen
    if app.currentScreen == "leaderboardScreen":
        
        screen.blit(backgroundImage, (0, 0))
        
        L = ["Rank", "Username", "Score"]
        
        for i in range(len(L)):
            s = app.menuChoiceFont.render(L[i], True, WHITE)
            screen.blit(s, app.leaderboardPos[i])
               
        for i in range(len(app.leaderboard)):
            profile = app.leaderboard[i]
            user = profile.split(":")
            
            username =  app.menuChoiceFont.render(user[0], True, WHITE)
            score = app.menuChoiceFont.render(user[1], True, WHITE)
            rank = app.menuChoiceFont.render("#" + f"{i+1}", True, WHITE)

            instruction = app.menuChoiceFont.render("Press 1 to return to menu", True, WHITE)
            
            screen.blit(rank, (app.leaderboardPos[0][0], 200 + 50 * i))
            screen.blit(username, (app.leaderboardPos[1][0], 200 + 50 * i))
            screen.blit(score, (app.leaderboardPos[2][0], 200 + 50 * i))
    
            screen.blit(instruction, (app.width / 2 - instruction.get_width() / 2, app. height - 50))
    
def drawPauseScreen(app,screen):
    #Draw paused type box
    if app.pause == True:
        
        pos1 = (app.width / 2 - 150, app.height / 2 - 80, 300, 20)
        pos2 = (app.width / 2 - 150, app.height / 2 - 60, 300, 120)
        
        pygame.draw.rect(screen, WHITE, pos1)
        pygame.draw.rect(screen, WHITE, pos2)

        wordFont = pygame.font.SysFont('Helvetica', 16)
        text1 = wordFont.render("Paused Window", True, BLACK)
        text2 = app.menuChoiceFont.render("Paused! ", True, BLACK)
        text3 = wordFont.render("Press 1: return to menu", True, BLACK)
        text4 = wordFont.render("Press 2: continue playing", True, BLACK)
         
        screen.blit(text2, (pos1[0] + pos1[2] / 2 - text2.get_width() / 2 + 20,
                            pos1[1] + pos1[3] / 2 - text2.get_height() / 2 + 30))
        
        screen.blit(text3, (pos1[0] + pos1[2] / 2 - text3.get_width() / 2,
                            pos1[1] + pos1[3] / 2 - text3.get_height() / 2 + 70))
        
        screen.blit(text4, (pos1[0] + pos1[2] / 2 - text4.get_width() / 2,
                            pos1[1] + pos1[3] / 2 - text4.get_height() / 2 + 100))

def drawPlayingScreen(app, screen):
    #complete the playing screen
    
    #when game is finshed --> draw game over screen
    if app.gameOver == True:
        drawGameOver(app,screen)
        drawScore(app,screen)
    
    #else: add all game elements together
    elif app.startGame == True:
        drawBackground(app,screen)
        
        drawBlackHole(screen)
        
        drawTypingKeys(app, screen)
        
        drawControlBox(app,screen)
        
        drawHealthBar(app, screen)
        
        drawAsteroids(app, screen)
               
        drawComputerWord(app, screen)
        
        drawBullet(app, screen)
        
        drawExplosion(app, screen)
    
    #when game is paused --> add pause box
    if app.pause == True:
        drawPauseScreen(app,screen)

################################# GAME MAIN LOOP ###############################
        
################################################################################

#Game main loop
while app.running:
    
    time = app.clock.tick(40)
    
    #get the time indicator
    if app.startGame == True and app.pause == False:
        app.blip += 1
    
    #draw game screens
    createTextMenu(app)
    drawMenuScreen(app,screen)
    
    drawUserBox(app,screen)
    
    createTextGameModes(app)
    drawGameModes(app,screen)
    
    createMyRecord(app)
    
    drawInstruction(app,screen)
    
    drawMyProfile(app,screen)
    
    createleaderboardPos(app)
    drawLeaderBoard(app, screen)
    
    #game main controller
    controlLevel(app, computerWord)
    
    createGameElement(app, computerWord)
    
    controlAsteroid(app, computerWord)
    
    calculateHealth(app)
        
    for event in pygame.event.get():
        #if the player press exit button --> game quit
        if event.type == pygame.QUIT:
            app.running = False
        
        #mousePressed() triggered
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed(app, event)
        
        #keyPressed() triggered
        if event.type == pygame.KEYDOWN:
            keyPressed(app, event)
            
            if app.startGame == True:
                #check if word that the typer types match any of the existing words
                computerWord.checkFirst(app)
                
                if app.startWord != False:
                    #compare words and typelist
                    app.result = computerWord.compare(app)
                else:
                    #add mistakes
                    app.wrong += 1
    
    computerWord.compareWord(app)
    
    controlBullet(app)
    
    drawPlayingScreen(app, screen)
    
    if app.gameOver == True and app.startGame == False:
        #when the game is finished
        #get the player's statistics and score
        app.myProfile = f"{app.charCount} {app.wrong} {app.avgWPM} {int (app.accuracy * 100)} {app.timer}\n" 
        app.score = (app.charCount - app.wrong) * 0.40 + app.avgWPM * 0.30 \
                        + int(app.accuracy * 100) * 0.40 - app.timer * 0.10
        app.score = int(app.score * 10)
    
    pygame.display.flip()
    
pygame.quit()


############################# ASSETS SOURCE ####################################

################################################################################
#1. IMAGES
#BACKGROUND: https://www.teahub.io/viewwp/xhomoJ_free-space-backgrounds-group-space-invaders-game-background/

#SPACE SHIP: https://www.pygame.org/project/4007

#ASTEROIDS: https://flyclipart.com/asteroid-pixel-art-maker-asteroid-png-514800#

#HEART: https://toppng.com/pixel-heart-PNG-free-PNG-Images_98517

#BULLET: https://opengameart.org/content/assets-free-laser-bullets-pack-2020

#EXPLOSION: https://www.cleanpng.com/png-body-jewellery-font-4261378/


#2. WORDS AND FONT
#WORD LIST 1: https://gist.github.com/deekayen/4148741

#WORD LIST 2: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-usa.txt

#FONT: https://www.fontspace.com/pixel-emulator-font-f21507


#3. SOUND EFFECTS
#BGM: https://www.proudmusiclibrary.com/en/tag/mario

#SOUND: http://www.classicgaming.cc/classics/asteroids/sounds
