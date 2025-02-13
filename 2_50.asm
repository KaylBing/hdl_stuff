// Initialize variables
@sum    // sum = 0
M=0
@i      // i = 2 (first even number)
M=2

(LOOP)
@i      // Load i
D=M
@50     // Load 50
D=D-A   // D = i - 50
@END    // If i > 50, jump to END
D;JGT

@i      // Load i
D=M
@sum    // Load sum
M=D+M   // sum = sum + i

@i      // Load i
M=M+2   // i = i + 2 (next even number)

@LOOP   // Repeat loop
0;JMP

(END)
@END    // Infinite loop to end program
0;JMP
