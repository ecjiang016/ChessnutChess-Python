from math import inf
import time
from game import Game
from profiler import profile
#from GUI import display_board

global game
game = Game()

def search(depth:int) -> tuple:
    if depth == 0:
        return 1
    
    if game.end:
        return 1

    positions = 0

    for move in game.all_moves():
        game.move(*move)
        #display_board(game)
        #time.sleep(0.01)
        positions += search(depth-1)
        game.undo_move(*move)
        #display_board(game)
        #time.sleep(0.01)

    return positions

@profile
def main():
    for depth in range(5):
        print(search(depth))

if __name__ == '__main__':
    main()