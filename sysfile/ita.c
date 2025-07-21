#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdint.h>

typedef uint64_t u64;
typedef uint32_t u32;

#define ADD_ANY 0xbeef
#define DEL_ANY 0x2333

struct in_args {
    u64 addr;
    u64 size;
    char *buf;
};

void sh(int signo) {
    printf("Segmentation fault (signal %d) caught, exiting.\n", signo);
    exit(1);
}

void logx(const char *name, int val) {
    printf("[*] %s: %d\n", name, val);
}

void loglx(const char *name, u64 val) {
    printf("[*] %s: 0x%lx\n", name, val);
}

void logs(const char *name, const char *msg) {
    printf("[*] %s: %s\n", name, msg);
}

void init() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    signal(SIGSEGV, sh);
}

int main(int argc, char **argv) {
    init();

    char *buf = malloc(0x1000); 
    if (!buf) {
        perror("malloc");
        return 1;
    }
    u64 *buf64 = (u64 *)buf;

    struct in_args *p = malloc(sizeof(struct in_args));
    if (!p) {
        perror("malloc");
        free(buf);
        return 1;
    }

    int op = 0;
    u64 input_size = 0;
    u64 freeaddr = 0;

    int fd = open("/dev/kpwn", O_RDWR);
    if (fd < 0) {
        perror("open /dev/kpwn");
        free(buf);
        free(p);
        return 1;
    }
    logx("fd", fd);

    while (1) {
        printf("1.malloc\n");
        printf("2.free\n");
        printf("3.exit\n");
        printf(">> ");

        if (scanf("%d", &op) != 1) {
            printf("Invalid input.\n");
            break;
        }

        switch (op) {
            case 1:
                printf("malloc size (hex): 0x");
                if (scanf("%lx", &input_size) != 1) {
                    printf("Invalid size input.\n");
                    break;
                }
                if (input_size > 0x10000) {
                    printf("Size too large! Max 0x10000\n");
                    break;
                }
                printf("Payload: ");
                read(0, buf, 0x1000);
                p->addr = 0;
                p->size = input_size;
                p->buf = buf;
                ioctl(fd, ADD_ANY, p);
                loglx("kmalloc", buf64[0]);
                break;

            case 2:
                printf("free addr (hex): 0x");
                if (scanf("%lx", &freeaddr) != 1) {
                    printf("Invalid address input.\n");
                    break;
                }
                loglx("read", freeaddr);
                p->addr = freeaddr;
                ioctl(fd, DEL_ANY, p);
                break;

            case 3:
                close(fd);
                free(buf);
                free(p);
                exit(0);
                break;

            default:
                printf("Unknown option.\n");
        }
    }

    close(fd);
    free(buf);
    free(p);
    logs("wtf", "aaaaa");

    return 0;
}
