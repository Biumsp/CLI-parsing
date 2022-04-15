from dispatcher import Dispatcher

dispatcher = Dispatcher("tests/commands")

for cmd in dispatcher.commands:
    print(cmd)
