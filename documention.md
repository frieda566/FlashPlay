- add flashcards for testing
- add the direct translator to flashcard app
- We crated the main idea in class on how we would like to create a gamified learning application. The first step stareted with one of the 
weekly assignment where we should search on Github to find similar code.
-  first file structure in class and for the presentation, we started to write def to create the first outline
- 
## main.py and flaschcards.py
- met to create an overall structure so we could program individually on our games first
- choose a color scheme so both games would match 
- the first problem occurred when Paula could not see the changes Frieda commited -> asked ChatGPT on what we could try to fix the problem
- To see if the Program was working in itself we asked ChatGPT to write a Memory Game just to test if all the different files were connected

## Memory Game 
## Memory Game - Paula
### Tkinter Fundamentals

**What I learned:** Tkinter is Python's standard GUI (Graphical User Interface) toolkit that comes built-in with Python. 
It provides widgets (buttons, labels, frames, etc.) to create desktop applications. 
It functions similarly to Pygame but focuses more on traditional desktop interfaces rather than game graphics.

**Key concepts implemented:** Firstly, I started with the main window structure. 
Here, I implemented the parent-child relationships as learned in class - each widget needs a parent container. 
For the basic layout, similar to what I knew from HTML, I used the layout managers tkinter provides: pack(), grid(), and place(). 
The event handling was done with bind() methods to capture mouse clicks and hover events. 
To understand how these worked together, I looked at the original Tkinter Documentation and found most of the basic concepts explained there.

**Sources that helped:** 

