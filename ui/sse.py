import multiprocessing

# Server sent events (SSE) for real-time updates

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = multiprocessing.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except multiprocessing.Full:
                del self.listeners[i]
