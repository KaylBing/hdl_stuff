@2
D=A
@i    // i refers to some mem. location
M=D    // i = 2
@sum    // sum refers to some mem. location
M=0    // sum = 0

(LOOP)
    @i
    D=M    // D = i
    @50
    D=D-A
    @END
    D;JGT    // If (i-50) > 0 goto END
    @i
    D=M    // D=i
    @sum
    M=D+M    // sum=sum+i
    @2
    D=A
    @i
    M=D+M    // i=i+1
    @LOOP
    0;JMP    //Goto LOOP
(END)
    @END
    0;JMP
