import itertools


styles: list = [
    "{a} {x} {b} {y} {c} {z} {d}",          # index: 0
    "({a} {x} {b}) {y} {c} {z} {d}",        # index: 1
    "{a} {x} {b} {y} ({c} {z} {d})",        # index: 2
    "({a} {x} {b} {y} {c}) {z} {d}",        # index: 3
    "{a} {x} ({b} {y} {c} {z} {d})",        # index: 4
    "{a} {x} ({b} {y} {c}) {z} {d}",        # index: 5
    "({a} {x} {b}) {y} ({c} {z} {d})",      # index: 6
    "(({a} {x} {b}) {y} {c}) {z} {d}",      # index: 7
    "({a} {x} ({b} {y} {c})) {z} {d}",      # index: 8
    "{a} {x} (({b} {y} {c}) {z} {d})",      # index: 9
    "{a} {x} ({b} {y} ({c} {z} {d}))"]      # index: 10


signal_priority = {
    '*': 3,
    '/': 2,
    '+': 1,
    '-': 0
}


class Expression:
    def __init__(self, style: str, numbers: list, signal: list) -> None:
        self.style = style; self.numbers = numbers.copy(); self.signal = signal.copy()
        self.expression = style.format(a = self.numbers[0], b = self.numbers[1], c = self.numbers[2], d = self.numbers[3],
                                       x = self.signal[0], y = self.signal[1], z = self.signal[2])
        
        self.addSignal = self.expression.count("+"); self.minSignal = self.expression.count("-")
        self.mulSignal = self.expression.count("*"); self.divSignal = self.expression.count("/")


def is_equal(a: float, b: float, precision: float = 1e-6) -> bool:
    return abs(a - b) < precision


# input 4 numbers:
def input_numbers() -> list:
    raw: list = input("Please input 4 numbers: ").split(" ")
    length: int = len(raw)
    if length == 4: return [int(raw[0]), int(raw[1]), int(raw[2]), int(raw[3])]
    else: print(("The length is: {} not 4: ").format(str(length))); return input_numbers()


