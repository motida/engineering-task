import random

ABBREVIATIONS = {'submarine': 'S', 'destroyer': 'D', 'cruiser': 'C', 'carrier': 'A'}
BATTLESHIPS = {'S': (1, 1), 'D': (2, 1), 'C': (3, 1), 'A': (4, 1)}  # Values are dimensions
                                                                    # (2, 1) means 1x2 or 2x1 positioning


class Battlefield:
    def __init__(self, n, m):
        self.m = m
        self.n = n
        self.board = [row[:] for row in [[None] * m] * n]

        self.free_battleship_pieces = self._generate_battleship_locations()

    def _generate_battleship_locations(self):
        """
        Generate all potential pieces, each piece is represented by a set of position on battlefield
        :return: set of free pieces
        """
        free_pieces = {}
        for battleship_type in BATTLESHIPS:
            dimension = BATTLESHIPS[battleship_type]
            free_pieces[battleship_type] = self._get_battleship_type_pieces(dimension)
            if dimension[0] != dimension[1]:  # switch orientation if necessary
                free_pieces[battleship_type] = free_pieces[battleship_type] | \
                                                  self._get_battleship_type_pieces((dimension[1], dimension[0]))
        return free_pieces

    def _get_battleship_type_pieces(self, dimension):
        """
        Generate all possible pieces for dimension
        :param dimension: represent a piece with specific orientation
        :return: set of free pieces  
        """
        x_size, y_size = dimension
        return {frozenset([(x_pos, y_pos)
                           for x_pos in range(row, row + x_size)
                           for y_pos in range(col, col + y_size)])
                for row in range(self.n - x_size + 1)
                for col in range(self.m - y_size + 1)}

    def __str__(self):
        """
        Generate a string with battlefield representation 
        :return: 
        """
        output = ''
        for row in range(self.n):
            for col in range(self.m):
                output += (self.board[row][col] if self.board[row][col] else '.')
            output += '\n'
        return output

    def _place_in_board(self, piece, piece_symbol):
        """
        Places piece on board for easy printing 
        :param piece: 
        :param piece_symbol: 
        :return: 
        """
        for (row, col) in piece:
            self.board[row][col] = piece_symbol

    def _remove_overlapping_free_locations(self, piece):
        """
        This will remove the placed piece itself and all other pieces whose locations overlaps with placed piece
        from free pieces pool
        """
        buffered_piece = self._generate_buffered_piece(piece)
        for battleship_type in BATTLESHIPS:
            locations_to_discard = []
            for free_piece in self.free_battleship_pieces[battleship_type]:
                if free_piece & buffered_piece:  # points in common means they overlap
                    locations_to_discard.append(free_piece)
            self.free_battleship_pieces[battleship_type].difference_update(locations_to_discard)

    def _generate_buffered_piece(self, piece):
        """
        Generate a piece that include a buffer surrounding original piece
        :param piece: 
        :return: buffered_piece
        """
        buffered_piece = set()
        for pos in piece:
            buffered_pos = {(pos[0] + x_delta, pos[1] + y_delta) for x_delta in (-1, 0, 1) for y_delta in (-1, 0, 1)}
            buffered_piece.update(buffered_pos)

        return buffered_piece

    def place_battleship(self, battleship_type):
        """
        Randomly chooses a battleship from free available pieces locations on battlefield
        places it on the board and removes it and overlapping available pieces locations
        :param battleship_type:
        :return: piece or None if no available space for battleship type on battlefield
        """
        if len(self.free_battleship_pieces[battleship_type]) == 0:
            return None
        piece = random.choice(tuple(self.free_battleship_pieces[battleship_type]))
        self._place_in_board(piece, battleship_type)
        self._remove_overlapping_free_locations(piece)
        return piece

    def place_submarine(self):
        """
        :return: submarine or None if no available space on battlefield
        """
        return self.place_battleship('S')

    def place_destroyer(self):
        """
        :return: destroyer or None if no available space on battlefield
        """
        return self.place_battleship('D')

    def place_cruiser(self):
        """
        :return: cruiser or None if no available space on battlefield
        """
        return self.place_battleship('C')

    def place_carrier(self):
        """
        :return: aircraft carrier or None if no available space on battlefield
        """
        return self.place_battleship('A')


if __name__ == '__main__':
    rows = 100  # Board x-size
    cols = 100  # Board y-size
    number_of_pieces = 500  # Number of pieces (might not all places if no free space)
    battlefield = Battlefield(rows, cols)
    for _ in range(number_of_pieces):
        battleship_type = random.choice(list(BATTLESHIPS.keys()))  # randomly choose battleship type
        if battleship_type == 'S':
            battlefield.place_submarine()
        elif battleship_type == 'D':
            battlefield.place_submarine()
        elif battleship_type == 'C':
            battlefield.place_cruiser()
        else:
            battlefield.place_carrier()
        # Alternatively can just do
        # battlefield.place_battleship(battleship_type)
    print(battlefield)

