import gdb
import re
from offset.kmem_cache_offset import KMEM_CACHE_OFFSET

def remove_ansi_colors(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class KmemCacheDumper(gdb.Command):
    """
    Linux kernel 6.15.7 
    Usage: kmem-cache-dumper 
    by. naup96321

    -help
    -debug
    -start <slab_caches address hex>
    -search <kmem_cache name>

    example: 0xffffffff82b6a3a0 T slab_caches
    """

    def __init__(self):
        super(KmemCacheDumper, self).__init__("kmem-cache-dumper", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):

        arg = arg.strip().split()

        start_addr = 0
        success_search = 0
        w_search = 0
        list_offset = KMEM_CACHE_OFFSET['list']
        name_offset = KMEM_CACHE_OFFSET['name']

        if "-help" in arg:
            print('<Usage>:\nkmem-cache-dumper\n-help\n-debug\n-start <slab_caches address hex>\n-search <kmem_cache name>')
            return

        if "-debug" in arg:
            debug = True
        else:
            debug = False

        if "-search" in arg:
            try:
                idx = arg.index("-search")
                w_search = arg[idx+1]
            except:
                print("Failed to -search")
                return

        if "-start" in arg:
            try:
                idx = arg.index("-start")
                start_addr = arg[idx+1]
                start_addr = int(gdb.execute(f"x/1xg {start_addr}", to_string=True).split()[-1],16)
            except:
                print("Failed to -start")
                return
        else:
            try:
                slab_caches = gdb.parse_and_eval("slab_caches")
                slab_caches_next = slab_caches['next']
                start_addr = int(slab_caches_next)
                if debug:
                    print(f"[debug] slab_caches -> next: {hex(start_addr)}")
            except gdb.error as e:
                print("[x] Failed to locate slab_caches symbol:", e)
                return

        print(f"Start traversal at: {hex(start_addr)}")
        
        while True:

            now_kmem_cache_start = start_addr - list_offset
            now_kmem_cache_name_ptr = now_kmem_cache_start + name_offset
            now_kmem_cache_list = now_kmem_cache_start + list_offset


            now_kmem_cache_name_ptr = int(gdb.execute(f"x/1xg {hex(now_kmem_cache_name_ptr)}", to_string=True).split()[1],16)
            if debug:
                print("[debug] now kmem_cache:", hex(now_kmem_cache_start))
                print("[debug] now kmem_cache name ptr:", hex(now_kmem_cache_name_ptr))
            
            now_kmem_cache_name = gdb.execute(f"x/1s {hex(now_kmem_cache_name_ptr)}", to_string=True).split()[-1][1:-1]
            
            if not w_search:
                print(hex(now_kmem_cache_start),":",now_kmem_cache_name)
            else:
                if w_search == now_kmem_cache_name:
                    success_search = 1
                    print(hex(now_kmem_cache_start),":",now_kmem_cache_name)

            if now_kmem_cache_name == "kmem_cache":
                if success_search == 0 and w_search != 0:
                    print("Not Found:", w_search)
                return
                
            next_kmem_cache_ptr = gdb.execute(f"x/1xg {hex(now_kmem_cache_list)}", to_string=True).split()[-1]
            start_addr = int(next_kmem_cache_ptr,16)
        

KmemCacheDumper()