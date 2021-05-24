# %%
# input: fileName.jack or directoryName
# output: .xml file for each jack file
# xml library:  Lxml
# We will use diff -w to compare your files, which ignores whitespaces. 
"""
Unit 10.7: The Jack Analyzer
unit test by generating xml code.
textual parse tree according to the Jack grammar.
variable names don't generate markup. 

Unit 10.9: Building a Syntax Analyzer
load the xml file into an internet browser

Unit 10.10: Perspective
we used top-down parsing (simpler than bottom-up parsing)
"""

import sys
import re
import os
import lxml
import re # regex
import CompilationEngine



def main():
    """
    Program structure:
    A Jack program is a collection of classes, each appearing in a separate file.
    The compilation unit is a class.
    """

    jack_files_list = []
    
    if file:
        
        jack_files_list.append(arg_string)
    else:
        for a_file in directory:
            jack_files_list.append(arg_string)
            compile_class(a_file)

    
    
    
    for jack_address in jack_files_list:
        engine = CompilationEngine(my_file)
        engine.run()
        
        
    return


if __name__ == "__main__":
    main()

"""
if os.path.isdir(arg_string):  # if argument is directory
        for file in os.listdir(arg_string):
            print("file found: ", file)
            if file.endswith(".jack"):
                if os.name == 'nt':  # if on windows
                    jack_files_list.append(arg_string + '\\' + file)
                else:  # on linux
                    jack_files_list.append(arg_string + '/' + file)

arg_string = os.path.abspath(sys.argv[1])
    if not os.path.exists(arg_string):
        sys.exit(1)
        
    if not sys.argv[1].endswith('.jack'):
            print("USAGE: unsupported file type")
            sys.exit(1)  

"""
