from time import sleep
from math import inf
import random


class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                    ['_', '_', '_', '_', '_', '_', '_', '_', '_']
                    ]

        self.globalBoard = [
                        ['_','_','_'],
                        ['_','_','_'],
                        ['_','_','_']
                        ]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'
        self.noPlayer = '_'
        self.maxDepth = 3
        self.tieSign = 'T'
        # The start indexes of each local board
        self.globalIdx = [(0, 0), (0, 3), (0, 6), (3, 0),
                           (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        # Start local board index for reflex agent playing
        self.startBoardIdx = 4
        # utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility = 10000
        self.twoInARowMaxUtility = 500
        self.preventThreeInARowMaxUtility = 100
        self.cornerMaxUtility = 30
        self.centerMaxUtility = 40

        self.winnerMinUtility = -10000
        self.twoInARowMinUtility = -100
        self.preventThreeInARowMinUtility = -500
        self.cornerMinUtility = -30
        self.centerMinUtility = -40

        self.expandedNodes = 0
        self.expandedNodesList = []
        self.currPlayer = True

        # customized variables
        self.threeInARow = False
        self.maxEvaluation = self.evaluatePredifined
        self.minEvaluation = self.evaluatePredifined
        self.maxOptimized = False
        self.minOptimized = False

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row])
              for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row])
              for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row])
              for row in self.board[6:9]])+'\n')

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        utility_total = 0
        num_corners = 0
        player = self.maxPlayer if isMax else self.minPlayer
        for i in range(9):
            local_board = self.globalIdx[i]
            corners = [(local_board[0] + 0, local_board[1] + 0),
                       (local_board[0] + 0, local_board[1] + 2),
                       (local_board[0] + 2, local_board[1] + 0),
                       (local_board[0] + 2, local_board[1] + 2)]
            for corner in corners:
                if self.board[corner[0]][corner[1]] == player:
                    num_corners += 1
            utility = self.calculateLocalBoardUtility(i, isMax)
            if abs(utility) == self.winnerMaxUtility:
                return utility
            utility_total += utility
        # return total utility score
        if utility_total == 0:
            return num_corners * self.cornerMaxUtility if isMax else num_corners * self.cornerMinUtility
        return utility_total


    # apply first rule and second rule
    def calculateLocalBoardUtility(self, boardIdx, isMax):
        utility = 0
        local_board = self.globalIdx[boardIdx]
        # rows to be checked
        rows = [(self.board[local_board[0] + 0][local_board[1] + 0],
                self.board[local_board[0] + 1][local_board[1] + 1],
                self.board[local_board[0] + 2][local_board[1] + 2]),
                (self.board[local_board[0] + 0][local_board[1] + 2],
                self.board[local_board[0] + 1][local_board[1] + 1],
                self.board[local_board[0] + 2][local_board[1] + 0])]
        for i in range(3):
            rows.append((self.board[local_board[0] + i][local_board[1] + 0],
                        self.board[local_board[0] + i][local_board[1] + 1],
                        self.board[local_board[0] + i][local_board[1] + 2]))
            rows.append((self.board[local_board[0] + 0][local_board[1] + i],
                        self.board[local_board[0] + 1][local_board[1] + i],
                        self.board[local_board[0] + 2][local_board[1] + i]))
        # check each of the rows
        for row in rows:
            self_freq, enemy_freq = self.frequency(row, isMax)
            if self_freq == 3:
                return self.winnerMaxUtility if isMax else self.winnerMinUtility
            elif self_freq == 2 and enemy_freq == 0:
                utility += self.twoInARowMaxUtility if isMax else self.twoInARowMinUtility
            elif self_freq == 1 and enemy_freq == 2:
                utility += self.preventThreeInARowMaxUtility if isMax else self.preventThreeInARowMinUtility
        return utility



    # Calculate the frequencies of both player itself and its enemy
    def frequency(self, pts, isMax):
        self_player = self.maxPlayer if isMax else self.minPlayer
        enemy_player = self.minPlayer if isMax else self.maxPlayer
        self_freq = 0
        enemy_freq = 0
        for pt in pts:
            if pt == self_player:
                self_freq += 1
            elif pt == enemy_player:
                enemy_freq += 1
        return self_freq, enemy_freq



    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # self_form, enemy_form, self_block, enemy_block, self_corner, enemey_corner
        offensiveUtilities = [500, -300, 100, -200, 30, -20]
        defensiveUtilities = [300, -500, 200, -100, 20, -30]
        utility_total = 0
        selfCorners = 0
        enemyCorners = 0
        useCornerUtility = True
        player = self.maxPlayer if isMax else self.minPlayer
        for boardIndex in range(9):
            local_board = self.globalIdx[boardIndex]
            corners = [(local_board[0] + 0, local_board[1] + 0),
                       (local_board[0] + 0, local_board[1] + 2),
                       (local_board[0] + 2, local_board[1] + 0),
                       (local_board[0] + 2, local_board[1] + 2)]
            for corner in corners:
                p = self.board[corner[0]][corner[1]]
                if p == player:
                    selfCorners += 1
                elif p != self.noPlayer:
                    enemyCorners += 1
            utility = 0
            # rows to be checked
            rows = [(self.board[local_board[0] + 0][local_board[1] + 0],
                    self.board[local_board[0] + 1][local_board[1] + 1],
                    self.board[local_board[0] + 2][local_board[1] + 2]),
                    (self.board[local_board[0] + 0][local_board[1] + 2],
                    self.board[local_board[0] + 1][local_board[1] + 1],
                    self.board[local_board[0] + 2][local_board[1] + 0])]
            for i in range(3):
                rows.append((self.board[local_board[0] + i][local_board[1] + 0],
                            self.board[local_board[0] + i][local_board[1] + 1],
                            self.board[local_board[0] + i][local_board[1] + 2]))
                rows.append((self.board[local_board[0] + 0][local_board[1] + i],
                            self.board[local_board[0] + 1][local_board[1] + i],
                            self.board[local_board[0] + 2][local_board[1] + i]))
            # check each of the rows
            for row in rows:
                self_freq, enemy_freq = self.frequency(row, isMax)
                if self_freq == 3:
                    return self.winnerMaxUtility if isMax else self.winnerMinUtility
                elif enemy_freq == 3:
                    return self.winnerMinUtility if isMax else self.winnerMaxUtility
                elif self_freq == 2 and enemy_freq == 0:
                    useCornerUtility = False
                    utility += defensiveUtilities[0] if isMax else offensiveUtilities[0]
                elif self_freq == 0 and enemy_freq == 2:
                    useCornerUtility = False
                    utility += defensiveUtilities[1] if isMax else offensiveUtilities[1]
                elif self_freq == 1 and enemy_freq == 2:
                    useCornerUtility = False
                    utility += defensiveUtilities[2] if isMax else offensiveUtilities[2]
                elif self_freq == 2 and enemy_freq == 1:
                    useCornerUtility = False
                    utility += defensiveUtilities[3] if isMax else offensiveUtilities[3]
            utility_total += utility
        # return total utility score
        if useCornerUtility:
            if isMax:
                utility_total = selfCorners * offensiveUtilities[4] + enemyCorners * offensiveUtilities[5]
            else:
                utility_total = selfCorners * defensiveUtilities[4] + enemyCorners * defensiveUtilities[5]
        return utility_total



    # Check if there is any legal moves left
    # @Return: True if still has legal moves, false otherwise.
    def checkMovesLeft(self):
        availableMoves = self.getAvailableMoves(self.startBoardIdx)
        return len(availableMoves) > 0


    # Get all remaining legal moves
    def getAvailableMoves(self, boardIdx):
        utility = self.calculateLocalBoardUtility(boardIdx, True)
        # if local board is not complete/full
        if abs(utility) != self.winnerMaxUtility:
            availableMoves = self.getLocalAvailableMoves(boardIdx)
            if len(availableMoves) > 0:
                return availableMoves
        availableMoves = []
        # if local board is complete/full, go to any other local board
        for i in range(9):
            if i != boardIdx:
                local = self.getLocalAvailableMoves(i)
                availableMoves.extend(local)
        return availableMoves


    # Get available moved in given local board
    def getLocalAvailableMoves(self, boardIdx):
        availableMoves = []
        localBoard = self.globalIdx[boardIdx]
        for i in range(3):
            for j in range(3):
                if self.board[localBoard[0] + i][localBoard[1] + j] == self.noPlayer:
                    availableMoves.append((localBoard[0] + i, localBoard[1] + j))
        return availableMoves


    # Check whether there is a winner on the board
    # @Return: Termimnal node status for maximizer player
    #  1: maxPlayer win
    #  0: no winner
    # -1: maxPlayer lose
    def checkWinner(self):
        for boardIdx in range(9):
            left_corner = self.globalIdx[boardIdx]
            # diagonals in one of the local board
            rows = [(self.board[left_corner[0] + 0][left_corner[1] + 0],
                    self.board[left_corner[0] + 1][left_corner[1] + 1],
                    self.board[left_corner[0] + 2][left_corner[1] + 2]),
                    (self.board[left_corner[0] + 0][left_corner[1] + 2],
                    self.board[left_corner[0] + 1][left_corner[1] + 1],
                    self.board[left_corner[0] + 2][left_corner[1] + 0])]
            for i in range(3):
                # columns and rows in one of the local board
                rows.append((self.board[left_corner[0] + i][left_corner[1] + 0],
                            self.board[left_corner[0] + i][left_corner[1] + 1],
                            self.board[left_corner[0] + i][left_corner[1] + 2]))
                rows.append((self.board[left_corner[0] + 0][left_corner[1] + i],
                            self.board[left_corner[0] + 1][left_corner[1] + i],
                          self.board[left_corner[0] + 2][left_corner[1] + i]))
            for row in rows:
                # check whether each one of the rows/columns has 3 player in one row
                maxFreq, minFreq = self.frequency(row, True)
                if maxFreq == 3:
                    if not self.threeInARow:
                        return 1
                    else:
                        tempGlobalBoardPos = self.globalBoard[boardIdx//3][boardIdx%3]
                        if tempGlobalBoardPos == self.noPlayer:
                            self.globalBoard[boardIdx // 3][boardIdx % 3] = self.maxPlayer
                elif minFreq == 3:
                    if not self.threeInARow:
                        return -1
                    else:
                        tempGlobalBoardPos = self.globalBoard[boardIdx // 3][boardIdx % 3]
                        if tempGlobalBoardPos == self.noPlayer:
                            self.globalBoard[boardIdx // 3][boardIdx % 3] = self.minPlayer
            if len(self.getLocalAvailableMoves(boardIdx)) == 0 and self.globalBoard[boardIdx // 3][boardIdx % 3] == self.noPlayer:
                self.globalBoard[boardIdx // 3][boardIdx % 3] =self.tieSign
                    
        # check winner board (three-in-row worldwide)
        globalRows = [
                (self.globalBoard[0][0], self.globalBoard[1][1], self.globalBoard[2][2]),
                (self.globalBoard[0][2], self.globalBoard[1][1], self.globalBoard[2][0]),
                (self.globalBoard[0][0], self.globalBoard[0][1], self.globalBoard[0][2]),
                (self.globalBoard[1][0], self.globalBoard[1][1], self.globalBoard[1][2]),
                (self.globalBoard[2][0], self.globalBoard[2][1], self.globalBoard[2][2]),
                (self.globalBoard[0][0], self.globalBoard[1][0], self.globalBoard[2][0]),
                (self.globalBoard[0][1], self.globalBoard[1][1], self.globalBoard[2][1]),
                (self.globalBoard[0][2], self.globalBoard[1][2], self.globalBoard[2][2])
                ]
        for globalRow in globalRows:
            globalMaxFreq, globalmMinFreq = self.frequency(globalRow, True)
            if globalMaxFreq == 3:
                return 1
            elif globalmMinFreq == 3:
                return -1
        check_full = True
        for i in range(3):
            for j in range(3):
                if self.globalBoard[i][j] == self.noPlayer:
                    check_full = False
        if check_full:
            return 100
        return 0


    def alphabeta(self, depth, currBoardIdx, alpha, beta, isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        bestValue, _, _ = self.best_move(depth, currBoardIdx, isMax, 0)
        return bestValue

    def alphabeta_helper(self, currBoard, depth, alpha, beta, isMax):
        player = self.maxPlayer if isMax else self.minPlayer
        alpha = -inf
        beta = inf
        if isMax:
            if self.threeInARow:
                while self.globalBoard[currBoard // 3][currBoard % 3] != self.noPlayer:
                    currBoard = random.randint(0, 8)
            curr_possible_moves = self.getLocalAvailableMoves(currBoard)
            maxEval = -inf
            nodesExplored = 1
            best_move = None
            if len(curr_possible_moves) == 0:
                return best_move, inf, 0
            for curr_move in curr_possible_moves:
                self.setPlayer(curr_move, player)
                if depth == 1:
                    eval = self.maxEvaluation(isMax)
                else:
                    nextBoard = self.nextBoardIndex(curr_move)
                    _, eval, childNodesExplored = self.alphabeta_helper(nextBoard, depth - 1, alpha, beta, False)
                    if eval > alpha:
                        alpha = eval
                    if beta <= alpha and not self.threeInARow:
                        self.setPlayer(curr_move, self.noPlayer)
                        break
                    if beta < alpha and self.threeInARow:
                        self.setPlayer(curr_move, self.noPlayer)
                        break
                    nodesExplored += childNodesExplored
                if eval > maxEval:
                    maxEval = eval
                    best_move = curr_move
                self.setPlayer(curr_move, self.noPlayer)
            return best_move, maxEval, nodesExplored
        else:
            if self.threeInARow:
                while self.globalBoard[currBoard // 3][currBoard % 3] != self.noPlayer:
                    currBoard = random.randint(0, 8)
            curr_possible_moves = self.getLocalAvailableMoves(currBoard)
            minEval = inf
            nodesExplored = 1
            best_move = None
            if len(curr_possible_moves) == 0:
                return best_move, -inf, 0
            for curr_move in curr_possible_moves:
                self.setPlayer(curr_move, player)
                if depth == 1:
                    eval = self.minEvaluation(isMax)
                else:
                    nextBoard = self.nextBoardIndex(curr_move)
                    _, eval, childNodesExplored = self.alphabeta_helper(nextBoard, depth - 1, alpha, beta, True)
                    if eval < beta:
                        beta = eval
                    if beta <= alpha and not self.threeInARow:
                        self.setPlayer(curr_move, self.noPlayer)
                        break
                    if beta < alpha and self.threeInARow:
                        self.setPlayer(curr_move, self.noPlayer)
                        break
                    nodesExplored += childNodesExplored
                if eval < minEval:
                    minEval = eval
                    best_move = curr_move
                self.setPlayer(curr_move, self.noPlayer)
            return best_move, minEval, nodesExplored
    


    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        bestValue, _, _ = self.best_move(self.maxDepth, currBoardIdx, isMax, 1)
        return bestValue


    def minimax_helper(self, currBoard, depth, isMax):
        player = self.maxPlayer if isMax else self.minPlayer
        if isMax:
            curr_possible_moves = self.getLocalAvailableMoves(currBoard)
            maxEval = -inf
            nodesExplored = 1
            best_move = None
            for curr_move in curr_possible_moves:
                self.setPlayer(curr_move, player)
                if depth == 1:
                    eval = self.maxEvaluation(isMax)
                else: 
                    nextBoard = self.nextBoardIndex(curr_move)
                    _, eval, childNodesExplored = self.minimax_helper(nextBoard, depth - 1, False)
                    nodesExplored += childNodesExplored
                if eval > maxEval:
                    maxEval = eval
                    best_move = curr_move
                self.setPlayer(curr_move, self.noPlayer)
            return best_move, maxEval, nodesExplored
        else:
            curr_possible_moves = self.getLocalAvailableMoves(currBoard)
            minEval = inf
            nodesExplored = 1
            best_move = None
            for curr_move in curr_possible_moves:
                self.setPlayer(curr_move, player)
                if depth == 1:
                    eval = self.minEvaluation(isMax)
                else: 
                    nextBoard = self.nextBoardIndex(curr_move)
                    _, eval, childNodesExplored = self.minimax_helper(nextBoard, depth - 1, True)
                    nodesExplored += childNodesExplored
                if eval < minEval:
                    minEval = eval
                    best_move = curr_move
                self.setPlayer(curr_move, self.noPlayer)
            return best_move, minEval, nodesExplored


    def boardIndex(self, pos):
        row = pos[0]//3
        col = pos[1]//3
        return row * 3 + col


    def nextBoardIndex(self, pos):
        row = pos[0] % 3
        col = pos[1] % 3
        return row * 3 + col


    def setPlayer(self, position, player):
        self.board[position[0]][position[1]] = player

    
    def best_move(self, depth, currBoardIdx, isMax, isMiniMax):
        best_move = None
        nodesExplored = 0
        bestValue = 0.0
        if isMiniMax:
            best_move, bestValue, nodesExplored = self.minimax_helper(currBoardIdx, depth, isMax)
        else:
            alpha = -inf
            beta = inf
            best_move, bestValue, nodesExplored = self.alphabeta_helper(currBoardIdx, depth, alpha, beta, isMax)
        return best_move, bestValue, nodesExplored



    def playGamePredifinedAgent(self, maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        self.threeInARow = False
        nextBoardIdx = self.startBoardIdx
        gameBoards = []
        bestMove = []
        bestValue = []
        expandedNodes = []
        isMaxTurn = maxFirst
        gameStatus = self.checkWinner()
        while (gameStatus == 0 and self.checkMovesLeft()):
            isMiniMax = isMinimaxOffensive if isMaxTurn else isMinimaxDefensive
            nextMove, nextValue, nodesExplored = self.best_move(self.maxDepth, nextBoardIdx, isMaxTurn, isMiniMax)
            self.setPlayer(nextMove, self.maxPlayer if isMaxTurn else self.minPlayer)
            nextBoardIdx = self.nextBoardIndex(nextMove)
            bestValue.append(nextValue)
            bestMove.append(nextMove)
            gameBoards.append(self.board)
            isMaxTurn = not isMaxTurn
            gameStatus = self.checkWinner()
            expandedNodes.append(nodesExplored)
        winner = gameStatus
        return gameBoards, bestMove, expandedNodes, bestValue, winner



    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        self.threeInARow = False
        self.minEvaluation = self.evaluateDesigned
        self.minOptimized = True
        nextBoardIdx = random.randint(0, 8)
        gameBoards = []
        bestMove = []
        isMaxTurn = random.choice([True, False])
        gameStatus = self.checkWinner()
        while (gameStatus == 0 and self.checkMovesLeft()):
            searchDepth = self.maxDepth if isMaxTurn else self.maxDepth
            if isMaxTurn:
                nextMove, _, nodesExplored = self.best_move(searchDepth, nextBoardIdx, isMaxTurn, False)
            else:
                nextMove, _, nodesExplored = self.best_move(searchDepth, nextBoardIdx, isMaxTurn, False)
            self.setPlayer(nextMove, self.maxPlayer if isMaxTurn else self.minPlayer)
            nextBoardIdx = self.nextBoardIndex(nextMove)
            bestMove.append(nextMove)
            gameBoards.append(self.board)
            isMaxTurn = not isMaxTurn
            gameStatus = self.checkWinner()
            (self.expandedNodesList).append(nodesExplored)
        winner = gameStatus
        return gameBoards, bestMove, winner



    def playUltimateYourAgent(self):
        self.threeInARow = True
        self.maxEvaluation = self.evaluateDesigned
        self.minEvaluation = self.evaluateDesigned
        nextBoardIdx = random.randint(0, 8)
        gameBoards = []
        bestMove = []
        isMaxTurn = random.choice([True, False])
        gameStatus = self.checkWinner()
        while (gameStatus == 0 and self.checkMovesLeft()):
            if len(self.getLocalAvailableMoves(nextBoardIdx)) == 0:
                nextBoardIdx = random.randint(0, 8)
            if len(self.getLocalAvailableMoves(nextBoardIdx)) == 1:
                nextMove = self.getLocalAvailableMoves(nextBoardIdx)[0]
            else:
                nextMove, _, _ = self.best_move(self.maxDepth, nextBoardIdx, isMaxTurn, False)
            print(nextMove)
            self.setPlayer(nextMove, self.maxPlayer if isMaxTurn else self.minPlayer)
            uttt.printGameBoard()
            nextBoardIdx = self.nextBoardIndex(nextMove)
            bestMove.append(nextMove)
            gameBoards.append(self.board)
            isMaxTurn = not isMaxTurn
            gameStatus = self.checkWinner()
            print(nextBoardIdx)
        winner = gameStatus
        return gameBoards, bestMove, winner



    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        self.minEvaluation = self.evaluateDesigned
        self.minOptimized = True
        nextBoardIdx = random.randint(0, 8)
        gameBoards = []
        bestMove = []
        isMaxTurn = random.choice([True, False])
        gameStatus = self.checkWinner()
        while (gameStatus == 0 and self.checkMovesLeft()):
            searchDepth = self.maxDepth if isMaxTurn else self.maxDepth
            if not isMaxTurn:
                nextMove, _, _ = self.best_move(searchDepth, nextBoardIdx, isMaxTurn, False)
            else:
               valid_human_move = False
               while (not valid_human_move):
                localAvailableMoves = self.getLocalAvailableMoves(nextBoardIdx)
                uttt.printGameBoard()
                print("You are now in board: ", nextBoardIdx)
                print("Your available moves in this board: ", localAvailableMoves)
                move_x = int(input("Enter a number for x: "))
                move_y = int(input("Enter a number for y: "))
                for availableMove in localAvailableMoves:
                    if availableMove == (move_x, move_y):
                        valid_human_move = True
                    if valid_human_move:
                        nextMove = (move_x, move_y)
            self.setPlayer(nextMove, self.maxPlayer if isMaxTurn else self.minPlayer)
            nextBoardIdx = self.nextBoardIndex(nextMove)
            bestMove.append(nextMove)
            gameBoards.append(self.board)
            isMaxTurn = not isMaxTurn
            gameStatus = self.checkWinner()
            self.printGameBoard()
        winner = gameStatus
        return gameBoards, bestMove, winner



def printGameResult(gameBoards, bestMove, expandedNodes, bestValue, winner):
    print("expandedNodes:")
    print(expandedNodes)
    print("bestValue:")
    print(bestValue)
    print("bestMove:")
    print(bestMove)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")



if __name__ =="__main__":

    print("offensive(minimax) vs defensive(minimax) - offensive first")
    uttt = ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(True,True,True)
    printGameResult(gameBoards, bestMove, expandedNodes, bestValue, winner)
    uttt.printGameBoard()
    print("*********************************************")



    print("offensive(minimax) vs defensive(alpha-beta) - offensive first")
    uttt = ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(True,True,False)
    printGameResult(gameBoards, bestMove, expandedNodes, bestValue, winner)
    uttt.printGameBoard()
    print("*********************************************")



    print("offensive(alpha-beta) vs defensive(minimax) - defensive first")
    uttt = ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(False,False,True)
    printGameResult(gameBoards, bestMove, expandedNodes, bestValue, winner)
    uttt.printGameBoard()
    print("*********************************************")



    print("offensive(alpha-beta) vs defensive(alpha-beta) - defensive first")
    uttt = ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(False,False,False)
    printGameResult(gameBoards, bestMove, expandedNodes, bestValue, winner)
    uttt.printGameBoard()
    print("*********************************************")



    rounds = 20
    minWin = 0
    for i in range(rounds):
        print("offensive(alpha-beta) vs custom(alpha-beta) - random first/start board index ({} games)".format(i))
        uttt = ultimateTicTacToe()
        gameBoards, bestMove, winner = uttt.playGameYourAgent()
        if (winner == -1):
            minWin += 1
        # print("bestMove:")
        # print(bestMove)
        uttt.printGameBoard()
        print(uttt.expandedNodesList)
        if winner == 1:
            print("The winner is maxPlayer!!!")
        elif winner == -1:
            print("The winner is minPlayer!!!")
        else:
            print("Tie. No winner:(")
        print("========================================")
    print("Custom agent win rate: {}".format(minWin/rounds))



    rounds = 10
    print("offensive(human) vs defensive(custom)) - random first/start board index ({} games)".format(rounds))
    minWin = 0
    for i in range(rounds):
        uttt = ultimateTicTacToe()
        gameBoards, bestMove, winner = uttt.playGameHuman()
        if (winner == -1):
            minWin += 1
        # print("bestMove:")
        # print(bestMove)
        uttt.printGameBoard()
        if winner == 1:
            print("The winner is human!!!")
        elif winner == -1:
            print("The winner is AI!!!")
        else:
            print("Tie. No winner:(")
        print("========================================")
    print("Custom agent win rate: {}".format(minWin/rounds))


    print("defensive-custom(alpha-beta) vs offensive-custom(alpha-beta) - random first/start board index")
    offensiveWin = 0
    defensiveWin = 0
    rounds = 1
    for i in range(rounds):
        uttt = ultimateTicTacToe()
        gameBoards, bestMove, winner = uttt.playUltimateYourAgent()
        if winner == 1:
            print("The winner is Player 'X' !!!")
            defensiveWin += 1
        elif winner == -1:
            print("The winner is Player 'O' !!!")
            offensiveWin += 1
        elif winner == 100:
            print("Tie. No winner:(")
        uttt.printGameBoard()
        print(uttt.globalBoard)
        print("========================================")
    print("Defensive agent win rate: ", defensiveWin/rounds)
    print("Offensive agent win rate: ", offensiveWin/rounds)