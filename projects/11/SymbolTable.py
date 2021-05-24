class SymbolTable:
    def __init():

    def start_subroutine(self):
        """
        starts a new subroutine scope
        """
        self.running_index = 0

    def define(name, type, kind):
        """
         String name, String type, STATIC/FIELD/ARG/VAR kind
         
         give each variable a running index.
         """

    def varCount(kind):
        """
        returns the number of variables of the given kind already defined in the current
        """
        return self.getVarIndex(kind)
         
    def kindOf(name):
        if:
            return kind
        else: return NONE # requirement: return NONE

    
    def typeOf(name):
        """
        * in the current scope
        """
        # suggestion by shimon shocken: two separate hash tables: one for the class scope, and one for the subroutine scope
        # when start compiling a new subroutine, the latter hash table can be reset.
        return type
        
 
    def indexOf(name):
        return index # in the same data structure as typeOf


"""
When compiling an error-free Jack code, each symbol not found in the symbol tables
can be assumed to be either a subroutine name or a class name

symbol table:
1. output the identifier's category: var(=local), argument, static, field, class, subroutine.
2. if the identifier’s category is var, argument, static, field, output also the
running index assigned to this variable in the symbol table
3.output whether the identifier is being defined (g var jeck command), or being used (eg evaluating an expression).
implementation: extend the syntax analyzer (developed in project 01) with the identifier
handling described above (use your own output/tags format). (not for submission, test using the tests of proj 10)

the syntax analyzer understands the semantics of the jack language.
"""

