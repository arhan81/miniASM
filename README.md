# MiniASM — Two-Pass Assembler

A Two-Pass Assembler built in Python with a Flask web GUI.

## What it does
Converts MiniASM assembly language into machine code using a two-pass assembly process.
- **Pass 1** — builds the symbol table and intermediate representation
- **Pass 2** — resolves symbols and generates machine code

## Supported Instructions
| Instruction | Description |
|-------------|-------------|
| `LOAD Rx, (label)` | Load value from memory into register |
| `STORE Rx, (label)` | Store register value into memory |
| `ADD Rx, Ry` | Add two registers |
| `SUB Rx, Ry` | Subtract two registers |
| `HALT` | Stop execution |

## Run Locally
```bash
pip install flask
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## Project Structure
```
miniASM/
├── app.py                  # Flask web server
├── main.py                 # CLI runner
├── miniasm_assembler.py    # Core assembler logic (two-pass)
├── sample_program.asm      # Sample assembly program
├── myprogram.asm           # Another sample program
├── test_samples.py         # Test cases
└── templates/
    └── index.html          # Web GUI
```

## Tech Stack
- **Python** — core language
- **Flask** — web framework
- **HTML / CSS / JavaScript** — frontend GUI
