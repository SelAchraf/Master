#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int binaryToDecimal(unsigned long long n) {
    if (n == 0) {
        return 0;
    } 
    else {
        return (n % 10) + 2 * binaryToDecimal(n / 10);
    }
}

int main() {
    unsigned long long binaryInput;

    printf("--- Binary to Decimal Converter ---\n");
    printf("Enter a binary number: ");

    if (scanf("%llu", &binaryInput) != 1) {
        printf("Error: Invalid input.\n");
        return 1;
    }
    
    int decimal = binaryToDecimal(binaryInput);

    printf("\nBinary:   %llu\n", binaryInput);
    printf("Decimal: %d\n", decimal);

    return 0;
}