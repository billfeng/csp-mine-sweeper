'''
Construct and return minesweeper CSP models.
'''

from cspbase import *
import itertools
import propagators


def minesweeper_csp_model_2d(initial_mine_board):
    '''
    Return a CSP object representing a minesweeper game.

    The input mine field would be represented by a list of lists of integers.
    An example mine field:
       -------------------
       |0|0|1|0|3|0|0|4|0|
       |1|2|2|3|0|4|0|0|2|
       |0|2|0|2|1|2|3|3|2|
       |2|3|2|2|1|0|1|0|1|
       |0|1|2|0|2|0|1|1|1|
       |1|1|2|0|2|0|0|0|0|
       -------------------

    And the solution should look something like this:
       -------------------
       | | |1|*|3|*|*|4|*|
       |1|2|2|3|*|4|*|*|2|
       |*|2|*|2|1|2|3|3|2|
       |2|3|2|2|1| |1|*|1|
       |*|1|2|*|2| |1|1|1|
       |1|1|2|*|2| | | | |
       -------------------
    '''
    variables = []
    variable_array = []
    for i in range(0, len(initial_mine_board)):
        row = []
        for j in range(0, len(initial_mine_board[0])):
            if initial_mine_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [0, 9])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_mine_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)
    #print(variable_array)
    reduce(variable_array, initial_mine_board)
    mine_csp = CSP("Minesweeper-2d", variables)

    # add constraints here
    for i in range(0, len(variable_array)):
        for j in range(0, len(variable_array[0])):
            if initial_mine_board[i][j] != 0:
                constraint = Constraint("C{},{}".format(i, j), get_variables_around(i, j, variable_array))

                domain = []
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if not (k == 0 and l == 0) and 0 <= (i + k) < len(variable_array) and 0 <= (j + l) < len(variable_array[0]):
                            domain.append(variable_array[i + k][j + l].cur_domain())
                #print("domain")
                #print(domain)
                holder = [0 for i in range(len(domain))]
                sat_tuples = []
                recursive_sat(domain, holder, sat_tuples, initial_mine_board[i][j])
                constraint.add_satisfying_tuples(sat_tuples)
                mine_csp.add_constraint(constraint)

    return mine_csp, variable_array


def minesweeper_csp_model_3d(initial_mine_board):
    variables = []
    variable_array = []
    for i in range(0, len(initial_mine_board)):
        layer = []
        for j in range(0, len(initial_mine_board[0])):
            row = []
            for k in range(0, len(initial_mine_board[0][0])):
                if initial_mine_board[i][j][k] == 0:
                    variable = Variable("V({},{},{})".format(i, j, k), [" ", "*"])
                else:
                    variable = Variable("V({},{},{})".format(i, j, k), [initial_mine_board[i][j][k]])
                variables.append(variable)
                row.append(variable)
        variable_array.append(layer)

    reduce_3d(variable_array, initial_mine_board)
    mine_csp = CSP("Minesweeper-3d", variables)

    # add constraints here
    for i in range(0, len(variable_array)):
        for j in range(0, len(variable_array[0])):
            for k in range(0, len(variable_array[0][0])):
                if initial_mine_board[i][j][k] != 0:
                    constraint = Constraint("C{},{},{}".format(i, j, k), get_variables_3d(i, j, k, variable_array))

                    domain = []
                    for l in range(-1, 2):
                        for m in range(-1, 2):
                            for n in range(-1, 2):
                                if not (l == 0 and m == 0 and n == 0) and 0 <= (i + l) < len(variable_array) and 0 <= (j + m) < len(variable_array[0]) and 0 <= (k + n) < len(variable_array[0][0]):
                                    domain.append(variable_array[i + l][j + m][k + n])
                    holder = [0, 0, 0, 0, 0, 0, 0, 0]
                    sat_tuples = []
                    recursive_sat(domain, holder, sat_tuples)
                    constraint.add_satisfying_tuples(sat_tuples)
                    mine_csp.add_constraint(constraint)

    return mine_csp, variable_array


def reduce(table, initial):
    for i in range(0, len(initial)):
        for j in range(0, len(initial[0])):
            if initial[i][j] == 0 and no_indicator(initial, i, j):
                table[i][j].prune_value(9)


def no_indicator(initial, i, j):
    for k in range(-1, 2):
        for l in range(-1, 2):
            if 0 <= (i + k) < len(initial) and 0 <= (j + l) < len(initial[0]):
                if initial[i + k][j + l] !=0:
                    return False
    return True


def reduce_3d(table, initial):
    for i in range(0, len(initial)):
        for j in range(0, len(initial[0])):
            for k in range(0, len(initial[0][0])):
                if initial[i][j][k] == 0 and no_indicator_3d(initial, i, j, k):
                    table[i][j].prune_value(9)


def no_indicator_3d(initial, i, j, k):
    for l in range(-1, 2):
        for m in range(-1, 2):
            for n in range(-1, 2):
                if 0 <= (i + l) < len(initial) and 0 <= (j + m) < len(initial[0]) and 0 <= (k + n) < len(initial[0]):
                    if initial[i + l][j + m][k + n] !=0:
                        return False
    return True


def get_variables_around(i, j, table):
    array = []
    for k in range(-1, 2):
        for l in range(-1, 2):
            if not(k == 0 and l == 0) and 0 <= (i + k) < len(table) and 0 <= (j + l) < len(table[0]):
                array.append(table[i + k][j + l])
    return array


def get_variables_3d(i, j, k, table):
    array = []
    for l in range(-1, 2):
        for m in range(-1, 2):
            for n in range(-1, 2):
                if not(l == 0 and m == 0 and n == 0) and 0 <= (i + l) < len(table) and 0 <= (j + m) < len(table[0]) and 0 <= (k + n) < len(table[0][0]):
                    array.append(table[i + l][j + m][k + n])
    return array


def recursive_sat(domain, holder, sat_tuples, value):
    if len(domain) == 1:
        for item in domain[0]:
            holder[len(holder) - 1] = item
            count = 0
            for i in holder:
                if i == 9:
                    count += 1
            if count == value:
                sat_tuples.append(list(holder))
    else:
        temp = domain.pop(0)
        for item in temp:
            holder[len(holder) - 1 - len(domain)] = item
            recursive_sat(list(domain), list(holder), sat_tuples, value)
