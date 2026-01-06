import time

import pygame
from constants import *


pygame.init()

# draw the chessboard
def draw_board():
    colors = ["light gray", "light green"]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, [col * square_size, row * square_size, square_size, square_size])

    bar_height = 100 
    pygame.draw.rect(screen, 'gray', [0, 8 * square_size, w, bar_height])  # Full gray bar
    pygame.draw.rect(screen, 'gold', [0, 8 * square_size, 8 * square_size + 2, bar_height - 4], 5)  # Gold border
    '''pygame.draw.rect(screen, 'gold', [8 * square_size, 0, w, h], 5)
    right_panel_width = w - (8 * square_size)
    pygame.draw.rect(screen, 'gold', [8 * square_size, 0, right_panel_width, h], 5)'''

    for i in range(9):
        pygame.draw.line(screen, 'black', (0, i * square_size), (8 * square_size, i * square_size), 2)  # Horizontal
        pygame.draw.line(screen, 'black', (i * square_size, 0), (i * square_size, 8 * square_size), 2)  # Vertical


    # Status Text
    status_text = [
        'White: Select a Piece to Move!',
        'White: Select a Destination!',
        'Black: Select a Piece to Move!',
        'Black: Select a Destination!'
    ]
    screen.blit(Big_font.render(status_text[turn_step], True, 'black'), (50, 8 * square_size + 20))  # Left-aligned
    pygame.draw.rect(screen, 'light blue', (705, 0, 200, 800))
    pygame.draw.rect(screen, 'gold', [705, 0, 195, 800], 5)
    screen.blit(font.render('FORFEIT', True, 'black'), (7*square_size-48, 8*square_size+40))
    pygame.draw.rect(screen, 'red', [6*square_size, 8*square_size+5, 2*square_size, 1*square_size-3], 5)
    if white_promote or black_promote:
        pygame.draw.rect(screen, 'gray', [0, 8 * square_size + 5, 8 * square_size , square_size+10])  # Full gray bar
        pygame.draw.rect(screen, 'gold', [0, 8 * square_size, 8 * square_size + 5, bar_height - 4 ], 5)
        pygame.draw.line(screen, 'black', (0, 8 * square_size), (8 * square_size, 8 * square_size), 2)
        screen.blit(Big_font.render('Select Piece to Promote Pawn (Up-Right)', True, 'black'), (50, 8 * square_size + 20))

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * square_size + (square_size - 65) // 2, white_locations[i][1] * square_size + (square_size - 65) // 2))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * square_size + (square_size - 80) // 2, white_locations[i][1] * square_size + (square_size - 80) // 2))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * square_size, white_locations[i][1] * square_size,
                                                     square_size, square_size], 3)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * square_size + (square_size - 65) // 2, black_locations[i][1] * square_size + (square_size - 65) // 2))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * square_size + (square_size - 80) // 2, black_locations[i][1] * square_size + (square_size - 80) // 2))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * square_size, black_locations[i][1] * square_size,
                                                  square_size, square_size], 3)

def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)

        all_moves_list.append(moves_list)
    return all_moves_list

def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list, castle_moves

def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False

    return moves_list

def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # check en passant
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # check en passant
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
        # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list



def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return  valid_options

def draw_valid(moves):
    if turn_step < 2:
        color = "red"
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * square_size + (square_size//2), moves[i][1] * square_size + (square_size//2)), 5)

def draw_captured():
    for i in range(len(captured_pieces_white)):
        row = i // 2
        col = i % 2
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)

        piece_x = 715 + (col * (30 + 5))
        piece_y = 10 + (row * (50))

        screen.blit(small_black_images[index], (piece_x, piece_y))

    for i in range(len(captured_pieces_black)):
        row = i // 2
        col = i % 2
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)

        piece_x = 810 + (col * (30 + 5))
        piece_y = 10 + (row * (50))

        screen.blit(small_white_images[index], (piece_x, piece_y))

def draw_check():
    global check
    check = False
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red',
                                     [white_locations[king_index][0] * square_size + 1, white_locations[king_index][1] * square_size + 1,
                                      square_size, square_size], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue',
                                         [black_locations[king_index][0] * square_size + 1,
                                          black_locations[king_index][1] * square_size + 1,
                                          square_size, square_size], 5)

def draw_game_over():
    screen_color = 'gold'
    if winner == 'white':
        text_color = 'white'
    else:
        text_color = 'black'
    pygame.draw.rect(screen, screen_color, [154, 200, 400, 80])
    screen.blit(Big_font.render(f'{winner} won the game!', True, text_color), (170, 210))
    screen.blit(Big_font.render(f'Press ENTER to Restart!', True, text_color), (170, 240))
    if counter < 10:
        pygame.draw.rect(screen, 'red', [252, 300, 200, 100])
    elif 10 < counter < 20:
        pygame.draw.rect(screen, 'green', [252, 300, 200, 100])
    else:
        pygame.draw.rect(screen, 'blue', [252, 300, 200, 100])
    screen.blit(Big_font.render(f'Game Over', True, 'white'), (270, 335))
    '''gameover ด้วยวิธี easter egg 
    กด Ctrl + Shift + F เพื่อเปิดโหมดลับ Auto Win (JJK ref)'''
    if easter_egg:
        pygame.draw.rect(screen, 'black', [204, 410, 300, 80])
        screen.blit(Big_font.render(f"NAH, I'D WIN.", True, 'white'), (257, 435))
        screen.blit(gojo, (204,510))

