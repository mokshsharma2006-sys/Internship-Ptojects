import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe: Human (X) vs AI (O)")

        
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]


        self.create_game_grid()
        self.create_restart_button()

    def create_game_grid(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window, text=' ', font=('Arial', 36),
                    width=5, height=2,
                    command=lambda r=row, c=col: self.handle_human_move(r, c)
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

    def create_restart_button(self):
        
        restart_button = tk.Button(
            self.window, text="Restart Game", font=('Arial', 14),
            command=self.restart_game
        )
        restart_button.grid(row=3, column=0, columnspan=3, pady=10)

    def handle_human_move(self, row, col):
        
        if self.board[row][col] == ' ':
            self.board[row][col] = 'X'
            self.buttons[row][col]['text'] = 'X'
            self.buttons[row][col]['state'] = 'disabled'

            result = self.check_game_result()
            if result:
                self.show_game_over(result)
                return

            
            self.window.after(200, self.handle_ai_move)

    def handle_ai_move(self):
        
        best_score = -math.inf
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'O'
                    score = self.minimax(is_maximizing=False, depth=0, alpha=-math.inf, beta=math.inf)
                    self.board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            row, col = best_move
            self.board[row][col] = 'O'
            self.buttons[row][col]['text'] = 'O'
            self.buttons[row][col]['state'] = 'disabled'

        result = self.check_game_result()
        if result:
            self.show_game_over(result)

    def minimax(self, is_maximizing, depth, alpha, beta):
        
        result = self.check_game_result()
        if result == 'X':
            return -1
        elif result == 'O':
            return 1
        elif result == 'Tie':
            return 0

        if is_maximizing:
            best = -math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'O'
                        score = self.minimax(False, depth + 1, alpha, beta)
                        self.board[row][col] = ' '
                        best = max(best, score)
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = math.inf
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        score = self.minimax(True, depth + 1, alpha, beta)
                        self.board[row][col] = ' '
                        best = min(best, score)
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def check_game_result(self):
        
        lines = []

        
        lines.extend(self.board)
        lines.extend([[self.board[r][c] for r in range(3)] for c in range(3)])

       
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line == ['X', 'X', 'X']:
                return 'X'
            elif line == ['O', 'O', 'O']:
                return 'O'

       
        if all(self.board[r][c] != ' ' for r in range(3) for c in range(3)):
            return 'Tie'

        return None 

    def show_game_over(self, winner):
       
        message = "It's a tie!" if winner == 'Tie' else f"{winner} wins!"
        messagebox.showinfo("Game Over", message)

       
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['state'] = 'disabled'

    def restart_game(self):
        
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                btn = self.buttons[row][col]
                btn['text'] = ' '
                btn['state'] = 'normal'

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    TicTacToe().run()
