from Logger import log_debug

class Events:
    def __init__(self):
        self.listeners = []

    def on(self, cmd, listener):
        self.listeners.append((cmd, listener))

    def call(self, origin, cmd, data):
        log_debug(f"({origin}->Master) cmd: {hex(cmd)} data: {hex(data)}")
        for listener in self.listeners:
            if listener[0] == cmd:
                listener[1](data)