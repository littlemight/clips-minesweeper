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
            ret += ''.join(f'{x:3}' for x in self.board[i]) + '\n'
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
    
    # digunakan untuk menaruh flag atau menekan sel yang dianggap aman pada sel (i, j)
    # jika ingin menaruh bom -> putbomb = True
    def make_assert(self, i, j, putbomb):
        if (putbomb):
            assert(self.endState[i][j] == Constant.BOMB)
            self.board[i][j] = Constant.BOMB
            self.bombFound.append((i, j))
        else:
            self.dfs_board(i, j)



# *** MAIN PROGRAM ***
n = int(input())
bombCnt = int(input())
bombPos = []
for i in range(bombCnt):
    x, y = [int(a) for a in input().split(',')]
    bombPos.append((x, y))

board = Board(n, bombCnt, bombPos)

def count_bomb(i, j):
    ret = 0
    for deli in range(-1, 2):
        for delj in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            ni = i + deli
            nj = j + delj
            if (not board.in_range(ni, nj)):
                continue
            if (board.board[ni][nj] == Constant.BOMB):
                ret += 1
    return ret

def count_slot(i, j):
    ret = 0
    for deli in range(-1, 2):
        for delj in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            ni = i + deli
            nj = j + delj
            if (not board.in_range(ni, nj)):
                continue
            if (board.board[ni][nj] == Constant.UNDEF):
                ret += 1
    return ret

def find_bomb():
    env = clips.Environment()
    env.reset()
    env.clear()
    template_index = ''
    for i in range(board.size):
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
        (deftemplate is-safe-around
            (slot x (type NUMBER))
            (slot y (type NUMBER))
        )
    """
    env.build(template_string)
    template_string = """
        (deftemplate is-unsafe-around
            (slot x (type NUMBER))
            (slot y (type NUMBER))
        )
    """
    env.build(template_string)
    

    template_string = '(index-x ' + template_index + ')'
    env.assert_string(template_string)
    
    template_string = '(index-y ' + template_index + ')'
    env.assert_string(template_string)
    
    env.define_function(count_bomb)
    env.define_function(count_slot)

    rule = """
        (defrule detect-bomb
            (index-x $? ?x $?)
            (index-y $? ?y $?)
            (safe-pos (x ?x) (y ?y) (val ?val))
            (test (eq ?val (+ (count_bomb ?x ?y) (count_slot ?x ?y))))
        =>
            (assert (is-unsafe-around (x ?x) (y ?y)))
        )
    """
    env.build(rule)
    rule = """
        (defrule detect-slot
            (index-x $? ?x $?)
            (index-y $? ?y $?)
            (safe-pos (x ?x) (y ?y) (val ?val))
            (test (eq ?val (count_bomb ?x ?y)))
        =>
            (assert (is-safe-around (x ?x) (y ?y)))
        )
    """
    env.build(rule)

    template = env.find_template('bomb-pos')
    for x in board.bombFound:
        new_fact = template.new_fact()
        new_fact['x'] = x[0]
        new_fact['y'] = x[1]
        new_fact.assertit()

    template = env.find_template('empty-slot')
    for i in range(board.size):
        for j in range(board.size):
            if (board.board[i][j] != Constant.UNDEF):
                continue
            new_fact = template.new_fact()
            new_fact['x'] = i
            new_fact['y'] = j
            new_fact.assertit()
    
    template = env.find_template('safe-pos')
    for i in range(board.size):
        for j in range(board.size):
            if (not is_safe(board.board[i][j])):
                continue
            new_fact = template.new_fact()
            new_fact['x'] = i
            new_fact['y'] = j
            new_fact['val'] = board.board[i][j]
            new_fact.assertit()
        
    # for fact in env.facts():
    #     print(fact)
    env.run()
    
    # activation = tuple(env.activations())
    # print(activation)
    # for fact in env.facts():
    #     print(fact)
    # import sys
    # sys.exit(0)
    
    for fact in env.facts():
        strfact = str(fact).replace('(', ' ').replace(')', ' ')
        words = strfact.split(' ')

        unsafe = False
        safe = False
        val = []
        bef = ''
        for word in words:
            if (word == "is-unsafe-around"):
                unsafe = True
            elif (word == "is-safe-around"):
                safe = True
            if (unsafe or safe):
                if (bef == 'x' or bef == 'y'):
                    val.append(int(word))
            bef = word
        if (safe or unsafe):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i == 0 or j == 0):
                        continue
                    ni = val[0] + i
                    nj = val[1] + j
                    if ((not board.in_range(ni, nj)) or board.board[ni][nj] != -2):
                        continue
                    board.make_assert(ni, nj, unsafe)



print(f'KONDISI AWAL \n{board.to_string()}')

step = 0
while (len(board.bombFound) < board.bombCnt):
    if (step == 0):
        board.make_assert(0, 0, 0)
    else:
        find_bomb()
    step += 1
    print(f'SETELAH STEP {step}\n{board.to_string()}')

print(f'DISELESAIKAN DALAM: {step} step')
