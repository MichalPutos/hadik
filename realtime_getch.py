import time
import msvcrt
import threading


class RealTimeyKey:

    def __init__(self):
        self.char = ''
        self.t = threading.Thread(target=self.press_key)
        self.t.start()

    def press_key(self):
        while True:
            self.char = msvcrt.getch().decode("utf-8")

#
# key_watcher = RealTimeyKey()
#
# while True:
#     time.sleep(0.1)
#     print(key_watcher.char)
