
from time import time


class TerminalColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'


def indent(num):
    result = ''
    while num > 1:
        result += ' '
        num -= 1
    return result


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func


def print_sorted_dict(var, num=0):
    num = indent(num)
    for a in sorted(var):
        print(num + str(a), ':', str(var[a]))

def print_list(list_array,indent=0):
    for item in list_array:
        for i in range(indent):
            item = '    ' + str(item)
        print(item)

def print_dict(dict_array,indent=0):
    for item in dict_array:
        for i in range(indent):
            item = '    ' + str(item)
        print(item, ':', dict_array[item])

if __name__ == '__main__':

    test_list = [1,2,3,4,5,6,7,8]
    test_dict = {'one':1, 'two':2}

    print_dict(test_dict)
    print_list(test_list)
