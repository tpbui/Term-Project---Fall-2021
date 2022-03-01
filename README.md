# Term-Project---Fall-2021
This is the user instruction for Term Project Demo - Tra Bui
Course: 15 - 112

SPACE TYPING

Project Overview
	Space Typing Game is a speed typing game in the form of a space video game that can give the user a fun time to practice their typing skills. The player will be given a limited amount of health to start with, and their mission is to use their typing skills to avoid asteroids from hitting them and survive through all the game levels. This game is developed using Pygame as the main module, and utilize Socket to incorporate networking features.  

Instruction step:
1. Setup
- Unzip the file "Tra Bui - TP3"

- In the folder "Tra Bui - TP3", you can open and run the file "TP3" using an IDE (please prioritise the use of Thonny)

2. App running
a. Game Menu:
a.1: Log in
- When the app starts, you will first see a main menu screen:
	+ Please type in your username. You have to do this step, otherwise you cannot proceed with other steps.
	+ After finish typing, please press "Enter" to log in.
	+ A few notes for username:
		  - 	You have to type in at least one character and at most 20 characters to form your name.
⁃	Create the name without using number 1. In fact, you will not be able to have a username with "1" in it because it is the controlling key of the game.
⁃	Preferably without white space.

a.2: Buttons
- Once logged in, you can click on the coloured buttons on the menu to move to the next screen. 

- If you are not during the game play, you can always return to the main menu and log out by pressing "1" on your keyboard.

b. Game Options

- If you want to read the game instruction: Click on "Instruction"

- If you want to see the record of your nearest games: Click on "My Profile"
	+ The information on the screen is your personal record playing the game
	+ This screen should start out empty

- If you want to see the leaderboard of TOP 3 user ever played this game: Click on "Leaderboard"
	+ The leaderboard will get updated every time you finish a game. 

- If you want to quit the game: Press "1" to return to the main menu --> Click the [x] box on the top-left corner to quit the program.

- If you want to play the game: Click on "Start game" --> Choose game mode. Currently, there is one "Normal Mode".
	
	+ On playing the screen, you can see:  moving asteroids carrying word, a timer that counts the passed time, a health bar on top of the screen, and a spaceship with word box below it.

c. Game Features
c.1: During game play:
	Basic features:
	+ When you have entered the playing screen, you can type keys on your keyboard to shoot down the asteroids carrying the word on the screen. 

	+ For every letter you type correctly for a word, the letter will change its color. If you type all the letter in the targeted word correctly, the according asteroid will explode. You can continue typing other words without pressing any extra keys. 

	+ Characters that you can type include alphabet letters, numbers, and punctuations. If there are capitalised characters, you can turn on Caps lock or hold Shift when typing.
	
	Other:
	+ Game Stages: The Normal mode is consisted of 8 stages. As you played, the game will get difficult with longer and many words.

	+ Asteroid Speed: The speed of the asteroids is based on your typing speed.

	+ Losing Health: You will lose health if an asteroid hits you because you couldn't type the word on top of it on time. 

	+ Bad Asteroid: During gameplay, you will see bad asteroids. If you accidentally type a letter that match this asteroid, you will lose health immediately. These asteroids will not make you lose health if they reach the end of the  road.
	
	+ Game Pause/Return: While playing the game (on the playing screen), press "TAB" if you want to pause the game. There will be a white box appear on the screen with instructions and the objects 	of the game will stop moving and running. If press "1", you will return to the menu and please note that your game progress will lose. If you press "2", you will continue playing.

	+ Game Ending: 
		+ (1): your health bar is not empty after passing all game stages --> Victory screen
		+ (2): your health bar is emptied because of the asteroid hitting --> Game over screen
		+ Once the game end, you can see a summary of your stats. Please press "1" to save the results and return to the main menu

c.2 Outside game play:
	- Note that whenever you come back to the menu by pressing "1", you are logged out. You can type in your old username to check the history of your game play or create new profiles to your liking. 
	Features:

	- Personal Profile: Your profile should start out empty. After playing, you can see the your most current game records. After finishing the game, please press "1" to return to menu --> Log in --> My 	Profile to see the updates.

	- Leaderboard: Same process as mentioned above. The difference is if you click on the Leaderboard page even in your first time playing the game, there might be some recorded results from some users because the leaderboard is getting updated continuously after a player submits their score to the system. Please press "1" to return to menu --> Log in --> Leaderboard to see the updates. If the leaderboard stays the same, that means your score did 	not beat them. You can try playing the game on different device to test this feature. 
