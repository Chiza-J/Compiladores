#include <stdio.h>

int main() {
    int x = 0;
    double t1;
    double t2;

    x = 10;
    t1 = x + 1;
    x = t1;
    t2 = x < 15;
    if (t2) goto L1;
    goto L2;
    L1:
    printf("%g\n", (double)(x));
    L2:

    return 0;
}