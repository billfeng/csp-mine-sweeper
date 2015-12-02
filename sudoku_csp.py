#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools
import propagators

def sudoku_csp_model_1(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).
    '''
    
#IMPLEMENT
    variables = []
    variable_array = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            if initial_sudoku_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_sudoku_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)

    reduce(variable_array,initial_sudoku_board)
    sudoku_csp = CSP("Sudoku-M1", variables)

    for i in range(0, 9):
        for j in range(0, 9):
            for k in range(j + 1, 9):
                constraint = Constraint("C(({},{}),({},{}))".format(i+1,j+1,i+1,k+1),[variable_array[i][j], variable_array[i][k]])
                sat_tuples = []
                for sat_tuple in itertools.product(variable_array[i][j].cur_domain(), variable_array[i][k].cur_domain()):
                    if sat_tuple[0] != sat_tuple[1]:
                        sat_tuples.append(sat_tuple)
                constraint.add_satisfying_tuples(sat_tuples)
                sudoku_csp.add_constraint(constraint)

    for i in range(0, 9):
        for j in range(0, 9):
            for k in range(i + 1, 9):
                constraint = Constraint("C(({},{}),({},{}))".format(i+1,j+1,k+1,j+1),[variable_array[i][j], variable_array[k][j]])
                sat_tuples = []
                for sat_tuple in itertools.product(variable_array[i][j].cur_domain(), variable_array[k][j].cur_domain()):
                    if sat_tuple[0] != sat_tuple[1]:
                        sat_tuples.append(sat_tuple)
                constraint.add_satisfying_tuples(sat_tuples)
                sudoku_csp.add_constraint(constraint)

    for i in range(0, 3):
        for j in range(0, 3):
            for k in range(0, 3):
                for l in range(0, 3):
                    for m in range(k*3+l+1, 9):
                        if k!=m//3 and l!=m%3:
                            constraint = Constraint("C(({},{}),({},{}))".format(i*3+k+1,j*3+l+1,i*3+m//3+1,j*3+m%3+1), [variable_array[i*3+k][j*3+l], variable_array[i*3+m//3][j*3+m%3]])
                            sat_tuples = []
                            for sat_tuple in itertools.product(variable_array[i*3+k][j*3+l].cur_domain(), variable_array[i*3+m//3][j*3+m%3].cur_domain()):
                                if sat_tuple[0] != sat_tuple[1]:
                                    sat_tuples.append(sat_tuple)
                            constraint.add_satisfying_tuples(sat_tuples)
                            sudoku_csp.add_constraint(constraint)

    for row in variable_array:
        for item in row:
            item.restore_curdom()
    return sudoku_csp, variable_array

##############################

def sudoku_csp_model_2(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''

#IMPLEMENT
    variables = []
    variable_array = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            if initial_sudoku_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_sudoku_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)

    reduce(variable_array, initial_sudoku_board)
    sudoku_csp = CSP("Sudoku-M2", variables)

    for i in range(0, 9):
        constraint = Constraint("C(ROW{})".format(i+1), variable_array[i])

        dm = [variable_array[i][0].cur_domain(),
              variable_array[i][1].cur_domain(),
              variable_array[i][2].cur_domain(),
              variable_array[i][3].cur_domain(),
              variable_array[i][4].cur_domain(),
              variable_array[i][5].cur_domain(),
              variable_array[i][6].cur_domain(),
              variable_array[i][7].cur_domain(),
              variable_array[i][8].cur_domain()]

        holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sat_tuples = []
        recursive_sat(dm, holder, sat_tuples)
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

        '''

        d1 = variable_array[i][0].cur_domain()
        d2 = variable_array[i][1].cur_domain()
        d3 = variable_array[i][2].cur_domain()
        d4 = variable_array[i][3].cur_domain()
        d5 = variable_array[i][4].cur_domain()
        d6 = variable_array[i][5].cur_domain()
        d7 = variable_array[i][6].cur_domain()
        d8 = variable_array[i][7].cur_domain()
        d9 = variable_array[i][8].cur_domain()

        holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for v1 in d1:
            if v1 not in holder:
                holder[0] = v1
                for v2 in d2:
                    if v2 not in holder:
                        holder[1] = v2
                        for v3 in d3:
                            if v3 not in holder:
                                holder[2] = v3
                                for v4 in d4:
                                    if v4 not in holder:
                                        holder[3] = v4
                                        for v5 in d5:
                                            if v5 not in holder:
                                                holder[4] = v5
                                                for v6 in d6:
                                                    if v6 not in holder:
                                                        holder[5] = v6
                                                        for v7 in d7:
                                                            if v7 not in holder:
                                                                holder[6] = v7
                                                                for v8 in d8:
                                                                    if v8 not in holder:
                                                                        holder[7] = v8
                                                                        for v9 in d9:
                                                                            if v9 not in holder:
                                                                                holder[8] = v9
                                                                                result.append(list(holder))
                                                                                holder[8] = 0
                                                                        holder[7] = 0
                                                                holder[6] = 0
                                                        holder[5] = 0
                                                holder[4] = 0
                                        holder[3] = 0
                                holder[2] = 0
                        holder[1] = 0
                holder[0] = 0
        constraint.add_satisfying_tuples(result)
        sudoku_csp.add_constraint(constraint)
        '''

    for i in range(0, 9):
        var_arr = []
        for j in range(0, 9):
            var_arr.append(variable_array[j][i])
        constraint = Constraint("C(COL{})".format(i+1), var_arr)

        dm = [variable_array[0][i].cur_domain(),
              variable_array[1][i].cur_domain(),
              variable_array[2][i].cur_domain(),
              variable_array[3][i].cur_domain(),
              variable_array[4][i].cur_domain(),
              variable_array[5][i].cur_domain(),
              variable_array[6][i].cur_domain(),
              variable_array[7][i].cur_domain(),
              variable_array[8][i].cur_domain()]

        holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        sat_tuples = []
        recursive_sat(dm, holder, sat_tuples)
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    for i in range(0, 3):
        for j in range(0, 3):
            var_arr = []
            for k in range(0, 3):
                for l in range(0, 3):
                    var_arr.append(variable_array[i*3+k][j*3+l])
            constraint = Constraint("C(BOX{})".format(i*3+j+1), var_arr)

            dm = [variable_array[i*3][j*3].cur_domain(),
                  variable_array[i*3][j*3+1].cur_domain(),
                  variable_array[i*3][j*3+2].cur_domain(),
                  variable_array[i*3+1][j*3].cur_domain(),
                  variable_array[i*3+1][j*3+1].cur_domain(),
                  variable_array[i*3+1][j*3+2].cur_domain(),
                  variable_array[i*3+2][j*3].cur_domain(),
                  variable_array[i*3+2][j*3+1].cur_domain(),
                  variable_array[i*3+2][j*3+2].cur_domain()]

            holder = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            sat_tuples = []
            recursive_sat(dm, holder, sat_tuples)
            constraint.add_satisfying_tuples(sat_tuples)
            sudoku_csp.add_constraint(constraint)

    for row in variable_array:
        for item in row:
            item.restore_curdom()
    return sudoku_csp, variable_array


def reduce(table,initial):
    for i in range(0, 9):
        for j in range(0, 9):
            if initial[i][j] != 0:
                for k in range(0, 9):
                    if k != i and initial[i][j] in table[k][j].cur_domain():
                        table[k][j].prune_value(initial[i][j])
                    if k != j and initial[i][j] in table[i][k].cur_domain():
                        table[i][k].prune_value(initial[i][j])
                blocki = i//3
                blockj = j//3
                for k in range(0, 3):
                    for l in range(0, 3):
                        if (blocki*3 + k != i or blockj*3 + l != j) and initial[i][j] in table[blocki*3 + k][blockj*3 + l].cur_domain():
                            table[blocki*3 + k][blockj*3 + l].prune_value(initial[i][j])


def recursive_sat(dm, holder, sat_tuples):
    if len(dm) == 1:
        for item in dm[0]:
            if item not in holder:
                holder[8] = item
                sat_tuples.append(list(holder))
    else:
        temp = dm.pop(0)
        for item in temp:
            if item not in holder:
                holder[8-len(dm)] = item
                recursive_sat(list(dm), list(holder), sat_tuples)
