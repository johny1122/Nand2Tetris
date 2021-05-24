// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INFINITE_LOOP)
	//init loop
	@SCREEN 
	D=A
	@address_to_print
	M=D		//address_to_print = SCREEN base address_to_print
	@color
	M=0		// color = white
	
	@8191
	D=A		// D = 512
	@n		// n = number of rows
	M=D
	@i		// i = index in for
	M=0
	
	@KBD
	D=M
	@LOOP_BLACK
	D;JGT	//if button pressed goto LOOP_BLACK
	
	// button not pressed so print white screen
(LOOP)
	@i
	D=M
	@n
	D=D-M
	@STOP
	D;JGT	// if i > n goto STOP
	
	@color
	D=M
	
	@address_to_print
	A=M
	M=D		// change pixels to color	
	
	@i
	M=M+1	// i++

	@address_to_print
	M=M+1 	// address_to_print++	

	@LOOP	
	0;JMP
	
		
(LOOP_BLACK)
	@color
	M=-1	// color = black
	@LOOP
	0;JMP
	
(STOP)
	//@INFINITE_LOOP
	//0;JMP
	