#include <stdio.h>
#include <stdint.h>
#include <string.h>

static uint8_t ror8(uint8_t x, int r) {
    return (uint8_t)((x >> r) | (x << (8 - r)));
}

int main() {
    char buf[64];
    printf("Input: ");
    if (!fgets(buf, sizeof(buf), stdin)) {
        return 0;
    }
    buf[strcspn(buf, "\n")] = '\0';

    uint8_t key[] = { 0x01, 0x02, 0x03, 0x04, 0x05 };
    uint8_t enc[] = {
        0x3B, 0x73, 0x13, 0x1B, 0xF3, 0x81, 0x81, 0x81, 0x0B, 0x89,
        0xA1, 0xA1, 0xA1, 0x49, 0x03, 0xC9, 0xD9, 0x0B, 0x49, 0xA1,
        0x99, 0x33, 0x81, 0x49, 0x23, 0xA9, 0xB9, 0xA9, 0x49, 0x89,
        0x99, 0xA1, 0xA9, 0xA9, 0x89, 0x81, 0xA9, 0xB9, 0xA1, 0xA9,
        0x89, 0xFB
    };
    size_t len = sizeof(enc) / sizeof(enc[0]);

    if (strlen(buf) != len) {
        printf("Access denied!\n");
        return 0;
    }

    for (size_t i = 0; i < len; i++) {
        uint8_t c = (uint8_t)buf[i];
        uint8_t t = ror8(enc[i], 3) ^ key[i % 5];
        if (t != c) {
            printf("Access denied!\n");
            return 0;
        }
    }

    printf("Access granted!\n");
    return 0;
}
