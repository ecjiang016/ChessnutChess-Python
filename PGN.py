import numpy as np
import time
import game as Chess

def letter_to_index(letter:str) -> int:
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].index(letter)

def letter_to_piece_number(letter:str) -> int:
    return {'p':1, 'n':2, 'b':3, 'r':4, 'q':5, 'k':6}[letter.lower()]

def class_to_letter(obj) -> str:
    return {Chess.Pawn:'P', Chess.Knight:'N', Chess.Bishop:'B', Chess.Rook:'R', Chess.Queen:'Q', Chess.King:'K'}[obj]

def Interpret(PGN:str, display=False) -> tuple[list, list, list]:
    """
    Takes in a PGN. Outputs a list with all the boards, a list elements of ((old_x, old_y), (new_x, new_y)), piece), and a list with the values (Winner value)
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

            moves.append((Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), promotion))
            game.move(Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), promotion)

            if display:
                GUI.display_board(game)
                time.sleep(0.7)

                print(turn)
                print((old_x, old_y), (new_x, new_y))

    
    print(f"{winner} (PGN)")
    if checkmate:
        assert game.result == winner

    return np.array(boards), moves, np.full(shape=len(moves), fill_value=winner)

if __name__ == '__main__':
    test_pgn = "1. e4 d5 2. exd5 Qxd5 3. Nc3 Qd8 4. Bc4 Nf6 5. Nf3 Bg4 6. h3 Bxf3 7. Qxf3 e6 8. Qxb7 Nbd7 9. Nb5 Rc8 10. Nxa7 Nb6 11. Nxc8 Nxc8 12. d4 Nd6 13. Bb5+ Nxb5 14. Qxb5+ Nd7 15. d5 exd5 16. Be3 Bd6 17. Rd1 Qf6 18. Rxd5 Qg6 19. Bf4 Bxf4 20. Qxd7+ Kf8 21. Qd8# 1-0"
    #print(test_pgn)
    start = time.time()
    Interpret(test_pgn, True)
    print(time.time() - start)