# คำนวณพิกัดพิเศษสำหรับการกินแบบ En Passant ซึ่งเป็นกฎที่ซับซ้อนของ Pawn
def check_ep(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        pass
    else:
        ep_coords = (100, 100)
    return ep_coords

def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = []
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index

def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [708, 0, 192, 5 * square_size])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (760, 3 + square_size + square_size * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (760, 3+ square_size + square_size * i))
    pygame.draw.rect(screen, color, [708, 0, 192, (5*square_size)+5], 5)

def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // square_size
    y_pos = mouse_pos[1] // square_size
    if white_promote and left_click and x_pos > 7 and y_pos <= 4:
        white_pieces[promo_index] = white_promotions[y_pos-1]
    elif black_promote and left_click and x_pos > 7 and y_pos <= 4:
        black_pieces[promo_index] = black_promotions[y_pos-1]

def check_castling():
    '''เงื่อนไขการเข้าป้อม
      1. King และ Rook ต้องไม่เคยขยับมาก่อน
      2. ต้องไม่มีตัวหมากขวางทาง
      3. King ต้องไม่ถูกรุก (Check) อยู่'''
    castle_moves = []
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if turn_step > 1:
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves

def draw_castling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * square_size + (square_size//2),
                                           moves[i][0][1] * square_size + (square_size//10*8)), 8)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * square_size + (square_size//10*3),
                                                         moves[i][0][1] * square_size + (square_size//10*8)))
        pygame.draw.circle(screen, color, (moves[i][1][0] * square_size + (square_size // 2),
                                           moves[i][1][1] * square_size + (square_size // 10 * 8)), 8)
        screen.blit(font.render('rook', True, 'black'), (moves[i][1][0] * square_size + (square_size // 10 * 3),
                                                         moves[i][1][1] * square_size + (square_size // 10 * 8)))
        pygame.draw.line(screen, color, (moves[i][0][0] * square_size + (square_size//2),
                                         moves[i][0][1] * square_size + (square_size//10*8)),
                         (moves[i][1][0] * square_size + (square_size//2),
                          moves[i][1][1] * square_size + (square_size//10*8)), 2)




# Main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
Run = True
while Run:
    time.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('light blue')

    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
        if selected_piece == 'king':
            draw_castling(castling_moves)

    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Run = False  # Press ESC to exit full-screen mode
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_cord = event.pos[0] // square_size
            y_cord = event.pos[1] // square_size
            click_cord = (x_cord, y_cord)
            # White turn
            if turn_step <= 1:
                if click_cord == (6, 8) or click_cord == (7, 8):
                    winner = 'black'
                if click_cord in white_locations:
                    selection = white_locations.index(click_cord)

                    # castling (only select king)
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step = 1
                if click_cord in valid_moves and selection != 100:
                    white_ep = check_ep(white_locations[selection], click_cord)
                    white_locations[selection] = click_cord
                    white_moved[selection] = True
                    if click_cord in black_locations:
                        black_piece = black_locations.index(click_cord)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)

                        # en passant capture
                    if click_cord == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                # add castle option
                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if click_cord == castling_moves[q][0]:
                            white_locations[selection] = click_cord
                            white_moved[selection] = True
                            if click_cord == (1, 0):
                                rook_coords = (0, 0)
                            else:
                                rook_coords = (7, 0)
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 100
                            valid_moves = []
            # Black turn
            if turn_step > 1:
                if click_cord == (6, 8) or click_cord == (7, 8):
                    winner = 'white'
                if click_cord in black_locations:
                    selection = black_locations.index(click_cord)

                    # castling (only select king)
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step = 3
                if click_cord in valid_moves and selection != 100:
                    black_ep = check_ep(black_locations[selection], click_cord)
                    black_locations[selection] = click_cord
                    black_moved[selection] = True
                    if click_cord in white_locations:
                        white_piece = white_locations.index(click_cord)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)

                        # en passant capture
                    if click_cord == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                elif selection != 100 and selected_piece == 'king':
                    for q in range(len(castling_moves)):
                        if click_cord == castling_moves[q][0]:
                            black_locations[selection] = click_cord
                            black_moved[selection] = True
                            if click_cord == (1, 7):
                                rook_coords = (0, 7)
                            else:
                                rook_coords = (7, 7)
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = castling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 0
                            selection = 100
                            valid_moves = []
        # force game over (easter egg)                  
        if event.type == pygame.KEYDOWN and not game_over:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_f and mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                if turn_step <= 1:
                    winner = 'white'
                else:
                    winner = 'black'
                easter_egg = True
        # restart game
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                easter_egg = False
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                white_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                black_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()