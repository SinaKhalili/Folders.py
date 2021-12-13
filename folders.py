"""
Folders is an esoteric programming language created by Daniel Temkin

More information here: http://danieltemkin.com/Esolangs/Folders/

This is a (OS-agnostic) python implementation
"""
import os
import re
import argparse


class FolderKeyword:
    """
    Simple class to hold all the magic strings
    """
    (IF, WHILE, DECLARE, LET, PRINT, INPUT) = (
        "IF", "WHILE", "DECLARE", "LET", "PRINT", "INPUT"
    )
    (VARIABLE, ADD, SUBTRACT, MULTIPLY, DIVIDE, LITERAL, EQ, GT, LT) = (
        "VARIABLE", "ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "LITERAL", "EQ", "GT", "LT"
    )
    (INT, FLOAT, STRING, CHAR) = ("INT", "FLOAT", "STRING", "CHAR")


class FolderToken:
    """
    Token class for the command types

    The list comprehension is to match value for the number of folders needed
    """
    (IF, WHILE, DECLARE, LET, PRINT, INPUT) = [
        i for i in range(6)
    ]
    (VARIABLE, ADD, SUBTRACT, MULTIPLY, DIVIDE, LITERAL, EQ, GT, LT) = [
        i for i in range(9)
    ]

    TYPES = ["INT", "FLOAT", "STRING", "CHAR"]

    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"<{self.token_type} :: {self.value}>"


