#include <stdio.h> // Required for printf

// Function declaration:
// Based on the name 'print3Zeroes' and its call signature 'print3Zeroes()',
// it is inferred to be a function that prints three zeroes and takes no arguments.
// As it's a printing function, it's expected to have a void return type.
void print3Zeroes();

int main() {
    print3Zeroes();
    return 0; // Added return 0 for good practice in main
}

// Function definition:
// Implements the logic to print three zeroes.
void print3Zeroes() {
    printf("000\n"); // Prints "000" followed by a newline
}