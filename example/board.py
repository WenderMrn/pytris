from blessed import Terminal
import time

term = Terminal()

# Tamanho do board (matriz)
ROWS = 10
COLS = 78
CELL_WIDTH = 2  # largura de cada "célula" (em caracteres)

# Exemplo de matriz
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            ch = board[row][col]
            x = col * CELL_WIDTH
            y = row
            print(term.move(y, x) + term.on_black + term.white(f' {ch} '))

def update_cell(row, col, ch, fg=term.white, bg=term.on_blue):
    board[row][col] = ch
    x = col * CELL_WIDTH
    y = row
    print(term.move(y, x) + bg + fg(f' {ch} ') + term.normal)

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        draw_board()

        # Exemplo: preencher algumas células
        update_cell(0, 0, 'A', fg=term.red, bg=term.on_yellow)
        update_cell(1, 1, 'B', fg=term.black, bg=term.on_cyan)
        update_cell(2, 2, 'X', fg=term.green, bg=term.on_red)

        print(term.move(ROWS + 1, 0) + term.white("Pressione 'q' para sair."))

        # Loop de espera
        while True:
            key = term.inkey(timeout=0.1)
            if key.lower() == 'q':
                break
            time.sleep(0.01)

if __name__ == "__main__":
    main()
