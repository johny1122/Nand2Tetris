@JUMP_START		//jump to start
0;JMP

(eq)			//functions
@R2
M=1				
@R14
A=M
0;JMP

(JUMP_START)	//start calling a function
@Jump_1
D=A
@R14
M=D
@eq
0;JMP

(Jump_1)		//after a function
@R1
M=1