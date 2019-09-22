import os
import time
from threading import Thread
from . import logger


class ContinuousFileLogger(Thread):
    def __init__(self, filename, no_timer):
        self._filename = filename
        self._logger = logger.Logger(no_timer)
        self._stop_reading = False
        self._content = []
        Thread.__init__(self)

    def run(self):
        while not os.path.exists(self._filename):
            time.sleep(0.1)
        file = self.open_default_encoding(self._filename, mode='r')
        while True:
            where = file.tell()
            line = file.readline()
            if self._stop_reading and not line:
                break
            if not line:
                time.sleep(1)
                file.seek(where)
            else:
                if sys.stdout.closed:
                    return
                self._logger.log("UNITY", line)
                self._content.append(line)

    def stop(self):
        self._stop_reading = True
        # Wait for thread read the remaining log after process quit in 5 seconds
        self.join(5)

    def get_current_content(self):
        return self._content

    @staticmethod
    def open_default_encoding(file, mode):
        return open(file, mode=mode, encoding='utf-8-sig')
