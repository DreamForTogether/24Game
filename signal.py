import itertools
import main

test_numbers = [2, 23, 67, 97]
number_p: list = list(itertools.permutations(test_numbers, 4))


def split() -> None:
    print("\n------------------------------------------------------------------------------------------------")
    

def formate_signal_0() -> None:
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 3))
    
    for i in signal_p:
        signal: list = list(i)
        x: chr = signal[0]; y: chr = signal[1]; z: chr = signal[2]
        if (main.signal_priority[x] >= main.signal_priority[y] >= main.signal_priority[z]) or (
           (x == '*' or x == '/') and (y == '+' or y == '-') and (z == '*' or z == '/')):
            continue
            
        if x != '*' and y != '*' and z != '*' and x != '/' and y != '/' and z != '/':
            continue
        
        if x != '+' and y != '+' and z != '+' and x != '-' and y != '-' and z != '-':
            continue
        
        print(signal, end=' ')
    
    split()


def formate_signal_1() -> None:
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))
    
    for i in signal_p:
        signal: list = list(i)
        y: chr = signal[0]; z: chr = signal[1]; 
        
        if main.signal_priority[y] >= main.signal_priority[z] or (y == '*' or y == '/') and (z == '+' or z == '-'):
            continue
        
        print(signal, end=' ')
        
    split()

    
def formate_signal_2() -> None:
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))
    
    for i in signal_p:
        signal: list = list(i)
        x: chr = signal[0]; y: chr = signal[1]; 
        
        if x == '*' and y == '*' or x == '+' and y == '+':
            continue

        if x == '-' and y == '-' or x == '/' and y == '/':
            continue
        
        print(signal, end=' ')
        
    split()


def formate_signal_3() -> None:
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))
    
    for i in signal_p:
        signal: list = list(i)
        x: chr = signal[0]; y: chr = signal[1]; 
        
        if main.signal_priority[x] >= main.signal_priority[y]:
            continue
        
        print(signal, end=' ')
        
    split()


def formate_signal_4() -> None:
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))
    
    for i in signal_p:
        signal: list = list(i)
        y: chr = signal[0]; z: chr = signal[1]; 
    
        if main.signal_priority[y] >= main.signal_priority[z]:
            continue
        
        print(signal, end=' ')
        
    split()


def formate_signal_5() -> None:
    signal_p: list = list(itertools.product(['*', '/', '+', '-'], repeat = 2))
    
    for i in signal_p:
        signal: list = list(i)
        x: chr = signal[0]; z: chr = signal[1]; 
    
        if x == '*' and z == '*' or x == '+' and z == '+': continue
        if x == '-' and z == '-' or x == '/' and z == '/': continue
        if main.signal_priority[x] > main.signal_priority[z]: continue
        
        print(signal, end=' ')
            
    split()


if __name__ == "__main__":
    formate_signal_0()
    formate_signal_1()
    formate_signal_2()
    formate_signal_3()
    formate_signal_4()
    formate_signal_5()