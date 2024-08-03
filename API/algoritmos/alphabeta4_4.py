import random

class Tic(object):
    winning_combos = (
        [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],  # filas
        [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],  # columnas
        [0, 5, 10, 15], [3, 6, 9, 12]  # diagonales
    )  # Tupla que contiene todas las combinaciones ganadoras posibles del juego
    winners = ('X-win', 'Draw', 'O-win')  # Tupla que contiene los posibles resultados del juego

    def __init__(self, squares=[]):  # Método inicializador de la clase, configura el tablero del juego
        """Inicializamos el tablero del juego"""
        if len(squares) == 0:
            self.squares = [None for _ in range(16)]
        else:
            self.squares = squares

    def show(self):  # Método que muestra en pantalla el estado actual del tablero
        """Indicamos en pantalla el estado actual del tablero"""
        for element in [
            self.squares[i: i + 4] for i in range(0, len(self.squares), 4)]:  # Recorremos el tablero de 4 en 4, para mostrarlo en forma de matriz 4x4
            print(element)

    def available_moves(self):  # Método que devuelve una lista con las posiciones disponibles en el tablero
        return [k for k, v in enumerate(self.squares) if v is None]

    def complete(self):  # Método que comprueba si el juego ha terminado
        """Check if game has ended"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() is not None:
            return True
        return False

    def X_won(self):  # Método que comprueba si el jugador X ha ganado
        return self.winner() == 'X'

    def O_won(self):  # Método que comprueba si el jugador O ha ganado
        return self.winner() == 'O'

    def tied(self):  # Método que comprueba si el juego ha terminado en empate
        return self.complete() and self.winner() is None

    def winner(self):  # Método que comprueba si hay un ganador en el juego
        for player in ('X', 'O'):
            positions = self.get_squares(player)  # Obtenemos las posiciones que ha ocupado el jugador
            for combo in self.winning_combos:  # Recorremos todas las combinaciones ganadoras posibles
                win = True  # Suponemos que el jugador ha ganado
                for pos in combo:  # Recorremos las posiciones de la combinación ganadora
                    if pos not in positions:  # Si alguna de las posiciones no ha sido ocupada por el jugador, entonces no ha ganado
                        win = False
                if win:  # Si el jugador ha ocupado todas las posiciones de una combinación ganadora, entonces ha ganado
                    return player
        return None

    def get_squares(self, player):  # Método que devuelve las posiciones que ha ocupado el jugador
        """Devuelve las posiciones que ha ocupado el jugador"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):  # Método que permite realizar un movimiento en el tablero
        self.squares[position] = player

    def evaluate(self):
        """Heurística mejorada para evaluar el estado del tablero"""
        if self.X_won():
            return -100
        elif self.O_won():
            return 100
        elif self.tied():
            return 0

        score = 0

        # Evalúa las líneas parciales
        for combo in self.winning_combos:
            X_count = O_count = 0
            for pos in combo:
                if self.squares[pos] == 'X':
                    X_count += 1
                elif self.squares[pos] == 'O':
                    O_count += 1
            score += self.evaluate_line(X_count, O_count)

        return score

    def evaluate_line(self, X_count, O_count):
        """Evaluar la línea basada en la cantidad de X y O en ella"""
        if X_count > 0 and O_count > 0:
            return 0
        elif X_count == 4:
            return -100
        elif O_count == 4:
            return 100
        elif X_count == 3:
            return -10
        elif O_count == 3:
            return 10
        elif X_count == 2:
            return -5
        elif O_count == 2:
            return 5
        return 0.5

    def alphabeta(self, node, player, alpha, beta, depth):
        """Algoritmo Alfa Beta para determinar el mejor movimiento"""
        if node.complete() or depth == 0:  # Si el juego ha terminado o alcanzamos la profundidad máxima
            return node.evaluate()

        if player == 'O':  # Maximizador
            max_eval = -float('inf')
            for move in node.available_moves():
                node.make_move(move, player)
                eval = self.alphabeta(node, get_enemy(player), alpha, beta, depth - 1)
                node.make_move(move, None)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:  # Minimizador
            min_eval = float('inf')
            for move in node.available_moves():
                node.make_move(move, player)
                eval = self.alphabeta(node, get_enemy(player), alpha, beta, depth - 1)
                node.make_move(move, None)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


def get_enemy(player):  # Método que devuelve el jugador contrario
    if player == 'X':
        return 'O'
    return 'X'


def determine(board, player, depth=4): # Indicamos la profundidad
    """Determina el mejor movimiento posible"""
    best_val = -float('inf')
    choices = []  # Lista para almacenar los mejores movimientos.

    # Para cada movimiento disponible en el tablero.
    for move in board.available_moves():
        # Realizamos el movimiento para el jugador actual.
        board.make_move(move, player)
        # Evaluamos el tablero resultante llamando a 'alphabeta'.
        val = board.alphabeta(board, get_enemy(player), -float('inf'), float('inf'), depth)
        # Deshacemos el movimiento para restaurar el estado original.
        board.make_move(move, None)

        # Si el valor devuelto por 'alphabeta' es mejor que 'best_val', actualizamos 'best_val' y los mejores movimientos.
        if val > best_val:
            best_val = val
            choices = [move]
        # Si el valor es igual a 'best_val', añadimos este movimiento a la lista de mejores movimientos.
        elif val == best_val:
            choices.append(move)

    # Seleccionamos y devolvemos uno de los mejores movimientos posibles aleatoriamente.
    return random.choice(choices)


if __name__ == '__main__':  # Si el script se ejecuta directamente y no se importa como módulo
    board = Tic()  # Creamos un tablero de juego, que es una instancia de la clase ConnectFour
    board.show()  # Mostramos el tablero en pantalla

    while not board.complete():  # Mientras el juego no haya terminado
        player = 'X'  # El jugador actual es 'X'
        player_move = int(input('Next Move: ')) - 1  # Pedimos al usuario que introduzca un movimiento, y lo reducimos en 1 para que sea un índice válido
        if player_move not in board.available_moves():  # Si el movimiento no es válido, pedimos otro
            continue
        board.make_move(player_move, player)  # Realizamos el movimiento
        board.show()  # Mostramos el tablero en pantalla

        if board.complete():  # Si el juego ha terminado, salimos del bucle
            break
        player = get_enemy(player)  # Cambiamos de jugador
        computer_move = determine(board, player, depth=6)  # Determinamos el mejor movimiento para el jugador actual
        board.make_move(computer_move, player)  # Realizamos el movimiento
        board.show()  # Mostramos el tablero en pantalla
    print('Winner is', board.winner())  # Mostramos el ganador del juego
