(BEGIN)
        // Set keyboard to address for keyboard input value.
        @24576
        D=A
        @keyboard
        M=D

(MAIN_LOOP)
        // Fill the screen with black.
        @fillvalue
        M=-1
        @FILL_SCREEN
        0;JMP

(FILL_SCREEN)
        // Set current to last screen pixel map.
        @24575
        D=A
        @current
        M=D

(DRAW)
        // Fill or clear current pixel, depending on fillvalue.
        @fillvalue
        D=M
        @current
        A=M
        M=D

        // If current pixel map is first pixel map, jump to DELAY.
        @current
        D=M
        @16384
        D=D-A
        @DELAY
        D;JLE

        // Decrement current pixel map.
        @current
        M=M-1

        // Continue drawing next pixel map.
        @DRAW
        0;JMP

(DELAY)
        // Delay loop to slow down the screen updates.
        @delay_counter
        M=0
(DELAY_LOOP)
        @delay_counter
        M=M+1
        D=M
        @10000              // Adjust this value for faster/slower delay.
        D=D-A
        @DELAY_LOOP
        D;JLT

        // Toggle fillvalue between black and white.
        @fillvalue
        D=M
        @TOGGLE_WHITE
        D;JNE
(TOGGLE_BLACK)
        @fillvalue
        M=-1
        @MAIN_LOOP
        0;JMP
(TOGGLE_WHITE)
        @fillvalue
        M=0
        @MAIN_LOOP
        0;JMP
