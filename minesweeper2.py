import clips
import os
import re
from board import Board
from bruteforce import Bruteforce
from constant import Constant, is_bomb, is_safe, is_undef

# *** MAIN PROGRAM ***
# n = int(input())
# bombCnt = int(input())
# bombPos = []
# for i in range(bombCnt):
#     x, y = [int(a) for a in input().split(',')]
#     bombPos.append((x, y))

# board = Board(n, bombCnt, bombPos)
n = 4
bombCnt = 3
bombPos = [(3,1),(2,3),(3,3)]
board = Board(n,bombCnt,bombPos)

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

env = clips.Environment()
env.load('minesweeper.clp')

def setup_env():
    env.reset()
    template_index = '-1'
    for i in range(board.size):
        template_index += ' ' + str(i)
    template_index += ' -1'
    
    print(template_index)
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
    
def find_bomb():
    setup_env()

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
        
    try:
        # Get activations
        activations = tuple(env.activations())
        # print('Conflict Set')
        # for act in activations:
        #     print(act)
        print(f'Activated Rule: {activations[0]}')
        stract = str(activations[0])
        rule_name, facts_id = stract.split(' ')[6:]
        rule_name = rule_name[:-1]
        facts_id = facts_id.split(',')
        # print(rule_name, facts_id)
        
        fax = tuple(env.facts())
        fax = [x for x in fax if f'f-{x.index}' in facts_id]
        print('LHS:')
        for f in fax:
            # print(type(f))
            print(f'\t{f}')
            # print(str(f))

        env.run()
        ret = False
        
        for fact in env.facts():
            strfact = str(fact).replace('(', ' ').replace(')', ' ')
            words = strfact.split(' ')

            bomb = False
            safe = False
            val = []
            bef = ''
            for word in words:
                if (word == "bomb-at"):
                    bomb = True
                elif (word == "safe-at"):
                    safe = True
                if (bomb or safe):
                    if (bef == 'x' or bef == 'y'):
                        val.append(int(word))
                bef = word
            if (safe or bomb):
                if (board.board[val[0]][val[1]] == Constant.UNDEF):
                    ret = True
                    board.make_assert(val[0], val[1], bomb)
        return ret
    except Exception as e:
        return False

def use_bruteforce():
    bf = Bruteforce(board)
    bf.run()

if __name__ == "__main__":
    print(f'KONDISI AWAL \n{board.to_string()}')
    step = 0
    while (len(board.bombFound) < board.bombCnt and step < 101):
        try:
            if (step == 0):
                board.make_assert(0, 0, 0)
            else:
                progress = find_bomb()
                if (not progress):
                    use_bruteforce()
            step += 1
            print(f'SETELAH STEP {step}\n{board.to_string()}')
        except Exception as e:
            print('Error:', e)
            step += 1

    if (len(board.bombFound) == board.bombCnt):
        print('SELURUH BOMB BERHASIL DITEMUKAN!!')
    else:
        print('TIDAK SEMUA BOMB BERHASIL DITEMUKAN.')
    print(f'DISELESAIKAN DALAM: {step} step')