class FolderAnalyzer:
    """
    Lexes path to `FolderToken` types
    """

    def __init__(self, path="."):
        self.path = path

    def lex(self,):
        """
        Returns an array of tokens
        """
        return self.lex_commands(self.path)

    def lex_commands(self, path):
        """
        Lex a folder of commands
        """
        curr_commands = []

        curr_dirs = self._get_dirs(path)

        for command in curr_dirs:
            command_dirs = self._get_dirs(command.path)
            command_length = len(self._get_dirs(command_dirs[0].path))

            if(command_length == FolderToken.IF):
                curr_commands.append(self.lex_if(command_dirs))
            elif(command_length == FolderToken.WHILE):
                curr_commands.append(self.lex_while(command_dirs))
            elif(command_length == FolderToken.DECLARE):
                curr_commands.append(self.lex_declare(command_dirs))
            elif(command_length == FolderToken.LET):
                curr_commands.append(self.lex_let(command_dirs))
            elif(command_length == FolderToken.PRINT):
                curr_commands.append(self.lex_print(command_dirs))
            elif(command_length == FolderToken.INPUT):
                curr_commands.append(self.lex_input(command_dirs))

        return curr_commands

    def lex_if(self, command_dirs):
        """
        Lexes an if command

        Second sub-folder holds expression, third holds list of commands
        """
        return FolderToken(
            FolderKeyword.IF,
            [
                self.lex_expression(command_dirs[1].path),
                self.lex_commands(command_dirs[2].path)
            ]
        )

    def lex_while(self, command_dirs):
        """
        Lexes a while command

        Second sub-folder holds expression, third holds list of commands
        """
        return FolderToken(
            FolderKeyword.WHILE,
            [
                self.lex_expression(command_dirs[1].path),
                self.lex_commands(command_dirs[2].path)
            ]
        )

    def lex_let(self, command_dirs):
        """
        Lexes a let statement

        Second holds var name (in number of folders), third holds expression
        """
        return FolderToken(
            FolderKeyword.LET,
            [
                self.lex_name(command_dirs[1].path),
                self.lex_expression(command_dirs[2].path)
            ]
        )

    def lex_input(self, command_dirs):
        """
        Lexes an input command

        Second sub-folder holds var name
        """
        return FolderToken(FolderKeyword.INPUT, self.lex_name(command_dirs[1].path))

    def lex_declare(self, command_dirs):
        """
        Lexes a declare statement

        Second sub-folder holds type, third holds var name (in number of folders)
        """
        return FolderToken(
            FolderKeyword.DECLARE,
            [
                self.lex_type(command_dirs[1].path),
                self.lex_name(command_dirs[2].path)
            ]
        )

    def lex_name(self, path):
        """
        Lexes a number to a variable name

        Simply does this by prepending var_ to the number
        """
        return f"var_{len(self._get_dirs(path))}"

    def lex_type(self, path):
        """
        Lex a type signature
        """
        type_len = len(self._get_dirs(path))

        return FolderToken.TYPES[type_len]

    def lex_print(self, command_dirs):
        """
        Lexes a print statement. Input the sorted directory of the commmand.

        Second sub-folder holds expression
        """
        return FolderToken(FolderKeyword.PRINT, self.lex_expression(command_dirs[1].path))

    def lex_expression(self, path):
        """
        Lexes an expression folder
        """
        expression_dirs = self._get_dirs(path)
        expression_length = len(self._get_dirs(expression_dirs[0].path))

        if (expression_length == FolderToken.VARIABLE):
            return FolderToken(FolderKeyword.VARIABLE, self.lex_name(expression_dirs[1].path))
        elif (expression_length == FolderToken.ADD):
            return FolderToken(
                FolderKeyword.ADD,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )
        elif (expression_length == FolderToken.SUBTRACT):
            return FolderToken(
                FolderKeyword.SUBTRACT,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )
        elif (expression_length == FolderToken.MULTIPLY):
            return FolderToken(
                FolderKeyword.MULTIPLY,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )
        elif (expression_length == FolderToken.DIVIDE):
            return FolderToken(
                FolderKeyword.DIVIDE,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )
        elif (expression_length == FolderToken.LITERAL):
            token_type = self.lex_type(expression_dirs[1].path)
            if (token_type == FolderKeyword.STRING):
                value = self.lex_string(expression_dirs[2].path)
            else:
                value = self.lex_value(expression_dirs[2].path)

            return FolderToken(FolderKeyword.LITERAL, [token_type, value])
        elif (expression_length == FolderToken.EQ):
            return FolderToken(
                FolderKeyword.EQ,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )
        elif (expression_length == FolderToken.GT):
            return FolderToken(
                FolderKeyword.GT,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )
        elif (expression_length == FolderToken.LT):
            return FolderToken(
                FolderKeyword.LT,
                [
                    self.lex_expression(expression_dirs[1].path),
                    self.lex_expression(expression_dirs[2].path)
                ]
            )

    def _get_hex_string(self, path):
        """
        Get the hex value from a path
        """
        dirs = self._get_dirs(path)
        if len(dirs) != 2:
            return ValueError("Error: Hex literal not two folders")

        dir_hex_left, dir_hex_right = dirs
        hex_left = hex_right = ""

        for folder in self._get_dirs(dir_hex_left.path):
            hex_left += str(len(self._get_dirs(folder.path)))

        for folder in self._get_dirs(dir_hex_right.path):
            hex_right += str(len(self._get_dirs(folder.path)))

        return hex_left + hex_right

    def lex_value(self, path):
        """
        Lex a generic value (INT, FLOAT, CHAR)
        since it's guaranteed to be a single hex
        """
        return self._get_hex_string(path)

    def lex_string(self, path):
        """
        Lex to one of the four types
        """
        string = ""
        for folder in self._get_dirs(path):
            string += self._bits2string([self._get_hex_string(folder.path)])

        return string

    def _get_dirs(self, path):
        """
        Helper to return the folders in alphabetically sorted order (not ASCIIbetically)

        Taken from:
        https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/

        NOTE: Uppercase/Lowercase of folder names are ignored. This is the behaviour of the
        original windows-based Folders language.
        """
        def convert(text): return int(text) if text.isdigit() else text

        def alphanum_key(key):
            return [convert(c) for c in re.split('([0-9]+)', key)]

        return sorted(
            [f for f in os.scandir(path) if f.is_dir()],
            key=lambda x: alphanum_key(x.path.lower())
        )

    def _bits2string(self, b=None):
        """
        Helper to turn a string like 1001010 to a character
        """
        return ''.join([chr(int(x, 2)) for x in b])


