import gdb
import re
from offset.kmem_cache_offset import KMEM_CACHE_OFFSET

def remove_ansi_colors(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class KmemCacheInfo(gdb.Command):
    """
    Linux kernel 6.15.7 
    Usage: kmem-cache-info
    by. naup96321

    kmem-cache-info <address>
    """

    def __init__(self):
        super(KmemCacheInfo, self).__init__("kmem-cache-info", gdb.COMMAND_USER)
        self.kmem_cache_ptr = 0

    def dump_flags(self):
        ptr = self.kmem_cache_ptr + KMEM_CACHE_OFFSET['flags']
        output = int(gdb.execute(f"x/1xg {ptr}", to_string=True).split()[1],16)
        print("flags : ", hex(output))

    def dump_size_and_object_size(self):
        size_ptr = self.kmem_cache_ptr + KMEM_CACHE_OFFSET['size']
        objsize_ptr = self.kmem_cache_ptr + KMEM_CACHE_OFFSET['object_size']
        size_output = int(gdb.execute(f"x/1xw {size_ptr}", to_string=True).split()[1],16)
        objsize_output = int(gdb.execute(f"x/1xw {objsize_ptr}", to_string=True).split()[1],16)
        print(f"object size : {hex(objsize_output)} (chunk size : {hex(size_output)})")


    def dump_name(self):
        ptr = self.kmem_cache_ptr + KMEM_CACHE_OFFSET['name']
        ptr = int(gdb.execute(f"x/1xg {hex(ptr)}", to_string=True).split()[1],16)
        output = gdb.execute(f"x/1s {hex(ptr)}", to_string=True).split()[-1][1:-1]
        print(f"\n**{output}**\n")

    def invoke(self, arg, from_tty):

        arg = arg.strip().split()
        self.kmem_cache_ptr = int(arg[0], 16)

        self.dump_name()
        print("kmem_cache : ", hex(self.kmem_cache_ptr))
        print("=================")
        self.dump_flags()
        self.dump_size_and_object_size()
        print("=================")
        

KmemCacheInfo()
