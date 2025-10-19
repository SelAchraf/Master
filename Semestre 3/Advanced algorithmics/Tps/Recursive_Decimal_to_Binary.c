#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int decimalToBinaryRecursive(int n) {
    if (n == 0) {
        return 0;
    }
    else {
        return (n % 2) + 10 * decimalToBinaryRecursive(n / 2);
    }
}

int main() {
    int decimalInput;

    printf("--- Recursive Decimal to Binary Converter ---\n");
    printf("Enter a number: ");

    if (scanf("%d", &decimalInput) != 1) {
        printf("Error: Invalid input.\n");
        return 1;
    }

    int binaryResult = decimalToBinaryRecursive(decimalInput);

    printf("Decimal: %d\n", decimalInput);
    printf("Binary:  %d\n", binaryResult);

    return 0;
}