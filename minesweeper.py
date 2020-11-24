import clips
import constant
import os
from constant import Constant, is_bomb, is_safe, is_undef

class Board():
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

        for i in range(size):
            for j in range(size):
                if (self.endState[i][j] == Constant.BOMB):
                    continue
                for deli in range(-1, 2):
                    for delj in range(-1, 2):
                        ni = i + deli
                        nj = j + delj
                        if (i == ni and j == nj):
                            continue
                        if (not self.in_range(ni, nj)):
                            continue
                        if (self.endState[ni][nj] == Constant.BOMB):
                            self.endState[i][j] += 1

        self.bombFound = []

    def in_range(self, i, j):
        return 0 <= i < self.size and 0 <= j < self.size

    def to_string(self):
        ret = ''
        for i in range(self.size):
            for j in range(self.size):
                ret += str(self.board[i][j])
                if (j < self.size - 1):
                    ret += ' '
                else:
                    ret += '\n'
        return ret
    
    # prekondisi: posisi (i, j) bukan tempat bomb
    def dfs_board(self, i, j):
        assert(self.endState[i][j] != Constant.BOMB)
        self.board[i][j] = self.endState[i][j]
        if (self.board[i][j] != 0):
            return
        for deli in range(-1, 2):
            for delj in range(-1, 2):
                if (deli == 0 and delj == 0):
                    continue
                ni = i + deli
                nj = j + delj
                if (not self.in_range(ni, nj)):
                    continue
                if (self.board[ni][nj] != -2):
                    continue

                self.dfs_board(ni, nj)
    
    def make_assert(self, i, j, putbomb):
        if (putbomb):
            assert(self.endState[i][j] == Constant.BOMB)
            self.board[i][j] = Constant.BOMB
            self.bombFound.append((i, j))
        else:
            self.dfs_board(i, j)

    def count_bomb(self, i, j):
        ret = 0
        for deli in range(-1, 2):
            for delj in range(-1, 2):
                if (i == 0 and j == 0):
                    continue
                ni = i + deli
                nj = j + delj
                if (not self.in_range(ni, nj)):
                    continue
                if (self.board[ni][nj] == Constant.BOMB):
                    ret += 1
        return ret

    def count_slot(self, i, j):
        ret = 0
        for deli in range(-1, 2):
            for delj in range(-1, 2):
                if (i == 0 and j == 0):
                    continue
                ni = i + deli
                nj = j + delj
                if (not self.in_range(ni, nj)):
                    continue
                if (self.board[ni][nj] == Constant.UNDEF):
                    ret += 1
        return ret
    
    def find_bomb(self):
        env = clips.Environment()
        template_index = '-1'
        for i in range(self.size + 1):
            template_index += ' ' + str(i)

        template_string = """
            (deftemplate bomb-pos
                (slot x (type NUMBER))
                (slot y (type NUMBER))
            )
        """
        env.build(template_string)
        template_string = """
            (deftemplate empty-slot
                (slot x (type NUMBER))
                (slot y (type NUMBER))
            )
        """
        env.build(template_string)
        template_string = """
            (deftemplate safe-pos
                (slot x (type NUMBER))
                (slot y (type NUMBER))
                (slot val (type NUMBER))
            )
        """
        env.build(template_string)
        template_string = """
            (deftemplate is-safe
                (slot x (type NUMBER))
                (slot y (type NUMBER))
            )
        """
        env.build(template_string)
        template_string = """
            (deftemplate is-unsafe
                (slot x (type NUMBER))
                (slot y (type NUMBER))
            )
        """
        env.build(template_string)

        template_string = '(index-x ' + template_index + ')'
        env.assert_string(template_string)
        
        template_string = '(index-y ' + template_index + ')'
        env.assert_string(template_string)

        template = env.find_template('bomb-pos')
        for x in self.bombFound:
            new_fact = template.new_fact()
            new_fact['x'] = x[0]
            new_fact['y'] = x[1]
            new_fact.assertit()

        template = env.find_template('empty-slot')
        for i in range(self.size):
            for j in range(self.size):
                if (self.board[i][j] != Constant.UNDEF):
                    continue
                new_fact = template.new_fact()
                new_fact['x'] = i
                new_fact['y'] = j
                new_fact.assertit()
        
        template = env.find_template('safe-pos')
        for i in range(self.size):
            for j in range(self.size):
                if (not is_safe(self.board[i][j])):
                    continue
                new_fact = template.new_fact()
                new_fact['x'] = i
                new_fact['y'] = j
                new_fact['val'] = self.board[i][j]
                new_fact.assertit()



        # for fact in env.facts():
        #     print(fact)

n = int(input())
bombCnt = int(input())
bombPos = []
for i in range(bombCnt):
    x, y = input().split(',')
    x = int(x)
    y = int(y)
    bombPos.append((x, y))

board = Board(n, bombCnt, bombPos)
board.make_assert(0, 0, 0)
print(board.to_string())
