import enum

TOKEN = "OTYxNTQ5MTE5OTc1OTk3NDYy.Yk6mZg.CdomTHWPthQYL9tjoiRXs4HKwV8"
COMMAND_PREFIX = "!"
COLOR = 0xFFBB33
SUCCESS_COLOR = 0x00C851
ERROR_COLOR = 0xFF4444


class ReminderType(enum.Enum):
    chat = 1
    user = 2
