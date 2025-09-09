- add flashcards for testing
- add the direct translator to flashcard app
- We crated the main idea in class on how we would like to create a gamified learning application. The first step stareted with one of the 
weekly assignment where we should search on Github to find similar code.
-  first file structure in class and for the presentation, we started to write def to create the first outline

# The beginning
After we created the first layout and the main structure of the main.py file each of us created their game until the first meeting 
on August the 18 where we talked about our next steps so the game would look whole at the end


## main.py and flaschcards.py
- met to create an overall structure so we could program individually on our games first
- choose a color scheme so both games would match 
- the first problem occurred when Paula could not see the changes Frieda commited -> asked ChatGPT on what we could try to fix the problem
- To see if the Program was working in itself we asked ChatGPT to write a Memory Game just to test if all the different files were connected

## Memory Game 
the structure of the memory game is very simple. Therefore there were quite a lot of example Code available on Github
This helped me to program the first structure of the game quite fast and only a few opstacles occurred. However with going deeper
in the design with tkinker it was firstly quite complicated because ive never worked with the library. So i firstly researched how the 
library worked and what I could achieve with it. Here ive looked on YouTube and watched several beginner Tutorials on How tkinter works e.g
https://www.youtube.com/watch?v=ibf5cx221hk. After some research it was very noticable that the structure of tkinster is similar to PyGame. 
Through e.g. tk.Button() you were able to create a Button and modify it within the Breckits. 
- crated design within the colorsceme
- wanted rounded cards
- wanting cards to flip
- rim changing color depending on the state
- different curser when entering the card https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
- more # comments

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

- Initial research:
- crating an overview on the structure on of the code 
  - Class Memory Game
  - mostly needed to google ones how to do it, then code blocks were also repetative in matter of design

  - 18. August
        online meeting together, planing next steps. Paula is responsible for designing the main.py interface and Frieda is reosposible for the flashcards.py 
        major problem: Frieda cannot push the old repository and therefore no updates accur. Trying several approchaces to fix the bug however nothing works. No Reddit Account and no AI ChatBot was able to help us -> created a new repositories only way we were able to fix the problem
  - Problem: Flashcard editing not possible
  - established design scheme so both apps will look similar at the end
  - Frieda: the color scheme of the buttons has to be changed so that it matches Paula's memory game 
            idea: actually writing (you/ your opponent) to understand who is who under ASCII characters 
            adding emoji & header "Race Game"
  - Paula:
    - both buttons "back to menu" "restart game" in the middle
    - stats at the end
      - designing stats



  - 21. August 
        online meeting together 
  - Frieda: spelling and formatting after # - adding # to better the structure and to make the code more understandable 
            submit button cursor hand2
  - Paula:
    - more # comments
    - designing adapting the the rest -> pretty much copying what i did in the memory card game
    -  designing adapting the the rest -> pretty much copying what i did in the memory card game
- managing flashcards
  - buttons at the top
  - search bar
    - when scrolling down buttons stay at top
      - first problem encountered with buttons disappearing
  - scrolling bar



  - 31. August 
        online meeting together 
  - Frieda: start to implement streak system to track progress 
            stats design and popup layout 
            adding into documentation 
  - Paula:
    - designing scrollbar
    - no doubles
  - integrated translator
  - info side



  - 07. September 
          online meeting together, planing final steps, adding # comments to make the code more readable, problem: streak_plant somehow doesn't show up in the main menu interface the way it should, "Back to Menu" doesn't work in Frieda's game_race, 
          wanting parents or friends to try out our program to see if there are any further ideas to make sure the program is understandable, talking about things that we should change to make our codes more readable and that they align with one another 
  - Frieda: finding out why streak_plant isn't working -> creating a better grid in setup_main_menu to ensure all aspects of main menu are visible 
