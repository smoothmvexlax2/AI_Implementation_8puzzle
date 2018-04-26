import itertools
import gc
import pickle
import random
from PuzzleTree import Node, Tree, GOAL_STATE, AVERAGE

class Game:
    def __init__(self, initial=None):
        if not initial:
            self.sequence = []
        else:
            self.sequence=[initial]
    
    @property
    def countMoves(self):
        if self.sequence:
            return len(self.sequence)
        else:
            return 0
      
    def addMove(self, board):
        if board != self.sequence[-1]:
            self.sequence.append(board)
    
    def getCurrentBoard(self):
        if self.sequence:
            return self.sequence[-1]
        else:
            print("haven't started")
            return None
    
    def isGoal(self):
        data = self.getCurrentBoard()
        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col]!= GOAL_STATE[row][col]:
                    return False
        return True
        
    def isSolvable(self):
        data = self.getCurrentBoard()
        flatten = list(itertools.chain.from_iterable(data))
        inverse = 0
        for index in range(len(flatten)):
            for ind2 in range(index+1,len(flatten)):
                if flatten[index]!=0 and flatten[ind2]!=0 and flatten[index]>flatten[ind2]:
                    inverse +=1
        return(inverse%2==0)
    

    
    def __str__(self):
        out = []
        for board in self.sequence:
            out.append(
                     " {0} \n {1} \n {2} \n".format(
                             board[0],
                             board[1],
                             board[2],
                             )
                     )
        return("\n".join(out))
            
        
def play(data, treedepth=10):
    game = Game(initial=data)
    if not game.isSolvable():
#        print("not solvable")
        return 0
    tree = Tree(data=game.getCurrentBoard())
    depth = treedepth
    iterdepth = treedepth
    while not game.isGoal():
        createChildren(tree.root, depth)
        move = findNextMove(tree)
        while move is tree.root:
            #---------------------------
            #if a smaller hueristic value is not found we look deeper
            #---------------------------
            iterdepth += 5
            tree = Tree(data=move.data) # Heuristic value is stored here.  Print out move.data/save it into an associative array
            #if it enters this loop we need to take the node data and store it in a different associative array TODO
            createChildren(tree.root, iterdepth)
            ## during this loop it's going to keep returning a value.
            move = findNextMove(tree)
            if isGoal(move.data):#this stack is popping off the top, so from here we can find the minimum value and the max value
                stack = [move.data]#stack of nodes.  pop off nodes to get move.data (st = [move.val] determines the highest and lowest val from this )
                #this gives us the "change of direction" from increasing to decreasing. TODO  numbers around ~20 and 0
                while move.getParent():
                    move = move.getParent()
                    stack.append(move.data)
                while len(stack)>1:
                    game.addMove(stack.pop())
                #---------------------------
                #this returns the path to the solution found. 
                #the stack is the best solution given the initial state for
                #the last move found outside the current while loop
                #---------------------------
                #print(game)
                return game.countMoves
        if isGoal(move.data):
                stack = [move.data]
                while move.getParent():
                    move = move.getParent()
                    stack.append(move.data)
                while stack:
                    game.addMove(stack.pop())
                break
        game.addMove(move.data)
        tree = Tree(data=game.getCurrentBoard())

    #---------------------------
    #This print statement is if the game has no local mins
    #---------------------------
    
    return game.countMoves # algorithm moves versus optimal moves (treenode of 999)
#after this store to pickle file, and then "learn"
    #print(game)
    #caleb's add to check whether or not to include the table in the pickle file
    
