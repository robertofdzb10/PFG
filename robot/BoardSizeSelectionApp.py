import tkinter as tk
from TicTacToe.TicTacToeApp import TicTacToeApp
from TicTacToe.alphabeta4_4 import Tic as Tic4x4, determine as determine4x4
from TicTacToe.alphabeta3_3 import Tic as Tic3x3, determine as determine3x3


class BoardSizeSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selecciona el tamaño del tablero")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Selecciona el tamaño del tablero", font='Arial 20').pack(pady=20)
        tk.Button(self.root, text="3x3", font='Arial 20', width=10, command=lambda: self.start_game(3)).pack(pady=10)
        tk.Button(self.root, text="4x4", font='Arial 20', width=10, command=lambda: self.start_game(4)).pack(pady=10)
        self.root.update_idletasks()
        self.center_window(self.root)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_game(self, board_size):
        self.root.destroy()
        main_app_root = tk.Tk()
        if board_size == 4:
            app = TicTacToeApp(main_app_root, board_size, determine4x4)
        else:
            app = TicTacToeApp(main_app_root, board_size, determine3x3)
        main_app_root.mainloop()