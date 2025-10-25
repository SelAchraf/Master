#include <stdio.h>

unsigned int ackermann(unsigned int m, unsigned int n) {
    if (m == 0) {
        // Rule 1 Ackermann(0, n) = n + 1
        return n + 1;
    } else if (n == 0) {
        // Rule 2 Ackermann(m, 0) = Ackermann(m - 1, 1)
        return ackermann(m - 1, 1);
    } else {
        // Rule 3 Ackermann(m, n) = Ackermann(m, Ackermann(m, n - 1))
        return ackermann(m - 1, ackermann(m, n - 1));
    }
}

int main() {
    unsigned int m, n;

    printf("Enter two non-negative integers (m n): ");
    scanf("%u %u", &m, &n);

    // Add a warning due to the function's rapid growth
    printf("\nCalculating Ackermann(%u, %u)...\n", m, n);

    unsigned int result = ackermann(m, n);
    
    printf("Result: %u\n", result);
    
    return 0;
}