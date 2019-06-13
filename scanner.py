keywords = ["var", "fun", "return", "if", "else"]
ops = ["++", "--", "+", "-", "*", "/", "=", "=="]
special = [";"]


def scan_alnum(str, cur, line, col):
    start = cur
    while cur < len(str) and str[cur].isalnum():
        cur += 1
        col += 1
    end = cur
    token = str[start:end]
    if token in keywords:
        return (token), start, cur, line, col
    return ("id", str[start:end]), start, cur, line, col


def scan_num(str, cur, line, col):
    start = cur
    while cur < len(str) and str[cur].isdigit():
        cur += 1
        col += 1

    end = cur
    return ("integer", int(str[start:end])), start, cur, line, col


def scan_other(str, cur, line, col):
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


def scan(str, cur, line, col):
    if str[cur].isalpha():
        return scan_alnum(str, cur, line, col)
    elif str[cur].isdigit():
        return scan_num(str, cur, line, col)
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
        return scan_other(str, cur, line, col)


f = open("sample1.aspl")
text = f.read()
cur = 0
line = 1
col = 1
while cur < len(text):
    x = scan(text, cur, line, col)
    token, start, cur, line, new_col = x
    if token == "invalid":
        print("ERROR: invalid token at", cur, ":" + text[cur])
        break
    else:
        # if token == "":
        #     continue
        if token != "":
            print(str(token) + " at " + str(start), " line: ", line, " col: ", col)
    col = new_col
    # print("col now is: ",)