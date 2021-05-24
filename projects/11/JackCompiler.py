class JackCompiler:
    """
    input: fileName.jack or directoryName
    output: .vm file for each .jack file

    for each jack file create a jackTokenizer, an a .vm file
    uses SymbolTable, CompilationEngine and VMWriter to write to the .vm file
    
    we never need more than two symbol tables, since we reset it at each new class, and at each new subroutine. thus 2 instances only.



    unit testing using the test programs. for each compile its directory, then look at generated code,(if OK) then load to VM emulator, run it.
    
    """

    