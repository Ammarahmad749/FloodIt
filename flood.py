import sys
from solution import Flood_it
from board import board


if __name__ == '__main__':
    '''
    main for setup board and solve board
    '''
    board = board()
    matrix, graph, col_val = board.make_board(sys.argv[1])
    print("\t\tInitial Given image matrix :")
    for row in matrix:
            print([str(x) for x in row],"\n")
    solve = Flood_it(matrix)
    var = solve.solve()
    
    print("\t\tValues choosen by program to solve the game",var,"\n")
    print("\t\tTotal no of steps required to solve the game : ",len(var))

#     print(matrix)
    



    
