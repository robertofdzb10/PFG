if __name__ == '__main__':
    import tkinter as tk
    from TicTacToe.TicTacToeApp import TicTacToeApp
    import warnings
    
    warnings.filterwarnings("ignore", category=UserWarning)

    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
