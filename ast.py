from colorama import Fore, Back
import copy
import logger

counter = 0

def make_ast_node(node, env=None):
    if node["type"] == "Declaration":
        return Declaration(node)
    if node["type"] == "Assignment":
        return Assignment(node, env)
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
        return Function(node, env)


class FunctionCall:
    def __init__(self, node):
        self.id = node["id"]
        self.args = [make_ast_node(arg) for arg in node["args"]]

    def accept(self, visitor):
        return visitor.visit_function_call(self)

    def __str__(self):
        return "(function_call " + self.id + " " + \
               str([str(arg) for arg in self.args]) + ")"


class Expression:
    def __init__(self, node):
        self.first = make_ast_node(node["first"])
        self.second = make_ast_node(node["second"])
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
    def __init__(self, node, env):
        self.params = [par["data"] for par in node["params"]]
        self.statements = [make_ast_node(stat) for stat in node["statements"]]
        # logger.debug(
        #     Back.YELLOW +
        #     Fore.BLACK,
        #     "NEW CLOSURE FOR FUNCTION",
        #     Back.RESET +
        #     Fore.RESET)
        # self.closure = env.copy()
        # self.closure.name = "CLOSURE FOR FUNCTION"
        # self.closure.store = env.store  # not SO DEEP COPY, MAINTAIN UNIQUE STORE
        # logger.debug(
        #     Back.RED +
        #     Fore.WHITE,
        #     "CLOSURE: ",
        #     self.closure,
        #     Back.RESET +
        #     Fore.RESET)

    def accept(self, visitor):
        return visitor.visit_function(self)

    def __str__(self):
        # return "FUN_STR"
        return "(fun " + str(self.params) + " " + \
               str([str(stat) for stat in self.statements]) + ")"

    def __repr__(self):
        return "FUN_REPR"


class Return:
    def __init__(self, node):
        self.exp = make_ast_node(node["exp"])

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
    def __init__(self, node, env):
        self.lvalue = make_ast_node(node["lvalue"])
        self.rvalue = make_ast_node(node["rvalue"], env)

    def accept(self, visitor):
        visitor.visit_assignment(self)

    def __str__(self):
        return "(assign " + str(self.lvalue) + " " + str(self.rvalue) + ")"


