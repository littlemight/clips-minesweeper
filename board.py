import clips
import constant
import os
import re
from constant import Constant, is_bomb, is_safe, is_undef

class Board():
    """
        Board permainan berada di atribut board.
        Nilai pada board[i][j] merepresentasikan state pada sel.
            -2 = unknown/undef
            -1 = flagged
            0, 1, 2, 3, 4 = safe cell

        endState merepresentasikan board jika permainan selesai, dan
        atribut ini digunakan untuk menyimpan hasil precompute.
    """
    def __init__(self, size, bombCnt, bomb):
        self.size = size
        self.bombCnt = bombCnt
        self.board = []
        self.endState = [ [0] * size for i in range(size) ]
        for i in range(size):
            temp = []
            for j in range(size):
                temp.append(Constant.UNDEF)
            self.board.append(temp)

        self.bombPos = []
        for x in bomb:
            self.bombPos.append(x)
            self.endState[x[0]][x[1]] = Constant.BOMB

        self.adjList = [ [0] * size for i in range(size) ]
        for i in range(size):
            for j in range(size):
                temp = []
                for deli in range(-1, 2):
                    for delj in range(-1, 2):
                        if (deli == 0 and delj == 0):
                            continue
                        ni = i + deli
                        nj = j + delj
                        if (self.in_range(ni, nj)):
                            temp.append((ni, nj))
                self.adjList[i][j] = temp

        for i in range(size):
            for j in range(size):
                if (self.endState[i][j] == Constant.BOMB):
                    continue
                for ni, nj in self.adjList[i][j]:
                    if (self.endState[ni][nj] == Constant.BOMB):
                        self.endState[i][j] += 1

        self.bombFound = []

    def in_range(self, i, j):
        return 0 <= i < self.size and 0 <= j < self.size

    def val2char(self, val):
        if (val == -1):
            return 'V'
        elif (val == -2):
            return 'X'
        else:
            return val

    def to_string(self):
        ret = ''
        for i in range(self.size):
            # ret += ''.join(f'{x:3}' for x in self.board[i]) + '\n'
            ret += ''.join(f'  {self.val2char(x)}' for x in self.board[i]) + '\n'
        return ret
    
    # prekondisi: posisi (i, j) bukan tempat bomb
    def dfs_board(self, i, j):
        assert(self.endState[i][j] != Constant.BOMB)
        self.board[i][j] = self.endState[i][j]
        if (self.board[i][j] != 0):
            return

        for ni, nj in self.adjList[i][j]:
            if (self.board[ni][nj] != -2):
                continue
            self.dfs_board(ni, nj)
    
    # digunakan untuk menaruh flag atau menekan sel yang dianggap aman pada sel (i, j)
    # jika ingin menaruh bom -> putbomb = True
    def make_assert(self, i, j, putbomb):
        if (putbomb):
            assert(self.endState[i][j] == Constant.BOMB)
            self.board[i][j] = Constant.BOMB
            self.bombFound.append((i, j))
        else:
            self.dfs_board(i, j)
        return (i, j)