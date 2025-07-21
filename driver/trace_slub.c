#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/string.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/miscdevice.h>
#include <linux/mm.h>

MODULE_LICENSE("Dual BSD/GPL");

#define ADD_ANY   0xbeef
#define DEL_ANY   0x2333

struct in_args {
    uint64_t addr;
    uint64_t size;
    char __user *buf;
};

static long add_any(struct in_args *args) {
    char *buffer;

    buffer = kmalloc(args->size, GFP_KERNEL);
    if (!buffer)
        return -ENOMEM;

    if (copy_from_user(buffer, args->buf, args->size)) {
        kfree(buffer);
        return -EFAULT;
    }

    if (copy_to_user(args->buf, &buffer, sizeof(buffer))) {
        kfree(buffer);
        return -EFAULT;
    }

    pr_info("add_any: allocated %llu bytes at %p\n", args->size, buffer);

    return 0;
}

static long del_any(struct in_args *args)
{
    void *ptr = (void *)(uintptr_t)args->addr;

    if (!ptr)
        return -EINVAL;

    pr_info("del_any: freeing pointer %p\n", ptr);

    kfree(ptr);
    return 0;
}

static long kpwn_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    struct in_args in;

    if (copy_from_user(&in, (void __user *)arg, sizeof(in)))
        return -EFAULT;

    switch (cmd) {
    case ADD_ANY:
        return add_any(&in);
    case DEL_ANY:
        return del_any(&in);
    default:
        return -EINVAL;
    }
}

static int kpwn_open(struct inode *inode, struct file *file)
{
    pr_info("kpwn device opened\n");
    return 0;
}

static int kpwn_release(struct inode *inode, struct file *file)
{
    pr_info("kpwn device closed\n");
    return 0;
}

static const struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = kpwn_open,
    .release = kpwn_release,
    .unlocked_ioctl = kpwn_ioctl,
};

static struct miscdevice misc = {
    .minor = MISC_DYNAMIC_MINOR,
    .name  = "kpwn",
    .fops = &fops,
};

static int __init kpwn_init(void)
{
    int ret;

    ret = misc_register(&misc);
    if (ret) {
        pr_err("Failed to register misc device\n");
        return ret;
    }
    pr_info("kpwn misc device registered\n");
    return 0;
}

static void __exit kpwn_exit(void)
{
    misc_deregister(&misc);
    pr_info("kpwn misc device deregistered\n");
}

module_init(kpwn_init);
module_exit(kpwn_exit);
