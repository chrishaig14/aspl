from parser import Parser

from helper import *
from scanner import Scanner



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

final = []
for statement in tree:
    statement_obj = convert(statement)
    final.append(statement_obj)
    print(statement_obj)

interpreter = Interpreter(final)
interpreter.run()
