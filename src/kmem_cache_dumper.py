import gdb
import re
from kmem_cache_offset import KMEM_CACHE_OFFSET

def remove_ansi_colors(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class FindSlubCache(gdb.Command):
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
        super(FindSlubCache, self).__init__("kmem-cache-dumper", gdb.COMMAND_USER)

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
        

FindSlubCache()
'''
gef> ptype struct kmem_cache
type = struct kmem_cache {
    struct kmem_cache_cpu *cpu_slab;
    slab_flags_t flags;
    unsigned long min_partial;
    unsigned int size;
    unsigned int object_size;
    struct reciprocal_value reciprocal_size;
    unsigned int offset;
    unsigned int cpu_partial;
    unsigned int cpu_partial_slabs;
    struct kmem_cache_order_objects oo;
    struct kmem_cache_order_objects min;
    gfp_t allocflags;
    int refcount;
    void (*ctor)(void *);
    unsigned int inuse;
    unsigned int align;
    unsigned int red_left_pad;
    const char *name;
    struct list_head list;
    struct kobject kobj;
    unsigned int remote_node_defrag_ratio;
    struct kmem_cache_node *node[64];
}

ptype /o struct kmem_cache
/* offset      |    size */  type = struct kmem_cache {
/*      0      |       8 */    struct kmem_cache_cpu *cpu_slab;
/*      8      |       4 */    slab_flags_t flags;
/* XXX  4-byte hole      */
/*     16      |       8 */    unsigned long min_partial;
/*     24      |       4 */    unsigned int size;
/*     28      |       4 */    unsigned int object_size;
/*     32      |       8 */    struct reciprocal_value {
/*     32      |       4 */        u32 m;
/*     36      |       1 */        u8 sh1;
/*     37      |       1 */        u8 sh2;
/* XXX  2-byte padding   */

                                   /* total size (bytes):    8 */
                               } reciprocal_size;
/*     40      |       4 */    unsigned int offset;
/*     44      |       4 */    unsigned int cpu_partial;
/*     48      |       4 */    unsigned int cpu_partial_slabs;
/*     52      |       4 */    struct kmem_cache_order_objects {
/*     52      |       4 */        unsigned int x;

                                   /* total size (bytes):    4 */
                               } oo;
/*     56      |       4 */    struct kmem_cache_order_objects {
/*     56      |       4 */        unsigned int x;

                                   /* total size (bytes):    4 */
                               } min;
/*     60      |       4 */    gfp_t allocflags;
/*     64      |       4 */    int refcount;
/* XXX  4-byte hole      */
/*     72      |       8 */    void (*ctor)(void *);
/*     80      |       4 */    unsigned int inuse;
/*     84      |       4 */    unsigned int align;
/*     88      |       4 */    unsigned int red_left_pad;
/* XXX  4-byte hole      */
/*     96      |       8 */    const char *name;
/*    104      |      16 */    struct list_head {
/*    104      |       8 */        struct list_head *next;
/*    112      |       8 */        struct list_head *prev;

                                   /* total size (bytes):   16 */
                               } list;
/*    120      |      64 */    struct kobject {
/*    120      |       8 */        const char *name;
/*    128      |      16 */        struct list_head {
/*    128      |       8 */            struct list_head *next;
/*    136      |       8 */            struct list_head *prev;

                                       /* total size (bytes):   16 */
                                   } entry;
/*    144      |       8 */        struct kobject *parent;
/*    152      |       8 */        struct kset *kset;
/*    160      |       8 */        const struct kobj_type *ktype;
/*    168      |       8 */        struct kernfs_node *sd;
/*    176      |       4 */        struct kref {
/*    176      |       4 */            refcount_t refcount;

                                       /* total size (bytes):    4 */
                                   } kref;
/*    180: 0   |       4 */        unsigned int state_initialized : 1;
/*    180: 1   |       4 */        unsigned int state_in_sysfs : 1;
/*    180: 2   |       4 */        unsigned int state_add_uevent_sent : 1;
/*    180: 3   |       4 */        unsigned int state_remove_uevent_sent : 1;
/*    180: 4   |       4 */        unsigned int uevent_suppress : 1;
/* XXX  3-bit padding    */
/* XXX  3-byte padding   */

                                   /* total size (bytes):   64 */
                               } kobj;
/*    184      |       4 */    unsigned int remote_node_defrag_ratio;
/* XXX  4-byte hole      */
/*    192      |     512 */    struct kmem_cache_node *node[64];

                               /* total size (bytes):  704 */
                             }

'''