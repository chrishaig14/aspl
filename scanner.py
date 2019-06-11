def scan(str, cur):
    if str[cur].isalpha():
        # print("starts with a letter")
        start = cur
        while cur < len(str) and str[cur].isalnum():
            cur += 1
        end = cur
        if str[start:end] == "var":
            return ("var"), start, cur
        return ("id", str[start:end]), start, cur
    elif str[cur].isdigit():
        # print("starts with a digit")
        start = cur
        while cur < len(str) and str[cur].isdigit():
            cur += 1
        end = cur
        return ("integer", int(str[start:end])), start, cur
    elif str[cur].isspace():
        start = cur
        while cur < len(str) and str[cur].isspace():
            cur += 1
        return "", start, cur
    elif str[cur] == ";":
        start = cur
        cur += 1
        return "semic", start, cur
    elif str[cur] == "=":
        start = cur
        if str[cur + 1] != "=":
            cur += 1
            return "assign", start, cur
        else:
            cur += 2
            return "eqop", start, cur
    elif str[cur] == "+":
        start = cur
        if str[cur + 1] != "+":
            cur += 1
            return "plus", start, cur
        else:
            cur += 2
            return "incrop", start, cur
    else:
        return "invalid", cur, cur


f = open("sample1.aspl")
text = f.read()
cur = 0
while cur < len(text):
    x = scan(text, cur)
    # print("scan returned ",x)
    token, start, cur = x
    if token == "invalid":
        print("ERROR: invalid token at", cur, ":" + text[cur])
        break
    else:
        if token == "":
            continue
        print(str(token) + " at " + str(start))
# print(result)
