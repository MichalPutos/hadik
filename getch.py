import msvcrt


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen. From http://code.activestate.com/recipes/134892/"""

    def __init__(self):
        self.impl = _GetchWindows()

    def __call__(self):
        return self.impl()


class _GetchWindows:
    def __init__(self):
        pass

    def __call__(self):
        return msvcrt.getch()


def getKey():
    inkey = _Getch()
    while True:
        k = inkey()
        if k != '':
            break

    return k.decode("utf-8")
