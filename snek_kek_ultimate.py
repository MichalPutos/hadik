import fancy_letters as fl
import realtime_getch
import random
import time


class Snek():

    def __init__(self, h, w):
        self.yummy_level = 0
        snek_pos_x = w // 2
        snek_pos_y = h // 2
        self.pos_list = [(snek_pos_x, snek_pos_y, '-'), (snek_pos_x + 1, snek_pos_y, '-')]
        self.eaten = False

    def determine_head(self, direction):
        heads_to_directions_dict = {'w': '<', 'e': '>', 's': 'v', 'n': '^'}
        head = heads_to_directions_dict.get(direction)
        return head

    def find_position_to_go(self, direction, pos_list):
        if direction in ('w', 'e'):
            orientation = '-'
        elif direction in ('n', 's'):
            orientation = '|'
        else:
            raise RuntimeError('to som necakal')
        movedict = {'w': (-1, 0), 'e': (+1, 0), 's': (0, +1), 'n': (0, -1)}
        pos_check_compute = movedict.get(direction)
        old_pos = pos_list[0]
        pos_check = (old_pos[0] + pos_check_compute[0], old_pos[1] + pos_check_compute[1], orientation)
        return pos_check

    def move(self, to_go, orientation):
        to_go = (to_go[0], to_go[1], orientation)
        pos_list_update = self.pos_list
        pos_list_update.insert(0, to_go)
        del pos_list_update[-1]
        self.pos_list = pos_list_update

    def devour(self, to_go, old_direction):
        self.eaten = True
        movedict = {'w': (-1, 0), 'e': (+1, 0), 's': (0, +1), 'n': (0, -1)}
        opposite_direction = self.determine_opposite_direction(old_direction)
        append_pos_compute = movedict.get(opposite_direction)
        last_pos = self.pos_list[-1]
        pos_to_append = (last_pos[0] + append_pos_compute[0], last_pos[1] + append_pos_compute[1], '')
        self.pos_list.append(pos_to_append)

        Game.generate = True
        self.yummy_level += 1

    @staticmethod
    def determine_opposite_direction(old_direction):
        return {
            'w': 'e',
            'e': 'w',
            'n': 's',
            's': 'n',
        }[old_direction]


