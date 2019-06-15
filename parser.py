class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = ""
        self.previous_token = None

    def parse_assign_exp(self):
        # print("parsing assignment/expression")
        # assignment => id = expression
        lvalue = self.parse_expression()
        # print("lvalue: ", lvalue)
        if self.match("assign"):
            rvalue = self.parse_expression()
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
        # print("parsing expression")
        term = self.parse_term()
        # print("parsed term: ", term)
        if term is not None:
            # expression => term + expression
            if self.check('plus'):
                self.advance()
                exp = self.parse_expression()
                return {"type": "Expression", "lvalue": term, "op": 'plus', "rvalue": exp}
            # expression => term
            return term

    def parse_term(self):
        # term => factor
        # print("parsing term")
        factor = self.parse_factor()
        if factor is not None:
            # term => factor * term
            if self.check('mult'):
                self.advance()
                term = self.parse_term()
                return {"type": "Term", "lvalue": factor, "op": 'mult', "rvalue": term}
            return factor

    def parse_function(self):

        self.expect("lparen")
        args = []
        if self.match("id"):
            args.append(self.previous_token)
            while self.match("comma"):
                self.expect("id")
                args.append(self.previous_token)

        self.expect("rparen")

        self.expect("lbrace")
        statements = []
        while not self.check("rbrace"):
            statement = self.parse_statement()
            statements.append(statement)
            print("function statement", statement)
            input("ENTER FOR NEXT STATEMENT")
        self.advance()
        return {"type": "Function", "arguments": args, "statements": statements}

    def parse_factor(self):
        # factor => number
        # print("parsing factor")
        # print("factor current token:", self.current_token)
        if self.match('string'):
            return ("String", self.previous_token["data"])
        if self.match('number'):
            return ("Number", self.previous_token["data"])
        # factor => id
        if self.match("id"):
            # print("FACTOR ID: ", self.previous_token)
            return ("Variable", self.previous_token["data"])
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
            return ("Return", exp)

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
            print("STATEMENT: ", statement)
            input("\nNEXT ...\n")
        return program

    def parse(self):
        self.current_token = self.scanner.get_next()
        print("current token: ", self.current_token)
        self.current_token = {"type": self.current_token[0][0], "data": self.current_token[0]
                              [1], "line": self.current_token[1], "col": self.current_token[2]}
        return self.parse_program()
        # token, line, col = self.scanner.get_next()
        # while token != "eof":
        #     print(token, " line: ", line, " col: ", col)
        #     token, line, col = self.scanner.get_next()
