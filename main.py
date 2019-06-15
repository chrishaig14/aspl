from parser import Parser
from scanner import Scanner

f = open("sample1.aspl")
text = f.read()

scanner = Scanner(text)
parser = Parser(scanner)
tree = parser.parse()
print("#####     PARSE TREE     #####")
for statement in tree:
	print(statement)