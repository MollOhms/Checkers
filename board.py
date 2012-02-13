# coding: utf-8
# Game board. It needs a height and a width in order
# to be instantiated
class board(object):
    BLACK = 1
    WHITE = 0
    NOTDONE = -1
    def __init__(self, height, width):
        # Set the height and width of the game board
        self.width = width
        self.height = height
        # Create two lists which will contain the pieces each player posesses
        self.blacklist = []
        self.whitelist = []
        # Set default piece positions
        for i in range(width):
            self.blacklist.append((i, (i+1)%2))
            self.whitelist.append((i, height - (i%2) - 1))
        # boardState contains the current state of the board for printing/eval
        self.boardState = [[' '] * self.width for x in range(self.height)]
        self.gameWon = self.NOTDONE
        self.turn = self.WHITE
        self.max_depth = 4
    
    # Returns True if there is a piece at that position 
    def contains(self, x, y):
        if ((x,y) in self.blacklist):
            return True
        elif ((x,y) in self.whitelist):
            return True
        else:
            return False
    
    # Generate an iterator for all of the moves
    def iterWhiteMoves(self):
        for piece in self.whitelist:
            for move in self.iterWhitePiece(piece):
                yield move
                
    def iterBlackMoves(self):
        for piece in self.blacklist:
            for move in self.iterBlackPiece(piece):
                yield move
                
    def iterWhitePiece(self, piece):
        """NEWSHIT"""            
        return self.iterBoth(piece, ((-1,-1),(1,-1)))
    
    def iterBlackPiece(self, piece):
        """NEWSHIT"""
        return self.iterBoth(piece, ((-1,1),(1,1)))

    def iterBoth(self, piece, moves):
        for move in moves:
            targetx = piece[0] + move[0]
            targety = piece[1] + move[1]
            if targetx < 0 or targetx >= self.width or targety < 0 or targety >= self.height:
                continue
            target = (targetx, targety)
            black = target in self.blacklist
            white = target in self.whitelist
            if not black and not white:
                yield (piece, target, self.NOTDONE)
            else:
                if self.turn == self.BLACK and black:
                    continue
                elif self.turn == self.WHITE and white:
                    continue
                else:
                    pass
    
    # Creates an iterable list of moves for a white piece
    def iterWhitePieceOld(self, piece):
        # White pieces can only move up the board
        possibleMove1 = (piece[0]+1, piece[1]-1)
        possibleMove2 = (piece[0]-1, piece[1]-1)
        for move in (possibleMove1, possibleMove2):
            # The move must not go outside the bounds of the board or move to 
            # a location where another piece is already located
            if (move[0] > -1 and move[0] < self.width):
                if (move[1] > -1 and move[1] < self.height):
                    if not(self.contains(move[0], move[1])):
                        yield (piece, move, self.NOTDONE)
                    # Jump condition (left)
                    elif (not(self.contains(move[0]-1, move[1]-1)) and (piece[0] == (move[0]+1)) ):                        
                        if (move[0] > 0 and move[0]-1 < self.width):
                            if (move[1] > 0 and move[1]-1 < self.height):
                                yield (piece, (move[0]-1, move[1]-1), self.WHITE)
                    # Jump condition (right)
                    elif (not(self.contains(move[0]+1, move[1]-1)) and (piece[0] == (move[0]-1)) ):
                        if (move[0] > -1 and move[0]+1 < self.width):
                            if (move[1] > -1 and move[1]-1 < self.height):
                                yield (piece, (move[0]+1, move[1]-1), self.WHITE)
#                    else:
#                        print move, "was eliminated from interWhitePiece"

    # Creates an iterable list of moves for a black piece
    def iterBlackPieceOld(self, piece):
        # White pieces can only move up the board
        possibleMove1 = (piece[0]+1, piece[1]+1)
        possibleMove2 = (piece[0]-1, piece[1]+1)
        for move in (possibleMove1, possibleMove2):
            if (move[0] > -1 and move[0] < self.width):
                if (move[1] > -1 and move[1] < self.height):
                    if not(self.contains(move[0], move[1])):
                        yield (piece, move, self.NOTDONE)
                    # We can only jump White pieces
                    elif move in self.whitelist:
                        # Jump condition (left)
                        if (not(self.contains(move[0]-1, move[1]+1)) and (piece[0] == (move[0]+1)) ):
                            if (move[0] > 0 and move[0]-1 < self.width):
                                if (move[1] > 0 and move[1]+1 < self.height):
                                    yield (piece, (move[0]-1, move[1]+1), self.BLACK)
                        # Jump condition (right)
                        elif (not(self.contains(move[0]+1, move[1]+1)) and (piece[0] == (move[0]-1))):
                            if (move[0] > -1 and move[0]+1 < self.width):
                                if (move[1] > -1 and move[1]+1 < self.height):
                                    yield (piece, (move[0]+1, move[1]+1), self.BLACK)
