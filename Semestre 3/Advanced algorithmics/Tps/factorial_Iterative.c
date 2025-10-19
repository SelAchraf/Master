#include <stdio.h>

unsigned long long factorialIterative(unsigned int n) {
    unsigned long long result = 1;
    for (unsigned int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    unsigned int num;

    printf("Enter a non-negative number: ");
    if (scanf("%u", &num) != 1) {
        printf("Invalid input.\n");
        return 1;
    }

    printf("\n--- Factorial of %u ---\n", num);
    printf("Result: %llu\n", factorialIterative(num));

    return 0;
}