gcc ita.c -o ita -g --static
gcc kmalloc16_script.c -o kmalloc16_script -g --static 
find . | cpio -o --format=newc > ../initramfs.cpio
