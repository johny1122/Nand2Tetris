// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R0
	D=M		// D = RAM[0]
	@n
	M=D		// n = R0
	@i
	M=1 	// i = 1
	@mult
	M=0		// mult = 0
	@R2		
	M=0		// R2 = 0
	
(LOOP)
	@i
	D=M
	@n
	D=D-M
	@STOP
	D;JGT	// if i > n goto STOP
	
	@R1
	D=M		// D = RAM[1]
	@mult
	M=M+D	// mult
	
	@i
	M=M+1	// i++
	
	@LOOP
	0;JMP
	
(STOP)
	@mult
	D=M
	@R2
	M=D		// save result: RAM[2] = mult
	
(END)
	//@END
	//0;JMP
	