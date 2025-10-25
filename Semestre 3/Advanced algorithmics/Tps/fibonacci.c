#include <stdio.h>

long long fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main() {
    int num;

    printf("Enter a non-negative number: ");
    if (scanf("%u", &num) != 1) {
        printf("Invalid input.\n");
        return 1;
    }

    printf("\n--- Fibonacci of %u ---\n", num);
    printf("Iterative: %llu\n", fibonacci(num));
    
    return 0;
}