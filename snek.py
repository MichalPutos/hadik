UP, DOWN, LEFT, RIGHT = 'w', 's', 'a', 'd'


class Snek():
    def __init__(self, position_x, position_y):
        self._position = (position_x, position_y)  # zaciatocna definicia pozicie
        self._snekfoods = 0  # pocet zozratych snekfoodov
        self._snek_body_coords = [self._position] # todo novoaddnute - list snekovych suradnic ktore sa budu priratavat z povodnych suradnic v metode move
    def move(self, direction):
        if direction not in [UP, DOWN, LEFT, RIGHT]:
            raise RuntimeError('zly smer' + direction)

        change = {
            UP: (0, -1),
            DOWN: (0, 1),
            LEFT: (-1, 0),
            RIGHT: (1, 0),
        }
        self._position = (self._position[0] + change[direction][0], self._position[1] + change[direction][1])
        self._snek_body_coords.insert(0, self._position) # todo prida na zaciatok listu suradnic sneka movnute suradnice


    def eat_snekfood(self, amount):
        if amount < 1:
            raise RuntimeError('Nic nevygrcam')
        self._snekfoods += amount

    def position(self):
        return self._position # metoda kt vytiahne z instancie Sneka suradnice x,y. pouzivane v board/round

    def set_position(self, position):
        self._position = position # prepise _position na zaklade vlozeneho parametru, pouzite zatial iba ak player trafi stenu, aby sa mu nemenila pozicia
