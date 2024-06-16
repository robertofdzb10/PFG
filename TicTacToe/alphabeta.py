import random


class Tic(object):

    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]) # Tupla que contiene todas las combinaciones ganadoras posibles del juego
    winners = ('X-win', 'Draw', 'O-win') # Tupla que contiene los posibles resultados del juego

    def __init__(self, squares=[]): # Metodo inicializador de la clase, configura el tablero del juego, si no se le pasa un tablero personalizado, crea uno por defecto, formado por una lista de 9 elementos, todos ellos con el valor None
        """Inicializamos el tablero del juego"""
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares

    def show(self): # Metodo que muestra en pantalla el estado actual del tablero
        """Indicamos en pantalla el estado actual del tablero"""
        for element in [
                self.squares[i: i + 3] for i in range(0, len(self.squares), 3)]: # Recorremos el tablero de 3 en 3, para mostrarlo en forma de matriz 3x3
            print(element)

    def available_moves(self): # Metodo que devuelve una lista con las posiciones disponibles en el tablero
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player): # Metodo que devuelve una lista con las posiciones disponibles en el tablero ademas de las posiciones que ya ha ocupado el jugador
        return self.available_moves() + self.get_squares(player)

    def complete(self): # Metodo que comprueba si el juego ha terminado, ya sea porque no quedan mas movimientos disponibles o porque ya hay un ganador
        """Check if game has ended"""
        if None not in [v for v in self.squares]:
            return True
        if self.winner() is not None:
            return True
        return False

    def X_won(self): # Metodo que comprueba si el jugador X ha ganado
        return self.winner() == 'X'

    def O_won(self): # Metodo que comprueba si el jugador O ha ganado
        return self.winner() == 'O'

    def tied(self): # Metodo que comprueba si el juego ha terminado en empate
        return self.complete() and self.winner() is None

    def winner(self): # Metodo que comprueba si hay un ganador en el juego
        for player in ('X', 'O'):
            positions = self.get_squares(player) # Obtenemos las posiciones que ha ocupado el jugador
            for combo in self.winning_combos: # Recorremos todas las combinaciones ganadoras posibles
                win = True # Suponemos que el jugador ha ganado
                for pos in combo: # Recorremos las posiciones de la combinacion ganadora
                    if pos not in positions: # Si alguna de las posiciones no ha sido ocupada por el jugador, entonces no ha ganado
                        win = False
                if win: # Si el jugador ha ocupado todas las posiciones de una combinacion ganadora, entonces ha ganado
                    return player
        return None

    def get_squares(self, player): # Metodo que devuelve las posiciones que ha ocupado el jugador
        """Devuelve las posiciones que ha ocupado el jugador"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player): # Metodo que permite realizar un movimiento en el tablero
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        """Algoritmo Alfa Beta para determinar el mejor movimiento"""
        if node.complete(): # Si el juego ha terminado
            if node.X_won(): # Si el jugador X ha ganado, devolvemos -1
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1

        for move in node.available_moves(): # Para cada movimiento disponible
            node.make_move(move, player) # Realizamos el movimiento
            val = self.alphabeta(node, get_enemy(player), alpha, beta) # Llamada recursiva
            node.make_move(move, None) # Deshacemos el movimiento

            if player == 'O': # Si el jugador es 'O' (maximizador)
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else: # Si el jugador es 'X' (minimizador)
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        return alpha if player == 'O' else beta



def get_enemy(player): # Metodo que devuelve el jugador contrario
    if player == 'X':
        return 'O'
    return 'X'


def determine(board, player):
    """Determine el mejor movimiento posible"""
    a = -2  # Inicializamos 'a' con un valor muy bajo.
    choices = []  # Lista para almacenar los mejores movimientos.

    # Si es el primer movimiento del juego, se elige el centro del tablero.
    if len(board.available_moves()) == 9:
        return 4

    # Para cada movimiento disponible en el tablero.
    for move in board.available_moves():
        # Realizamos el movimiento para el jugador actual.
        board.make_move(move, player)
        # Evaluamos el tablero resultante llamando a 'alphabeta'.
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        # Deshacemos el movimiento para restaurar el estado original.
        board.make_move(move, None)

        # Si el valor devuelto por 'alphabeta' es mejor que 'a', actualizamos 'a' y los mejores movimientos.
        if val > a:
            a = val
            choices = [move]
        # Si el valor es igual a 'a', añadimos este movimiento a la lista de mejores movimientos.
        elif val == a:
            choices.append(move)

    # Seleccionamos y devolvemos uno de los mejores movimientos posibles aleatoriamente.
    return random.choice(choices)



if __name__ == '__main__': # Si el script se ejecuta directamente y no se importa como modulo
    board = Tic() # Creamos un tablero de juego, que es una instancia de la clase Tic
    board.show() # Mostramos el tablero en pantalla

    while not board.complete(): # Mientras el juego no haya terminado
        player = 'X' # El jugador actual es 'X'
        player_move = int(input('Next Move: ')) - 1 # Pedimos al usuario que introduzca un movimiento, y lo reducimos en 1 para que sea un indice valido
        if player_move not in board.available_moves(): # Si el movimiento no es valido, pedimos otro
            continue
        board.make_move(player_move, player)  # Realizamos el movimiento
        board.show() # Mostramos el tablero en pantalla

        if board.complete(): # Si el juego ha terminado, salimos del bucle
            break
        player = get_enemy(player) # Cambiamos de jugador
        computer_move = determine(board, player) # Determinamos el mejor movimiento para el jugador actual
        board.make_move(computer_move, player) # Realizamos el movimiento
        board.show() # Mostramos el tablero en pantalla
    print('Winner is', board.winner()) # Mostramos el ganador del juego
