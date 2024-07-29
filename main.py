if __name__ == '__main__':
    import tkinter as tk
    from TicTacToe.TicTacToeApp import TicTacToeApp
    from robot.BoardSizeSelectionApp import BoardSizeSelectionApp
    import warnings
    
    warnings.filterwarnings("ignore", category=UserWarning)

    root = tk.Tk()
    selection_app = BoardSizeSelectionApp(root)
    root.mainloop()
