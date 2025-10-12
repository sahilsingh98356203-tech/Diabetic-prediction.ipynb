# Smart Calculator - C++ 

A beautiful C++ calculator with an enhanced console UI featuring a white and light blue color scheme.

## Features

- **Modern UI**: Clean interface with white and light blue color theme
- **Multiple Operations**: 
  - Basic arithmetic (addition, subtraction, multiplication, division)
  - Advanced operations (power, square root, sine, cosine, modulo)
- **Error Handling**: Comprehensive error checking with user-friendly messages
- **Input Validation**: Robust input validation for all user inputs
- **Interactive Menu**: Easy-to-use menu system with visual feedback

## Compilation

### Using Make (Recommended)
```bash
make
```

### Manual Compilation
```bash
g++ -std=c++17 -Wall -Wextra -O2 -o calculator calculator.cpp
```

## Running the Calculator

### Using Make
```bash
make run
```

### Direct Execution
```bash
./calculator
```

## Operations Supported

1. **Addition (+)**: Add two numbers
2. **Subtraction (-)**: Subtract two numbers
3. **Multiplication (*)**: Multiply two numbers
4. **Division (/)**: Divide two numbers (with zero-division protection)
5. **Modulo (%)**: Find remainder of division
6. **Power (^)**: Raise first number to the power of second
7. **Square Root (√)**: Calculate square root of a number
8. **Sine (sin)**: Calculate sine of angle in radians
9. **Cosine (cos)**: Calculate cosine of angle in radians

## Color Scheme

- **Primary**: Light Blue (#94B3FD)
- **Secondary**: White (#FFFFFF)
- **Accent**: Cyan (#00FFFF)
- **Background**: Light Blue background for headers
- **Error**: Red for error messages

## Requirements

- C++17 compatible compiler (g++, clang++)
- Terminal with ANSI color support
- Unix-like system (macOS, Linux) or Windows with proper terminal

## Clean Up

To remove compiled files:
```bash
make clean
```

## Example Usage

```
Choose an operation (0-9): 1
Enter first number: 15.5
Enter second number: 4.2
RESULT: 19.700000
```

Enjoy calculating with style! 🧮✨
