import time

import pyfirmata2
import Constants
import Logger
from CommandInterface import CommandInterface
from Events import Events
from Queue import Queue
from SlaveDevice import SlaveDevice
from Logger import log_info, log_warning, log_debug

devices = []
queue = Queue()
events = Events()

for port in Constants.SLAVE_PORTS:
    device = SlaveDevice(port, events, queue)

    # voeg alleen verbonden devices toe aan de lijst
    if device.connected:
        devices.append(device)

log_info(f"Verbonden met {len(devices)} device(s)")

# voer tests uit
log_warning("Self-test is actief!")
for device in devices:
    log_debug(f"Voer test uit op device op poort {device.com_port}")
    device.send_command(Constants.CMD_RUN_TESTS, 0)

log_info("Self-test is voltooid!")

# functies
def update_all():
    in_queue = queue.get_queue_length()
    capacity = queue.get_hourly_capacity()
    duration = queue.get_queue_duration_minutes()
    duration_aligned = int(queue.get_queue_duration_aligned_minutes())

    log_debug(f"Queue: {in_queue} / {Constants.QUEUE_CAPACITY} - {duration} minuten ({duration_aligned} met alignment) - {capacity}/man per uur")
    for device in devices:
        device.send_command(Constants.CMD_UPDATE_INFO, 0)

# events impl
def cmd_add_person(data):
    queue.add_person()
    update_all()

def cmd_remove_person(data):
    queue.remove_person()
    update_all()

# events reg
events.on(Constants.CMD_QUEUE_ENTER, cmd_add_person)
events.on(Constants.CMD_QUEUE_LEAVE, cmd_remove_person)

# eerste update
update_all()

# main loop
command_interface = CommandInterface(events, queue, devices)
command_interface.main_loop()