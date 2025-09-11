f- add flashcards for testing
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

- Python.org Tkinter Tutorial https://docs.python.org/3/library/tkinter.html
- Real Python Tkinter Guide https://realpython.com/python-gui-tkinter/
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

## Race Game - Frieda 
### Tkinter Fundamentals & ASCII Integration 

**What I learned**
I had never worked with tkinter before, so I first needed to learn how to build an interactive game using frames, labels, canvases, and buttons.
Instead of images, I used predefined ASCII characters (different from the ... library we used in class) - ascii_art_TNH - because they matched my theme better. 
Additionally, here I deleted the line under the characters (for instance "woof" under the dog) to match the aesthetic better. 

**Key concepts implemented**
I implemented a game board using a Canvas widget, where both the player and the opponent are drawm as ASCII characters. I created functions to place, label, and move these characters horizontally across the racetrack.
Moreover, I used tkinter's after() method to schedule animations and opponent movements in timed intervals, which allowed both the player and opponent to advance independently. I designed the movement logic so the opponent always advances in small increments while the player's increments depend on answer speed (faster answer = bigger steps, slower answer = smaller ones). 
I also integrated user input with an Entry widget and bound the Enter key so answers could be submitted quickly - otherwise a special cursor appears when the enter button is pressed. 
Furthermore, I created an end-of-game popup that displays stats including the outcome of the race, the moves of the ASCII character of the user and the correct answers. 

**Sources that helped**

### Animation, Opponent Logic & Game Flow 

**What I learned**




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

  # 18. August - online meeting
        online meeting together, planing next steps. Paula is responsible for designing the main.py interface and Frieda is reosposible for the flashcards.py interface
        major problem: Frieda cannot push the old repository and therefore no updates accur. Trying several approchaces to fix the bug however nothing works. No Reddit Account and no AI ChatBot was able to help us -> created a new repositories only way we were able to fix the problem
  - Problem: Flashcard editing not possible
  - established design scheme so both apps will look similar at the end
  - Frieda: the color scheme of the buttons has to be changed so that it matches Paula's memory game 
            idea: actually writing (you/ your opponent) to understand who is who under ASCII characters 
            adding emoji & header "Race Game"
    ## Paula
#### Designing and Adapting the UI Framework.
Key concepts implemented: I started by copying the visual styling system from my Memory Game - the layered card design with brown shadows, sage/lime color schemes, and the rounded button effects. 
The main menu layout required understanding grid management in tkinter and weight distribution in grid layouts to make the interface responsive. The code was similar to the memory game and i struggled most with the adaption to the new design.
Sources that helped:
* My own Memory Game code - I referenced my previous work extensively
* Tkinter Grid Documentation - https://tkdocs.com/tutorial/grid.html
* Color theory resources for maintaining visual consistency across components

#### Managing Flashcards Interface
To Do: Creating the flashcard management screen required building a more complex data-driven interface. This was different from the Memory Game because I needed to display dynamic content that could change based on user input.

Key concepts implemented: I implemented a card-based display system where each flashcard gets its own visual card container. The challenge was creating a consistent layout that could handle different text lengths. I learned about text wrapping and calculating available space for content.
The most important concept was the separation between the visual card (with its styling) and the content area. Each flashcard item has a fixed-width container but flexible content area. I also implemented the button positioning on the right side of each card, which required understanding how to use frames to control layout precisely.
Sources that helped:
* tkinter Frame and packing documentation - https://docs.python.org/3/library/tkinter.html#tkinter.Frame
* Text wrapping and layout tutorials - similar resources as used in Memory Game
    
  # 21. August - online meeting
        online meeting together 
  - Frieda: spelling and formatting after # - adding # to better the structure and to make the code more understandable 
            submit button cursor hand2
   ## Paula
  #### Game Buttons at the Top 
To Do: I wanted the control buttons (Add New Flashcard, Back to Main Menu) to stay at the top while users scrolled through flashcards.

Key concepts implemented: I used separate frames for different UI sections - a header frame for fixed elements and a scrollable container for the list. The key insight was that the pack() order determines stacking, so I had to pack the header frame first, then the scrollable area. I also learned about fill="x" to make the header span the full width.
Problem Encountered - Buttons Disappearing: Initially, my buttons would disappear when I scrolled. I discovered this was because I had packed them inside the scrollable frame instead of the parent frame.

Sources that helped:
* tkinter layout management tutorials - understanding parent-child relationships
* Stack Overflow discussions about fixed headers with scrollable content: https://stackoverflow.com/questions/78769920/how-to-define-fixed-header-in-tk-grid-grid10x5
 
