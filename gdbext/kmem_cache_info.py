import gdb
import re

def remove_ansi_colors(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class FindSlubCache(gdb.Command):
    """
    Linux kernel 6.15.7 
    Usage: kmem-cache-info
    by. naup96321

    kmem-cache-info <address>
    """

    def __init__(self):
        super(FindSlubCache, self).__init__("kmem-cache-info", gdb.COMMAND_USER)
        self.kmem_cache = 0
        self.kmem_cache_t_cpu_slab = 0
        self.kmem_cache_t_flags = 0
        self.kmem_cache_t_object_size = 0
        

    def invoke(self, arg, from_tty):

        arg = arg.strip().split()
        self.kmem_cache = int(arg[0], 16)
        self.flags = self.kmem_cache

FindSlubCache()
