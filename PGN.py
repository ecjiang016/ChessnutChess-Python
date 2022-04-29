import numpy as np
import time
import game as Chess

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

            moves.append((Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), promotion))
            game.move(Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), promotion)

            if display:
                GUI.display_board(game, (old_x, old_y), (new_x, new_y))
                time.sleep(delay)

    
    print(f"{winner} (PGN)")
    if checkmate:
        assert game.result == winner

    return boards, moves, [winner] * len(moves)

if __name__ == '__main__':
    test_pgn = '1. e4 c5 2. Nf3 d6 3. d4 Nf6 4. Nc3 cxd4 5. Nxd4 g6 6. f3 Bg7 7. Be3 O-O 8. Qd2 Nc6 9. Nb3 Be6 10. Bh6 a5 11. Bxg7 Kxg7 12. g4 Ne5 13. Be2 Nc4 14. Bxc4 Bxc4 15. h4 a4 16. Nd4 e5 17. Ndb5 d5 18. g5 Nh5 19. exd5 Nf4 20. O-O-O Ra5 21. Na3 Bxd5 22. Nxd5 Rxd5 23. Qe3 Rxd1+ 24. Rxd1 Qc7 25. Qe4 Qc5 26. Qxb7 Ne2+ 27. Kd2 Qf2 28. Qc7 e4 29. fxe4 Re8 30. e5 Qd4+ 31. Ke1 Qe4 32. Kd2 Rxe5 33. c4 Qf4+ 34. Kc2 Nd4+ 35. Rxd4 Qxd4 36. Qxe5+ Qxe5 37. b4 Qe2+ 0-1'
    #print(test_pgn)
    start = time.time()
    Interpret(test_pgn, display=True, delay=0.1, start_GUI_game_at="Qf2")
    print(time.time() - start)