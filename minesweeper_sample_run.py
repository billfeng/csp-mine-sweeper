from minesweeper_csp import *
from propagators import *
from mine_board_generator import *

b1a, b1b = mine_board_generator_2d(9, 9)

b2 = mine_board_generator_3d(9, 9, 9)

def print_sudo_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":
    print("Solving board b1:")
    for row in b1a:
        print(row)
    print("Using 2d Model")
    csp, var_array = minesweeper_csp_model_2d(b1a)
    solver = BT(csp)
    print("=======================================================")
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_sudo_soln(var_array)

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
