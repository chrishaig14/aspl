keywords = ["var", "fun", "return", "if", "else"]
ops = ["++", "--", "+", "-", "*", "/", "=", "=="]
special = [";"]


class Scanner:

    def __init__(self, text):
        self.str = text
        self.cur = 0
        self.line = 1
        self.col = 1

    def scan_alnum(self, str, cur, line, col):
        start = cur
        while cur < len(str) and str[cur].isalnum():
            cur += 1
            col += 1
        end = cur
        token = str[start:end]
        if token in keywords:
            return (token), start, cur, line, col
        return ("id", str[start:end]), start, cur, line, col

    def scan_num(self, str, cur, line, col):
        start = cur
        while cur < len(str) and str[cur].isdigit():
            cur += 1
            col += 1

        end = cur
        return ("integer", int(str[start:end])), start, cur, line, col

    def scan_other(self, str, cur, line, col):
        if str[cur] == ";":
            start = cur
            cur += 1
            col += 1
            return "semic", start, cur, line, col
        elif str[cur] == "=":
            start = cur
            if str[cur + 1] != "=":
                cur += 1
                col += 1
                return "assign", start, cur, line, col
            else:
                cur += 2
                col += 2
                return "eqop", start, cur, line, col
        elif str[cur] == "+":
            start = cur
            if str[cur + 1] != "+":
                cur += 1
                col += 1
                return "plus", start, cur, line, col
            else:
                cur += 2
                col += 2
                return "incrop", start, cur, line, col
        else:
            return "invalid", cur, cur, line, col

    def scan(self, str, cur, line, col):
        if cur >= len(str):
            return "eof",-1,-1,-1,-1
        if str[cur].isalpha():
            return self.scan_alnum(str, cur, line, col)
        elif str[cur].isdigit():
            return self.scan_num(str, cur, line, col)
        elif str[cur].isspace():
            start = cur
            while cur < len(str) and str[cur].isspace():
                if str[cur] == "\n":
                    line += 1
                    col = 1
                else:
                    col += 1
                cur += 1
            return "", start, cur, line, col
        else:
            return self.scan_other(str, cur, line, col)

    def get_next(self):
        token, start, cur, line, new_col = self.scan(
            self.str, self.cur, self.line, self.col)
        ret_token = (token, line, self.col)
        self.col = new_col
        self.line = line
        self.cur = cur
        if token == "":
            return self.get_next()
        return ret_token

f = open("sample1.aspl")
text = f.read()

scanner = Scanner(text)

token, line, col = scanner.get_next()

while token != "eof":
    print(str(token) + " line: ", line, " col: ", col)
    token, line, col = scanner.get_next()
    # input()
