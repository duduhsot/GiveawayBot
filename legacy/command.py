

from pyclbr import Function


class Command(object):

    def __init__(self, command: str, action: Function, description: str, pattern: str, example: str):
        self.command = command,
        self.action = action,
        self.description = description,
        self.pattern = pattern,
        self.example = example,