# Remove the brackets
def simplify(self: Expression) -> Expression:
    x: chr = self.signal[0]; y: chr = self.signal[1]; z: chr = self.signal[2]
    
    # "{a} {x} {b} {y} {c} {z} {d}",          # index: 0
    if self.style == styles[0]:
        return self
        
    # "({a} {x} {b}) {y} {c} {z} {d}",        # index: 1
    # (when y is '+' or y is '-') or (when x is '*' or x is '/')
    if self.style == styles[1]:
        if y == '+' or y == '-' or x == '*' or x == '/':
            return Expression(styles[0], self.numbers, self.signal)
        
    # "{a} {x} {b} {y} ({c} {z} {d})",        # index: 2
    # (when y is '+') or [when y is '-' and (when z is '*' or '/')] or [when y is '*' and (when z is '*' or '/')]
    if self.style == styles[2]:
        if y == '+' or (y == '-' and (z == '*' or z == '/')) or (y == '*' and (z == '*' or z == '/')):
            return Expression(styles[0], self.numbers, self.signal)
            
    # "({a} {x} {b} {y} {c}) {z} {d}",        # index: 3
    # (when z is '+' or '-') or [(x is '*' or '/') and (y is '*' or '/')]
    if self.style == styles[3]:
        if (x == '*' or x == '/') and (y == '*' or y == '/') or z == '+' or z == '-':
            return Expression(styles[0], self.numbers, self.signal)
        
    # "{a} {x} ({b} {y} {c} {z} {d})",        # index: 4
    # (when x is '+') or [(x is '-' or x is '*') and (y is '*' or y is '/') and (z is '*' or z is '/')]
    if self.style == styles[4]:
        if x == '+' or (x == '-' or x == '*') and (y == '*' or y == '/') and (z == '*' or z == '/'):
            return Expression(styles[0], self.numbers, self.signal)
        
    # "{a} {x} ({b} {y} {c}) {z} {d}",        # index: 5
    # [(when y is '*' or y is '/') and x is not '/'] or [(when y is '+' or y is '-') and x is '+' and (z is '+' or '-')]
    if self.style == styles[5]:
        if (y == '*' or y == '/') and x != '/' or (y == '+' or y == '-') and x == '+' and (z == '+' or z == '-'):
            return Expression(styles[0], self.numbers, self.signal)
    
    # "({a} {x} {b}) {y} ({c} {z} {d})",      # index: 6
    # (when x is '*' or x is '/') or [(when x is '+' or x is '-') and (when y is '+' or y is '-')] => styles[2]
    # [when y is '*' and (z is '*' or z is '/')] or [when y is '+' and (z is '+' or z is '-')] => styles[1]
    if self.style == styles[6]:
        if x == '*' or x == '/' or (x == '+' or x == '-') and (y == '+' or y == '-'):
            return simplify(Expression(styles[2], self.numbers, self.signal))
        if y == '*' and (z == '*' or z == '/') or y == '+' and (z == '+' or z == '-'):
            return simplify(Expression(styles[1], self.numbers, self.signal))
        
    # "(({a} {x} {b}) {y} {c}) {z} {d}",      # index: 7
    # (when x is '*' or x is '/') or [(when x is '+' or x is '-') and (y is '+' or y is '-')] => styles[3]
    # (when z is '+' or z is '-') or [(when z is '*' or z is '/') and (y is '*' or y is '/)] => styles[1]
    if self.style == styles[7]:
        if x == '*' or x == '/' or (x == '+' or x == '-') and (y == '+' or y == '-'):
            return simplify(Expression(styles[3], self.numbers, self.signal))
        if z == '+' or z == '-' or (z == '*' or z == '/') and (y == '*' or y == '/'):
            return simplify(Expression(styles[1], self.numbers, self.signal))
        
    # "({a} {x} ({b} {y} {c})) {z} {d}",      # index: 8
    # [when x is not '/' and (y is '*' or y is '/')] or [(when y is '+' or y is '-') and x is '+'] => styles[3]
    # (when z is '+' or z is '-') or [(when z is '*' or z is '/') and (x is '*' or x is '/)] => styles[5]
    if self.style == styles[8]:
        if (y == '+' or y == '-') and x == '+' or (y == '*' or y == '/') and x != '/':
            return simplify(Expression(styles[3], self.numbers, self.signal))
        if z == '+' or z == '-' or (z == '*' or z == '/') and (x == '*' or x == '/'):
            return simplify(Expression(styles[5], self.numbers, self.signal))
    
    # "{a} {x} (({b} {y} {c}) {z} {d})",      # index: 9
    # (when y is '*' or y is '/') or [(when y is '+' or y is '-') and (z is '+' or z is '-')] => styles[4]
    # [(when z is '*' or z is '/') and x is not '/'] or [(when z is '+' or z is '-') and x is '+'] => styles[5]
    if self.style == styles[9]:
        if y == '*' or y == '/' or (y == '+' or y == '-') and (z == '+' or z == '-'):
            return simplify(Expression(styles[4], self.numbers, self.signal))
        if (z == '*' or z == '/') and x != '/' or (z == '+' or z == '-') and x == '+':
            return simplify(Expression(styles[5], self.numbers, self.signal))
        
    # "{a} {x} ({b} {y} ({c} {z} {d}))"]      # index: 10
    # [when y is not '/' and (z is '*' or z is '/')] or [(when z is '+' or z is '-') and y is '+'] => styles[4]
    # [(when y is '*' or y is '/') and x is not '/')] or [(when y is '+' or y is '-') and x is '+'] => styles[2]
    if self.style == styles[10]:
        if y != '/' and (z == '*' or z == '/') or (z == '+' or z == '-') and y == '+':
            return simplify(Expression(styles[4], self.numbers, self.signal))
        if (y == '*' or y == '/') and x != '/' or (y == '+' or y == '-') and x == '+':
            return simplify(Expression(styles[2], self.numbers, self.signal))
        
    return self


