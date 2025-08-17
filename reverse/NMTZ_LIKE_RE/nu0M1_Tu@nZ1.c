#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <tlhelp32.h>

void anti_debug() {
    if (IsDebuggerPresent()) {
        printf("Debugger detected! Exiting...\n");
        exit(1);
    }

    BOOL isDebugged = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &isDebugged);
    if (isDebugged) {
        printf("Remote Debugger detected! Exiting...\n");
        exit(1);
    }

    typedef NTSTATUS(WINAPI *pNtQueryInformationProcess)(HANDLE, UINT, PVOID, ULONG, PULONG);
    pNtQueryInformationProcess NtQueryInformationProcess = (pNtQueryInformationProcess)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtQueryInformationProcess");
    if (NtQueryInformationProcess) {
        DWORD debugPort = 0;
        NTSTATUS status = NtQueryInformationProcess(GetCurrentProcess(), 7, &debugPort, sizeof(DWORD), NULL);
        if (status == 0 && debugPort != 0) {
            printf("Debugger detected via NtQueryInformationProcess! Exiting...\n");
            exit(1);
        }
    }

    CONTEXT ctx;
    memset(&ctx, 0, sizeof(CONTEXT));
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    if (GetThreadContext(GetCurrentThread(), &ctx)) {
        if (ctx.Dr0 || ctx.Dr1 || ctx.Dr2 || ctx.Dr3 || ctx.Dr6 || ctx.Dr7) {
            printf("Debugger detected via Debug Registers! Exiting...\n");
            exit(1);
        }
    }

    HWND hConsole = GetConsoleWindow();
    ShowWindow(hConsole, SW_HIDE);
}

// 右移函数
unsigned char ror(unsigned char val, int r) {
    return ((val >> r) | (val << (8 - r))) & 0xFF;
}

int main() {
    anti_debug();
    unsigned char encrypted_flag[41] = {
        0xf8, 0xd0, 0xe0, 0x98, 0x40, 0xb7, 0x78, 0x5a, 0xd8, 0x6f,
        0x72, 0xe8, 0x77, 0x28, 0x07, 0xb8, 0xe8, 0x47, 0x8a, 0xe0,
        0x72, 0x88, 0xf0, 0x7f, 0xc8, 0x62, 0xe8, 0xaf, 0x57, 0x8a,
        0x08, 0x8a, 0x90, 0x80, 0xe0, 0xdf, 0x8f, 0xa7, 0x7a, 0x78, 0x50
    };
    unsigned char decrypted_flag[42] = {0};
    int len = 41;
    int dkey = 0x5A;

    for (int i = 0; i < len; i++) {
        unsigned char val = encrypted_flag[i];
        val = (val - 0x17) & 0xFF;
        val = ror(val, 3);
        val ^= dkey;
        val = (val - (i % 5)) & 0xFF;
        decrypted_flag[i] = val;
    }
    decrypted_flag[len] = '\0';
    char input[128] = {0};
    printf("Enter the password: ");
    fflush(stdout);
    if (fgets(input, sizeof(input), stdin) == NULL) {
        printf("Wrong!\n");
        exit(1);
    }
    input[strcspn(input, "\n")] = '\0';

    if (strcmp((char *)decrypted_flag, input) == 0) {
        printf("%s\n", decrypted_flag);
    } else {
        printf("Wrong!\n");
    }

    return 0;
}
