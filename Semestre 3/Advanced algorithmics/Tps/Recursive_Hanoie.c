#include <stdio.h>

void towerOfHanoi(int n, char from_rod, char to_rod, char aux_rod) {
    if (n == 1) {
        printf("Move disk 1 from rod %c to rod %c\n", from_rod, to_rod);
        return;
    }
    
    // Step 1:
    towerOfHanoi(n - 1, from_rod, aux_rod, to_rod);
    
    // Step 2:  
    printf("Move disk %d from rod %c to rod %c\n", n, from_rod, to_rod);
    
    // Step 3:
    towerOfHanoi(n - 1, aux_rod, to_rod, from_rod);
}

int main() {
    int n;

    printf("Enter the number of disks: ");
    scanf("%d", &n);
    
    printf("\nThe sequence of moves involved in the Tower of Hanoi are:\n");
    towerOfHanoi(n, 'A', 'C', 'B'); 
    
    return 0;
}