import time

import pyfirmata2

import Constants
import Logger
from Logger import log_error, log_info, log_debug
from DisplayDriver import LCD

class SlaveDevice:
    def __init__(self, port, events, queue):
        """
        Maakt een nieuw slave device aan.
        :param port: het COM port / linux path waarop het device is aangesloten, je mag AUTODETECT gebruiken
        """
        self.com_port = port
        self.events = events
        self.queue = queue
        self.connected = False

        try:
            self.connection = pyfirmata2.Arduino(self.com_port)
        except Exception as e:
            log_error(f"Connectie mislukt op poort {self.com_port}")
            return

        # sampling
        self.connection.samplingOn()

        # button up
        self.button_up = self.connection.get_pin("d:2:u")
        self.button_up.register_callback(self.button_up_cb)
        self.button_up.enable_reporting()

        # button down
        self.button_down = self.connection.get_pin("d:3:u")
        self.button_down.register_callback(self.button_down_cb)
        self.button_down.enable_reporting()

        # servo
        self.servo = self.connection.get_pin("d:9:s")

        # display
        self.display = LCD(self.connection)
        self.display.clear()
        self.display.set_cursor(0, 0)
        self.display.print("Opstarten...")

        # klaar met init
        self.connected = True
        log_info(f"Verbonden aan device op poort {self.com_port}")

    def button_up_cb(self, state):
        if state == True:
            return

        self.events.call(self.com_port, Constants.CMD_QUEUE_ENTER, 0)

    def button_down_cb(self, state):
        if state == True:
            return

        self.events.call(self.com_port, Constants.CMD_QUEUE_LEAVE, 0)

    def send_command(self, command: int, data):
        """
        Voer een commando uit op het device.
        :param command: het commando dat uitgevoerd moet worden
        :param data: de data die meegestuurd moet worden
        """
        log_debug(f"(Master->{self.com_port}) cmd: {hex(command)} data: {hex(data)}")

        if not self.connected:
            log_error("Kan geen commando sturen naar een niet verbonden device")
            return

        match command:
            case 0x01:
                self.servo_test()
            case 0x02:
                self.set_waiting_time(self.queue)
            case _:
                log_error(f"Commando {command} is niet bekend")

    def servo_test(self):
        """
        Voer een servo test uit.
        """
        # display
        self.display.set_cursor(0, 1)
        self.display.print("Test Uitvoeren!")

        # servo
        self.servo.write(180)
        time.sleep(2)
        self.servo.write(0)
        time.sleep(2)
        self.servo.write(180)

        # display
        self.display.set_cursor(0, 1)
        self.display.print(f"{'Test OK!':<16}")

        # delay
        time.sleep(2)

    def set_waiting_time(self, queue):
        """
        Zet de wachttijd in op de servo.
        :param max: de maximale wachttijd
        :param curr: de huidige wachttijd
        """
        if not self.connected:
            log_error("Kan geen commando sturen naar een niet verbonden device")
            return

        curr = queue.get_queue_duration_minutes()
        max = 180

        # servo
        if (curr == 0):
            angle = 180
        else:
            angle = 180 - (180 * curr / max) # 180deg is de startpositie

        self.servo.write( int(angle) ) # cast naar int anders word servo zeer zenuwachtig

        # display
        self.update_display(queue)

    def update_display(self, queue):
        """
        Update de display met de huidige wachttijd.
        :param time: de huidige wachttijd
        """
        if not self.connected:
            log_error("Kan geen commando sturen naar een niet verbonden device")
            return

        time = queue.get_queue_duration_aligned_minutes()
        people = queue.get_queue_length()

        # display
        self.display.clear()
        self.display.set_cursor(0, 0)
        self.display.print(Constants.RIDE_NAME)
        self.display.set_cursor(0, 1)
        self.display.print(f"{int(time)} minuten")

    def dispose(self):
        """
        Sluit de connectie met het device.
        """
        if self.connected:
            self.connection.exit()
            self.connected = False
            log_info(f"Connectie met device op poort {self.com_port} gesloten")
        else:
            log_error("Kan geen connectie sluiten met een niet verbonden device")
