#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int decimalToBinaryIterative(unsigned int n) {
    int binaryResult = 0;
    int place = 1;

    if (n == 0) {
        return 0;
    }

    while (n > 0) {
        binaryResult += (n % 2) * place;

        place *= 10;
        
        n /= 2;
    }

    return binaryResult;
}

int main() {
    unsigned int decimalInput;

    printf("--- Iterative Decimal to Binary Converter ---\n");
    printf("Enter a number: ");

    if (scanf("%u", &decimalInput) != 1) {
        printf("Error: Invalid input.\n");
        return 1;
    }

    int binaryResult = decimalToBinaryIterative(decimalInput);

    printf("Decimal: %u\n", decimalInput);
    printf("Binary:  %d\n", binaryResult);

    return 0;
}