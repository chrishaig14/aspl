from colorama import Fore

def convert(node):
    if node["type"] == "Declaration":
        return Declaration(node)
    if node["type"] == "Assignment":
        return Assignment(node)
    if node["type"] == "Expression":
        return Expression(node)
    if node["type"] == "Variable":
        return Variable(node)
    if node["type"] == "Number":
        return Number(node)
    if node["type"] == "String":
        return String(node)
    if node["type"] == "FunctionCall":
        return FunctionCall(node)
    if node["type"] == "Return":
        return Return(node)
    if node["type"] == "Function":
        print("Going to convert function : ", node)
        input()
        input()
        return Function(node)


class FunctionCall:
    def __init__(self, node):
        self.id = node["id"]
        self.args = [convert(arg) for arg in node["args"]]

    def accept(self, visitor):
        return visitor.visit_function_call(self)

    def __str__(self):
        return "(function_call " + self.id + " " + \
            str([str(arg) for arg in self.args]) + ")"


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.dict = {}

    def define(self, id):
        self.dict[id] = None

    def assign(self, id, value):
        self.dict[id] = value

    def get(self, id):
        if id in self.dict:
            return self.dict[id]
        if self.parent is not None:
            return self.parent.get(id)
        print("### ERROR: Undefined variable", id, "###")
        return self.dict[id]

    def __str__(self):
        return str(self.dict)
    def __del__(self):
        print(Fore.RED + "################# DESTROYING ENVIRONMENT" + str(self) + Fore.RESET)


class Expression:
    def __init__(self, node):
        self.first = convert(node["first"])
        self.second = convert(node["second"])
        self.op = node["op"]

    def accept(self, visitor):
        return visitor.visit_expression(self)

    def __str__(self):
        return "(" + self.op + " " + str(self.first) + \
            " " + str(self.second) + ")"


class Declaration:
    def __init__(self, node):
        self.id = node["id"]

    def accept(self, visitor):
        visitor.visit_declaration(self)

    def __str__(self):
        return "(declare " + self.id + ")"


class String:
    def __init__(self, node):
        self.string = node["value"]

    def accept(self, visitor):
        return self.string

    def __str__(self):
        return "(string " + self.string + ")"


class Function:
    def __init__(self, node):
        self.params = [par["data"] for par in node["params"]]
        self.statements = [convert(stat) for stat in node["statements"]]

    def accept(self, visitor):
        return self

    def __str__(self):
        # return "FUN_STR"
        return "(fun " + str(self.params) + " " + \
            str([str(stat) for stat in self.statements]) + ")"
    def __repr__(self):
        return "FUN_REPR"


class Return:
    def __init__(self, node):
        self.exp = convert(node["exp"])

    def accept(self, visitor):
        return visitor.visit_return(self)

    def __str__(self):
        return "(return " + str(self.exp) + ")"


class Variable:
    def __init__(self, node):
        self.id = node["id"]

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __str__(self):
        return "(variable " + self.id + ")"


class Number:
    def __init__(self, node):
        self.number = node["value"]

    def accept(self, visitor):
        return self.number

    def __str__(self):
        return "(number " + str(self.number) + ")"


class Assignment:
    def __init__(self, node):
        self.lvalue = convert(node["lvalue"])
        self.rvalue = convert(node["rvalue"])

    def accept(self, visitor):
        visitor.visit_assignment(self)

    def __str__(self):
        return "(assign " + str(self.lvalue) + " " + str(self.rvalue) + ")"


class Interpreter:
    def __init__(self, program):
        self.program = program
        self.environment = Environment()
        self.return_value = None
        self.set_return_val = False

    def run(self):
        for statement in self.program:
            input()
            statement.accept(self)
            print(self.environment)

    def visit_variable(self, variable):
        return self.environment.get(variable.id)

    def visit_function_call(self, function_call):
        args = [arg.accept(self) for arg in function_call.args]
        if function_call.id == "print":
            print(args[0])
            return
        self.environment = Environment(self.environment)
        function = self.environment.get(function_call.id)
        for i in range(len(function.params)):
            param = function.params[i]
            arg = args[i]
            print("PARAM:",param)
            print("ARG:", arg)
            self.environment.assign(param, arg)
        for stat in function.statements:
            stat.accept(self)
            if self.set_return_val:
                self.set_return_val = False
                self.environment = self.environment.parent
                return self.return_value

        # return None

    def visit_declaration(self, declaration):
        self.environment.define(declaration.id)

    def visit_return(self, return_s):
        val = return_s.exp.accept(self)
        self.return_value = val
        self.set_return_val = True
        return val

    def visit_expression(self, expression):
        xxx = expression.first.accept(self)
        second = expression.second.accept(self)
        if expression.op == "plus":
            r = xxx + second
            return r
        if expression.op == "minus":
            return xxx - second

    def visit_assignment(self, assignment):
        print("My rvalue is ", assignment.rvalue)
        val = assignment.rvalue.accept(self)
        self.environment.assign(assignment.lvalue.id,
                                val)