def playWithAlgorithm(data, treedepth, nChoice):
    game = Game(initial=data)
    if not game.isSolvable():
    #        print("not solvable")
        return 0
    tree = Tree(data=game.getCurrentBoard())
    depth = treedepth
    iterdepth = treedepth
    while not game.isGoal():
        createChildren(tree.root, depth)
        move = findNextMoveImproved(tree, nChoice)
        while move is tree.root:
            #---------------------------
            #if a smaller hueristic value is not found we look deeper
            #---------------------------
            iterdepth += 5
            tree = Tree(data=move.data) # Heuristic value is stored here.  Print out move.data/save it into an associative array
            #if it enters this loop we need to take the node data and store it in a different associative array TODO
            createChildren(tree.root, iterdepth)
            ## during this loop it's going to keep returning a value.
            move = findNextMoveImproved(tree, nChoice)
            if isGoal(move.data):#this stack is popping off the top, so from here we can find the minimum value and the max value
                stack = [move.data]#stack of nodes.  pop off nodes to get move.data (st = [move.val] determines the highest and lowest val from this )
                #this gives us the "change of direction" from increasing to decreasing. TODO  numbers around ~20 and 0
                while move.getParent():
                    move = move.getParent()
                    stack.append(move.data)
                while len(stack)>1:
                    game.addMove(stack.pop())
                #---------------------------
                #this returns the path to the solution found. 
                #the stack is the best solution given the initial state for
                #the last move found outside the current while loop
                #---------------------------
                #print(game)
                return game.countMoves
        if isGoal(move.data):
                stack = [move.data]
                while move.getParent():
                    move = move.getParent()
                    stack.append(move.data)
                while stack:
                    game.addMove(stack.pop())
                break
        game.addMove(move.data)
        tree = Tree(data=game.getCurrentBoard())
    #---------------------------
    #This print statement is if the game has no local mins
    #---------------------------
    return game.countMoves # algorithm moves versus optimal moves (treenode of 999)

def isBoardSolvable(data):
    flatten = list(itertools.chain.from_iterable(data))
    inverse = 0
    for index in range(len(flatten)):
        for ind2 in range(index+1,len(flatten)):
            if flatten[index]!=0 and flatten[ind2]!=0 and flatten[index]>flatten[ind2]:
                inverse +=1
    return(inverse%2==0)
    
def isGoal(data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col]!= GOAL_STATE[row][col]:
                return False
    return True
	 

def findNextMoveImproved(tree, nChoice):
    #------------------------------------------------
    #suseptible to local min in hill climbing problem
    #------------------------------------------------
    if nChoice == 0:
        boardsize = len(tree.root.data)
        minval = boardsize**boardsize
        minnode = None
        que, gen = [tree.root], []
        while que:
            currentgen = []
            for node in que:
                for kid in node.children:
                    currentgen.append(kid)
                if node.val == 0:
                    minval = node.val
                    minnode = node
                    return minnode
                elif node.val <= minval and not minnode:
                    minval=node.val
                    minnode = node
                elif node.val < minval and node is not tree.root:
                    minval=node.val
                    minnode = node
            gen.append(currentgen)
            que=currentgen
        nodes = 0
        for group in gen:
            nodes += len(gen)
#        print("Number of nodes in bfs: ",nodes)
        if minnode is tree.root:
            return minnode
        while minnode.getParent() is not tree.root:
            minnode = minnode.getParent()
        return minnode
    
    if nChoice == 1:
           #implementation of depth-first search
        boardsize = len(tree.root.data)
        minval = boardsize**boardsize
        minnode = None
        stack, nodes = [tree.root],[]
        while stack:
            cur_node = stack.pop()
            nodes.append(cur_node)
            for child in cur_node.get_rev_children():
                stack.append(child)
#        print("Number of nodes in dfs: ",len(nodes))    
        for node in nodes:
            if node.val == 0:
                minval = node.val
                minnode = node
                return minnode
            elif node.val < minval and not minnode:
                minval=node.val
                minnode = node
# if we want above elif condition to be < or = then uncomment logic below
#            elif node.val<minval and node is not tree.root:
#                minval=node.val
#                minnode = node

        if minnode is tree.root:
            return minnode
        while minnode.getParent() is not tree.root:
            minnode = minnode.getParent()
        return minnode 
    else:
        print('not able to use choice 1 or 2, unable to do anything')
        

