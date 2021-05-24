class VMWriter:
    """
    """
    def __init(self):
    """
    create new output .vm file and preparess it for writing
    """

    def writePush(self, segment, index):
    """
    writes a VM push command
    know to which segment, and the index we want to effect

    segment can be: CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP

    "this routine is trivial"
    """


    def writePop(self, segment, index):
        """
        writes a VM pop command
        also trivial
        """


    def writeArithmetic(self, command):
        """
        command can be: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        """

    def writeLabel(self, label):
        """
        writes a VM label command
        """

    def writeGoto(self, label):
        """
        writes a VM goto command
        """

    def writeif(self, label):
        """
        writes a VM if-goto command

        slide 26:
source code
if (expression)
statements1
else
statements2
...

compiled (expression)
not
if-goto L1
compiled (statements1)
goto L2
label L1
compiled (statements2)
label L2
...
        """

    def writecall(self, label):
        """
        writes a VM call command

        slide 9:





        """

    def writeFunction(self, label):
        """
        writes a VM function command
        """

    def writeReturn(self, label):
        """
        writes a VM return command
        """

    def close(self):
        """
        closes the output file
        """


"""
me{thod int bar(int a1; int a2)
var int v1, v2, v3;
...
let c = a2 + (x – v3);
...
}
...
}
Variables
VM code (pseudo)
...
// let c = a2 + (x – v3)
push a2
push x
push v3
sub
add
pop c
...
...
push argument 1
push static 0
push local 2
sub
add
pop this 2

slide 21:
The Jack language definition specifies no operator priority;
The Jack language definition specifies that expressions in parentheses are evaluated first
let x = a + (b * c); compiler
push a
push b
push c
*
+
pop x







slide 105: are related to the function call-and-return contract.
pop temp 0 # a void method (printInt) pops to temp 0, since we don't need a return value (we throw it away)
push constant 0 # any function, including void function (main), must return *some* value.





    