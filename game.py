import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (80, 80, 80)
WIDTH, HEIGHT = 700, 700
SQUARE_SIZE = WIDTH // 8
BOARD_COLOR = (240, 217, 181)  # Light Brown
SQUARE_COLORS = [WHITE, BLACK]
SELECTED_COLOR = (113, 121, 126)  # Highlight selected piece in green
VALID_MOVE_COLOR = (192,192,192)  # Blue for valid moves
TURN_COLOR = (255, 0, 0)  # Red color to indicate whose turn it is

# Chess Piece Images
piece_images = {}

# Load piece images
def load_images():
    pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
    colors = ['white', 'black']
    for color in colors:
        for piece in pieces:
            try:
                piece_images[f'{piece}_{color}'] = pygame.transform.scale(pygame.image.load(f'images/{piece}_{color}.png'), (SQUARE_SIZE, SQUARE_SIZE))
            except pygame.error:
                print(f"Error loading image for {piece}_{color}")

# Create an empty board
def create_board():
    board = [[None] * 8 for _ in range(8)]
    
    # White Pieces
    board[0] = ['rook_white', 'knight_white', 'bishop_white', 'queen_white', 'king_white', 'bishop_white', 'knight_white', 'rook_white']
    board[1] = ['pawn_white'] * 8
    # Black Pieces
    board[6] = ['pawn_black'] * 8
    board[7] = ['rook_black', 'knight_black', 'bishop_black', 'queen_black', 'king_black', 'bishop_black', 'knight_black', 'rook_black']
    
    return board

# Check if a move is valid for a specific piece
def is_valid_move(piece, start_row, start_col, end_row, end_col, board):
    if not (0 <= end_row < 8 and 0 <= end_col < 8):
        return False  # Out of bounds
    
    # Check if destination is occupied by a piece of the same color
    destination_piece = board[end_row][end_col]
    if destination_piece and destination_piece.endswith(piece.split('_')[1]):
        return False  # Can't land on a piece of the same color

    if piece.startswith('king'):
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    if piece.startswith('queen'):
        return (start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col))

    if piece.startswith('rook'):
        return start_row == end_row or start_col == end_col

    if piece.startswith('bishop'):
        return abs(start_row - end_row) == abs(start_col - end_col)

    if piece.startswith('knight'):
        return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

    if piece.startswith('pawn'):
        direction = 1 if 'white' in piece else -1
        if start_col == end_col and board[end_row][end_col] is None:
            if (start_row == 1 or start_row == 6) and abs(end_row - start_row) <= 2:  # First move
                return True
            elif abs(end_row - start_row) == 1:  # Normal move
                return True
        elif abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1 and board[end_row][end_col]:
            return True  # Pawn captures
    return False

# Draw the chessboard
def draw_board(screen, board, selected_square=None, valid_moves=[]):
    for row in range(8):
        for col in range(8):
            color = SQUARE_COLORS[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Highlight selected square
            if selected_square == (row, col):
                pygame.draw.rect(screen, SELECTED_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Highlight valid moves
            if (row, col) in valid_moves:
                pygame.draw.rect(screen, VALID_MOVE_COLOR, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[row][col]
            if piece:
                screen.blit(piece_images.get(piece, None), (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Handle Pawn Promotion
def promote_pawn(board, row, col, color):
    board[row][col] = f'queen_{color}'  # Promote pawn to a queen (you can change this to select other pieces)

# Display whose turn it is with a more visible and enhanced design
def draw_turn_indicator(screen, turn):
    font = pygame.font.SysFont(None, 24)  # Increased font size for better visibility
    text = font.render(f"{turn.capitalize()}'s Turn", True, WHITE)  # White text for contrast

    # Create a background rectangle for the indicator
    rect_width = text.get_width() + 20  # Adding padding around the text
    rect_height = text.get_height() + 10
    rect_x = (WIDTH - rect_width) // 2
    rect_y = HEIGHT - rect_height  # Positioning it slightly above the bottom edge

    # Draw the background rectangle with a more visible color
    pygame.draw.rect(screen, TURN_COLOR, pygame.Rect(rect_x, rect_y, rect_width, rect_height), border_radius=10)

    # Blit the text onto the screen, centered in the rectangle
    screen.blit(text, (rect_x + 10, rect_y + 5))  # Padding inside the rectangle


# Main Game Loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    load_images()
    board = create_board()
    
    selected_square = None  # To keep track of the square currently selected by the player
    valid_moves = []  # List of valid moves for the selected piece
    turn = 'white'  # White goes first
    game_over = False

    while not game_over:
        screen.fill(BOARD_COLOR)
        draw_board(screen, board, selected_square, valid_moves)
        draw_turn_indicator(screen, turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE

                if selected_square:
                    start_row, start_col = selected_square
                    piece = board[start_row][start_col]
                    if is_valid_move(piece, start_row, start_col, row, col, board):
                        # Move piece
                        board[row][col] = piece
                        board[start_row][start_col] = None
                        
                        # Check for pawn promotion
                        if piece.startswith('pawn') and (row == 0 or row == 7):
                            promote_pawn(board, row, col, turn)
                        
                        # Switch turns
                        turn = 'black' if turn == 'white' else 'white'
                        selected_square = None
                        valid_moves = []
                    else:
                        selected_square = None  # Reset selection if move is invalid
                        valid_moves = []
                else:
                    # Select a piece
                    piece = board[row][col]
                    if piece and piece.endswith(turn):  # Only select the correct player's piece
                        selected_square = (row, col)
                        valid_moves = []

                        # Find all valid moves for the selected piece
                        for r in range(8):
                            for c in range(8):
                                if is_valid_move(piece, row, col, r, c, board):
                                    valid_moves.append((r, c))

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
