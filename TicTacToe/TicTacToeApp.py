import threading
import tkinter as tk
from TicTacToe.alphabeta4_4 import Tic as Tic4x4, determine as determine4x4, get_enemy
from TicTacToe.alphabeta3_3 import Tic as Tic3x3, determine as determine3x3
import gestureDetection.gestosToTicTacToe as ttt
from robot.urx import coger_pieza, dejar_pieza, recoger_tablero, monitor_force, desapilar_pieza, apilar_pieza_de_vuelta

class TicTacToeApp:
    def __init__(self, root, board_size, determine_func):
        self.root = root  # Ventana principal
        self.root.title("Tic-Tac-Toe")  # Titulo de la ventana
        self.board_size = board_size #NEW2.0
        self.determine = determine_func #NEW2.0
        self.force_threshold = 25.0  # Define el umbral de fuerza para iniciar la partida #NEW4.0
        self.first_move = True  # NEW4.0
        self.board = self.create_board_instance()  # Instancia de la clase Tic que contiene la lógica del juego #NEW2.0
        self.buttons = [tk.Button(self.root, text="", font='Arial 20', width=5, height=2,
                                  command=lambda i=i: self.on_button_click(i+1)) for i in range(16)]  # 16 botones para un tablero de 4x4
        self.create_board()  # Método que organiza los botones en una cuadrícula 3x3
        self.current_player = 'X'  # Jugador actual
        self.game_over = False  # Booleano que indica si el juego ha terminado
        self.root.update_idletasks()
        self.center_window(self.root)  # Centra la ventana principal
        
        # Iniciar hilo de detección de gestos
        self.start_gesture_detection()

        # Añadir botón para reiniciar secuencia de gestos
        self.reset_button = tk.Button(self.root, text="Reiniciar Secuencia", command=self.reset_sequence, font='Arial 15')
        self.reset_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Contadores de piezas
        self.x_counter = 1
        self.o_counter = 1
        
        #NEW
        self.computer_move_thread = None
        self.computer_move = None
        
        # Hilo para monitorear la fuerza #NEW4.0
        self.monitor_thread = threading.Thread(target=self.monitor_force)
        self.monitor_thread.start()
    
    #NEW 4.0
    def monitor_force(self):
        if (monitor_force(self.force_threshold, self.first_move)):
            self.current_player = 'O'
            self.start_computer_move()
            self.first_move = False  # NEW4.0
                               
    #NEW2.0
    def create_board_instance(self):
        if self.board_size == 4:
            return Tic4x4()
        else:
            return Tic3x3()    

    def create_board(self): #NEW2.0
        for i in range(self.board_size * self.board_size):
            row, col = divmod(i, self.board_size)
            self.buttons[i].grid(row=row, column=col)

    def center_window(self, window, parent=None):
        """Centra la ventana en la pantalla o dentro de la ventana principal sin cambiar su tamaño"""
        window.update_idletasks()  # Asegura que la geometría esté actualizada
        width = window.winfo_width()
        height = window.winfo_height()
        if parent is None:
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
        else:
            parent.update_idletasks()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            x_offset = parent.winfo_x()
            y_offset = parent.winfo_y()
            x = x_offset + (parent_width - width) // 2
            y = y_offset + (parent_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def on_button_click(self, index):  # Método que se ejecuta al hacer clic en un botón
        if not self.game_over and self.board.squares[index-1] is None:  # Si el juego no ha terminado y la casilla está vacía
            self.make_move(index-1, self.current_player)  # Realizamos el movimiento
            if not self.game_over:  # Si el juego no ha terminado
                self.current_player = get_enemy(self.current_player)  # Cambiamos de jugador
                if self.first_move:
                    self.first_move = False
                    print(False)
                #if self.current_player == 'O':  # Si el jugador actual es la computadora
                    #self.start_computer_move()  # Realizamos el movimiento de la computadora

    def make_move(self, index, player):  # Método que realiza un movimiento en el tablero
        self.board.make_move(index, player)  # Realizamos el movimiento en el tablero
        self.buttons[index].config(text=player, state='disabled')  # Configuramos el botón correspondiente con el texto del jugador y lo deshabilitamos
        
        if player == 'X' and not self.game_over: #New
            self.start_computer_move()  # Inicia el cálculo del movimiento del ordenador
        
        self.root.update_idletasks()  # Asegura que la interfaz gráfica se actualice
        self.perform_robot_move(index, player)  # Llama a la función para que el robot realice el movimiento
        
        if self.board.complete():  # Si el juego ha terminado
            self.game_over = True  # Indicamos que el juego ha terminado
            winner = self.board.winner()  # Obtenemos al ganador
            if winner:  # Si hay un ganador
                self.show_result(f"¡{winner} ha ganado!")  # Mostramos el resultado
            else:  # Si no hay ganador
                self.show_result("¡Empate!")  # Mostramos el resultado
        
    #new
    def start_computer_move(self):
        self.computer_move_thread = threading.Thread(target=self.calculate_computer_move)
        self.computer_move_thread.start()

    #New
    def calculate_computer_move(self):
        self.computer_move = self.determine(self.board, 'O')
        self.root.after(0, self.finish_computer_move) # Actualizamos la GUI tan pronto como sea posible

    #New
    def finish_computer_move(self):
        if self.computer_move is not None:
            self.make_move(self.computer_move, 'O')
            self.computer_move = None
        self.current_player = get_enemy(self.current_player)

    def perform_robot_move(self, index, player):
        # Lógica para controlar al robot y colocar la pieza
        row, col = divmod(index, self.board_size)  # Cambiado de 3 a 4 #NEW2.0
        config = f"{row + 1}{col + 1}"
        if self.board_size == 4: #NEW5.0
            if player == 'X':
                desapilar_pieza('X', self.x_counter)
                self.x_counter += 1
            elif player == 'O':
                desapilar_pieza('O', self.o_counter)
                self.o_counter += 1
            dejar_pieza(config)
        else:
            if player == 'X':
                coger_pieza(f"X{self.x_counter}")
                dejar_pieza(config)
                self.x_counter += 1
            elif player == 'O':
                coger_pieza(f"O{self.o_counter}")
                dejar_pieza(config)
                self.o_counter += 1


    def show_result(self, message):  # Método que muestra el resultado del juego
        self.result_window = tk.Toplevel(self.root)  # Ventana secundaria para mostrar el resultado
        self.result_window.title("Resultado")  # Título de la ventana
        tk.Label(self.result_window, text=message, font='Arial 20').pack()  # Etiqueta con el mensaje del resultado
        tk.Button(self.result_window, text="Reiniciar", command=self.restart_game).pack()  # Botón para reiniciar el juego
        self.result_window.update_idletasks()
        self.center_window(self.result_window, parent=self.root)  # Centra la ventana secundaria

    def show_wait_window(self):
        self.wait_window = tk.Toplevel(self.root)
        self.wait_window.title("Espere por favor")
        tk.Label(self.wait_window, text="Recogiendo el tablero, espere por favor...", font='Arial 20').pack()
        self.wait_window.update_idletasks()
        self.center_window(self.wait_window, parent=self.root)

    def hide_wait_window(self):
        self.wait_window.destroy()

    def restart_game(self):
        self.show_wait_window()  # Mostrar ventana de espera

        # Restablecer el tablero y limpiar los contadores de piezas
        threading.Thread(target=self.reset_board).start()

    def reset_board(self):
        #NEW7.0
        # Llamar a la función para que el robot recoja las piezas
        recoger_tablero()
        
        # Limpiar el tablero en la interfaz gráfica
        self.board = self.create_board_instance()  # Reiniciamos el tablero #NEW2.0
        self.current_player = 'X'  # Jugador actual
        self.first_move = True #NEW4.0
        self.game_over = False  # Indicamos que el juego no ha terminado
        self.x_counter = 1  # Reiniciamos el contador de piezas X
        self.o_counter = 1  # Reiniciamos el contador de piezas O
        for button in self.buttons:  # Reiniciamos los botones
            button.config(text="", state='normal')  # Configuramos los botones con texto vacío y habilitados
        
        self.root.after(100, self.hide_wait_window)  # Cerrar ventana de espera
    
    def reset_sequence(self):
        global sequence
        sequence = []  # Reiniciar la secuencia de gestos
        print("Secuencia de gestos reiniciada")

    def start_gesture_detection(self):
        # Iniciar el hilo de detección de gestos
        gesture_thread = threading.Thread(target=ttt.detect_gestures, args=(self.make_move_from_gesture,))
        gesture_thread.daemon = True  # Permite que el hilo se cierre cuando el programa principal termine
        gesture_thread.start()

    def make_move_from_gesture(self, fila, columna):
        # Convierte la fila y columna en un índice del tablero de 0 a 8
        index = (fila - 1) * 3 + (columna - 1)
        if not self.game_over and self.board.squares[index] is None:
            self.make_move(index, self.current_player)
            if not self.game_over:
                self.current_player = get_enemy(self.current_player)
                if self.first_move:
                    self.first_move = False
                    print(False)
