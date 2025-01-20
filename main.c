#include <stdint.h>
#include <stdio.h>

extern void E_(uint16_t *data0, uint16_t *data1);

int main() {
    uint16_t data0[1];
    uint16_t data1[1] = {17948};  // 17948 = 0x461c = 9984 in bf16  0x461c0000 in float32 is 9984
    printf("Input: %x\n", data1[0]);

    // Call the LLVM compiled function
    E_(data0, data1);

    // Print the result
    printf("Result: %x\n", data0[0]);

    return 0;
}