from minesweeper_csp import *
from propagators import *
from mine_board_generator import *

def print_sudo_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":
    test_count = 5
    while test_count > 0:
        b = mine_board_generator_2d(9, 9)
        print("Solving board " + 6 - test_count + ": ")
        for row in b:
            print(row)
        print("Using 2d Model")
        csp, var_array = minesweeper_csp_model_2d(b)
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_sudo_soln(var_array)
        test_count = test_count - 1

    '''
    print("Using 3d Model")
    csp, var_array = minesweeper_csp_model_3d(b2)
    solver = BT(csp)
    print("=======================================================")
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_sudo_soln(var_array)
    print("=======================================================")
    '''
