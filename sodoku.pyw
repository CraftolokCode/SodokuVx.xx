import pygame
import sys

# Sudoku tábla
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Inicializáljuk a Pygame-et
pygame.init()

# Ablak beállításai
cell_size = 60
window_size = (cell_size * 9, cell_size * 9)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Sudoku")

# Színek
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Betűtípus inicializálása
font = pygame.font.Font(None, 36)

selected_cell = None
input_text = ""

def draw_grid():
    for i in range(9):
        for j in range(9):
            pygame.draw.rect(window, BLACK, (i * cell_size, j * cell_size, cell_size, cell_size), 1)

def draw_numbers(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                number = font.render(str(board[i][j]), True, BLACK)
                window.blit(number, (i * cell_size + 20, j * cell_size + 10))

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def is_solved(board):
    for row in board:
        if 0 in row:
            return False
    return True

def draw_selected_cell(selected_cell):
    row, col = selected_cell
    pygame.draw.rect(window, GREEN, (col * cell_size, row * cell_size, cell_size, cell_size), 3)

def draw_input_box():
    pygame.draw.rect(window, BLACK, (selected_cell[1] * cell_size, selected_cell[0] * cell_size, cell_size, cell_size), 3)

def main():
    clock = pygame.time.Clock()
    solving = False

    global selected_cell
    global input_text

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not solving:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // cell_size, y // cell_size
                    if sudoku_board[row][col] == 0:
                        selected_cell = (row, col)
                        input_text = ""

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solving:
                    solving = True
                    if is_solved(sudoku_board):
                        solve_sudoku(sudoku_board)
                elif selected_cell and not solving:
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        input_text = event.unicode
                        sudoku_board[selected_cell[0]][selected_cell[1]] = int(input_text)
                    elif event.key == pygame.K_RETURN:
                        selected_cell = None
                        input_text = ""

        window.fill(WHITE)
        draw_grid()
        draw_numbers(sudoku_board)
        if selected_cell:
            draw_selected_cell(selected_cell)
            draw_input_box()
            input_surface = font.render(input_text, True, BLACK)
            window.blit(input_surface, (selected_cell[1] * cell_size + 20, selected_cell[0] * cell_size + 10))

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
