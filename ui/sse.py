import multiprocessing
import logging
import traceback

# Server sent events (SSE) for real-time updates

class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self):
        q = multiprocessing.Queue()
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except Exception as e:
                logging.error(traceback.format_exc())
                del self.listeners[i]