#                    else:
#                        print move, "was eliminated from interBlackPiece"
    
    # Updates the array containing the board to reflect the current state
    # of the pieces on the board
    def updateBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                self.boardState[i][j] = " "
        for piece in self.blacklist:
            self.boardState[piece[1]][piece[0]] = u'◆'
        for piece in self.whitelist:
            self.boardState[piece[1]][piece[0]] = u'◇'

#############
#############
#############
    def getWin(self):
        return self.g
    
    def setWin(self, val):
#        if val == 0:
#            raise Exception("Game won by white")
        self.g = val

    gameWon=property(getWin, setWin)
#############
#############
#############

    # Move a blackPiece from one spot to another
    def moveBlack(self, moveFrom, moveTo, winLoss):
        if (moveTo[0] > -1 and moveTo[0] < self.width):
            if (moveTo[1] > -1 and moveTo[1] < self.height):
                if not(self.contains(moveTo[0], moveTo[1])):
                    self.blacklist[self.blacklist.index(moveFrom)] = moveTo
                    self.printBoard()
                    self.turn = self.WHITE
                    self.gameWon = winLoss
                else:
                    print "Black Piece", moveFrom, "moving to", moveTo
                    raise Exception("MoveTo location already contains a piece!")
        
    def moveWhite(self, moveFrom, moveTo, winLoss):
        if (moveTo[0] > -1 and moveTo[0] < self.width):
            if (moveTo[1] > -1 and moveTo[1] < self.height):
                if not(self.contains(moveTo[0], moveTo[1])):
                    self.whitelist[self.whitelist.index(moveFrom)] = moveTo
                    self.printBoard()
                    self.turn = self.BLACK
                    self.gameWon = winLoss
                else:
                    print "White Piece", moveFrom, "moving to", moveTo
                    raise Exception("MoveTo location already contains a piece!")
            else:
                print "I'M A DICK AND I TRIED TO MOVE OUT OF BOUNDS! FALALAH!"
        else:
            print "I'M A DICK AND I TRIED TO MOVE OUT OF BOUNDS! FALALAH!"
    
    def printBoard(self):
        print unicode(self)
        
    def __unicode__(self):
        # Updates Game board
        self.updateBoard()
        lines = []
        # This prints the numbers at the top of the Game Board
        lines.append('    ' + '   '.join(map(str, range(self.width))))
        # Prints the top of the gameboard in unicode
        lines.append(u'  ╭' + (u'───┬' * (self.width-1)) + u'───╮')
        
        # Print the boards rows
        for num, row in enumerate(self.boardState[:-1]):
            lines.append(chr(num+65) + u' │ ' + u' │ '.join(row) + u' │')
#            lines.append(str(num) + u' │ ' + u' │ '.join(row) + u' │')
            lines.append(u'  ├' + (u'───┼' * (self.width-1)) + u'───┤')
        
        #Print the last row
        lines.append(chr(self.height+64) + u' │ ' + u' │ '.join(self.boardState[-1]) + u' │')
#        lines.append(str(self.height-1) + u' │ ' + u' │ '.join(self.boardState[-1]) + u' │')

        # Prints the final line in the board
        lines.append(u'  ╰' + (u'───┴' * (self.width-1)) + u'───╯')
        return '\n'.join(lines)

    # Move without printing
    def moveSilentBlack(self, piece, move, winLoss): 
        if ((move[0] > -1 and move[0] < self.width)
            and (move[1] > -1 and move[1] < self.height)
            and not(self.contains(move[0], move[1]))):
                self.blacklist[self.blacklist.index(piece)] = move
                self.updateBoard()
                self.turn = self.WHITE
                self.gameWon = winLoss
        else:
            raise Exception("Not a valid black move!")
        
    def moveSilentWhite(self, piece, move, winLoss):
        if ((move[0] > -1 and move[0] < self.width)
            and (move[1] > -1 and move[1] < self.height)
            and not(self.contains(move[0], move[1]))):
                self.whitelist[self.whitelist.index(piece)] = move
                self.updateBoard()
                self.turn = self.BLACK
                self.gameWon = winLoss
        else:
            raise Exception("Not a valid white move!")
