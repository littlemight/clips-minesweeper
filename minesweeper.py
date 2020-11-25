import clips
import os
import re
from board import Board
from constant import Constant, is_bomb, is_safe, is_undef

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
    for ni, nj in board.adjList[i][j]:
        if (board.board[ni][nj] == Constant.BOMB):
            ret += 1
    return ret

def count_slot(i, j):
    ret = 0
    for ni, nj in board.adjList[i][j]:
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
            (test (> (count_slot ?x ?y) 0))
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
            (test (> (count_slot ?x ?y) 0))
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
            # print(unsafe, end=' ')
            # print(str(val[0]) + ", " + str(val[1]))
            for ni, nj in board.adjList[val[0]][val[1]]:
                if (board.board[ni][nj] != -2):
                    continue
                board.make_assert(ni, nj, unsafe)


print(f'KONDISI AWAL \n{board.to_string()}')

step = 0
while (len(board.bombFound) < board.bombCnt):
    if (step == 0):
        board.make_assert(0, 0, 0)
    else:
        try:
            find_bomb()
        except Exception as e:
            print(e)
    step += 1
    print(f'SETELAH STEP {step}\n{board.to_string()}')

print(f'DISELESAIKAN DALAM: {step} step')
