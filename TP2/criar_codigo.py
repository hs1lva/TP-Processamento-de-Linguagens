# Definindo a codificação como UTF-8
# -*- coding: utf-8 -*-
class Node:
    def evaluate(self, env):
        pass

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self, env):
        if self.op == '+':
            return self.left.evaluate(env) + self.right.evaluate(env)
        elif self.op == '-':
            return self.left.evaluate(env) - self.right.evaluate(env)
        elif self.op == '*':
            return self.left.evaluate(env) * self.right.evaluate(env)
        elif self.op == '/':
            return self.left.evaluate(env) // self.right.evaluate(env)
        elif self.op == 'E':
            return self.left.evaluate(env) and self.right.evaluate(env)
        elif self.op == 'OU':
            return self.left.evaluate(env) or self.right.evaluate(env)

class Num(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

class Id(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        return env[self.name]

class Assign(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def evaluate(self, env):
        env[self.name] = self.expr.evaluate(env)
        return env[self.name]

class Escrever(Node):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, env):
        value = self.expr.evaluate(env)
        if isinstance(value, str):
            print(value)
        else:
            print(value)
        return value

class String(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

class Concatenate(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, env):
        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)
        return str(left_val) + str(right_val)

class Funcao(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def evaluate(self, env):
        env[self.name] = self
        return self

class Lista(Node):
    def __init__(self, elements):
        self.elements = elements

    def evaluate(self, env):
        return [element.evaluate(env) for element in self.elements]

class Map(Node):
    def __init__(self, func, lst):
        self.func = func
        self.lst = lst

    def evaluate(self, env):
        func = self.func.evaluate(env)
        lst = self.lst.evaluate(env)
        return [func.evaluate({'_': elem}) for elem in lst]

class Fold(Node):
    def __init__(self, func, lst, init):
        self.func = func
        self.lst = lst
        self.init = init

    def evaluate(self, env):
        func = self.func.evaluate(env)
        lst = self.lst.evaluate(env)
        result = self.init.evaluate(env)
        for elem in lst:
            result = func.evaluate({'_1': result, '_2': elem})
        return result

class And(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, env):
        return self.left.evaluate(env) and self.right.evaluate(env)

class Or(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, env):
        return self.left.evaluate(env) or self.right.evaluate(env)

class Not(Node):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, env):
        return not self.expr.evaluate(env)

class Bool(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value == 'verdadeiro'