def findNextMove(tree): # see where this could be failing
    #------------------------------------------------
    #suseptible to local min in hill climbing problem
    #------------------------------------------------
    boardsize = len(tree.root.data)
    minval = boardsize**boardsize
    minnode = None
    que, gen = [tree.root], []
    while que:
        currentgen = []
        for node in que:
            for kid in node.children:
                currentgen.append(kid)
            if node.val == 0:
                minval = node.val
                minnode = node
                return minnode
            # this returns minnode but need 
            elif node.val <= minval and not minnode:
                minval=node.val
                minnode = node
            elif node.val<minval and node is not tree.root:
                minval=node.val
                minnode = node
        gen.append(currentgen)
        que=currentgen
    if minnode is tree.root:
        return minnode
    while minnode.getParent() is not tree.root:
        minnode = minnode.getParent()
    return minnode
                 
def createState(data, r0, c0, r1, c1):
    num = data[r1][c1]
    state = []
    for row in range(len(data)):
        group = []
        for col in range(len(data[row])):
            if row==r0 and col==c0:
                group.append(num)
            elif row==r1 and col==c1:
                group.append(0)
            else:
                same = data[row][col]
                group.append(same)
        state.append(group)
    return state


def find0(data):
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c]==0:
                 return r , c 
    return -1, -1 

# create function to three numbers from the run and have it decide which run you should use
# edit function to choose how to go through tree
# 

def createChildren(root, maxdepth):
        que, mem = [root], []
        while que:
            gen = []
#            cost = 0 if not mem else cost+1
            #------------------------------
            #need to edit for cost of each move
            #------------------------------
            for parent in que:
                current_state = parent.data
                r0, c0 = find0(current_state)
                kidState = []
                if r0-1>=0:
                    #------------------------------------------------
                    #can move left
                    #------------------------------------------------
                    r1 = r0-1
                    kidState.append(createState(current_state, r0, c0, r1, c0))
                if r0+1<=2:
                    #------------------------------------------------
                    #can move right
                    #------------------------------------------------
                    r2 = r0+1
                    kidState.append(createState(current_state, r0, c0, r2, c0))
                if c0-1>=0:
                    #------------------------------------------------
                    #can move down
                    #------------------------------------------------
                    c1 = c0-1
                    kidState.append(createState(current_state, r0, c0, r0, c1))
                if c0+1<=2:
                    #------------------------------------------------
                    #can move up
                    #------------------------------------------------
                    c2 = c0+1
                    kidState.append(createState(current_state, r0, c0, r0, c2))
                
                for x in range(9):
                    if random.randint(2,99)%2 ==1:
                        shift = kidState.pop()
                        kidState = [shift] + kidState
                
                # ^^^ is to remove bias from move order logic for searches
                
                for state in kidState:
                    #------------------------------------------------
                    #can move left
                    #------------------------------------------------
                    if state == GOAL_STATE:
                        #------------------------------------------------
                        #no need to go any further
                        #------------------------------------------------
                        kid = Node(data=state)
                        parent.addChild(kid)
                        return
                    
                    elif parent.parent is None:
                        #------------------------------------------------
                        #first generation from root
                        #------------------------------------------------
                        kid = Node(data=state)
                        parent.addChild(kid)
                        gen.append(kid)
                        
                    elif state != parent.parent.data:
                        #------------------------------------------------
                        #removing kids that are same move as grandparent
                        #reducing copies deduces branching affect 
                        #helps optimize searches
                        #------------------------------------------------
                        kid = Node(data=state)
                        parent.addChild(kid)
                        
                        gen.append(kid)
                    #thinking randomize placement 2
            mem.append(gen)
            que = gen
            if len(mem) >= maxdepth:
                que=[]

