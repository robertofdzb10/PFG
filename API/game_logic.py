from algoritmos.alphabeta4_4 import Tic as Tic4x4, determine as determine4x4, get_enemy
from algoritmos.alphabeta3_3 import Tic as Tic3x3, determine as determine3x3
from PIL import Image, ImageDraw, ImageFont
import io

class TicTacToe:
    def __init__(self, board_size):
        self.board_size = board_size
        self.cell_size = 400 // board_size  # Ajustar dinámicamente el tamaño de las celdas
        self.board = self.create_board_instance()
        self.current_player = 'X'
        self.game_over = False

    def create_board_instance(self):
        if self.board_size == 4:
            return Tic4x4()
        else:
            return Tic3x3()

    def make_move(self, index, player):
        if not self.game_over and self.board.squares[index] is None:
            self.board.make_move(index, player)
            if player == 'X' and not self.game_over:
                self.start_computer_move()
            return True
        return False

    def start_computer_move(self):
        if not self.game_over:
            computer_move = determine4x4(self.board, 'O') if self.board_size == 4 else determine3x3(self.board, 'O')
            if computer_move is not None:
                self.make_move(computer_move, 'O')
            self.current_player = get_enemy(self.current_player)

    def check_game_over(self):
        if self.board.complete():
            self.game_over = True
            winner = self.board.winner()
            if winner:
                return f"{winner} ha ganado!"
            else:
                return "Empate!"
        return None

    def reset(self):
        self.board = self.create_board_instance()
        self.current_player = 'X'
        self.game_over = False

    def get_board(self):
        return self.board.squares

    def get_board_image(self):
        cell_size = self.cell_size  # Tamaño de cada celda en píxeles
        board_size_px = self.board_size * cell_size  # Tamaño del tablero en píxeles
        image = Image.new("RGB", (board_size_px, board_size_px), "white")  # Creamos una imagen en blanco, con el tamaño del tablero
        draw = ImageDraw.Draw(image)  # Creamos un objeto para dibujar en la imagen
        font = ImageFont.load_default()  # Cargamos la fuente por defecto

        for i in range(1, self.board_size):  # Dibujamos las líneas del tablero
            draw.line((i * cell_size, 0, i * cell_size, board_size_px), fill="black")
            draw.line((0, i * cell_size, board_size_px, i * cell_size), fill="black")

        for i, cell in enumerate(self.board.squares):  # Dibujamos las fichas en el tablero
            if cell is not None:  # Si la celda no está vacía
                row, col = divmod(i, self.board_size)  # Obtenemos la fila y la columna de la celda
                x = col * cell_size + cell_size // 2 
                y = row * cell_size + cell_size // 2
                draw.text((x, y), cell, font=font, fill="black", anchor="mm")  # Dibujamos la ficha en el centro de la celda

        return image 

    def click_cell(self, x, y):
        cell_size = self.cell_size  # Tamaño de cada celda en píxeles
        row = y // cell_size  # Fila de la celda clickeada
        col = x // cell_size  # Columna de la celda clickeada
        index = row * self.board_size + col  # Índice de la celda clickeada

        # Depuración: Imprimir las coordenadas calculadas y el índice
        print(f"Click at x={x}, y={y}; row={row}, col={col}; index={index}")


        if self.make_move(index, self.current_player):  # Si se pudo realizar el movimiento
            self.current_player = get_enemy(self.current_player)  # Cambiamos de jugador
        return self.check_game_over()  # Comprobamos si el juego ha terminado