#### Search Bar Implementation
To Do: Adding a search function which required understanding tkinter's StringVar system and event handling.

Key concepts implemented: I implemented the StringVar.trace() method to detect when the search field changes. The challenge was connecting the search input to the display update function. I used lambda functions and callback systems in GUI programming.
The search functionality required filtering the flashcard list and then updating the display. I worked with lists of data and implement case-insensitive searching. The key insight was that I needed to store both the original list (all_flashcards) and the filtered list (filtered_flashcards) separately.
Sources that helped:
* tkinter StringVar documentation - https://docs.python.org/3/library/tkinter.html#tkinter.StringVar
* search Bar Stack Overflow. https://stackoverflow.com/questions/74700510/how-to-create-a-search-bar-to-search-keywords-in-my-tkinter-table

#### Scrolling Bar Implementation
To Do: Creating smooth scrolling for the flashcard list using a scroll bar.

Key concepts implemented: The scrolling system uses a Canvas widget as a viewport, with a Frame widget as the actual scrollable content, connected to a Scrollbar widget. This three-part system was confusing at first. I learned that the Canvas creates a "window" that contains the Frame, and the Scrollbar controls which part of the Frame is visible through the Canvas viewport.
One challenging part was getting the scroll region to update automatically when content changes. I implemented the configure event binding to recalculate the scrollable area whenever the content frame changes size. I also added mouse wheel support, which was at first quite confusing because different systems (macos/ linux/ windows) required different handling operating systems.
Sources that helped:
* Scrollbar documentation - https://www.tutorialspoint.com/python/tk_scrollbar.htm
* Scrollable Frame tutorials - https://tkdocs.com/tutorial/canvas.html
* Platform-specific mouse wheel handling - https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
  
  # 31. August - online meeting
        online meeting together 
  - Frieda: start to implement streak system to track progress 
            stats design and popup layout 
            adding into documentation
    ## Paula
   #### Designing Custom Scrollbar
To Do: The default tkinter scrollbar looked inconsistent with my custom styling. 

Key concepts implemented: I implemented a custom ttk.Style configuration that changes the scrollbar colors to match the sage/brown/lime color palette. The challenge was understanding which style properties control which parts of the scrollbar (background, trough, arrows, etc.).
I created a reusable create_styled_scrollbar() method that I could use throughout the application. This taught me about creating utility functions for UI components.

Sources that helped:
* ttk.Style documentation - https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Style
* ttk theming tutorials for custom widget appearance
  
#### No Duplicate Flashcards System
To Do: I needed to prevent users from creating flashcards with identical terms or translations. This required implementing data validation and comparison logic.

Key concepts implemented: I created a check_duplicate_flashcard() function that compares new entries against existing flashcards. The challenge was handling different comparison scenarios - not just exact matches, but also checking if a new term matches an existing translation or vice versa.
I used case-insensitive string comparison and learned the importance of stripping whitespace before comparing. I also implemented an exclude_id parameter for the edit function, so users can save edits to existing flashcards without triggering false duplicate warnings. Here I used familiar coding patterns such as looping through the vocabs to check for duplicates
  

  # 07. September - online meeting
          online meeting together, planing final steps, adding # comments to make the code more readable, problem: streak_plant somehow doesn't show up in the main menu interface the way it should, "Back to Menu" doesn't work in Frieda's game_race, 
          wanting parents or friends to try out our program to see if there are any further ideas to make sure the program is understandable, talking about things that we should change to make our codes more readable and that they align with one another 
  - Frieda: finding out why streak_plant isn't working -> creating a better grid in setup_main_menu to ensure all aspects of main menu are visible

 ## Paula
 #### Info Side Implementation
To Do: implementing a info side, for explanations on how the program works.

Key concepts implemented: I created a separate info window using tk.Toplevel() that displays help text imported from an external module. This was relevantly easy because we looked at module imports in class.
I implemented error handling for the info module import, with fallbacks and clear error messages if the info.py file is missing. I also added scrollable text display using the same Canvas/Frame system I learned for the flashcard list.
Lastly, I implemented the window centering calculation and making the text area responsive to window resizing.
Sources that helped:
* tkinter Toplevel documentation - https://docs.python.org/3/library/tkinter.html#tkinter.Toplevel
* Module importing and error handling - https://docs.python.org/3/tutorial/errors.html
 
# 10. September - online meeting

## Paula

The last steps focused on final touch-ups, such as implementing a method in main.py to ensure that all popup windows follow the same design scheme as the rest of the application.
In addition, I created a fallback mechanism to return to the main menu whenever an AttributeError occurs.
Finally, I added more comments throughout the code to improve readability.