def createTestData():
    boards = list(itertools.permutations([2, 4, 3, 1, 5, 6, 7, 8, 0]))
    allboards = {}
    nBoardCount = 0
    nCounter = 0
    for x in boards:
        nBoardCount += 1
        boardList = []
        mylist = []
        count = 1
        for nIndex in x:
            mylist.append(nIndex)
            if count%3 == 0:
                boardList.append(mylist)
                mylist = []
            count += 1
        allboards['board' + str(nBoardCount)] = boardList
    playable = {}
    boardcounts = {}
    boardcount = 0
    for key in allboards.keys():
        boardcount +=1 # start at on
        result = play(allboards[key])
        if result!=0:
            nCounter += 1
            boardcounts['board'+str(boardcount)+'_moves']=result
            playable['board'+str(boardcount)]=allboards[key]
            print('index: ' + str(nCounter) + ' Result: ' + str(result) + '\r\n')
            if boardcount%20==0:
            #during testing, large tree depths filled RAM 
                gc.collect()
            if nCounter > 400:
                break;
    savedata(playable, '8puzzle_boards3_test_outofOrder')#playable boards
    savedata(boardcounts, '8puzzle_board_moves3_test_outOfOrder')
        

def createPlayableBoards():
    boards = list(itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8]))
    #all possible board configurations
    allboards = {}
    boardcount = 0
    for x in boards:
        boardcount +=1
        boardlist = []
        mylist = []
        count = 1
        for index in x:
            #configuring the boards as 3x3 list
            mylist.append(index)
            if count%3==0:
                boardlist.append(mylist)
                mylist = []
            count +=1
        allboards['board'+str(boardcount)]=boardlist
    
    playable = {}
    boardcounts = {}
    boardcount=0
    nCounter = 0
    for key in allboards.keys():
        #now looking for the boards which have a solution
        #using default limited depth of 10 to save time and space
        #result = play(allboards[key])
        result = play(allboards[key])
        if result!=0:
            nCounter += 1
            boardcount +=1
            boardcounts['board'+str(boardcount)+'_moves']=result
            playable['board'+str(boardcount)]=allboards[key]
            print('index: ' + str(nCounter) + 'Result: ' + str(result) + '\r')
            if boardcount%20==0:
            #during testing, large tree depths filled RAM 
                gc.collect()
            if nCounter > 7000:
                break;
    savedata(playable, '8puzzle_boards2')#playable boards
    savedata(boardcounts, '8puzzle_board_moves2')
    # playable boards' number of moves with default
        
def findGameBoards(data):
    #8puzzle_board_moves3_test_outOfOrder
    boardsWithCount= pickle.load(open('8puzzle_board_moves.pickle','rb'))
    allBoardsRan  = pickle.load(open('8puzzle_boards.pickle','rb'))
    nBoardCount = 0
    nTotalMoves = 0
    nTotalOccurances = 0
    print('before data driven')
    for key in allBoardsRan.keys():
        nBoardCount += 1 # start at one
        board = allBoardsRan[key]
        #print(board[0])
        #print(str(boardsWithCount['board'+str(nBoardCount)+'_moves']))
        if board[0] == data:
            nTotalMoves += boardsWithCount['board'+str(nBoardCount)+'_moves']
            nTotalOccurances += 1
    print('Total Moves: ' + str(nTotalMoves) +' Total occurances of '+ str(data) + ': ' + str(nTotalOccurances))
    if nTotalOccurances != 0:
        if (nTotalMoves / nTotalOccurances) > AVERAGE:
            return 1
        else:
            return 0
    else:
        return 1
           
