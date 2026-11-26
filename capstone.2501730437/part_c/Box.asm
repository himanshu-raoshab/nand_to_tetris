// Box.asm | Roll no. 2501730437 | K=37
// Required box: starts at row 37, height 20 rows, width 32 pixels (2 words).
// Draw while a key is pressed; clear when no key is pressed.

(START)
    @KBD
    D=M
    @DRAW
    D;JNE
    @CLEAR
    0;JMP

(DRAW)
    @17568
    D=A
    @R13
    M=D
    @20
    D=A
    @R14
    M=D
(DRAW_LOOP)
    @R13
    A=M
    M=-1
    A=A+1
    M=-1
    @32
    D=A
    @R13
    M=D+M
    @R14
    MD=M-1
    @DRAW_LOOP
    D;JGT
    @START
    0;JMP

(CLEAR)
    @17568
    D=A
    @R13
    M=D
    @20
    D=A
    @R14
    M=D
(CLEAR_LOOP)
    @R13
    A=M
    M=0
    A=A+1
    M=0
    @32
    D=A
    @R13
    M=D+M
    @R14
    MD=M-1
    @CLEAR_LOOP
    D;JGT
    @START
    0;JMP
