// Sort.asm

	@R14
	D=M		// D = RAM[14] (start of array)
	@start_of_array
	M=D		// start_of_array = R14
	
	@R15
	D=M		// D = RAM[15] (length of array)
	@length_of_array
	M=D	// length_of_array = R15
	
	@j		// j = index in for
	M=0
	
	@element_subtract
	M=0
	
	@element1Address
	M=0

	@element1
	M=0
	
	@element2
	M=0
	
	
(OUTLOOP)
	@j
	D=M
	@length_of_array
	D=D-M
	@STOP
	D;JGE	// if j >= length_of_array goto STOP
	
	@j
	M=M+1	// j++
	
	@i
	M=0		// i = 0
	
	@INLOOP
	0;JMP
	
	

(INLOOP)
	@j
	D=M		// D = j
	@length_of_array
	D=M-D	// D = length_of_array - j
	@i
	D=M-D	// D = i - length_of_array - j
	@OUTLOOP
	D;JGE	// if j >= length_of_array - j - i goto OUTLOOP
	
	@start_of_array
	D=M
	@i
	D=D+M	// D = address of array[i]
	
	@element1Address
	M=D		// element1Address = address of array[i]
	
	A=D
	D=M		// D = array[i]
	
	@element_subtract
	M=D		// element_subtract = array[i]
	
	@element1Address
	D=M+1	// D = address of array[i+1]
	
	A=D		// A = address of array[i+1]
	D=M		// D = array[i+1]
	
	@element_subtract
	M=M-D	// element_subtract = element_subtract - array[i+1] (element_subtract = array[i]-array[i+1])
	D=M		
	
	@i
	M=M+1	// i++
	
	@IF_LEFT_ELEMENT_SMALLER
	D;JLT	// if array[i] < array[i+1] goto IF_LEFT_ELEMENT_SMALLER
	
	@INLOOP
	0;JMP	
	
	
(IF_LEFT_ELEMENT_SMALLER)
	@element1Address
	D=M		// D = address of array[i]
	A=D
	D=M		// D = array[i]
	@element1
	M=D		// element1 = array[i]
	
	@element1Address
	D=M+1	// D = address of array[i+1]
	A=D
	D=M		// D = array[i+1]
	@element2
	M=D		// element2 = array[i+1]
	D=M
	
	@element1Address
	A=M		// D = address of array[i]
	M=D		// array[i] = array[i+1]
	
	@element1
	D=M		// D = array[i]
	@element1Address
	A=M+1	// D = address of array[i+1]
	M=D		// array[i+1] = array[i]
	
	@INLOOP
	0;JMP
	
	
(STOP)
