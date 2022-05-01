import numpy as np
import time
try:
    import game as Chess
except ModuleNotFoundError:
    from . import game as Chess

def letter_to_index(letter:str) -> int:
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(letter)

def letter_to_piece_number(letter:str) -> int:
    return {'p':1, 'n':2, 'b':3, 'r':4, 'q':5, 'k':6}[letter.lower()]

def class_to_letter(obj) -> str:
    return {Chess.Pawn:'P', Chess.Knight:'N', Chess.Bishop:'B', Chess.Rook:'R', Chess.Queen:'Q', Chess.King:'K'}[obj]

def Interpret(PGN:str, display=False, delay=0.7, start_GUI_game_at="") -> tuple[list, list, list]:
    """
    Takes in a PGN. Outputs a list with all the boards, a list elements of ((old_x, old_y), (new_x, new_y)), piece), and a list with the values (Winner value)
    Args:
        - `PGN`: Chess game in PGN format
        - `display`: When `True`, the GUI will display the moves being loaded
        - `delay`: Time waited before displaying the next move. Doesn't do anything if `display` is `False`
        - `start_GUI_game_at`: Takes in a string. Will stop interpreting the PGN and launch the GUI game at that move
    """
    if display:
        import GUI

    boards = []
    moves = []

    game = Chess.Game()

    pgn = PGN.split(". ")
    del pgn[0]

    winner = int(pgn[-1][-1])
    if winner == 0: #White wins
        winner = 1
    elif winner == 1: #Black wins
        winner = -1
    else: #Draw
        winner = 0

    checkmate = False

    for i in range(len(pgn)):
        pgn[i] = pgn[i].split(" ")
        del pgn[i][-1]

    for turns in pgn:
        for turn in turns:
            #Load a game
            if start_GUI_game_at and turn == start_GUI_game_at:
                import GUI
                GUI.main(load=game)

            promotion = None
            if turn[-1] == "+" or turn[-1] == "#":
                if turn[-1] == "#":
                    checkmate = True
                turn = turn[:-1]

            if turn[0].islower():
                if game.player_color == 1: #White pawn move
                    old_x = letter_to_index(turn[0])
                    try:
                        new_y = 8 - int(turn[1])
                        new_x = old_x
                        for y in range(new_y+1, new_y+3):
                            if game.board.reshape(8, 8)[y, old_x] == 1:
                                old_y = y
                                break      

                    except ValueError: #Capture
                        new_x = letter_to_index(turn[2])
                        new_y = 8 - int(turn[3])
                        old_y = new_y + 1

                    if turn[-2] == "=": #Pawn promotion
                        promotion = turn[-1]
            
                else: #Black pawn move
                    old_x = letter_to_index(turn[0])
                    try:
                        new_y = 8 - int(turn[1])
                        new_x = old_x
                        for y in reversed(range(new_y-2, new_y)):
                            if game.board.reshape(8, 8)[y, old_x] == -1:
                                old_y = y
                                break

                    except ValueError: #Capture
                        new_x = letter_to_index(turn[2])
                        new_y = 8 - int(turn[3])
                        old_y = new_y - 1

                    if turn[-2] == "=": #Pawn promotion
                        promotion = turn[-1]

            elif turn[0].isupper():
                if turn[0] != 'O':
                    moved_piece = turn[0]
                    if len(turn) == 3:
                        new_x = letter_to_index(turn[1])
                        new_y = 8 - int(turn[2])

                        for piece in (game.white_pieces if game.player_color == 1 else game.black_pieces):
                            if Chess.coords_2D_to_1D(new_x, new_y) in game.get_moves(piece.pos, piece.color) and class_to_letter(piece.__class__) == moved_piece:
                                old_x, old_y = Chess.coords_1D_to_2D(piece.pos)
                                break

                    elif len(turn) == 4:
                        new_x = letter_to_index(turn[2])
                        new_y = 8 - int(turn[3])
                        if turn[1] == "x": #Capture
                            for piece in (game.white_pieces if game.player_color == 1 else game.black_pieces):
                                if Chess.coords_2D_to_1D(new_x, new_y) in game.get_moves(piece.pos, piece.color) and class_to_letter(piece.__class__) == moved_piece:
                                    old_x, old_y = Chess.coords_1D_to_2D(piece.pos)
                                    break
                        
                        else:
                            try:
                                line = 8 - int(turn[1])
                                column = False
                            except ValueError:
                                line = letter_to_index(turn[1])
                                column = True
                            
                            if column:
                                for piece in (game.white_pieces if game.player_color == 1 else game.black_pieces):
                                    old_x, old_y = Chess.coords_1D_to_2D(piece.pos)
                                    if old_x == line and class_to_letter(piece.__class__) == moved_piece:
                                        break

                            else:
                                for piece in (game.white_pieces if game.player_color == 1 else game.black_pieces):
                                    old_x, old_y = Chess.coords_1D_to_2D(piece.pos)
                                    if old_y == line and class_to_letter(piece.__class__) == moved_piece:
                                        break

                    else:
                        new_x = letter_to_index(turn[3])
                        new_y = 8 - int(turn[4])
                        try:
                            line = 8 - int(turn[1])
                            column = False
                        except ValueError:
                            line = letter_to_index(turn[1])
                            column = True
                        
                        if column:
                            for piece in (game.white_pieces if game.player_color == 1 else game.black_pieces):
                                old_x, old_y = Chess.coords_1D_to_2D(piece.pos)
                                if old_x == line and class_to_letter(piece.__class__) == moved_piece:
                                    break

                        else:
                            for piece in (game.white_pieces if game.player_color == 1 else game.black_pieces):
                                old_x, old_y = Chess.coords_1D_to_2D(piece.pos)
                                if old_y == line and class_to_letter(piece.__class__) == moved_piece:
                                    break

                else:
                    if game.player_color == 1:
                        if len(turn) == 3: #White short castle
                            old_x = 4
                            old_y = 7
                            new_x = 6
                            new_y = 7
                        
                        else: #White long castle
                            old_x = 4
                            old_y = 7
                            new_x = 2
                            new_y = 7
                    
                    else:
                        if len(turn) == 3: #Black short castle
                            old_x = 4
                            old_y = 0
                            new_x = 6
                            new_y = 0 

                        else: #Black long castle
                            old_x = 4
                            old_y = 0
                            new_x = 2
                            new_y = 0
            
            else:
                boards.append(game.board)

            if display:
                print(turn)
                print((old_x, old_y), (new_x, new_y))

            moves.append((Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), letter_to_piece_number(promotion) if promotion else None))
            game.move(Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), letter_to_piece_number(promotion) if promotion else None)

            if display:
                GUI.display_board(game, (old_x, old_y), (new_x, new_y))
                time.sleep(delay)

    if display:
       print(f"{winner} (PGN)")
    if checkmate:
        assert game.result == winner

    return boards, moves, [winner] * len(moves)