def movesTest(depth=None):
    #given a depth for the tree (depth), go through all the playable boards and
    #create a file for the number of moves taken
    allboards = pickle.load(open('8puzzle_boards3_test.pickle', 'rb'))
    depth = 10 if not depth else depth
         
    boardcounts = {}
    garbagecount=0
    nCounter = 0
    nTotalMovesDepth99 = 0;
    nTotalMovesDepth10 = 0;
    nMoveType = -2;
    for key in allboards.keys():
        tBoard = allboards[key]
        nMoveType = findGameBoards(tBoard[0])
        moves = play(allboards[key], treedepth=depth)
        nTotalMovesDepth10 = nTotalMovesDepth10 + moves;
        moves2 = play(allboards[key], treedepth=99)
        nTotalMovesDepth99 = nTotalMovesDepth99 + moves2;
        search = "BFS" if nMoveType == 0 else "DFS"
        print("Index: %s Moves: %s MoveType: %s" % (key, moves, search))
        if moves==0:
            continue
        boardcounts[key+'_moves']=moves
        garbagecount +=1
        nCounter += 1
        if garbagecount%5==0:
            #during testing, large tree depths filled RAM 
            gc.collect()
            #Caleb's add to stop at 1000
        if nCounter > 500:
            break
    #print(moves2/moves)
    print("Moves2: %s\r\n" % nTotalMovesDepth99)
    print("Moves1: %s\r\n" % nTotalMovesDepth10)
    print(nTotalMovesDepth10/nTotalMovesDepth99)
    
    #savedata(boardcounts, "%s%s" % ('8puzzle_board_moves_depth_10', "_FirstRun"))
def findAverage():
    boardsWithCount = pickle.load(open('8puzzle_board_moves.pickle','rb'))
    nBoardCount = 0
    nTotalMoves = 0
    nCounter = 0
    for key in boardsWithCount.keys():
        nBoardCount += 1
        nTotalMoves += boardsWithCount['board'+str(nBoardCount)+'_moves']
        nCounter += 1
        if nCounter >= 720: # cant go past this because of mathematics
            break
    print(' average: ' + str(nTotalMoves / nBoardCount))
    return nTotalMoves / nBoardCount
    
def wrapper():
    # if findGameBoards == 1 do DFS, otherwise do the BFS
    #given a depth for the tree (depth), go through all the playable boards and
    #create a file for the number of moves taken
    allboards = pickle.load(open('8puzzle_boards.pickle', 'rb'))
    garbagecount=0
    nCounter = 0
    nTotalMovesDepth99 = 0
    nTotalMovesDepth10 = 0
    ratio = 0
    nMoveType = -2
    for key in allboards.keys():
        nCounter += 1
        tBoard = allboards[key] # get the board type
        nMoveType = findGameBoards(tBoard[0]) # send the first three data points to this func
        moves = playWithAlgorithm(allboards[key], 10, nMoveType)
        nTotalMovesDepth10 += moves
        moves2 = play(allboards[key], treedepth=99) # regular play against what we had before
        nTotalMovesDepth99 += moves2
        ratio += moves/moves2
        search = "BFS" if nMoveType == 0 else "DFS"
        print("Index: %s Moves: %s MoveType: %s" % (key, moves, search))
        if moves==0 or moves2==0:
            continue
        garbagecount +=1
        if garbagecount%5==0:
            #during testing, large tree depths filled RAM 
            gc.collect()
        #Caleb's add to stop at 500
        if nCounter > 100:
            break
    ratio = ratio/nCounter
    print("Moves without ai: %s\r\n" % nTotalMovesDepth99)
    print("Moves with algorithm: %s\r\n" % nTotalMovesDepth10)
    print("ratio of AI/Optimal ",ratio)
        
def savedata(data, fname):
    #nfile = fname + '.pickle'  
    #changed by Caleb due to some odd string concat error.  So far resolved. and moving forward. 4/14/2018
    nfile = "%s%s" % (fname, '.pickle')      
    pickle_out = open(nfile,'wb')#'wb' writing the pickled dataframe as bytes
    pickle.dump(data, pickle_out)#dumping the bytes to open pickle file
    pickle_out.close()
#data = pickle.load(open('filename.pickle', 'rb'))







