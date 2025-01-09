import pyfirmata2

# config
PARK_NAME = "Lake Side Mania"
RIDE_NAME = "Log Flume"
QUEUE_CAPACITY = 100
SLAVE_PORTS = ["COM5"]

# commandos
CMD_RUN_TESTS = 0x01
CMD_UPDATE_INFO = 0x02
CMD_QUEUE_ENTER = 0x03
CMD_QUEUE_LEAVE = 0x04