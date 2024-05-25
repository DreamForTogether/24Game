import itertools
import main

test_numbers = [2, 23, 67, 97]
number_p: list = list(itertools.permutations(test_numbers, 4))
signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 3))

def formate_number_0():
    arr: dict = dict()
    for i in signal_p:
        signals: list = list(i)

        self: main.Expression = main.Expression(main.styles[0], test_numbers, signals)
        modify: main.Expression = main.format_signal(main.format_signal(self))

        if modify.addSignal == 0 and modify.minSignal == 0: continue
        if modify.mulSignal == 0 and modify.divSignal == 0: continue

        if arr.__contains__(str(modify.signal)): continue

        arr[str(modify.signal)] = 1

        print(str(modify.signal), end = ' ')


def formate_number_3():
    arr: dict = dict()
    signal: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))

    for i in signal:
        signals: list = list(i)

        x = signals[0]; y = signals[1]

        if x == '+' and y == '+' or x == '*' and y == '*':
            continue
        
        if x == '-' and y == '-' or x == '/' and y == '/':
            continue
        
        if x == '*' and y != '/':
            continue

        if arr.__contains__(str([x, y])): continue
        else: arr[str([x, y])] = 1

        print (signals, end = ' ')

def formate_number_5():
    arr: dict = dict()
    signal: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))

    for i in signal:
        signals: list = list(i)

        y = signals[0]; z = signals[1]

        if y == '+' and z == '+' or y == '*' and z == '*': continue
        
        # a ? (b -/ c -/ d) => [c, d] sort
        if y == '-' and z == '-' or y == '/' and z == '/': continue
        
        # a ? (b * c +-/ d) ? d => [b, c] sort
        if y == '*' and z != '/': continue

        if arr.__contains__(str([y, z])): continue
        else: arr[str([y, z])] = 1

        print (signals, end = ' ')


if __name__ == '__main__':
    formate_number_0()
    formate_number_3()
    formate_number_5()