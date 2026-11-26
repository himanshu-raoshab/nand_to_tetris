# CAPSTONE PROJECT REPORT
## Make the Computer Draw a Box
**Course:** Nand to Tetris – I (ETCCNT301)  
**University:** School of Engineering & Technology, K.R. Mangalam University  
**Student Name:** __________________________  
**Roll Number:** 2501730437  
**Personal Number:** K = 37  

---

## 1. Aim
The aim of this capstone is to make the Hack computer display a black rectangular box on the screen while a key is pressed and remove the box when the key is released. The project combines the Hack hardware platform, a Python assembler, and a Hack assembly program.

## 2. Personal calculation and required dimensions
The personal number is the last two digits of roll number 2501730437, so K = 37. Therefore K mod 3 = 1, which selects the assembler feature that prints a clear error message with the source line number for an invalid instruction. Also, K mod 4 = 1. The box width is 16 × ((K mod 4)+1) = 16 × 2 = 32 pixels. Its height is 20 rows and its first row is row 37.

The Hack screen begins at memory address SCREEN = 16384. Each screen row contains 32 words, and each word represents 16 horizontal pixels. Therefore, the first word of row 37 is 16384 + (32 × 37) = 17568. Two consecutive words are written for each row to create a 32-pixel-wide box.

## 3. Part A — Build the computer
The Hack computer is composed of the CPU, Memory, and Computer chips. The CPU executes instructions and contains the ALU, registers, and program counter. Memory provides access to RAM, screen memory, and the keyboard-mapped memory. Computer connects the CPU, memory, and instruction ROM.

**Files:** CPU.hdl, Memory.hdl, Computer.hdl, together with the dependent chips used in the lab.

**Test evidence to insert:**  
- [Insert screenshot: CPU.tst passing]  
- [Insert screenshot: Memory.tst passing]  
- [Insert screenshot: ComputerAdd.tst passing]  
- [Insert screenshot: ComputerMax.tst passing]  
- [Insert screenshot: ComputerRect.tst passing]

Only describe tests as passed after running them in the Hardware Simulator. If a built-in chip is used instead of an earlier lab chip, identify it here as required by the assignment.

## 4. Part B — Python assembler
The assembler converts Hack assembly instructions (`.asm`) into 16-bit machine instructions (`.hack`). It uses two passes. In the first pass it removes comments and blank lines, counts ROM instructions, and records label addresses. In the second pass it translates A-instructions and C-instructions into binary. New variables are assigned RAM addresses beginning at 16.

The assembler supports the predefined Hack symbols, destination fields, computation fields, and jump fields. The K-specific feature is line-numbered error reporting. For example, an invalid computation on source line 2 produces a message identifying line 2 and the invalid instruction instead of an unhandled exception.

**Test evidence to insert:** Run the assembler on Add.asm, Max.asm, Rect.asm, and Pong.asm and compare its output with the official assembler. Insert screenshots or a comparison table showing the result. Also insert the invalid-line test screenshot.

## 5. Part C — Box program
The Box.asm program continuously checks the keyboard-mapped address KBD. If a key is pressed, it writes -1 to two consecutive screen words for each of 20 rows. If no key is pressed, it writes 0 to the same locations. The pointer begins at address 17568 and advances by 32 words after each row. The loop counter ensures exactly 20 rows are processed.

**Insert screenshot:** CPU Emulator displaying the box while a key is pressed.  
**Insert screenshot:** CPU Emulator after the key is released and the box is cleared.

## 6. Mistake fixed
During development, the screen starting address needed careful calculation. A common mistake is to add the row number directly to SCREEN. However, each row contains 32 words, so row 37 starts at SCREEN + 32×37 = 17568. I corrected the starting address and used a 32-word stride between rows. This ensures the rectangle appears at the required vertical position rather than in an incorrect screen location.

## 7. Conclusion
This capstone demonstrates the connection between the Hack computer architecture, assembly language, and machine code. The Python assembler translates symbolic instructions into binary instructions, while the assembly program interacts with memory-mapped keyboard and screen locations to draw and clear a rectangle. The personal parameters derived from roll number 2501730437 are applied to the assembler feature and box dimensions.

**Note:** Complete the screenshot evidence and verify all official tests before final submission.
