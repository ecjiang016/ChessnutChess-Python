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

    for i in range(len(pgn)):
        pgn[i] = pgn[i].split(" ")
        del pgn[i][-1]

    for turns in pgn:
        for turn in turns:
            promotion = None
            if turn[-1] == "+" or turn[-1] == "#":
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
                GUI.display_board(game)
                time.sleep(0.7)

                print(turn)
                print((old_x, old_y), (new_x, new_y))
                
            moves.append((Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), promotion))
            game.move(Chess.coords_2D_to_1D(old_x, old_y), Chess.coords_2D_to_1D(new_x, new_y), promotion)

    print(f"{winner} (PGN)")
    return boards, moves, [winner]*len(moves)

if __name__ == '__main__':
    test_pgn = "1. d4 d5 2. c4 e6 3. Nc3 a6 4. cxd5 exd5 5. Nf3 Nf6 6. Bg5 Be6 7. e3 Nbd7 8. Be2 Bd6 9. O-O c6 10. Qc2 Qc7 11. Bh4 h6 12. Rac1 O-O 13. Rfe1 Rfe8 14. a3 Bg4 15. Bg3 Bxg3 16. hxg3 Qd6 17. Nd2 Re6 18. Bxg4 Nxg4 19. Qf5 Ndf6 20. Na4 Rae8 21. Nc5 R6e7 22. b4 h5 23. Qf4 Qxf4 24. gxf4 Nh6 25. Nf3 Nf5 26. Red1 Nd6 27. Ne5 Nfe4 28. Nxe4 Nxe4 29. Nd3 f6 30. g3 Kf7 31. Kg2 Nd6 32. a4 Nc4 33. Rb1 Kg6 34. b5 axb5 35. axb5 Na3 36. Rb3 Nxb5 37. Rdb1 Kf5 38. Kf3 g5 39. fxg5 fxg5 40. Rxb5 cxb5 41. Rxb5 Rd8 42. Ne5 h4 43. g4+ Ke6 44. Rb6+ Rd6 45. Rb5 b6 46. Kg2 Rb7 47. Kh3 Rd8 48. f4 Kf6 49. Nf3 gxf4 50. exf4 Ra8 51. Kxh4 Ra3 52. Kg3 Ke6 53. f5+ Kd6 54. Kf4 Kc6 55. Rb1 b5 56. Ne5+ Kd6 57. g5 b4 58. g6 Ra2 59. f6 Ke6 60. g7 Rg2 61. f7 Rxf7+ 62. Nxf7 Kxf7 63. Rxb4 Kxg7 64. Ke5 Rg5+ 65. Ke6 Kf8 66. Rb8+ Kg7 67. Rb5 Rg6+ 68. Kxd5 Kf7 69. Rb7+ Ke8 70. Kc5 Kd8 71. d5 Rh6 72. Rg7 Rf6 73. Rg1 Rh6 74. Ra1 Rg6 75. Ra7 Rh6 76. Ra8+ Kc7 77. Rf8 Rg6 78. Rf7+ Kc8 79. Kd4 Rh6 80. Ke5 Ra6 81. Re7 Kd8 82. Re6 Ra1 83. Rh6 Ke8 84. Ke6 Re1+ 85. Kd6 Ra1 86. Rh8+ Kf7 87. Rc8 Ra6+ 88. Rc6 Ra1 89. Kc7 Ra7+ 90. Kd6 Ra1 91. Rb6 Ke8 92. Kc7 Rc1+ 93. Rc6 Ra1 94. Re6+ Kf7 95. Re2 Rc1+ 96. Kd7 Rd1 97. Rf2+ 1-0"
    print(test_pgn)
    start = time.time()
    Interpret(test_pgn, False)
    print(time.time() - start)