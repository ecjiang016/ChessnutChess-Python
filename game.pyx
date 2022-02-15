# distutils: language = c++

"""
Board is 1D NumPy memory view

Piece type numbers:
- Pawn: 1
- Knight: 2
- Bishop: 3
- Rook: 4
- Queen: 5
- King: 6
Positive for white, negative for Black
"""

import numpy as np
from libcpp.vector cimport vector
from cython.parallel cimport prange
from libc.stdio cimport printf

cdef class Game:
    cdef int [:] board
    def __cinit__(self,  int [:] board):
        self.board = board

    cdef move(self, int old_x, int old_y, int new_x, int new_y):
        cdef int old_coord = old_y * 8 + old_x
        cdef int new_coord = new_y * 8 + new_x
        cdef int piece = self.board[old_coord]
        
        #Move the piece on the board
        self.board[old_coord] = 0
        self.board[new_coord] = piece


cdef class Rook:
    cdef int pos
    cdef int color #1 for white, -1 for black

    def __cinit__(self, int pos, int color):
        self.pos = pos
        self.color = color

    cdef possible_moves(self, int [64] board):
        cdef int [4] directions = [8, -8, 1, -1]
        cdef int x = self.pos % 8
        cdef int y = self.pos // 8
        cdef int [4] spaces_to_edge = [7-y, y, 7-x, x]

        cdef int d
        cdef vector[int] possible_spaces

        cdef int space
        cdef int check_pos #Position being checked
        cdef int color_pos #Positive if piece is friendy, negative if not
        for d in prange(4, nogil=True): #Loop over all directions
            for space in range(1, spaces_to_edge[d]+1): #Loop until you hit a opposing piece
                check_pos = space * directions[d] + self.pos
                color_pos = board[self.pos] * self.color
                if color_pos > 0: #They are the same color
                    break
                elif color_pos < 0:
                    possible_spaces.push_back(check_pos) #Can capture
                    break
                else:
                    possible_spaces.push_back(check_pos)

        return possible_spaces

    def py_moves(self, board):
        cdef vector[int] ps
        cdef int [64] cboard = board
        return self.possible_moves(cboard)
