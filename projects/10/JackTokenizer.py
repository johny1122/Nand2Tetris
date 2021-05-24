"""

When translating string constants:
1. The tokenizer throws away the double quote characters (").
2. Escaped characters are handled as regular characters ('\t' is translated to '\t').
3. In any case of "\X" where '\' and 'X' are two different characters, handle it as two
different characters (as you would usually handle it!).
Notice the difference between the two cases: the current one is a string comprised of two
characters, and the previous is a single character.

Empty tags (tags that have no content between the opening tag and closing tag) should be
written as: "<xxx>      </xxx>" where xxx is the corresponding tag name and the opening and
closing tags are separated by a line-break. For example, this is relevant for empty
parameterLists.

use built in libraries and functions to handle whitespaces/line endings.
"""

import sys
import os
import re # regex

class JackTokenizer:
    """
    transforming a string of characters in to a stream of meaningful tokens
    """

    def __init(self, input_file):
        """
        :param file_text: a given text file to split into tokens.
        """
        self.index = 0
        text = ''.join(input_file.readlines())
        self.current_token = None # initially there's no current token       
        self.tokenize(text)


    def advance(self):
        """
        Advancing the input, one token at a time.
        get next token, make it the current, return it.
        
        use the grammar as guide to decide whether to appends next char or return.
        """
        if self.has_more_tokens():
            self.current_token = self.tokens[self.index].strip()
            self.index += 1

        return self.current_token


    def token_type(self):
        """
        returns the name of the token type of the token the tokenizer is pointing at
        """
        if self.key_word():
            return "keyword"
        if self.symbol():
            return "symbol"
        if self.int_val():
            return "IntegerConstant"
        if self.string_val():
            return "StringConstant"
        else: # the input is valid, so by exclusion it's true
            return "identifier" # a sequence of letters, digits, and underscore ( '_' ) not starting with a digit.


    def tokenize(self, text):
        """
        :return:
        """
        text = self.clearComments(text)
        # re.search("[a-zA-Z] ", token): # replace "" with &quot
        
        # move all strings to a separate list.
        """
        strings_list = re.findall("\".*?\"", text, re.DOTALL) # copies all strings from text
        text = re.sub("\".*?\"", " @STRING@ ", text, flags=re.DOTALL).replace("\n", " ") # replaces strings with a dummy-value
        """

        # adds spaces between all special characters.
        symbol_regex = re.compile("{|}|(|)|[|]|.|,|;|+|-|*|/|&|||<|>|=|~")
        text = symbol_regex.sub(lambda x: " " + x.group(0) + " ", text)
        tokens_list = text.split()
        
        """
        counter = 0
        #adds the strings back
        for (index, token) in enumerate(tokens_list):
            if token == "@STRING@":
                tokens_list[index] = strings_list[counter]
                counter += 1
        """
        self.tokens = tokens_list


    def getCurrentToken(self):
        return self.current_token

    def peek(self):
        """
        retrieve the next token without advancing.
        """
        if self.has_more_tokens():
            return self.tokens[self.index]
        else:
            return

    def has_more_tokens(self):
        return not self.index == len(self.tokens)


    def clearComments(self, text):
        """
        remove all comments form file, then return file
        """ 
        cleared = ""
        i = 0
        for char in text:

            # if string, jump to end and append it
            if char == "\"":
                end_index = text.index("\"", i + 1)
                cleared += text[i: end_index + 1]
                i = end_index + 1
                continue

            elif char == "/": # start of a comment

                # single-line comment: jump to end of line and remove it
                if text[i + 1] == "/":
                    sl_comment_end_index = text.index("\n", i + 1)
                    i = sl_comment_end_index + 1
                    cleared += " "
                    continue

                # multi-line comment: jump to end of comment and remove it
                if text[i + 1] == "*":
                    ml_comment_end_index = text.index("*/", i)
                    i = ml_comment_end_index + 2
                    cleared += " "
                    continue
                else:
                    cleared += char
                    i += 1
            else:
                cleared += char
                i += 1
        return cleared


    def key_word(self):
        """
        keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 'static' | 'var'
        | 'int' | 'char' | 'boolean' | 'void' | 'true' | 'false' | 'null' | 'this' | 'let'
        | 'do' | 'if' | 'else' | 'while' | 'return’
        """
        keywords_list = [ "class" , "constructor", "function", "method", "field", "static",
                        "var", "int", "char", "boolean", "void", "true", "false", "null", "this",
                        "let", "do", "if", "else", "while", "return"]
        # only for matches at the beginning of the string, unlike search
        if self.current_token in keywords_list:
            return True
        return False

    def symbol(self):
        """
        symbol: '{' | '}' | '(' | ')' | '[' | ']' | '. ' | ', ' | '; ' | '+' | '-' | '*' |
        '/' | '&' | '|' | '<' | '>' | '=' | '~'
        """
        symbols_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', ',', '<', '>', '=', '~', '|']
        return self.current_token in symbols_list

    def int_val(self):
        # integerConstant: a decimal number in the range 0 ... 32767
        int_regex = '^\d+$'
        return re.match(int_regex, self.current_token)

    def string_val(self):
        # StringConstant: '"' a sequence of Unicode characters, not including double quote or newline '"'
        string_regex = '^\".*\"$'
        return re.match(string_regex, self.current_token)


        