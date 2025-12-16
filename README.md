HOW TO RUN THE GAME

The code for the game is stored inside the “script” folder.
	1.	Make sure Python 3 is installed on your computer.
	2.	Install PyGame by opening a terminal or command prompt and typing:
pip install pygame
	3.	Open a terminal and change into the script folder where main.py is located.
For example:
cd path\to\space_invaders\script
	4.	Run the game using:
python main.py

The game starts immediately and can be played straight away.

⸻

CONTROLS

Left Arrow  – Move left
Right Arrow – Move right
Space Bar   – Shoot bullets

⸻

REQUIREMENT 1 – INVADER ARRAY

The invaders are created in rows and placed evenly across the screen.

They move left and right together as a group.
When any invader reaches the edge of the screen, the whole group moves down and changes direction.
As invaders are destroyed, their movement speed increases automatically.

This behaviour is handled using simple movement logic and position checks in the main game loop.

⸻

REQUIREMENT 2 – PLAYER, SHOOTING, COLLISIONS AND LIVES

The player is controlled using the left and right arrow keys and is kept within the screen boundaries.

Pressing the space bar fires bullets upwards using the DefenderBullet class.
Invaders also fire bullets using the InvaderBullet class.

When a player bullet collides with an invader, the invader is removed and the score increases.
If an invader bullet hits the player, one life is lost.

The player starts with a limited number of lives.
When all lives are lost, the game ends and a “GAME OVER” message is displayed.

⸻

REQUIREMENT 3 – BARRIERS THAT BREAK APART

The barriers are built from many small square blocks.

Each barrier is created using a small 2D pattern.
Every block is its own sprite.

When a bullet hits a barrier, only the block that was hit is removed.
This causes the barriers to slowly crumble as the game continues.

⸻

GAME START AND END CONDITIONS

The game starts as soon as main.py is run.

The game ends when:
	•	The player loses all of their lives, or
	•	The invaders move too far down the screen

When the game ends, a simple “GAME OVER” message is shown.

⸻

TESTING

I tested the game by playing it and trying different actions, including:
	•	Moving left and right to confirm the screen boundaries work
	•	Shooting invaders to check collisions and scoring
	•	Shooting the barriers to confirm individual blocks are removed
	•	Letting invader bullets hit the player to test lives
	•	Allowing invaders to reach the bottom to check the game-over condition

⸻

USE OF RESOURCES

I mainly followed the COM4008 PyGame lecture material, especially for the game loop, sprites, and collision handling.

I also used ChatGPT as a learning tool to help understand how to organise the project into separate files and to troubleshoot errors while learning.
All final code was written by me, and I made sure I understood how each part of the program works.
