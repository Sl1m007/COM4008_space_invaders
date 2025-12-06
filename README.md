COM4008 – Space Invaders Coursework  
Author: Terry Catchpole  

This project contains my Space Invaders style game for COM4008 Programming Concepts.  
The game is written in Python using PyGame and includes invaders, barriers, player shooting, collisions, and a basic game-over state.

------------------------------------------------------------

HOW TO RUN THE GAME

The code for the game is stored inside the “script” folder.

1. Make sure Python 3 is installed.
2. Install PyGame by opening a terminal or command prompt and typing:

   pip install pygame

3. Open a terminal and change into the script folder where main.py is located.  
   For example:

   cd path\to\space_invaders\script

4. Run the game with:

   python main.py

The game starts immediately, and you can move and shoot straight away.

------------------------------------------------------------

CONTROLS

Left Arrow  – Move left  
Right Arrow – Move right  
Space Bar   – Shoot bullets upwards  

------------------------------------------------------------

REQUIREMENT 1 – INVADER ARRAY

The invaders are arranged in rows using the “create_invader_array” function in invader.py.  
The invaders move left and right across the screen.  
When any invader reaches the edge, they drop down and reverse direction.  
The speed increases automatically as invaders are destroyed.

------------------------------------------------------------

REQUIREMENT 2 – PLAYER, SHOOTING, COLLISIONS AND LIVES

The Player class (in player.py) handles movement and keeps the player inside the screen.  
Pressing the space bar fires bullets using the Bullet class in bullet.py.

Bullets destroy invaders on collision, and the score increases.  
Invader bullets can hit the player, reducing lives.  
When all lives are lost, the game ends with a “GAME OVER” message.

------------------------------------------------------------

REQUIREMENT 3 – BARRIERS THAT BREAK APART

The barriers are made from small square blocks.  
Each block can be destroyed individually by any bullet.

The barrier code is in barrier.py.  
Collisions between bullets and barriers are detected in main.py, removing the piece that was hit.

------------------------------------------------------------

GAME START AND END CONDITIONS

The game begins immediately when “python main.py” is run from inside the script folder.

The game ends when:
- The player loses all of their lives, or
- The invaders move too far down the screen.

A simple “GAME OVER” message is displayed.

------------------------------------------------------------

TESTING

I tested the game by trying different player actions:

- Moving left and right to confirm the boundaries work  
- Shooting invaders to confirm bullets behave correctly  
- Shooting the barriers to check they crumble  
- Letting invader bullets hit the player to test lives  
- Allowing the invaders to reach the bottom to check the game-over condition  

------------------------------------------------------------

USE OF RESOURCES

I mainly followed the COM4008 PyGame lecture material for the game loop and sprite usage.  
I also used ChatGPT as a learning tool for understanding how to organise my code into separate files and troubleshoot issues.  
All final code was written by me, and I made sure I understood how everything works.
