import tkinter as tk
import random

class ReversiGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Reversi")
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'X'
        self.board[4][4] = 'X'
        self.board[3][4] = 'O'
        self.board[4][3] = 'O'
        self.current_player = 'X'
        self.draw_board()
        self.game_over = False
        if self.current_player == 'O':
            self.computer_move()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="green")
                if self.board[i][j] == 'X':
                    self.canvas.create_oval(j * 50 + 5, i * 50 + 5, (j + 1) * 50 - 5, (i + 1) * 50 - 5, fill="black")
                elif self.board[i][j] == 'O':
                    self.canvas.create_oval(j * 50 + 5, i * 50 + 5, (j + 1) * 50 - 5, (i + 1) * 50 - 5, fill="white")

    def human_move(self, event):
        if self.game_over or self.current_player != 'X':
            return
        col = event.x // 50
        row = event.y // 50
        if self.is_valid_move(row, col):
            self.make_move(row, col)
            self.draw_board()
            if not self.game_over:
                self.computer_move()

    def computer_move(self):
        if self.game_over or self.current_player != 'O':
            return
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    possible_moves.append((i, j))
        if possible_moves:
            row, col = random.choice(possible_moves)
            self.make_move(row, col)
            self.draw_board()

    def is_valid_move(self, row, col):
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        if self.board[row][col] != ' ':
            return False
        return self.check_directions(row, col)

    def check_directions(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.get_opponent():
                r, c = r + dr, c + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] == self.current_player:
                        return True
                    elif self.board[r][c] == ' ':
                        break
                    r, c = r + dr, c + dc
        return False

    def make_move(self, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player
            self.flip_tiles(row, col)
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if not any(' ' in row for row in self.board):
                self.game_over = True
                self.show_winner()

    def flip_tiles(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            tiles_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.get_opponent():
                tiles_to_flip.append((r, c))
                r, c = r + dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player:
                for tile_row, tile_col in tiles_to_flip:
                    self.board[tile_row][tile_col] = self.current_player

    def get_opponent(self):
        return 'O' if self.current_player == 'X' else 'X'

    def show_winner(self):
        x_count = sum(row.count('X') for row in self.board)
        o_count = sum(row.count('O') for row in self.board)
        if x_count > o_count:
            winner = "Player X"
        elif x_count < o_count:
            winner = "Player O"
        else:
            winner = "It's a tie"
        self.game_over = True
        self.master.title(f"Reversi - {winner} wins with {max(x_count, o_count)} circles!")


def main():
    root = tk.Tk()
    game = ReversiGUI(root)
    game.canvas.bind("<Button-1>", game.human_move)
    root.mainloop()

if __name__ == "__main__":
    main()
