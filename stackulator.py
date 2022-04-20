import os

def hasGui() -> bool:
    if os.name == 'nt':
        ## windows always has a gui
        return True
    ## check for apple
    elif os.name == 'posix':
        if 'Apple' in os.uname():
            return True
        else:
            ## check for x11
            if 'X11' in os.uname():
                return True
    try:
        import tkinter
        return True
    except ImportError:
        return False
    return False

if hasGui():
    from tkinter.messagebox import showerror
else:
    def showerror(title, message):
        raise Exception(message)
from numpy import array as nparray
from sympy import ln
from math import *

class stackArray:
    def __init__(self, vals:list[int|float]) -> None:
        self.vals = vals
        self.size = len(vals)
        
    def append(self, val:int|float) -> None:
        if not isinstance(val, int) and not isinstance(val, float):
            showerror("Error", "Invalid input")
            return
        self.vals.append(val)
        self.size += 1
    
    def pop(self) -> int|float:
        if self.size == 0:
            showerror("Error", "Stack is empty")
            return
        self.size -= 1
        return self.vals.pop()
    
    def find(self, val:int|float) -> int:
        return self.vals.index(val)
    
    def remove(self, val:int|float) -> None:
        if not isinstance(val, int) and not isinstance(val, float):
            showerror("Error", "Invalid input")
            return
        self.vals.remove(self.find(val))
        self.size -= 1
        
    def __format__(self, format_spec:str) -> str:
        return format(str(self.vals), format_spec)
    
    def __ne__(self, other:int|float|stackArray) -> bool:
        return self.vals != other
    
    def __add__(self, other:int|stackArray|float) -> stackArray:
        if isinstance(other, stackArray):
            return stackArray(x for x in range(self.size) if self.vals[x] + other.vals[x])
        return stackArray([x + other for x in self.vals])
    
    def __mul__(self, other:int|stackArray|float) -> stackArray:
        if isinstance(other, stackArray):
            return stackArray(x for x in range(self.size) if self.vals[x] * other.vals[x])
        return stackArray([x * other for x in self.vals])
    
    def __sub__(self, other:int|stackArray|float) -> stackArray:
        if isinstance(other, stackArray):
            return stackArray(x for x in range(self.size) if self.vals[x] - other.vals[x])
        return stackArray([x - other for x in self.vals])
    
    def __truediv__(self, other:int|float|stackArray) -> stackArray:
        if isinstance(other, stackArray):
            return stackArray(x for x in range(self.size) if self.vals[x] / other.vals[x])
        return stackArray([x / other for x in self.vals])
    
    def __rtruediv__(self, other:int|float|stackArray) -> stackArray:
        if isinstance(other, stackArray):
            return stackArray(x for x in range(self.size) if other.vals[x] / self.vals[x])
        return stackArray([other / x for x in self.vals])
    
    def __pow__(self, other:int|float) -> stackArray:
        return stackArray([x ** other for x in self.vals])

    def __neg__(self) -> stackArray:
        return stackArray([-x for x in self.vals])
    
    def __str__(self) -> str:
        return str(self.vals)
    
    def __eq__(self, other:int|float|stackArray) -> bool:
        if isinstance(other, stackArray):
            return self.vals == other.vals
        return self.vals == other

class stackulator:
    def __init__(self) -> None:
        self.stack:list[int|float] = []
        self.max_stack:int|float   = 1000
        
    def push(self, value:int|float) -> None:
        if len(self.stack) >= self.max_stack:
            showerror("Stackulator", "Stack overflow")
            return
        self.stack.append(value)
    
    def pop(self) -> int|float:
        if (len(self.stack) == 0):
            showerror("Stackulator", "Stack underflow")
            return
        return self.stack.pop()
    
    def peek(self) -> int|float:
        if (len(self.stack) == 0):
            showerror("Stackulator", "Stack underflow")
            return
        return self.stack[-1]
    
    def add(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-2] += self.stack[-1]
        self.stack.pop()
        
    def sub(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-2] -= self.stack[-1]
        self.stack.pop()
        
    def mul(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-2] *= self.stack[-1]
        self.stack.pop()
        
    def div(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-2] /= self.stack[-1]
        self.stack.pop()
        
    def pow(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-2] **= self.stack[-1]
        self.stack.pop()
    
    def sqrt(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = sqrt(self.stack[-1])
    
    def xroot(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        base = self.pop()
        root = self.pop()
        self.push(root ** (1/base))
        
    def join(self) -> None:
        sr = stackArray([])
        i = len(self.stack) - 1
        while i >= 0:
            if not isinstance(self.stack[i], stackArray):
                sr.append(self.stack[i])
                self.stack.remove(self.stack[i])
            i -= 1
        self.stack.append(sr)
        
    def sin(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = sin(self.stack[-1])
        
    def cos(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = cos(self.stack[-1])
        
    def tan(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = tan(self.stack[-1])
        
    def asin(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = asin(self.stack[-1])
        
    def acos(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = acos(self.stack[-1])
        
    def atan(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = atan(self.stack[-1])
        
    def log(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        
        if (self.stack[-1] <= 0):
            raise Exception("Logarithm of negative number")
        
        ## check if we have a base
        if (len(self.stack) < 2):
            self.stack[-1] = log(self.stack[-1])
            return
        
        base = self.stack[-2]
        self.stack[-1] = log(self.stack[-1], base)
    
    def ln(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = ln(self.stack[-1])
        
    def abs(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = abs(self.stack[-1])
        
    def fact(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-1] = factorial(self.stack[-1])
    
    def clear(self) -> None:
        self.stack.clear()
        
    def dup(self) -> None:
        if (len(self.stack) < 1):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack.append(self.stack[-1])
    
    def swap(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack[-2], self.stack[-1] = self.stack[-1], self.stack[-2]

    def roll(self) -> None:
        if (len(self.stack) < 2):
            showerror("Stackulator", "Stack underflow")
            return
        self.stack = self.stack[::-1]


if __name__ == "__main__":
    sk = stackulator()
    sk.push(1)
    sk.push(21)
    sk.add()
    print(sk.pop())