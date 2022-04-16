from dispatcher import Dispatcher


correct = ["add -o=B --opt1 -m arg3 arg4"]
correct += ["  add --opt2=33 -m --opt arg3 arg4 "]
correct += ["add -o"]
correct += ["add -o=B"]
correct += ["add -o=B --opt1"]
correct += ["add -o=B --opt1 -m"]
correct += ["add arg3"]
correct += ["add -m arg3 arg4"]
correct += ["add --opt-1 arg4"]
correct += ["add -m --opt1 arg3 arg4"]
correct += ["add --opt1 -m -o=B arg3 arg4"]

incorrect = ["cmd arg3 arg4 -o=B --opt1 -m arg5"]
incorrect += ["cmd --o=B --opt1 -m arg3 arg4 arg5"]
incorrect += ["cmd -o=B -opt1 -m arg3 arg4 arg5"]
incorrect += ["cmd -o=B --opt1 -m --arg=ab arg4 arg5"]
incorrect += ["cmd -o=B --opt1 --m arg4 arg5 arg6"]
incorrect += ["cmd -o=B arg --opt1 -m arg4"]
incorrect += ["cm3 -o=B --opt1 -m arg4 arg5"]
incorrect += ["Cmd arg5"]
incorrect += ["c-md -o=B --opt1 -m arg3 arg4 arg5"]
incorrect += ["cmd -o=B --opt:1 -m arg arg5"]


def test_correct():
    for cmd in correct:
        assert not dispatcher.dispatch(cmd), f"<{cmd}> isn't correct"

    for cmd in incorrect:
        assert dispatcher.dispatch(cmd), f"<{cmd}> isn't incorrect"


if __name__ == "__main__":
    dispatcher = Dispatcher("tests\commands")
    dispatcher.log_info()
