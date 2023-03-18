# Hasami Shogi

Implementation of Hasami Shogi in Python. \
Playable from the command line with inputs in the form "ab, cd" where a and b are the row and column of the square the piece is moving from and c and d are the row and column the piece is moving to, i.e. "i1, b1". \
Ruleset is refered to on Wikipedia as ["Variant 1"](https://en.wikipedia.org/wiki/Hasami_shogi#Variant_1). \
The Board is displayed as below, where letters mark the rows, numbers mark the columns, and Red and Black pieces are represented by 'R' and 'B' respectively. 
```
  1 2 3 4 5 6 7 8 9
a R R R R R R R R R 
b - - - - - - - - - 
c - - - - - - - - - 
d - - - - - - - - - 
e - - - - - - - - - 
f - - - - - - - - - 
g - - - - - - - - - 
h - - - - - - - - - 
i B B B B B B B B B 
```

## Requirements
Python 3.6 or greater.

## To Play
In the terminal, navigate to the directory this repo is in and enter \
`python PlayShogi.py` (Windows) \
or \
`python3 PlayShogi.py` (MacOS, Linux) \
to start a game.
