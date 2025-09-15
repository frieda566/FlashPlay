# FlashPlay

## Description:
FlashPlay is a gamified vocabulary learning app. Players start by importing or creating a deck of flashcards, which becomes the foundation for a series of interactive mini games. In total, you can choose between two different mini games: 
1. game_memory: The flashcards are upside-down, and you have to find the matching pairs <br>
2. game_race: You race against a timed opponent. If you answer the question correctly your character moves forward, if you answer incorrectly the character does not move forward. <br>

#### other files:
- info.py is for information content for FlashPlay application. Here learns the user how the game works.
- streak_plants.py generates a widget that visually represents a daily streak as a growing plant using .json as a build in package
- flashcards.py defines the basic structure for handling the flashcards
- flashcards.db saves the created flashcards so the user does not have to type in new ones, everytime entering the application.

*The program assumes that the user enters English vocabulary and can translate it into nine languages.*

## Installation
### Libraries:
1. tkinter 
2. random
3. time
4. math
5. json 
6. cowsay
7. io
8. sys
9. json
10. datetime
11. pathlib

### file structure:
vocab_flashcards/ 

├── .idea <br>
├── images <br>
│   ├── main.png <br>
│   ├── memory.png <br>
│   └── race_game.png <br>
├── DB/ <br>
│   └── flashcards.db    <br>
├── game_resources <br>
│   ├── flashcards.py <br>
│   └── info.py <br>
├── games/ <br>
│   ├── game_memory.py <br>
│   └── game_race.py <br>
├── streak <br>
│   ├── streak_data.json <br>
│   └── streak_plants.py <br>
├── .gitignore <br>
├── readme.md  <br>
├── documentation.md     .<br>
└── main.py <br>

## usage
run from terminal
python main.py