class Game():
    def __init__(self, h, w):
        self.game_over = False
        self.generate_needed = True
        self.snekfood_position = []
        self.snek = Snek(h, w)
        self.board = self.board_f(h, w)
        self.key_watcher = realtime_getch.RealTimeyKey()

    def main(self, h, w):
        board = self.board
        self.startup_frame(h, w)
        self.game_cycle(h, w)

    def startup_frame(self, h, w):
        head = '<'
        self.snekfood_position = self.generate_snekfood(h, w, self.snek.pos_list)
        board = self.board
        board = self.draw_snekfood(board, self.snekfood_position)
        board = self.draw_snek(board, self.snek.pos_list, head)

        self.draw(board)

    def check_position(self, to_go, w, h, direction, old_direction, snekfood_position):
        snekfood_x = snekfood_position[0]
        snekfood_y = snekfood_position[1]
        snekfood_pos = (snekfood_x, snekfood_y)
        orientation = to_go[2]
        to_go = (to_go[0], to_go[1])
        pos_tuples_check = [(pos_tuple[0], pos_tuple[1]) for pos_tuple in self.snek.pos_list]

        if to_go == snekfood_pos:
            self.snek.devour(to_go, old_direction)
            self.snek.move(to_go, orientation)

        elif to_go in pos_tuples_check:
            # self.snek.move(to_go)
            self.game_over = True
            print('kusanie do seba')
        elif to_go[0] == 1 or to_go[0] == w + 2:
            # self.snek.move(to_go)
            self.game_over = True
            print('stena x')
        elif to_go[1] == 0 or to_go[1] == h - 1:
            # self.snek.move(to_go)
            self.game_over = True
            print('stena y')
        else:
            self.snek.move(to_go, orientation)

    def game_cycle(self, h, w):
        old_direction = 'w'
        round_count = 0
        snekfood_position = self.snekfood_position
        while not self.game_over:
            time.sleep(0.4)
            board = self.board_f(h, w)
            if self.generate_needed:
                snekfood_position = self.generate_snekfood(h, w, self.snek.pos_list)
            if self.snek.eaten:
                board = self.snekfood_eaten(board, snekfood_position)
                self.generate_needed = True

            direction = self.determine_direction(old_direction)
            to_go = self.snek.find_position_to_go(direction, self.snek.pos_list)
            self.check_position(to_go, w, h, direction, old_direction, snekfood_position)
            head = self.snek.determine_head(direction)
            if self.snek.eaten:  # test, potom zmazat
                board = self.draw_snek_2(board, self.snek.pos_list, head)
            else:
                board = self.draw_snek(board, self.snek.pos_list, head)
            if not self.snek.eaten:
                board = self.draw_snekfood(board, snekfood_position)

            self.draw(board)
            round_count += 1
            old_direction = direction
        self.key_watcher.t.join(timeout=1)
        self.game_over_screen(self.snek.yummy_level, round_count)



    def determine_direction(self, old_direction):
        pressed_key = self.key_watcher.char
        keys_to_directions = {'a': 'w', 'd': 'e', 's': 's', 'w': 'n'}
        impossible_direction = self.determine_impossible_direction(old_direction)
        if pressed_key not in keys_to_directions:
            direction = old_direction
        elif keys_to_directions.get(pressed_key) == impossible_direction:
            direction = old_direction
        else:
            direction = keys_to_directions.get(pressed_key)
        return direction

    def determine_impossible_direction(self, old_direction):
        return Snek.determine_opposite_direction(old_direction)

    def board_f(self, h, w):
        board_list = [(w + 2) * '#' if he in (0, h - 1) else '#' + w * ' ' + '#' for he in range(h)]
        return board_list

    def generate_snekfood(self, height, width, pos_list):
        pos_x_foodcheck = set()
        pos_y_foodcheck = set()
        for pos in pos_list:
            pos_x_foodcheck.add(pos[0])
            pos_y_foodcheck.add(pos[1])
        snekfood_x = pos_list[0][0]
        snekfood_y = pos_list[0][1]
        while snekfood_x in pos_x_foodcheck:
            snekfood_x = random.randint(2, width - 3)
        while snekfood_y in pos_y_foodcheck:
            snekfood_y = random.randint(2, height - 3)
        self.generate_needed = False
        return [snekfood_x, snekfood_y]

    def draw_snekfood(self, board, snekfood_position):
        updated_board = []
        line_count = 0
        snekfood_x = snekfood_position[0]
        snekfood_y = snekfood_position[1]
        for line in board:
            if line_count == snekfood_y:
                if snekfood_x == 1:
                    snekfood_x = 2
                updated_line = line[:snekfood_x - 1] + 'o' + line[snekfood_x:-1] + '#'
                updated_board.append(updated_line)
                line_count += 1
            else:
                updated_board.append(line)
                line_count += 1
        return updated_board

    def draw_snek(self, board, pos_list, head):
        first = True
        for pos in pos_list:
            pos_x = pos[0]
            pos_y = pos[1]
            orientation = pos[2]
            line_count = 0
            updated_board = []
            for line in board:
                if line_count == pos_y:
                    if first:
                        updated_line = line[:pos_x - 1] + head + line[pos_x:-1] + '#'
                        updated_board.append(updated_line)
                        first = False
                        line_count += 1
                    else:
                        updated_line = line[:pos_x - 1] + orientation + line[pos_x:-1] + '#'
                        updated_board.append(updated_line)
                        line_count += 1
                else:
                    line_count += 1
                    updated_board.append(line)
            board = updated_board
        return board

    def draw_snek_2(self, board, pos_list, head):
        first = True
        for pos in pos_list:
            pos_x = pos[0]
            pos_y = pos[1]
            orientation = pos[2]
            line_count = 0
            updated_board = []
            for line in board:
                if line_count == pos_y:
                    if first:
                        updated_line = line[:pos_x - 1] + head + line[pos_x:-1] + '#'
                        updated_board.append(updated_line)
                        first = False
                        line_count += 1
                    else:
                        updated_line = line[:pos_x - 1] + orientation + line[pos_x:-1] + '#'
                        updated_board.append(updated_line)
                        line_count += 1
                else:
                    line_count += 1
                    updated_board.append(line)
            board = updated_board
        return board

    def snekfood_eaten(self, board, snekfood_position):
        updated_line = board[snekfood_position[1]]
        updated_line = updated_line.replace('o', ' ')
        del board[snekfood_position[1]]
        board.insert(snekfood_position[1], updated_line)
        self.snek.eaten = False
        self.snekfood_position = None
        return board

    def draw(self, board_list_updated, ):
        print('Rules: \nWASD to move \nEat tasty snekfood (o) to increase yummy level\nyummy level:',
              self.snek.yummy_level, '\n', self.snek.pos_list)
        if self.snek.eaten:
            print('YUMMY!')
        print('\n'.join(board_list_updated))

    def game_over_screen(self, yummy_level, round_count):
        fl.fancy_letters('game over')
        print('\n\n\nyour yummy level is', yummy_level, 'and you survived', round_count,
              'rounds but the snek is ded...kek :(')
        print('press r to restart, or anything else to quit')
        x = input()
        print(x)
        if x == 'r':
            h, w = 15, 30
            Game(h, w).main(h, w)




def main():
    fl.fancy_letters('snek')
    time.sleep(0.5)
    fl.fancy_letters('the')
    time.sleep(0.5)
    fl.fancy_letters('venom')
    time.sleep(0.5)
    fl.fancy_letters('of')
    time.sleep(0.5)
    fl.fancy_letters('ultimate')
    time.sleep(0.5)
    fl.fancy_letters('destruction')
    time.sleep(0.5)
    h, w = 15, 30
    Game(h, w).main(h, w)


if __name__ == '__main__':
    main()
# todo ide do nekonecneho loopu pri novom vykresleni a asi zaroven zmene smeru
