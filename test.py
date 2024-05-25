import itertools

import main

test_numbers = [2, 23, 67, 97]
number_p: list = list(itertools.permutations(test_numbers, 4))
signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 3))


def is_equal(a: float, b: float, precision: float = 1e-6) -> bool:
    return abs(a - b) < precision


def test_simplify():
    print("Testing simplify...")
    for str1 in main.styles:
        for str2 in number_p:
            for str3 in signal_p:
                instance: main.Expression = main.Expression(str1, list(str2), list(str3))
                modified: main.Expression = main.simplify(instance)
                    
                try:
                    if not is_equal(eval(instance.expression), eval(modified.expression)):
                        print("wrong instance in {} and {}".format(instance.expression, modified.expression))
                except ZeroDivisionError:
                    print("warning: zero division in {}".format(instance.expression))
                        
    print("Testing simplify is completed")
    
    
def test_format_signal():
    print("Testing format_signal ...")
    for str1 in main.styles:
            for str2 in number_p:
                for str3 in signal_p:
                    instance: main.Expression = main.Expression(str1, list(str2), list(str3))
                    modified: main.Expression = main.format_signal(instance)
                    
                    try:
                        if not is_equal(eval(instance.expression), eval(modified.expression)):
                            print("wrong instance in {} and {}".format(instance.expression, modified.expression))
                    except ZeroDivisionError:
                        print("warning: zero division in {}".format(instance.expression))
    print("Testing format_signal is completed")


def test_format_number():
    print("Testing format_number ...")
    for str1 in main.styles:
            for str2 in number_p:
                for str3 in signal_p:
                    instance: main.Expression = main.Expression(str1, list(str2), list(str3))
                    modified: main.Expression = main.format_number(main.format_signal(main.format_signal(instance)))
                    
                    try:
                        if not is_equal(eval(instance.expression), eval(modified.expression)):
                            print("wrong instance in {} and {}".format(instance.expression, modified.expression))
                    except ZeroDivisionError:
                        print("warning: zero division in {}".format(instance.expression))
    print("Testing format_number is completed")


if __name__ == '__main__':
    test_simplify()
    test_format_signal()
    test_format_number()