class FolderTranspiler:
    """
    Transpilation class, takes a list of tokens as input
    """

    def __init__(self, commands):
        self.commands = commands

    def transpile(self):
        """
        Transpilation entry point
        """
        return self.transpile_commands(self.commands)

    def transpile_commands(self, commands):
        """
        Transpile list of commands
        """
        program_code = ""
        for command in commands:
            ctype = command.token_type
            if(ctype == FolderKeyword.IF):
                program_code += self.transpile_if(command)
            elif(ctype == FolderKeyword.WHILE):
                program_code += self.transpile_while(command)
            elif(ctype == FolderKeyword.DECLARE):
                program_code += self.transpile_declare(command)
            elif(ctype == FolderKeyword.LET):
                program_code += self.transpile_let(command)
            elif(ctype == FolderKeyword.PRINT):
                program_code += self.transpile_print(command)
            elif(ctype == FolderKeyword.INPUT):
                program_code += self.transpile_input(command)
        return program_code



    def transpile_input(self, command):
        """
        Transpile an input command, which will just be value of name
        """

        return f"{command.value} = input()\nif {command.value}.isdigit():\n    {command.value} = int({command.value})\nelse:\n    {command.value} = {command.value}\n"

    def transpile_if(self, command):
        """
        Transpile an if command, which takes the following for

        [Expression, Commands]
        """
        expression, commands = command.value

        code = f"if ({self.transpile_expression(expression)}):\n"
        command_code = self.transpile_commands(commands)
        code += self._indent_commands(command_code)
        return code

    def transpile_while(self, command):
        """
        Transpile a while command, which takes the following for

        [Expression, Commands]
        """
        expression, commands = command.value

        code = f"while ({self.transpile_expression(expression)}):\n"
        command_code = self.transpile_commands(commands)
        code += self._indent_commands(command_code)
        return code

    def _indent_commands(self, code):
        """
        Takes a newline delimited code and adds an indent to each
        """
        indented_code = ""
        for line in code.split("\n"):
            indented_code += f"    {line}\n"
        return indented_code

    def transpile_declare(self, command):
        """
        HAHAHAHAHA DYNAMIC TYPE SYSTEMS
        """
        _, name = command.value
        return f"{name} = None\n"

    def transpile_let(self, command):
        """
        Transpile a let expression, which we could use the shiny
        walrus operator := for but to keep it legacy, let's not

        Lets can look like
        Value [NAME, EXPRESSION]
        """
        var_name, expression = command.value
        return f"{var_name} = {self.transpile_expression(expression)}\n"

    def transpile_print(self, command):
        """
        Transpile a print statement, which looks like a value as an expression
        """
        return f"print({self.transpile_expression(command.value)}, end='', flush=True)\n"

    def transpile_expression(self, command):
        """
        Dispatch to correct expression transpiler
        """
        ctype = command.token_type
        if(ctype == FolderKeyword.VARIABLE):
            return self.transpile_variable(command.value)
        elif(ctype == FolderKeyword.ADD):
            return self.transpile_binary_op(command.value, "+")
        elif(ctype == FolderKeyword.SUBTRACT):
            return self.transpile_binary_op(command.value, "-")
        elif(ctype == FolderKeyword.MULTIPLY):
            return self.transpile_binary_op(command.value, "*")
        elif(ctype == FolderKeyword.DIVIDE):
            return self.transpile_binary_op(command.value, "/")
        elif(ctype == FolderKeyword.LITERAL):
            return self.transpile_literal(command.value)
        elif(ctype == FolderKeyword.EQ):
            return self.transpile_binary_op(command.value, "==")
        elif(ctype == FolderKeyword.GT):
            return self.transpile_binary_op(command.value, ">")
        elif(ctype == FolderKeyword.LT):
            return self.transpile_binary_op(command.value, "<")

    def transpile_variable(self, value):
        """
        Transpile a variable (just the name)
        """
        return f"{value}"

    def transpile_binary_op(self, value, op):
        """
        Transpile any binary operation command of the form

        (expression) operation (expression)
        """
        left_val, right_val = value
        return f"({self.transpile_expression(left_val)}) {op} ({self.transpile_expression(right_val)})"

    def transpile_literal(self, value):
        """
        Transpile the literal value

        ex. ['STRING', 'foo'],
        ['INT', '01100011']
        """
        literal_type, literal_value = value
        if (literal_type == FolderKeyword.STRING):
            return f'"{literal_value}"'
        literal_value = int(literal_value, 2)
        if (literal_type == FolderKeyword.CHAR):
            return f"'{chr(literal_value)}'"
        elif (literal_type == FolderKeyword.FLOAT):
            return f"{float(literal_value)}"
        return f"{literal_value}"


def main():
    """
    Main entrypoint
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder", help="name of the folder entrypoint of the program")
    parser.add_argument("-l", "--list", help="Show the transpiled python code output on stdout instead of running",
                        action="store_true")
    args = parser.parse_args()
    tokens = FolderAnalyzer(args.folder).lex()
    code = FolderTranspiler(tokens).transpile()
    if args.list:
        print(code)
    else:
        exec(code)


if __name__ == '__main__':
    main()
