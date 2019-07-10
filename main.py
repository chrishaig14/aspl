from interpreter import Interpreter
from parser import Parser

# from helper import *
from ast import make_ast_node
from scanner import Scanner
import logger

logger.ACTIVE = False
logger.DEBUG = True

f = open("sample1.aspl")
text = f.read()

scanner = Scanner(text)

parser = Parser(scanner)
tree = parser.parse()
print("#####     PARSE TREE     #####")
for statement in tree:
    print(statement)

print("##### PRESS ENTER TO RUN #####")
input()

logger.ACTIVE = True
logger.DEBUG = False

prog = []

for node in tree:
    # print("NODE: ", node)
    node = make_ast_node(node)
    prog.append(node)
    print(node)

interpreter = Interpreter(prog)
interpreter.run()
