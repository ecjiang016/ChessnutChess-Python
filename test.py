from math import inf
import time
from game import Game
from copy import deepcopy

global game
game = Game()

def search(depth:int, undo_move_check=True) -> tuple:
    if depth == 0:
        return 1
    
    if game.end:
        return 1

    positions = 0

    for move in game.all_moves():
        game_before_move = deepcopy(game)
        game.move(*move)
        positions += search(depth-1)
        game.undo_move(*move)
        if undo_move_check:
            try:
                assert game.all_moves().sort() == game_before_move.all_moves().sort()
                assert (game.board == game_before_move.board).all()
            except AssertionError as e:
                print(e)
                from GUI import display_board
                display_board(game_before_move)
                time.sleep(3)
                game_before_move.move(*move)
                display_board(game_before_move)
                time.sleep(3)
                game_before_move.undo_move(*move)
                display_board(game_before_move)
                time.sleep(5)
                raise Exception

    return positions

def main():
    for depth in range(5):
        print(search(depth))

if __name__ == '__main__':
    main()