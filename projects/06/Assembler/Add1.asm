// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/add/Add.asm

// Computes R0 = 2 + 3  (R0 refers to RAM[0])

//@2
//(Hello)
//D=A
//@3		 // D = second number
//D=D+A
//@0
D*A
D>>     // try
D=M<<
A>>;JGE     // test
D*M
M=A<<;JMP
// M=D  // test