def format_signal(self: Expression) -> Expression:
    a: int = self.numbers[0]; b: int = self.numbers[1]; c: int = self.numbers[2]; d: int = self.numbers[3] 
    x: chr = self.signal[0]; y: chr = self.signal[1]; z: chr = self.signal[2]
    
    # define cannot styles sign:
    # "{a} {x} {b} {y} {c} {z} {d}"
    if self.style == styles[0]:
        if (signal_priority[x] >= signal_priority[y] >= signal_priority[z]) or (
           (x == '*' or x == '/') and (y == '+' or y == '-') and (z == '*' or z == '/')):
            return self

        # only contain + and -
        if self.mulSignal == 0 and self.divSignal == 0:
            min_numbers: list = []
            if x == '-': min_numbers.append(self.numbers[1])
            if y == '-': min_numbers.append(self.numbers[2])
            if z == '-': min_numbers.append(self.numbers[3])
            
            self.numbers.remove(min_numbers[0])
            
            try: self.numbers.remove(min_numbers[1])
            except: pass
            
            self.numbers = self.numbers + min_numbers
            
            new_signal: list = ['+', '+', '-']
            
            if len(min_numbers) == 2:
                new_signal[1] = '-'
            
            return Expression(styles[0], self.numbers, new_signal)
        
        # only contain * and /
        if self.addSignal == 0 and self.minSignal == 0:
            div_numbers: list = []
            if x == '/': div_numbers.append(self.numbers[1])
            if y == '/': div_numbers.append(self.numbers[2])
            if z == '/': div_numbers.append(self.numbers[3])
            
            self.numbers.remove(div_numbers[0])
            
            try: self.numbers.remove(div_numbers[1])
            except: pass
            
            self.numbers = self.numbers + div_numbers
            
            new_signal: list = ['*', '*', '/']
            
            if len(div_numbers) == 2:
                new_signal[1] = '/'
            
            return Expression(styles[0], self.numbers, new_signal)
        
        # the remain combination are:
        # (1) ['*', '-', '+']
        # (2) ['/', '*', '+'] ['/', '*', '-'] ['/', '-', '+']
        # (3) ['+', '*', '*'] ['+', '*', '/']
        #     ['+', '/', '*']
        #     ['+', '/', '/'] 
        #     ['+', '*', '+'] ['+', '*', '-'] ['+', '/', '+'] ['+', '/', '-']
        #     ['+', '+', '*'] ['+', '+', '/']
        #     ['+', '-', '*'] ['+', '-', '/']
        # (4) ['-', '*', '*'] ['-', '*', '/'] ['-', '/', '/']
        #     ['-', '/', '*'] 
        #     ['-', '*', '+'] ['-', '*', '-'] ['-', '/', '+'] ['-', '/', '-']
        #     ['-', '+', '*'] ['-', '+', '/']
        #     ['-', '-', '*'] ['-', '-', '/']
        
        # (1) ['*', '-', '+']
        # a * b - c + d == a * b + d - c
        if self.signal == ['*', '-', '+']: return Expression(styles[0], [a, b, d, c], ['*', '+', '-'])
        
        # (2) ['/', '*', '+'] ['/', '*', '-']
        # a / b * c +- d == a * c / b +- d
        if x == '/' and y == '*': return Expression(styles[0], [a, c, b, d], ['*', '/', z])
        
        # (2) ['/', '-', '+']
        # a / b - c + d == a / b + d - c
        if self.signal == ['/', '-', '+']: return Expression(styles[0], [a, b, d, c], ['/', '+', '-'])
        
        # (3) ['+', '*', '*'] ['+', '*', '/']
        # a + b * c */ d == format_signal(b * c */ d + a)
        if x == '+' and y == '*' and (z == '*' or z == '/'): return format_signal(Expression(styles[0], [b, c, d, a], [y, z, '+']))
        
        # (3) ['+', '/', '*']
        # a + b / c * d == b * d / c + a
        if self.signal == ['+', '/', '*']: return Expression(styles[0], [b, d, c, a], ['*', '/', '+'])

        # (3) ['+', '/', '/']
        # a + b / c / d = b / c / d + a
        if self.signal == ['+', '/', '/']: return Expression(styles[0], [b, c ,d, a], ['/', '/', '+'])

        # (3) ['+', '*', '+'] ['+', '*', '-'] ['+', '/', '+'] ['+', '/', '-']
        # a + b */ c +- d == format_signal(b */ c +- d + a)
        if x == '+' and (y == '*' or y == '/') and (z == '+' or z == '-'): return format_signal(Expression(styles[0], [b, c, d, a], [y, z, '+']))
        
        # (3) ['+', '+', '*'] ['+', '+', '/']
        # a + b + c */ d == c */ d + a + b
        if x == '+' and y == '+' and (z == '*' or z == '/'): return Expression(styles[0], [c, d, a, b], [z, '+', '+'])
        
        # (3) ['+', '-', '*'] ['+', '-', '/']
        # a + b - c */ d == b - c */ d + a
        if x == '+' and y == '-' and (z == '*' or z == '/'): return Expression(styles[0], [b, c, d, a], ['-', z, '+'])
        
        # (4) ['-', '*', '*'] ['-', '*', '/'] ['-', '/', '/']
        if self.signal == ['-', '*', '*'] or self.signal == ['-', '*', '/'] or self.signal == ['-', '/', '/']: return self
        
        # (4) ['-', '/', '*']
        # a - b / c * d = a - b * d / c
        if self.signal == ['-', '/', '*']: return Expression(styles[0], [a, b, d, c], ['-', '*', '/'])
        
        # (4) ['-', '*', '+'] ['-', '*', '-'] ['-', '/', '+'] ['-', '/', '-']
        if x == '-' and (y == '*' or y == '/') and (z == '+' or z == '-'): return self
        
        # (4) ['-', '+', '*'] ['-', '+', '/']
        # a - b + c */ d = c */ d + a - b
        if x == '-' and y == '+' and (z == '*' or z == '/'): return Expression(styles[0], [c, d, a, b], [z, '+', '-'])
        
        # (4) ['-', '-', '*'] ['-', '-', '/']
        # a - b - c */ d = a - c */ d - b
        if x == '-' and y == '-' and (z == '*' and z == '/'): return format_signal(Expression(styles[0], [a, c, d, b], ['-', z, '-']))

        return self
    
    # "({a} {x} {b}) {y} {c} {z} {d}"
    if self.style == styles[1]:
        # (a ? b) * c +- d
        if signal_priority[y] >= signal_priority[z] or (y == '*' or y == '/') and (z == '+' or z == '-'): return self
        
        # remain
        # (1) ['+', '*'] ['+', '/'] ['-', '*'] ['-', '/'] ['-', '+']
        # (2) ['/', '*']
        
        # (1) ['+', '*'] ['+', '/'] ['-', '*'] ['-', '/'] ['-', '+']
        if (y == '+' or y == '-') and (z == '*' or z == '/'): return self
        
        # (2) ['/', '*']
        # (a ? b) / c * d = d * (a ? b) / c
        if y == '/' and z == '*': return Expression(styles[5], [d, a, b, c], ['*', x, '/'])
        
        return self
    
    # "{a} {x} {b} {y} ({c} {z} {d})"
    if self.style == styles[2]:
        # a * b * ? == format_signal(? * a * b)
        if x == '*' and y == '*' or x == '+' and y == '+': return format_signal(Expression(styles[1], [c, d, a, b], [z, x, y]))

        # a /- b /- ? == format_signal(a /- ? /- b)
        if x == '-' and y == '-' or x == '/' and y == '/': return format_signal(Expression(styles[5], [a, c, d, b], [x, z, y]))

        # remain
        # (1) ['*', '/']
        #     ['*', '+'] ['*', '-']
        # (2) ['/', '*']
        #     ['/', '+'] ['/', '-']
        # (3) ['+', '*'] ['+', '/']
        #     ['+', '-']
        # (4) ['-', '*'] ['-', '/']
        #     ['-', '+']

        # (1) ['*', '/']
        # a * b / ? == b / ? * a
        if x == '*' and y == '/': return format_signal(Expression(styles[5], [b, c, d, a], ['/', z, '*']))

        # (1) ['*', '+'] ['*', '-']
        if x == '*' and (y == '+' or y == '-'): return self

        # (2) ['/', '*']
        # a / b * ? == ? * a / b
        if x == '/' and y == '*': return format_signal(Expression(styles[1], [c, d, a, b], [z, '*', '/']))

        # (2) ['/', '+'] ['/', '-']
        if x == '/' and (y == '+' or y == '-'): return self

        # (3) ['+', '*'] ['+', '-']
        # a + b *- ? == format_signal(b *- ? + a)
        if x == '+' and (y == '*' or y == '/'): return format_signal(Expression(styles[5], [b, c, d, a], [y, z, '+']))

        # (3) ['+', '-']
        # a + b - ? == (b - ? + a)
        if x == '+' and y == '-': return format_signal(Expression(styles[5], [b, c, d, a], ['-', z, '+']))

        # (4) ['-', '*'] ['-', '/']
        if x == '-' and (y == '*' or y == '/'): return self

        # (4) ['-', '+']
        # a - b + ? == format_signal(a + ? - b)
        if x == '-' and y == '+': return format_signal(Expression(styles[5], [a, c, d, b], ['+', z, '-']))

        return self

    # "({a} {x} {b} {y} {c}) {z} {d}",        # index: 3
    if self.style == styles[3]:
        if signal_priority[x] >= signal_priority[y]: return self

        # remain
        # (1) ['+', '*'] ['+', '/']
        # (2) ['-', '*'] ['-', '/']
        #     ['-', '+']
        # (3) ['/', '*'] 

        # (1) ['+', '*'] ['+', '/']
        # a + b * c == b * c + a
        if x == '+' and (y == '*' or y == '/'): return Expression(styles[3], [b, c, a, d], [y, '+', z])

        # (2) ['-', '*'] ['-', '/']
        if x == '-' and (y == '*' or y == '/'): return self

        # (2) ['-', '+']
        # a - b + c == a + c - b
        if x == '-' and y == '+': return Expression(styles[3], [a, c, b, d], ['+', '-', z])

        # (3) ['/', '*']
        # a / b * c == a * c / b
        if x == '/' and y == '*': return Expression(styles[3], [a, c, b, d], ['*', '/', z])

        return self

    # "{a} {x} ({b} {y} {c} {z} {d})",        # index: 4
    if self.style == styles[4]:
        if x == '+' or x == '*': return format_signal(Expression(styles[3], [b, c, d, a], [y, z, x]))

        if signal_priority[y] >= signal_priority[z]: return self

        # remain
        # (1) ['+', '*'] ['+', '/']
        # (2) ['-', '*'] ['-', '/']
        #     ['-', '+'] ['/', '*']

        # (1) ['+', '*'] ['+', '/']
        # a ? (b + c */ d) == a ? (c */ d + b)
        if y == '+' and (z == '*' or z == '/'): return Expression(styles[4], [a, c, d, b], [x, z, '+'])

        # (2) ['-', '*'] ['-', '+']
        if y == '-' and (z == '*' or z == '/'): return self

        # (2) ['-', '+'] ['/', '*']
        # a ? (b /- c *+ d) == a ? (b *+ d -/ c)
        if y == '-' and z == '+' or y == '/' and z == '*': return Expression(styles[4], [a, b, d, c], [x, z, y])



        return self
    
    # "{a} {x} ({b} {y} {c}) {z} {d}",        # index: 5
    if self.style == styles[5]:
        if x == '*': return format_signal(Expression(styles[1], [b, c, a, d], [y, x, z]))

        # a + ? +- d == ? + a +- d
        if x == '+' and (z == '+' or z == '-'): return format_signal(Expression(styles[1], [b, c, a, d], [y, '+', z]))

        # remain
        # (1) ['/', '*'] ['/', '/'] ['/', '+'] ['/', '-']
        # (2) ['+', '*'] ['+', '/']
        # (3) ['-', '*'] ['-', '/'] ['-', '+'] ['-', '-']

        # (1) ['/', '*'] ['/', '/'] ['/', '+'] ['/', '-']
        if x == '/': return self

        # (2) ['+', '*'] ['+', '/']
        # a + ? */ d == format_signal(? */ d + a)
        if x == '+' and (z == '*' or z == '/'): return format_signal(Expression(styles[1], [b, c, d, a], [y, z, x]))

        # (3) ['-', '*'] ['-', '/'] ['-', '+'] ['-', '-']
        if x == '-': return self

        return self
    
    # "({a} {x} {b}) {y} ({c} {z} {d})",      # index: 6
    if self.style == styles[6]: return self

    # "(({a} {x} {b}) {y} {c}) {z} {d}",      # index: 7
    if self.style == styles[7]: return self

    # "({a} {x} ({b} {y} {c})) {z} {d}",      # index: 8
    if self.style == styles[8]:
        if x == '+' or x == '*': return format_signal(Expression(styles[7], [b, c, a, d], [y, x, z]))
        return self

    # "{a} {x} (({b} {y} {c}) {z} {d})",      # index: 9
    if self.style == styles[9]:
        if x == '+' or x == '*': return format_signal(Expression(styles[7], [b, c, d, a], [y, z, x]))
        return self

    # "{a} {x} ({b} {y} ({c} {z} {d}))"       # index: 10
    if self.style == styles[10]:
        if x == '+' or x == '*': return format_signal(Expression(styles[8], [b, c, d, a], [y, z, x]))
        return self

    return self


