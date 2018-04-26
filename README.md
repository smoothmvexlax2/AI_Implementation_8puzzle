# AI_Implementation_8puzzle
Myself and two other students used my 8_puzzle program for an AI project. The program uses a knowledge base of test data and decides whether a DFS or BFS search is the best for navigating through a tree of heuristic values. 

# Decision Process
The decision process compares a mean score of the number of moves from our knowledge base of boards having the same intitial top row. We understand the decision process is not ideal, but was a good starting point for an intro AI project.  

# Data
The pickle file 8_puzzle_boards holds all the solvable eight puzzle initial boards. We have filtered through all the board permutations. 8_puzzle_board_moves is the training results used for the decision process.

# Potential
1) Creating more detailed training data. I.E. the starting heuristic value, moves before a one is in a hill climbing trap, storing the occurances of the first row, etc. 
2) Working with different tree depths and implementing an AI decision process for the treedepth.
3) Implement the project on 15 puzzle.

# Beware
Some of these functions can be very costly and can take many hours to run.