if __name__ == '__main__':
    test_pgn = '1. d4 d5 2. c4 e6 3. Nf3 Nf6 4. Nc3 Be7 5. Bf4 O-O 6. e3 c5 7. dxc5 Bxc5 8. Qc2 Nc6 9. a3 a6 10. O-O-O Be7 11. Ng5 g6 12. h4 e5 13. Nxd5 Nxd5 14. Rxd5 Qc7 15. Bg3 Bf5 16. Bd3 Bxd3 17. Qxd3 Rfd8 18. Kb1 b5 19. cxb5 axb5 20. Rc1 Qb6 21. Qxb5 Rdb8 22. Qxb6 Rxb6 23. Rd3 h6 24. Ne4 f5 25. Nd2 Rab8 26. Nc4 Rb5 27. Rc2 Rf8 28. Nd6 Rb6 29. Rdc3 Bxd6 30. Rxc6 Rfb8 31. Ka2 Rxc6 32. Rxc6 Rd8 33. f3 Kf7 34. Be1 Be7 35. Bc3 Bxh4 36. Bxe5 Rd2 37. a4 Bd8 38. Rd6 Rxd6 39. Bxd6 Ke6 40. Bf8 h5 41. Kb3 g5 42. Kc4 g4 43. fxg4 fxg4 44. Kd4 h4 45. Ke4 h3 46. gxh3 gxh3 47. Kf3 Bb6 48. e4 h2 49. Kg2 Ke5 50. b4 Kxe4 51. Kxh2 Kd5 52. Kg3 Ba5 53. bxa5 Kc6 54. Kf4 Kb7 55. Bc5 Ka8 56. Ke5 Kb7 57. Kd6 Ka8 58. Kc7 1/2-1/2'
    #print(test_pgn)
    start = time.time()
    Interpret(test_pgn, display=True, delay=0, start_GUI_game_at="")
    print(time.time() - start)