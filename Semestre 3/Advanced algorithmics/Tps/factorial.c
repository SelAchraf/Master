#include <stdio.h>

unsigned long long factorial(unsigned int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int main() {
    unsigned int num;

    printf("Enter a non-negative number: ");
    if (scanf("%u", &num) != 1) {
        printf("Invalid input.\n");
        return 1;
    }

    printf("\n--- Factorial of %u ---\n", num);
    printf("Result: %llu\n", factorial(num));

    return 0;
}