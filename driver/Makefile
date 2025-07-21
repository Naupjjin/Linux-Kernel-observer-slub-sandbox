obj-m += trace_slub.o

KDIR = /home/naup/Desktop/trace-slub/linux-6.15.7
EXTRA_CFLAGS += -g

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules EXTRA_CFLAGS="$(EXTRA_CFLAGS)"

clean:
	rm -rf *.o *.ko *.mod.* *.symvers *.order
