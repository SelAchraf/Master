#include <stdio.h>

unsigned long long fibonacciIterative(unsigned int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;

    unsigned long long a = 0;
    unsigned long long b = 1;
    unsigned long long next;

    for (unsigned int i = 2; i <= n; i++) {
        next = a + b;
        a = b;
        b = next;
    }
    return b;
}

int main() {
    unsigned int num;

    printf("Enter a non-negative number: ");
    if (scanf("%u", &num) != 1) {
        printf("Invalid input.\n");
        return 1;
    }

    printf("\n--- Fibonacci of %u ---\n", num);
    printf("Iterative: %llu\n", fibonacciIterative(num));
    
    return 0;
}