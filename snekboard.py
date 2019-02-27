import random
import snek
import getch


class Snekboard():
    def __init__(self, width: int, height: int):
        self._width = width  # sirka
        self._height = height  # vyska
        self._rewards = self._generate_snekfoods()  # vola generovanie snekfoodu
        self._player = snek.Snek(random.randint(0, self._width - 1), random.randint(0,
                                                                                    self._width - 1))  # instancia klasy snek o random pozicii v dimenziach boardu

    def _draw(self):
        """
        draws the board
        """
        print('\n'.join(self._board()))  # linebreak
        print('-' * self._width) # ohranici board zo spodu pomlckami?

    def _round(self):
        pressed_key = getch.getKey()  # ziska key
        previous_position = self._player.position()  # urci staru poziciu - naco?
        self._player.move(pressed_key)  # na zaklade inputnuteho pressedkeya movene
        x, y = self._player.position()  # urci x,y pomocou metody zo Snek-a

        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            self._player.set_position(
                previous_position)  # todo v starom zabranovalo aby sa playa hybal mimo stien, prerobit na snekovrazdu v [pripade narazenia do steny
        if self._player.position() in self._rewards:
            self._player.eat_snekfood(1)
                # todo prerobit na if prvy prvok listu hadieho tela in self.rewards -> append nakoniec proti smeru direkcie/na zaciatok waewa
            self._rewards.remove(self._player.position())  # vyhodi z boardu popapany snekfood
        else:
            del self._player._snek_body_coords[-1] # todo novoaddnuta vec - vyhodi na konci kola posledny prvok suradnic ak nebol zjedeny snekfood

    def _board(self):
        for y in range(self._height):  # za kazde y v rangi vysky vznikne prazdny riadok
            line = ""
            for x in range(self._width):
                line += self._at(x,
                                 y)  # za kazdy x v rangi sirky sa k prazdnemu riadku appendne prvok vykreslujuci board podla metody _at
            yield line  # vykaka Y riadkov

    def play(self):
        self._draw()  # zavola nakreslenie boardu
        while True:
            self._round()  # udeje sa kolo a vyhodnotia sa blbosti ako ci sa had nazral a kam siel
            self._draw()  # opat zavola nakreslenie boardu, opakuje sa cyklus
        # print('Koniec uchvatnej hry, dosiahol si skore {}'.format(self._player.moneyz())) todo prerobit na zaverecnoherny message v pripade kusnutia sa/narazenia

    def _random_snekfood(self):  # metoda co randomne urci suradnice snekfoodu
        return random.randint(0, self._width - 1), random.randint(0, self._height - 1)

    def _generate_snekfoods(
            self):  # returnne dict??? nahodne sa nachadajucich snekfoodov podla predchadzajucej metody za kazdy bod sirky boardu
        return {self._random_snekfood()
                for _ in range(self._width)}

    def _at(self, x, y):
        if self._player.position() == (x, y):  # todo tuto nech to robi podla listu hadovych suradnic
            return 'OO'  # vypluje kus hada
        if (x, y) in self._rewards:
            return ' S'  # vypluje snekfood
        return ' -'  # vypluje prazdnu vypln boardu
