# python

## 1. blobwars.py

In this mini project, we propose to implement a text mode interface for the game Blob wars. The game is played with two players (blues and reds) on an 8x8 size board. The boxes are numbered from 0 to 63.

The board contains blue and red pawns (also called blobs). We each take our turn. Each turn the current player chooses one of his pawns and moves it. Any pawn can move to an empty adjacent square, including diagonally, by duplicating itself and thus creating a new pawn of the same color. A pawn can also move two squares, ie max(∆line,∆column) = 2. In this case, there is no duplication and the pawn is said to make a "jump". Once arrived at its destination, a pawn transforms all of its adversary's neighboring pawns into pawns of its own color. The game stops as soon as a player cannot play. The player with the most pawns on the board then wins the game.