- Python.org Tkinter Tutorial - Official documentation where I learned the basic widget types (https://docs.python.org/3/library/tkinter.html)
- Real Python Tkinter Guide - Comprehensive tutorial that helped me understand layout managers (https://realpython.com/python-gui-tkinter/)
- in general used as a source https://tkdocs.com/shipman/tkinter.pdf
### Creating Rounded Corners with Canvas

**What I learned:**
Tkinter widgets are rectangular by default, so creating rounded corners required learning about the Canvas widget and polygon drawing. 
This was completely new to me since I had only worked with basic rectangular widgets before.

**Key concepts implemented:**
The biggest challenge was understanding how to calculate the points for a rounded rectangle mathematically. 
I had to figure out that you need to define specific coordinates that create smooth curves. 
I started by looking up how rounded rectangles work geometrically, then implemented the _round_points() function that calculates all the corner positions. T
he Canvas widget's create_polygon() method with smooth=True was the key to making the corners actually look rounded.
I also learned about layering - drawing the shadow first, then outer rim, then inner rim, so they stack properly.

**Sources that helped:**

- Tkinter Canvas Documentation (https://docs.python.org/3/library/tkinter.html#tkinter.Canvas)
- Stack Overflow: Rounded Rectangle in Tkinter (https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners=, https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_polygon.html?utm_source=chatgpt.com)
- A geometry tutorial I found online that explained how to calculate rounded rectangle points (https://stackoverflow.com/questions/76318063/rounded-rectangle-in-tkinter-that-i-can-fill-inside-and-change-the-color-from-un)

### Hover Effects and Dynamic Styling

**What I learned:**

Making cards respond to mouse hover required understanding tkinter's event system. 
This was more complex than I initially thought because I had to manage different visual states.

**Key concepts implemented:**

I discovered that tkinter uses specific event names like "<Enter>" and "<Leave>" for mouse hover detection. 
The tricky part was creating the closure functions (mk_hover) to capture the right widget references - 
I learned about Python closures here. 
I had to use configure() to change widget properties dynamically, 
and I learned to check the current game state before applying hover effects (like not showing hover during animations). 
The conditional styling was important - different colors for different card states.

**Sources that helped:**

- Tkinter Event Handling tutorial  (https://python-course.eu/tkinter/events-and-binds-in-tkinter.php)
Tkinter Hover Effects - (https://www.geeksforgeeks.org/python/tkinter-button-that-changes-its-properties-on-hover/, https://coderslegacy.com/python/tkinter-config/)

### Multi-Layer Card Design with Rims

**What I learned:**
Creating visually appealing cards required understanding how to layer multiple shapes on a Canvas to create depth effects. 
This was like creating a layered design in image editing software, but with code.

**Key concepts implemented:**
I learned that drawing order matters - background elements must be drawn first. 
I implemented a system where I draw the shadow (offset by a few pixels), then outer rim, then inner rim, then the main card background. 
Each layer uses slightly different sizes and positions to create the visual depth. 
I had to track the canvas IDs for each layer so I could modify colors later. 
The hardest part was getting the mathematical offsets right so all the layers aligned properly.

**Sources that helped:**

- Canvas Layering Tutorial - (https://tkdocs.com/tutorial/canvas.html, https://stackoverflow.com/questions/43400856/change-the-color-of-an-object-after-tkinter-has-been-initiated/43400938#43400938)

### Card Flip Animation

**What I learned:**
Creating smooth animations without external libraries was challenging. 
I had to understand frame-based animation and timing in tkinter.

**Key concepts implemented:**
I implemented a two-phase animation: shrink the card width to zero, change the content, then expand back to full width. 
This creates the illusion of the card flipping. 
I used tkinter's after() method for timing - scheduling the next animation frame. 
The key insight was that I needed to prevent user interaction during animation with the flip_animation_running flag.
I also learned about mathematical interpolation - calculating intermediate values between start and end positions.

**Sources that helped:**

- Tkinter after() Method documentation - https://www.pythontutorial.net/tkinter/tkinter-after/, https://inf-schule.de/software/gui/entwicklung_tkinter/timer
- Game development tutorials that explained frame-based animation concepts https://tkinter.com/widget-animation-tkinter-customtkinter-23/

### Dynamic Color Changes Based on Card State

**What I learned:**
Cards needed different visual states (normal, hover, flipped, matched), which required a systematic approach to color management. 
This taught me about state machines in GUI programming.

**Key concepts implemented:**
I created a set_card_colors() method that can change all the rim colors at once. 
The challenge was managing all the different states - face-down cards use one color scheme, flipped term cards use another, flipped translation cards use a third, and matched cards use yet another. 
I had to use Canvas itemconfig() to modify the colors of already-drawn polygons. 
For the logic to work I needed to check the current state before applying color changes.

**Sources that helped:**

- here I used similar sources as i  number 3, because this bit relies on the same hover recognition

### Layout Management and Responsive Design

**What I learned:**
Making the game work at different window sizes required understanding tkinter's layout system. 
I learned about grid weights and dynamic sizing.

**Key concepts implemented:**
I implemented a grid system that automatically calculates the best arrangement of cards (trying to keep it roughly square). 
The _best_grid() function finds the optimal rows and columns for any number of cards. 
I learned about grid weights - making rows and columns expand proportionally when the window resizes. 
The responsive card sizing was tricky - I had to calculate available space and size cards proportionally while maintaining their aspect ratio.

**Sources that helped:**

- Tkinter Grid Manager documentation https://tkdocs.com/tutorial/grid.html
- winfo to measure available space https://www.tcl-lang.org/man/tcl8.4/TkCmd/winfo.htm
- Mathematical optimization tutorials for the grid calculation algorithm https://tkdocs.com/tutorial/concepts.html, https://docs.python.org/3/library/math.html

### Memory Management and Cleanup

**What I learned:**
Preventing memory leaks and crashes required proper cleanup of timers and event bindings. 
This was important for a smooth user experience.

**Key concepts implemented:**
I learned to track all after() timer IDs in a set so I could cancel them when the game exits. 
Event bindings also needed to be unbound to prevent orphaned references. 
The _cleanup() method handles all of this systematically. 
I also learned about the importance of checking if widgets still exist before trying to update them - the update_timer() method includes this check.

**Sources that helped:**

- destroying widgets during cleanup https://tkdocs.com/tutorial/windows.html
- event bindings https://tkdocs.com/shipman/tkinter.pdf

## Race Game 
like the memory game - the race game is very simple. I was inspired to use predefined ASCII characters like we did in class. Yet I used a different one 
since I didn't want the jokes and the ones I found felt more fitting. For the race track I...
Regarding the design there were a few obstacles as I had never worked with tkinter before and needed support. Therefore I...
After understanding, it got easier and easier the more I worked with it and the more ideas I added. 
- created design within the color scheme we agreed on 
- wanting movement animations for both ASCII characters 
- wanting the ASCII opponent to move at the same time in same increments 
- wanting the ASCII character of the user to move in bigger increments if the user answered faster 
- wanting the ASCII character of the user to move in smaller increments if the user answered later than 8s 
- having an Entry field where the user could write the translations 
- different curser when entering 
- stats at the end 

# main.py
- designign adapting the the rest -> pretty much copying what i did in the memory card game
- managing flashcards
  - buttons at the top
  - search bar
  - scrolling bar
  - no doubles
  - integrated translator
- 

- Initial research:
- crating an overview on the structure on of the code 
  - Class Memory Game
  - mostly needed to google ones how to do it, then code blocks were also repetative in matter of design

  - 18. August
        online meeting together, planing next steps. Paula is responsible for designing the main.py interface and Frieda is reosposible for the flashcards.py interface
        major problem: Frieda cannot push the old repository and therefore no updates accur. Trying several approchaces to fix the bug however nothing works. No Reddit Account and no AI ChatBot was able to help us -> created a new repositories only way we were able to fix the problem
  - Problem: Flashcard editing not possible
  - established design scheme so both apps will look similar at the end
  - Frieda: the color scheme of the buttons has to be changed so that it matches Paula's memory game 
            idea: actually writing (you/ your opponent) to understand who is who under ASCII characters 
            adding emoji & header "Race Game"
  - 21. August 
        online meeting together 
  - Frieda: spelling and formatting after # - adding # to better the structure and to make the code more understandable 
            submit button cursor hand2
  - 31. August 
        online meeting together 
  - Frieda: start to implement streak system to track progress 
            stats design and popup layout 
            adding into documentation
  - 07. September 
          online meeting together, planing final steps, adding # comments to make the code more readable, problem: streak_plant somehow doesn't show up in the main menu interface the way it should, "Back to Menu" doesn't work in Frieda's game_race, 
          wanting parents or friends to try out our program to see if there are any further ideas to make sure the program is understandable, talking about things that we should change to make our codes more readable and that they align with one another 
  - Frieda: finding out why streak_plant isn't working -> creating a better grid in setup_main_menu to ensure all aspects of main menu are visible 
