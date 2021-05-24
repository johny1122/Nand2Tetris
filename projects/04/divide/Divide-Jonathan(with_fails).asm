// Divide.asm

	// R13/R14 = number/divide
	
	@R13
	D=M		// D = RAM[13]
	@number
	M=D		// number = RAM[13]

	@R14
	D=M		// D = RAM[14]
	@divide
	M=D		// divide = RAM[14]
	
	@R15
	M=0		// answer = 0
	
	@temp_answer
	M=1		// temp_answer = 1
	
	@counter
	M=0		// counter = 0

	
(LOOP) // if number is biggen than divide jump to END
	@number
	D=M
	
	@divide
	D=D-M	// D =  number - divide
	
	@END
	D;JLT
	
(DIVIDELOOP)
	@number
	D=M
	
	@divide
	D=D-M
	
	@IF_NEGATIVE
	D;JLE
	
	@divide
	M=M<<

	@counter
	M=M+1
	
	@DIVIDELOOP
	0;JMP
	
(IF_NEGATIVE)
	@counter
	M=M-1
	D=M
	
	@END_COUNT
	D;JLE
	
	@temp_answer
	M=M<<
	
	@counter
	@IF_NEGATIVE
	0;JMP
	
(END_COUNT)
	@temp_answer
	D=M
	
	@R15
	M=M+D
	
	@divide
	D=M>>
	
	@number
	M=M-D
	
	// reset:
	@R14
	D=M
	
	@divide
	M=D
	
	@temp_answer
	M=1
	
	@LOOP
	0;JMP
	
(END)

