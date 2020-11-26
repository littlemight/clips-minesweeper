import clips
import os
import re
from board import Board
from constant import Constant, is_bomb, is_safe, is_undef

class Bruteforce():
    def __init__(self, board):
        self.board = board
        self.adjList = [ [0] * self.board.size for i in range(self.board.size) ]
        for i in range(self.board.size):
            for j in range(self.board.size):
                temp = []
                for ni, nj in self.board.adjList[i][j]:
                    if (self.board.board[i][j] == Constant.UNDEF and is_safe(self.board.board[ni][nj])):
                        temp.append((ni, nj))
                    elif (is_safe(self.board.board[i][j]) and self.board.board[ni][nj] == Constant.UNDEF):
                        temp.append((ni, nj))
                self.adjList[i][j] = temp

        self.visited = [ [False] * self.board.size for i in range(self.board.size) ]

    def get_CC(self, x, y, all_node):
        if (self.visited[x][y]):
            return
        self.visited[x][y] = True
        all_node.append((x, y))
        for ni, nj in self.adjList[x][y]:
            self.get_CC(ni, nj, all_node)

    def solve(self, x, y):
        all_node = []
        slot_node = []
        safe_node = []

        solution = None
        counter = 0

        ret = []
        self.get_CC(x, y, all_node)
        if (len(all_node) == 1):
            return ret
        for x, y in all_node:
            if (self.board.board[x][y] == Constant.UNDEF):
                slot_node.append((x, y))
            else:
                safe_node.append((x, y))
        
        if (len(slot_node) > 15):
            return ret
        
        n = len(slot_node)
        val = [ [0] * self.board.size for i in range(self.board.size) ]
        for x, y in safe_node:
            for ni, nj in self.board.adjList[x][y]:
                if (self.board.board[ni][nj] == Constant.BOMB):
                    val[x][y] += 1

        for mask in range(1, (1 << n)):
            for i in range(n):
                if (mask & (1 << i)):
                    x, y = slot_node[i]
                    for ni, nj in self.adjList[x][y]:
                        val[ni][nj] += 1

            ok = True
            for x, y in safe_node:
                if (val[x][y] == self.board.board[x][y]):
                    continue
                ok = False
                break
            if (ok):
                counter += 1
                if (counter == 1):
                    solution = mask
                else:
                    return ret
            for i in range(n):
                if (mask & (1 << i)):
                    x, y = slot_node[i]
                    for ni, nj in self.adjList[x][y]:
                        val[ni][nj] -= 1

        if (counter != 1):
            return ret
        
        for i in range(n):
            x, y = slot_node[i]
            if (self.board.board[x][y] == Constant.UNDEF):
                if (solution & (1 << i)):
                    ret.append(self.board.make_assert(x, y, 1))
                else:
                    ret.append(self.board.make_assert(x, y, 0))
            if (len(ret)):
                break
        return ret

    def run(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                if (self.visited[i][j]):
                    continue
                prog = self.solve(i, j)
                if (len(prog) > 0):
                    return prog
        return ([])
