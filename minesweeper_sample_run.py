from minesweeper_csp import *
from propagators import *
from mine_board_generator import *

def print_sudo_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])


def print_sudo_soln_3d(var_array):
    for layer in var_array:
        for row in layer:
            print([var.get_assigned_value() for var in row])
        print("===========================")


if __name__ == "__main__":
    #the amount of tests to be run
    test_count = 1
    
    #run 2d or 3d
    dim = 3
    
    #board size
    height = 3
    width = 3
    depth = 3
    step = 1
    
    if dim == 2:
        while test_count > 0:
            b, res = mine_board_generator_2d(height, width)
            print("Solving board: ")
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

            if(var_array == res):
                print("Answer is correct!")
            else:
                print("Answer is wrong!")

            print(res)

            test_count = test_count - 1
            height += step
            width += step*2
            depth += step*3
    else:
        while test_count > 0:
            b, res = mine_board_generator_3d(height, width, depth)
            print("Solving board: ")
            for row in b:
                print(row)
            print("Using 3d Model")
            csp, var_array = minesweeper_csp_model_3d(b)
            solver = BT(csp)
            print("=======================================================")
            print("GAC")
            solver.bt_search(prop_GAC)
            print("Solution")
            print_sudo_soln_3d(var_array)
            test_count = test_count - 1
            height += step
            width += step*2
            depth += step*3
