import pygame
import time
import numpy as np
import os
try:
    from game import Game, coords_2D_to_1D
except ModuleNotFoundError:
    from .game import Game, coords_2D_to_1D


WINDOW_SIZE = 800
TILE_SIZE = WINDOW_SIZE // 8

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

image_names = [
    'pl.png',
    'nl.png',
    'bl.png',
    'rl.png',
    'ql.png',
    'kl.png',
    'kd.png',
    'qd.png',
    'rd.png',
    'bd.png',
    'nd.png',
    'pd.png'
]

paths = [os.path.join(os.path.dirname(__file__), "Chess Pieces", image_names[i]) for i in range(12)]
images = [pygame.image.load(path) for path in paths]

pieces = []
for i in range(12):
    images[i] = pygame.transform.scale(images[i], (100, 100))
    pieces.append(images[i].get_rect())

def coords_to_mask(moves) -> np.ndarray:
    """
    Takes in a list of coords and outputs an 8 by 8 array with 1's on the coords and 0's everywhere else
    """
    out = np.zeros(64)
    out[moves] = 1
    return out.reshape(8, 8)

def create_background_board(moves_board, selected_piece):
    board = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))

    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (y+x) % 2 == 0:
                color = pygame.Color(192, 192, 192) #Lighter color

                if selected_piece != 0 and moves_board[y, x] == 1:
                    color = pygame.Color(210, 43, 43) #Red

            else:
                color = pygame.Color(105 ,105, 105) #Darker color

                if selected_piece != 0 and moves_board[y, x] == 1:
                    color = pygame.Color(165, 42, 42) #Red

            if x == selected_piece[1] and y == selected_piece[2]:
                color = pygame.Color(227, 11, 92) #Selected piece color
            

            pygame.draw.rect(board, color, rect)

    return board

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v // TILE_SIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            piece = board[y, x]
            if piece:
                return piece, x, y
            else:
                return None, x, y

    except IndexError:
        pass

    return None, None, None

def draw_pieces(screen, board, selected_piece):
    sx, sy = None, None
    if selected_piece[0]:
        piece, sx, sy = selected_piece

    for y in range(8):
        for x in range(8):
            piece = board[y, x]
            if piece:
                selected = (x == sx and y == sy)
                piece = piece if piece < 0 else piece - 1
                img = images[piece]
                pieces[piece].center = (x * 100 + 50), (y * 100 + 50)
                if not selected:
                    screen.blit(img, pieces[piece])

def draw_drag(screen, board, selected_piece):
    if selected_piece[0]:
        _, x, y = get_square_under_mouse(board)
        pos = pygame.Vector2(pygame.mouse.get_pos())
        img = images[selected_piece[0] if selected_piece[0] < 0 else selected_piece[0] - 1]
        screen.blit(img, img.get_rect(center=pos))
        return (x, y)

def display_board(game, old_xy=None, new_xy=None):
    old_x, old_y = old_xy
    new_x, new_y = new_xy

    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

    #board_surface = create_background_board(np.zeros((8, 8)), (0, 8, 8))
    board_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (y+x) % 2 == 0:
                color = pygame.Color(192, 192, 192) #Lighter color
                if (x, y) == old_xy or (x, y) == new_xy:
                    color = pygame.Color(255, 255, 153) #Yellow for piece being moved
            else:
                color = pygame.Color(105, 105, 105) #Darker color
                if (x, y) == old_xy or (x, y) == new_xy:
                    color = pygame.Color(255, 255, 102) #Yellow for piece being moved
            

            pygame.draw.rect(board_surface, color, rect)
    screen.fill(pygame.Color('grey'))

    screen.blit(board_surface, (0, 0))
    draw_pieces(screen, game.board.reshape(8, 8), (None,))

    pygame.display.flip()

def single_move(game):
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    board_surface = create_background_board(np.zeros((8, 8)), (0, 0, 0))
    selected_piece = 0, -1, -1
    drop_pos = None

    while True:
        piece, x, y = get_square_under_mouse(np.array(game.board).reshape(8, 8))
        selected_x, selected_y = selected_piece[1:3]
        piece_moves = coords_to_mask(game.get_moves(coords_2D_to_1D(selected_x, selected_y), game.player_color))
        board_surface = create_background_board(piece_moves, selected_piece)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if piece != None and np.sign(piece) == game.player_color:
                    selected_piece = piece, x, y

            elif event.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    new_x, new_y = drop_pos
                    if piece_moves[new_y, new_x] == 1:
                        piece, old_x, old_y = selected_piece
                        promote = None
                        if (piece == 1 and new_y == 0) or (piece == -1 and new_y == 7):
                            promote = ""
                            while promote.upper() not in ["Q", "N", "R", "B"]:
                                promote = input("Promote to Q, R, B, or N: ")

                            promote = {"Q":5, "N":2, "R":4, "B":3}[promote.upper()]
                            
                        game.move(coords_2D_to_1D(old_x, old_y), coords_2D_to_1D(new_x, new_y), promote)
                        return game

                selected_piece = 0, -1, -1
                drop_pos = None

        screen.fill(pygame.Color('grey'))

        screen.blit(board_surface, (0, 0))
        draw_pieces(screen, np.array(game.board).reshape(8, 8), selected_piece)
        drop_pos = draw_drag(screen, np.array(game.board).reshape(8, 8), selected_piece)

        pygame.display.flip()
        clock.tick(60)

def main(load=False):
    """
    Args:
        - load: Load a game by passing in a game object
    """
    if load:
        game = load
    else:
        game = Game()

    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    board_surface = create_background_board(np.zeros((8, 8)), (0, 0, 0))
    selected_piece = 0, -1, -1

    while True:
        piece, x, y = get_square_under_mouse(np.array(game.board).reshape(8, 8))
        selected_x, selected_y = selected_piece[1:3]
        piece_moves = coords_to_mask(game.get_moves(coords_2D_to_1D(selected_x, selected_y), game.player_color))
        board_surface = create_background_board(piece_moves, selected_piece)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if piece != None and np.sign(piece) == game.player_color:
                    selected_piece = piece, x, y

            elif event.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    new_x, new_y = drop_pos
                    if piece_moves[new_y, new_x] == 1:
                        piece, old_x, old_y = selected_piece
                        promote = None
                        if (piece == 1 and new_y == 0) or (piece == -1 and new_y == 7):
                            promote = ""
                            while promote.upper() not in ["Q", "N", "R", "B"]:
                                promote = input("Promote to Q, R, B, or N: ")

                            promote = {"Q":5, "N":2, "R":4, "B":3}[promote.upper()]
                            
                        game.move(coords_2D_to_1D(old_x, old_y), coords_2D_to_1D(new_x, new_y), promote)

                selected_piece = 0, -1, -1
                drop_pos = None

        screen.fill(pygame.Color('grey'))

        screen.blit(board_surface, (0, 0))
        draw_pieces(screen, np.array(game.board).reshape(8, 8), selected_piece)
        drop_pos = draw_drag(screen, np.array(game.board).reshape(8, 8), selected_piece)

        pygame.display.flip()
        clock.tick(60)

        if game.end:
            print("Game End")
            time.sleep(7)
            return

if __name__ == '__main__':
    main()