def format_number(self: Expression) -> Expression:
    a: int = self.numbers[0]; b: int = self.numbers[1]; c: int = self.numbers[2]; d: int = self.numbers[3] 
    x: chr = self.signal[0]; y: chr = self.signal[1]; z: chr = self.signal[2]

    # "{a} {x} {b} {y} {c} {z} {d}",          # index: 0
    if self.style == styles[0]:
        # only contain * and /
        if self.addSignal == 0 and self.minSignal == 0:
            # find the numbers.py divided
            nums: list = []
            if x == '/': nums.append(b)
            if y == '/': nums.append(c)
            if z == '/': nums.append(d)

            nums.sort()
            try: self.numbers.remove(nums[0]); self.numbers.remove(nums[1]); self.numbers.remove(nums[2])
            except: pass

            self.numbers.sort()
            new: list = self.numbers + nums
            return Expression(styles[0], new, self.signal)

        # only contain + and -
        if self.mulSignal == 0 and self.divSignal == 0:
            # find the numbers.py divided
            nums: list = []
            if x == '-': nums.append(b)
            if y == '-': nums.append(c)
            if z == '-': nums.append(d)

            nums.sort()
            try: self.numbers.remove(nums[0]); self.numbers.remove(nums[1]); self.numbers.remove(nums[2])
            except: pass

            self.numbers.sort()
            new: list = self.numbers + nums
            return Expression(styles[0], new, self.signal)

        # remain:
        # (1) ['*', '*', '+'] ['*', '*', '-']
        # (2) ['/', '/', '+'] ['/', '/', '-']
        # (3) ['*', '/', '+'] ['*', '/', '-']
        # (4) ['*', '+', '*']
        # (5) ['*', '+', '/']
        # (6) ['*', '+', '+'] ['*', '-', '-']
        # (7) ['*', '+', '-']
        # (8) ['*', '-', '*'] ['*', '-', '/']
        # (9) ['/', '+', '*'] ['/', '+', '/']
        # (10) ['/', '+', '+']
        # (11) ['/', '+', '-'] ['/', '-', '/']
        # (12) ['/', '-', '*'] ['/', '-', '-']
        # (13) ['-', '*', '+'] ['-', '*', '-']
        # (14) ['-', '*', '*']
        # (15) ['-', '/', '+'] ['-', '/', '-']
        # (16) ['-', '*', '/']
        # (17) ['-', '/', '/'] ['-', '-', '*']
        # (18) ['-', '-', '/']

        # (1) ['*', '*', '+'] ['*', '*', '-']
        # a * b * c +- d => [a, b, c] => sort
        if x == '*' and y == '*':
            new: list = [a, b, c]; new.sort(); new.append(d)
            return Expression(styles[0], new, self.signal) 
        
        # (2) ['/', '/', '+'] ['/', '/', '-']
        # a / b / c +- d => [b, c] => sort
        if x == '/' and y == '/':
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[0], new, self.signal)
        
        # (3) ['*', '/', '+'] ['*', '/', '-']
        # a * b / d +- d => [a, b] => sort
        if x == '*' and y == '/':
            new: list = [a, b]; new.sort(); new = new + [c, d]
            return Expression(styles[0], new, self.signal)

        # (4) ['*', '+', '*']
        if self.signal == ['*', '+', '*']:
            new: list = []
            if a * b < c * d: new = [a, b, c, d]
            else: new = [c, d, a, b]
            if new[0] > new[1]: new[0], new[1] = new[1], new[0]
            if new[2] > new[3]: new[2], new[3] = new[3], new[2]
            return Expression(styles[0], new, self.signal)
        
        # (5) ['*', '+', '/']
        if self.signal == ['*', '+', '/']:
            new: list = []
            if a * b < c / d: new = [a, b, c, d]
            else: new = [c, d, a, b]; self.signal = ['/', '+', '*']
            if z == '*' and new[0] > new[1]: new[0], new[1] = new[1], new[0]
            if x == '*' and new[2] > new[3]: new[2], new[3] = new[3], new[2]
            return Expression(styles[0], new, self.signal)

        # (6) ['*', '+', '+'] ['*', '-', '-']
        # a * b +- c +- d => [a, b] and [c, d] => sort
        if self.signal == ['*', '+', '+'] or self.signal == ['*', '-', '-']:
            new: list = [a, b]; new.sort(); temp = [c, d]; temp.sort(); new = new + temp
            return Expression(styles[0], new, self.signal)
        
        # (7) ['*', '+', '-']
        # a * b + c - d => [a, b] sort
        if self.signal == ['*', '+', '-']:
            new: list = [a, b]; new.sort(); new = new + [c, d]
            return Expression(styles[0], new, self.signal)

        # (8) ['*', '-', '*'] ['*', '-', '/']
        if x == '*' and y == '-' and (z == '*' or z == '/'):
            new: list = [a, b]; new.sort()
            if z == '/': new = new + [c, d]
            else: temp = [c, d]; temp.sort(); new = new + temp
            return Expression(styles[0], new, self.signal)
        
        # (9) ['/', '+', '*'] ['/', '+', '/']
        if x == '/' and y == '+' and (z == '*' or z == '/'):
            new: list = []
            if a / b < eval(str(c) + z + str(d)): new = [a, b, c, d]
            else: new = [c, d, a, b]
            if x == '*' and new[0] > new[1]: new[0], new[1] = new[1], new[0]
            if z == '*' and new[2] > new[3]: new[2], new[3] = new[3], new[2]
            return Expression(styles[0], new, self.signal)

        # (10) ['/', '+', '+']
        # a / b + c + d => [c, d] => sort
        if self.signal == ['/', '+', '+']:
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[0], new, self.signal)
        
        # (11) ['/', '+', '-'] ['/', '-', '/']
        if self.signal == ['/', '+', '-'] or self.signal == ['/', '-', '/']: return self

        # (12) ['/', '-', '*'] ['/', '-', '-']
        # a / b - c *- d => [c, d] => sort
        if x == '/' and y == '-' and (z == '*' or z == '-'):
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[0], new, self.signal)
        
        # (13) ['-', '*', '+'] ['-', '*', '-']
        # a - b * c +- d => [b, c] sort
        if x == '-' and y == '*' and (z == '+' or z == '-'):
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[0], new, self.signal)

        # (14) ['-', '*', '*']
        # a - b * c * d => [b, c, d] sort
        if self.signal == ['-', '*', '*']:
            new: list = [b, c, d]; new.sort(); new = [a] + new
            return Expression(styles[0], new, self.signal)
        
        # (15) ['-', '/', '+'] ['-', '/', '-']
        if x == '-' and y == '/' and (z == '+' or z == '-'): return self
        
        # (16) ['-', '*', '/']
        # a - b * c / d => [b, c] sort
        if self.signal == ['-', '*', '/']:
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[0], new, self.signal)
        
        # (17) ['-', '/', '/'] ['-', '-', '*']
        # a - b /- c /* d => [c, d] => sort
        if self.signal == ['-', '/', '/'] or self.signal == ['-', '-', '*']:
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[0], new, self.signal)
        
        # (18) ['-', '-', '/']
        if self.signal == ['-', '-', '/']: return self

    # "({a} {x} {b}) {y} {c} {z} {d}",        # index: 1
    if self.style == styles[1]:
        if x == '+' or x == '*':
            new: list = [a, b]; new.sort()

            if y == z: temp = [c, d]; temp.sort(); new = new + temp
            else: new = new + [c, d]

            return Expression(styles[1], new, self.signal)
        
        if y == z:
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[1], new, self.signal)

        return self

    # "{a} {x} {b} {y} ({c} {z} {d})",        # index: 2
    if self.style == styles[2]:
        if z == '+' or z == '*':
            new: list = [c, d]; new.sort()

            if x == '*' and y == '*' or x == '+' and (y == '+' or y == '-'):
                temp = [a, b]; temp.sort()
                new = temp + new
            else: new = [a, b] + new

            return Expression(styles[2], new, self.signal)

        new: list = [c, d]

        if x == '*' and y == '*' or x == '+' and (y == '+' or y == '-'):
            temp = [a, b]; temp.sort()
            new = temp + new
        else: new = [a, b] + new

        return Expression(styles[2], new, self.signal)
    
    # "({a} {x} {b} {y} {c}) {z} {d}",        # index: 3
    if self.style == styles[3]:
        # (a *+ b *+ c) ? d => [a, b, c] sort
        if x == '+' and y == '+' or x == '*' and y == '*':
            new: list = [a, b, c]; new.sort(); new.append(d)
            return Expression(styles[3], new, self.signal)
        
        # (a -/ b -/ c) ? d => [b, c] sort
        if x == '-' and y == '-' or x == '/' and y == '/':
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[3], new, self.signal)
        
        # (a * b +-/ c) ? d => [a, b] sort
        if x == '*' and y != '/':
            new: list = [a, b]; new.sort(); new = new + [c, d]
            return Expression(styles[3], new, self.signal)
        
        # remain:
        # (1) ['*', '/'] ['+', '-']
        # (2) ['+', '*'] ['-', '*']
        # (4) ['/', '+'] ['/', '-'] ['+', '/'] ['-', '/']
        # (5) ['/', '*'] ['-', '+']

        # (1) ['*', '/'] ['+', '-']
        # (a *+ b /- c) ? d => [a, b] sort
        if x == '*' and y == '/' or x == '+' and y == '-':
            new: list = [a, b]; new.sort(); new = new + [c, d]
            return Expression(styles[3], new, self.signal)
        
        # (2) ['+', '*'] ['-', '*']
        # (a +- b * c) ? d => [b, c] sort
        if y == '*' and (x == '+' or x == '-'):
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[3], new, self.signal)
        
        # (4) ['/', '+'] ['/', '-'] ['+', '/'] ['-', '/']
        if x == '/' and (y == '+' or y == '-') or x == '+' and y == '/' or x == '-' and y == '/': return self

        # (5) ['/', '*'] ['-', '+']
        # (a - b + c) ? d => [a, c] sort
        if x == '-' and y == '+' or x == '/' and y == '*':
            new: list = self.numbers
            if a > c: new[0], new[2] = new[2], new[0]
            return Expression(styles[3], new, self.signal)
        
        return self


    # "{a} {x} ({b} {y} {c} {z} {d})",        # index: 4
    if self.style == styles[4]:
        # a ? (b *+ c *+ d) ? d => [b, c, d] sort
        if y == '+' and z == '+' or y == '*' and z == '*':
            new: list = [b, c, d]; new.sort(); new = [a] + new
            return Expression(styles[4], new, [x, y, z])
        
        # a ? (b -/ c -/ d) => [c, d] sort
        if y == '-' and z == '-' or y == '/' and z == '/':
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[4], new, self.signal)
        
        # a ? (b * c +-/ d) ? d => [b, c] sort
        if y == '*' and z != '/':
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[4], new, self.signal)
        
        # (1) ['*', '/'] ['+', '-'] 
        # (2) ['/', '*'] ['-', '+'] 
        # (3) ['/', '+'] ['/', '-']
        # (4) ['+', '*'] ['-', '*']
        # (5) ['+', '/'] ['-', '/']

        # (1) ['*', '/'] ['+', '-']
        # a ? (b *+ c /- d) ? d => [b, c] sort
        if y == '*' and z == '/' or y == '+' and z == '-':
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[4], new, self.signal)
        
        # (2) ['/', '*'] ['-', '+']
        # a ? (b /- c *+ d) ? d => [b, d] sort
        if y == '/' and z == '*' or y == '-' and z == '+':
            new: list = self.numbers
            if b > d: new[0], new[2] = new[2], new[0]
            return Expression(styles[4], new, self.signal)
        
        # (3) ['/', '+'] ['/', '-']
        if y == '/' and x == '+' or y == '-' and x == '/': return self

        # (4) ['+', '*'] ['-', '*']
        # a ? (b +- c * d) => [c, d] sort
        if (y == '+' or y == '-') and z == '*':
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[4], new, self.signal)
        
        # (5) ['+', '/'] ['-', '/']
        if (y == '+' or y == '-') and z == '/': return self

        return self

    # "{a} {x} ({b} {y} {c}) {z} {d}",        # index: 5
    if self.style == styles[5]:
        new: list = self.numbers

        if y == '+' and y == '*':
            if b > c: new[1], new[2] = new[2], new[1]

        if x == '*' and z == '*' or x == '+' and z == '+':
            if a > d: new[0], new[2] = new[2], new[0]
            return Expression(styles[5], new, [x, y, z])
                
        if x == '-' and z == '-' or x == '/' and z == '/': return self

        if signal_priority[x] > signal_priority[z]: return self

        # remain
        # (1) ['/', '*'] ['-', '+'] 
        # (2) ['+', '*'] ['+', '/'] ['-', '*'] ['-', '/']

        # (1) ['/', '*'] ['-', '+']
        # a /- ? *+ d => [a, d] sort
        if x == '/' and z == '*' or x == '-' and z == '+':
            new2: list = new
            if a > d: new2[0], new2[3] = new2[3], new2[0]
            return Expression(styles[5], new2, self.signal)
                
        # (2) ['+', '*'] ['+', '/'] ['-', '*'] ['-', '/']
        if (x == '+' or x == '-') and (z == '*' or z == '/'): return self
        return self

    # "({a} {x} {b}) {y} ({c} {z} {d})",      # index: 6
    if self.style == styles[6]:
        new: list = self.numbers
        if a > b and (x == '+' or x == '*'): new[0], new[1] = new[1], new[0]
        if c > d and (z == '+' or z == '*'): new[2], new[3] = new[3], new[2]

        if y == '+' or y == '*':
            if eval(str(a) + x + str(b)) > eval(str(c) + z + str(d)):
                self.signal[0], self.signal[2] = self.signal[2], self.signal[0]
                new[0], new[2] = new[2], new[0]
                new[1], new[3] = new[3], new[1]

        return Expression(styles[6], new, self.signal)

    # "(({a} {x} {b}) {y} {c}) {z} {d}",      # index: 7
    if self.style == styles[7]:
        if x == '+' or x == '*':
            new: list = [a, b]; new.sort(); new = new + [c, d]
            return Expression(styles[7], new, [x, y, z])
        
        return self

    # "({a} {x} ({b} {y} {c})) {z} {d}",      # index: 8
    if self.style == styles[8]:
        if y == '+' or y == '*':
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[8], new, [x, y, z])
        
        return self

    # "{a} {x} (({b} {y} {c}) {z} {d})",      # index: 9
    if self.style == styles[9]:
        if y == '+' or y == '*':
            new: list = [b, c]; new.sort(); new = [a] + new + [d]
            return Expression(styles[9], new, [x, y, z])
        
        return self

    #"{a} {x} ({b} {y} ({c} {z} {d}))"      # index: 10
    if self.style == styles[10]:
        if z == '+' or z == '*':
            new: list = [c, d]; new.sort(); new = [a, b] + new
            return Expression(styles[10], new, [x, y, z])
        
        return self

    return self 


def has_equivalent(nums: list, string: Expression) -> bool:
    for i in nums:
        if string.expression == i.expression:
            return True
    return False


def get_answer(input_number: list) -> list:
    number_p: list = list(itertools.permutations(input_number, 4))
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 3))
    raw_result: list = []; unique_result: list = []; string_result = []

    for str1 in styles:
        for str2 in number_p:
            for str3 in signal_p:
                instance: Expression = Expression(str1, list(str2), list(str3))
                
                try:
                    value: int = eval(instance.expression)
                except ZeroDivisionError:
                    value: int = 0
                    
                if is_equal(value, 24):
                    simlified_expression: Expression = simplify(instance)
                    raw_result.append(format_number(format_signal(format_signal(simlified_expression))))
                    #raw_result.append(instance)

    for i in raw_result:
        if not has_equivalent(unique_result, i):
            unique_result.append(i)
            string_result.append(i.expression)

    if len(string_result) == 0:
        return ["false"]
    
    return string_result


if __name__ == "__main__":
    while True:
        inputs: list = input_numbers()
        ans: list = get_answer(inputs)
        print("Result(s): ")
        for i in ans:
            print(i)
