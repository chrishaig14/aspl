from colorama import Fore, Back, Style

class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = ""
        self.previous_token = None

    def parse_assign_exp(self):
        # assignment => id = expression
        lvalue = self.parse_expression()
        # print("lvalue: ", lvalue)
        if self.match("assign"):
            rvalue = self.parse_expression()
            print("rvalue:", rvalue)
            input()
            return {"type": "Assignment", "lvalue": lvalue, "rvalue": rvalue}
        else:
            return lvalue

    def parse_declaration(self):
        # print("parsing declaration")
        # declaration => var id
        if self.check("var"):
            self.advance()
            self.expect("id")
            return {"type": "Declaration", "id": self.previous_token["data"]}

    def parse_expression(self):
        # print("PARSING NEW EXPRESSION:::")
        # print("parsing expression")
        exp = self.parse_term()
        # print("parsed term: ", term)
        # print("parsed term", exp)
        while self.check("plus") or self.check("minus"):
            # print("THERES MORE")
            op = self.current_token["type"]
            self.advance()
            second = self.parse_term()
            print("second: ", second)
            exp = {"type": "Expression", "first": exp,
                   "op": op, "second": second}

        return exp
        # if term is not None:
        #     # expression => term + expression
        #     if self.check('plus'):
        #         self.advance()
        #         exp = self.parse_expression()
        #         return {"type": "Expression", "first": term, "op": 'plus', "second": exp}
        #     if self.check('minus'):
        #         self.advance()
        #         exp = self.parse_expression()
        #         return {"type": "Expression", "first": term, "op": 'minus', "second": exp}
        #     # expression => term
        #     return term

    def parse_term(self):
        # term => factor
        # print("parsing term")
        factor = self.parse_factor()
        if factor is not None:
            # term => factor * term
            if self.check('mult'):
                self.advance()
                term = self.parse_term()
                return {"type": "Expression", "first": factor, "op": 'mult', "second": term}
            return factor

    def parse_function(self):
        print("NOW PARSING A FUNCTION")
        self.expect("lparen")
        params = []
        if self.match("id"):
            params.append(self.previous_token)
            while self.match("comma"):
                self.expect("id")
                params.append(self.previous_token)

        self.expect("rparen")

        self.expect("lbrace")
        statements = []
        while not self.check("rbrace"):
            statement = self.parse_statement()
            statements.append(statement)
            # print("function statement", statement)
            # input("ENTER FOR NEXT STATEMENT")
        self.advance()
        # input()
        # input()
        # input()
        # input()
        # print("FUNCTION PARSED IS: ", {"type": "Function", "arguments": args, "statements": statements})
        return {"type": "Function", "params": params, "statements": statements}

    def parse_factor(self):
        # factor => number
        # print("parsing factor")
        # print("factor current token:", self.current_token)
        if self.match('string'):
            return {"type": "String", "value": self.previous_token["data"]}
        if self.match('number'):
            return {"type": "Number", "value": self.previous_token["data"]}
        # factor => id
        if self.match("id"):
            # print("FACTOR ID: ", self.previous_token)
            id = self.previous_token["data"]
            # print("Found simple variable:", id)
            if self.match("lparen"):
                if self.match("rparen"):
                    # print("Found empty function call")
                    return {"type": "FunctionCall", "id": id, "args": []}
                else:
                    arg = self.parse_expression()
                    # print("Found argument: ", arg)
                    args = [arg]
                    while self.match("comma"):
                        arg = self.parse_expression()
                        args.append(arg)
                        # print("Found argument: ", arg)
                    self.match("rparen")
                    return {"type": "FunctionCall", "id": id, "args": args}
            else:
                # print("Found simple variable:", id)
                return {"type": "Variable", "id": id}
            # self.expect("rparen")

        # factor => ( exp )
        if self.match("lparen"):
            exp = self.parse_expression()
            if exp is not None:
                self.expect("rparen")
                return exp
        if self.match("fun"):
            # self.expect("lparen")
            # self.expect("rparen")
            # self.expect("lbrace")
            # self.expect("rbrace")
            fun = self.parse_function()
            print("FUNCTION: ", fun)
            return fun

    def parse_statement(self):
        # print("parsing statement")
        # statement => declaration;
        if self.check("var"):
            decl = self.parse_declaration()
            # print("EXPECTING SEMICOLON FOR DECLARATION")
            self.expect("semicolon")
            # print("EXPECTING SEMICOLON FOR DECLARATION END")

            if decl is not None:
                return decl

        # statement => assign_exp;
        if self.check("id"):
            assign = self.parse_assign_exp()
            # print("CURRENT TOKEN: ", self.current_token)
            # print("EXPECTING SEMICOLON HERE")
            self.expect("semicolon")
            if assign is not None:
                return assign
        if self.check("return"):
            self.advance()
            exp = self.parse_expression()
            # print("RETURN EXPRESSION: ", exp)
            self.expect("semicolon")
            return {"type":"Return", "exp":exp}

        print("Error: expected statement, got", self.current_token["type"])

    def match(self, token):
        if self.check(token):
            self.advance()
            return True
        return False

    def expect(self, token):
        if self.match(token):
            pass
        else:
            print("<<<### ERROR: expected", token, "instead of",
                  self.current_token["type"], "at line", self.current_token["line"], "###>>>")

    def advance(self):
        self.previous_token = self.current_token
        self.current_token = self.scanner.get_next()
        self.current_token = {"type": self.current_token[0][0], "data": self.current_token[0]
                              [1], "line": self.current_token[1], "col": self.current_token[2]}

    def check(self, token):
        # print("accept token ", token, "? ",
              # "current token ", self.current_token)
        # print("self.current_token =", self.current_token)
        if self.current_token["type"] == token:
            # print("accept", token, " true")

            return True
        # print("accept", token, " false")
        return False

    def parse_program(self):
        program = []
        while not self.check("eof"):
            statement = self.parse_statement()
            program.append(statement)
            # print("STATEMENT: ", statement)
            # input("\nNEXT ...\n")
        return program

    def parse(self):
        self.current_token = self.scanner.get_next()
        # print("current token: ", self.current_token)
        self.current_token = {"type": self.current_token[0][0], "data": self.current_token[0]
                              [1], "line": self.current_token[1], "col": self.current_token[2]}
        return self.parse_program()
        # token, line, col = self.scanner.get_next()
        # while token != "eof":
        #     print(token, " line: ", line, " col: ", col)
        #     token, line, col = self.scanner.get_next()
