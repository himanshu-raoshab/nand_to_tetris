#!/usr/bin/env python3
"""Hack assembler for Nand to Tetris. Roll number: 2501730437 (K=37).
Extra feature: K mod 3 = 1 -> report invalid instructions with source line numbers.
Usage: python assembler.py Box.asm
"""
import sys
from pathlib import Path

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    **{f"R{i}": i for i in range(16)},
    "SCREEN": 16384, "KBD": 24576
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
COMP = {
    "0":"0101010", "1":"0111111", "-1":"0111010",
    "D":"0001100", "A":"0110000", "M":"1110000",
    "!D":"0001101", "!A":"0110001", "!M":"1110001",
    "-D":"0001111", "-A":"0110011", "-M":"1110011",
    "D+1":"0011111", "A+1":"0110111", "M+1":"1110111",
    "D-1":"0001110", "A-1":"0110010", "M-1":"1110010",
    "D+A":"0000010", "D+M":"1000010", "D-A":"0010011",
    "D-M":"1010011", "A-D":"0000111", "M-D":"1000111",
    "D&A":"0000000", "D&M":"1000000", "D|A":"0010101",
    "D|M":"1010101"
}

class AssemblyError(Exception):
    pass

def is_valid_symbol(name):
    """Return True if name follows Hack symbol rules (letters, digits, _ . $ :, not starting with a digit)."""
    return bool(name) and not name[0].isdigit() and all(ch.isalnum() or ch in "_.$:" for ch in name)

def clean_source(source):
    instructions = []
    for line_no, raw in enumerate(source.splitlines(), 1):
        code = raw.split("//", 1)[0].strip()
        if code:
            instructions.append((line_no, code))
    return instructions

def assemble(source):
    lines = clean_source(source)
    symbols = dict(PREDEFINED)
    rom = 0

    # Pass 1: collect labels and their ROM addresses.
    for line_no, code in lines:
        if code.startswith("(") and code.endswith(")"):
            label = code[1:-1].strip()
            if not is_valid_symbol(label):
                raise AssemblyError(f"Line {line_no}: invalid label declaration")
            if label in symbols:
                raise AssemblyError(f"Line {line_no}: duplicate or reserved label '{label}'")
            symbols[label] = rom
        else:
            rom += 1

    # Pass 2: encode instructions and allocate variables from RAM[16].
    output = []
    next_variable = 16
    for line_no, code in lines:
        if code.startswith("(") and code.endswith(")"):
            continue
        try:
            if code.startswith("@"):
                value = code[1:].strip()
                if not value:
                    raise ValueError("missing A-instruction value")
                if value.isdigit():
                    number = int(value)
                elif value in symbols:
                    number = symbols[value]
                else:
                    if not is_valid_symbol(value):
                        raise ValueError(f"invalid symbol '{value}'")
                    number = next_variable
                    symbols[value] = number
                    next_variable += 1
                if not 0 <= number <= 32767:
                    raise ValueError("A-instruction value must be between 0 and 32767")
                output.append(format(number, "016b"))
                continue

            if code.count("=") > 1 or code.count(";") > 1:
                raise ValueError("malformed C-instruction")
            if "=" in code:
                dest, rest = code.split("=", 1)
            else:
                dest, rest = "", code
            if ";" in rest:
                comp, jump = rest.split(";", 1)
            else:
                comp, jump = rest, ""
            dest, comp, jump = dest.strip(), comp.strip(), jump.strip()
            if dest not in DEST:
                raise ValueError(f"invalid destination '{dest}'")
            if comp not in COMP:
                raise ValueError(f"invalid computation '{comp}'")
            if jump not in JUMP:
                raise ValueError(f"invalid jump '{jump}'")
            output.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
        except (ValueError, KeyError) as exc:
            raise AssemblyError(f"Line {line_no}: invalid instruction '{code}': {exc}") from None
    return output, symbols

def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <input.asm>")
        sys.exit(2)
    source_path = Path(sys.argv[1])
    if not source_path.is_file():
        print(f"Error: file not found: {source_path}")
        sys.exit(1)
    try:
        machine_code, symbols = assemble(source_path.read_text(encoding="utf-8"))
    except AssemblyError as exc:
        print(exc)
        sys.exit(1)
    output_path = source_path.with_suffix(".hack")
    output_path.write_text("\n".join(machine_code) + "\n", encoding="utf-8")
    print(f"Success: wrote {len(machine_code)} instructions to {output_path}")
    print("Personal feature active: invalid instructions report their source line number (K mod 3 = 1).")

if __name__ == "__main__":
    main()
