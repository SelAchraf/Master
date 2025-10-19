#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int binaryToDecimalIterative(unsigned long long n) {
    int decimalResult = 0;
    int base = 1; // Represents (2^0)

    while (n > 0) {
        int lastDigit = n % 10;
        
        n = n / 10;
        
        decimalResult += lastDigit * base;
        
        base = base * 2;
    }
    
    return decimalResult;
}

int main() {
    unsigned long long binaryInput;

    printf("--- Binary to Decimal Converter ---\n");
    printf("Enter a binary number: ");

    if (scanf("%llu", &binaryInput) != 1) {
        printf("Error: Invalid input.\n");
        return 1;
    }

    int decimal = binaryToDecimalIterative(binaryInput);

    printf("\nBinary:   %llu\n", binaryInput);
    printf("Decimal: %d\n", decimal);

    return 0;
}