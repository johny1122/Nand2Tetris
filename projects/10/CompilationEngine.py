# this is the parser
"""
Unit 10.3: Grammars
the order of tokens.
terminal rules ( = tokens) and non-terminal rules ( = statements, expressions, etc.).
parsing is the process of detemining whether an input conforms to a grammar.

Unit 10.4: Parse Trees
is a recursive structure.
xml describes structured data.

Unit 10.5: Parser Logic
parser design: a method (parsing routine) for each non-terminal rule. compilexxx.
LL grammar, LL(k) parser. 
programming languages grammar is usually LL(1).
natural languages are more diffucul to parse ( large k).
look a head at most k tokens in order to determine which rule is applicable.
"""
statements_dict = {"let": compileLet,
                       "if": compileIf,
                       "while": compileWhile,
                       "do": compileDo,
                       "return": compileReturn}

symbol_dict = {"<": "&lt;",
                   ">": "&gt;",
                   "\"": "&quot;",
                   "&": "&amp;"}






import sys
import re
import os
import xml.etree.ElementTree as ET # USE TO CREATE A TREE, FOR INDENTATION, ETC.
# vocab: attribute, child, content model, element, parent, root element, schema, 
import re # regex


from Tokenizer import Tokenizer

class CompilationEngine:
    """
    gets input from JackTokenizer, emits output to an output file.
    """

    def __init__(self, file_name, path_name):
        # self.compiled_code = ""
        self.file_name = file_name
        self.path_name = path_name
        # self.indentation = 0
        self.root = None

    def run(self):
        """
        Run compiler on file.
        compile token list generated by the tokenizer into output file.
        """
        with open(self.path_name, 'r') as current_file:
            self.tokenizer = JackTokenizer(current_file)
            self.compile_class()
        with open(self.path_name.replace(".jack", ".xml"), 'w') as output_file:
            for line in self.compiled_code:
                output_file.write(line + "\n")
        # jack_file.close()

    def advance_tokenizer(self):
        """
        return current_token, token_type
        """
        self.tokenizer.advance()
        current_token = self.tokenizer.get_current_token()
        token_type = self.tokenizer.token_type()
        return current_token, token_type

    
    def compile_class(self):
        """
        A class is a sequence of tokens structured according to the following context free syntax.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.root = etree.Element('class')
        # class beginning: 'class' keyword, class_name identifier, '{' symbol
        for i in range(3):
            current_token, token_type = self.advance_tokenizer()
            class_subelement = ET.SubElement(root, token_type)
            class_subelement.text = current_token
        # class fields:
        current_token, token_type = self.advance_tokenizer()
        while current_token in ["field", "static"]:
            compile_class_var_dec() # previoiusly: output += compile_class_var_dec()
            current_token, token_type = self.advance_tokenizer()
            # self.tokenizer.peek() # they used "peek"
        # class subroutines:
        while current_token in ["constructor", "function", "method"]:
            self.compile_subroutine_dec()
            current_token, token_type = self.advance_tokenizer() # they used "peek"
        # class ending: '}'
        class_subelement = ET.SubElement(root, token_type)
        class_subelement.text = current_token


    def compile_class_var_dec(): # dec = declaration
        """
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        type: 'int' | 'char' | 'boolean' | className
        
        """
        current_token = self.tokenizer.get_token_type()
        token_type = self.tokenizer.peek()

        field_type = ET.SubElement(root, token_type) # static/field keyword
        field_type.text = current_token
        
        current_token, token_type = self.advance_tokenizer()
        compile_var_dec(field_type)


    def compile_subroutine_dec():
        """
        subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        subroutineName: identifier
        """
        current_token = self.tokenizer.get_token_type()
        token_type = self.tokenizer.peek()
        subroutine_type = ET.SubElement(root, token_type) # type: contructor/function/method keyword
        subroutine_type.text = current_token
        
        current_token, token_type = self.advance_tokenizer()
        return_type = ET.SubElement(root, token_type) # return type: void/boolean/int/char keyword, or object identifier
        return_type.text = current_token
        
        current_token, token_type = self.advance_tokenizer()
        subroutine_name = ET.SubElement(root, token_type) # name: identifier
        subroutine_name.text = current_token
        
        current_token, token_type = self.advance_tokenizer()
        subroutine_name = ET.SubElement(root, token_type) # '(' symbol
        subroutine_name.text = current_token
        
        compile_parameter_list()

        current_token, token_type = self.advance_tokenizer()
        subroutine_name = ET.SubElement(root, token_type) # ')' symbol
        subroutine_name.text = current_token
        
        compile_subroutine_body()


    def compile_parameter_list():
        """
        parameterList: ((type varName) (',' type varName)*)?
        varName: identifier
        """
        current_token, token_type = self.advance_tokenizer()
        param_type = ET.SubElement(field_type, token_type) # boolean/int/char(/object?) keyword
        param_type.text = current_token
        current_token, token_type = self.advance_tokenizer()
        param_name = ET.SubElement(field_type, token_type) # param_name identifier
        param_name.text = current_token

        current_token, token_type = self.advance_tokenizer()
        while current_token is ',': # loop is for second parameter and so on
            # boolean/char/int/obj: # we assume valid input
            var_type = ET.SubElement(field_type, token_type) # , symbol
            var_type.text = current_token
            current_token, token_type = self.advance_tokenizer() # advance tokenizer
            else: # did not adavance tokenizer
                current_token = self.tokenizer.get_token_type()
                token_type = self.tokenizer.peek()
            
            param_type = ET.SubElement(field_type, token_type) # boolean/int/char(/object?) keyword
            param_type.text = current_token
            param_name = ET.SubElement(field_type, token_type) # param_name identifier
            param_name.text = current_token
        
        

    def compile_subroutine_body():
        """
        subroutineBody: '{' varDec* statements '}'        
        """
        for:
            compile_statements()


    def compile_var_dec(field_type):
        """
        varDec: 'var' type varName (',' varName)* ';'
        varName: identifier
        """
        while current_token is not ';': # we assume valid input
            if current token is ',':
                var_type = ET.SubElement(field_type, token_type) # , symbol
                var_type.text = current_token
                current_token, token_type = self.advance_tokenizer() # advance tokenizer
            else: # did not adavance tokenizer
                current_token = self.tokenizer.get_token_type()
                token_type = self.tokenizer.peek()
            
            var_type = ET.SubElement(field_type, token_type) # boolean/int/char keyword
            var_type.text = current_token
            var_name = ET.SubElement(field_type, token_type) # var_name identifier
            var_name.text = current_token
            
            current_token, token_type = self.advance_tokenizer()


    def compile_statements():
    """
    statements: statement*
    statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement

    Each compilexxx routine is responsible for handling all the tokens that make up
    xxx, advancing the tokenizer exactly beyond these tokens, and outputing the
    parsing of xxx
    """

    def compile_let_statement():
    """
    letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    """
    return 
        



    def compile_if_statement():
    """
    ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
    """
    def compile_while_statement():
    """
    whileStatement: 'while' ( 'expression' ) '{' statements '}'
    """

    def compile_do_statement(output):
    """
    doStatement: 'do' subroutineCall ';'

    we should get here only if we're certain it's a do
    """
    output += self.tokenizer.token_type(current_token)
    self.advance_tokenizer()
    return output

    def compile_return_statement():
        

}


def compile_expression(self):
    """
    expression structure. including term or subroutine call, in which the language is LL(2).
    expression: term (op term)*
    
    subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    expressionList: (expression (',' expression)* )?
    op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    unaryOp: '-' | '~'
    keywordConstant: 'true' | 'false' | 'null' | 'this'
    """
    if:
        self.compile_term()
    for:
        self.compile_op()
        self.compile_term()

def compile_term(self):
    """
    term: integerConstant | stringConstant | keywordConstant | varName | varName '['expression']' | subroutineCall | '(' expression ')' |
    unaryOp term
    """

def compile_expression_list():


























































# use xml package instead

# type 1 tag
    def start_tag(): # remember to later indentation += 2
        return " " * self.indentation + "<" + token_type + ">"

    def end_tag(): # remember to later indentation += 2
        return " " * self.indentation + "</" + token_type + ">"

    def special_tags(self, token, token_type): #line type 2
        """
        if token.equals('<'):
            return "<symbol>" + &lt + "</symbol>" 
        elif token.equals('>'):
            return "<symbol>" + &gt + "</symbol>" 
        elif token.equals('"'):
            return "<symbol>" + &quot + "</symbol>" 
        elif token.equals('>'):
            return "<symbol>" + &amp + "</symbol>" 
        return "<symbol>" + token + "</symbol>"
        """
        if token_type == "symbol" and token in ["<", ">", "\"", "&"]:
            token = self.symbol_dict[token]
        line = " " * self.indentation + "<" + token_type + "> " + token + " </" + token_type + ">"
        return line
