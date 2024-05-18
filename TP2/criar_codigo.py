class Node: # Necessário para a função de nó abstrato
    def evaluate(self, env):
        pass

class BinOp(Node): # Necessário para a função de operação binária
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

class Num(Node): # Necessário para a função de número
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

class Id(Node): # Necessário para a função de identificação
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        return env[self.name]

class Assign(Node): # Necessário para a função de atribuição
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def evaluate(self, env):
        env[self.name] = self.expr.evaluate(env)
        return env[self.name]

class Escrever(Node): # Necessário para a função de escrita
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, env):
        value = self.expr.evaluate(env)
        print(value)
        return value
