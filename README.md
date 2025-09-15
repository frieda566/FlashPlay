# FlashPlay

## Description:
FlashPlay is a gamified vocabulary learning app. Players start by importing or creating a deck of flashcards, which becomes the foundation for a series of interactive minigames. In total you can choose between two different mini games: 
1. Memory Game: The flashcards are upside-down and you have to find the matching pairs <br>
3. Race Game: You race against a timed opponent. If you answer the question correctly your character moves forward, if you answer incorrectly the character does not move forward. <br>

The program assumes that the user enters English vocabulary and can translate it into nine languages.

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


