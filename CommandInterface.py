import Constants


class CommandInterface:
    def __init__(self, events, queue, devices):
        self.commands = {}
        self.register("help", self.help)
        self.register("add_person", self.add_person)
        self.register("remove_person", self.remove_person)
        self.register("devices", self.list_devices)
        self.register("update_all", self.update_all)
        self.register("queue_info", self.queue_info)
        self.register("test", self.test_device)
        self.register("exit", self.exit_cmd)

        self.events = events
        self.queue = queue
        self.devices = devices

    def help(self):
        for command in self.commands:
            print(command)

    def add_person(self):
        self.events.call("CLI", Constants.CMD_QUEUE_ENTER, 0)

    def remove_person(self):
        self.events.call("CLI", Constants.CMD_QUEUE_LEAVE, 0)

    def list_devices(self):
        for device in self.devices:
            print(device.com_port)

    def update_all(self):
        for device in self.devices:
            device.send_command(Constants.CMD_UPDATE_INFO, 0)

    def queue_info(self):
        in_queue = self.queue.get_queue_length()
        capacity = self.queue.get_hourly_capacity()
        duration = self.queue.get_queue_duration_minutes()
        duration_aligned = int(self.queue.get_queue_duration_aligned_minutes())

        print(f"Queue: {in_queue} / {Constants.QUEUE_CAPACITY} - {duration} minuten ({duration_aligned} met alignment) - {capacity}/man per uur")

    def test_device(self, device_port):
        for device in self.devices:
            if device.com_port == device_port:
                device.send_command(Constants.CMD_RUN_TESTS, 0)
                return
        print("Device niet gevonden!")

    def exit_cmd(self):
        for device in self.devices:
            device.dispose()

        print("Bye!")
        exit()

    def main_loop(self):
        while True:
            user_input = input("$ ")
            parts = user_input.split(" ")
            command = parts[0]

            if len(parts) > 1:
                self.execute(command, parts[1])
            else:
                self.execute(command)

    def register(self, command, function):
        self.commands[command] = function

    def execute(self, command, *args):
        if command in self.commands:
            try:
                self.commands[command](*args)
                print("OK")
            except Exception as e:
                print("Missende argumenten!")

        else:
            print("Commando niet gevonden!")