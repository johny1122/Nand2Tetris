@result
M = 0

@R14
D = M
@divisor
M = D

@R13
D = M
@dividend
M = D

// if divident is smaller than divisor
@R15
M=0
@tempResult
M=D
@R14
D=M
@tempResult
D=M-D
@END
D ; JLT


(OUTERLOOP) // while dividend \geq divisor
// tempDivisor = divisor
@divisor
D = M
@tempDivisor
M = D

@tempResult
M = 1


(INNERLOOP) // while dividend \geq tempDivisor
@tempDivisor
M = M<<
@tempResult
M = M<<


// if dividend \geq tempDivisor GOTO INNERLOOP
@dividend
D = M
@tempDivisor
D = D - M
@INNERLOOP
D ; JGE

// dividend -= tempDivisor
@tempDivisor
M = M>>
(NEGATIVE)
@tempDivisor
M = -M // if tempDivisor < 0
D = M
@NEGATIVE
D ; JLT
@tempDivisor
D = M
@dividend
M = M - D

// result += tempResult
@tempResult
M = M>>
D = M
@result
M = M + D


// if dividend \geq divisor GOTO OUTERLOOP
@dividend
D = M
@divisor
D = D - M
@OUTERLOOP
D ; JGE

@result
D = M
@R15
M = D

(END)
@END
0 ; JMP
