KMEM_CACHE_OFFSET = {
    "cpu_slab": 0,
    "flags": 8,
    "min_partial": 16,
    "size": 24,
    "object_size": 28,
    "reciprocal_size": 32,       
    "offset": 40,
    "cpu_partial": 44,
    "cpu_partial_slabs": 48,
    "oo": 52,
    "min": 56,
    "allocflags": 60,
    "refcount": 64,
    "ctor": 72,
    "inuse": 80,
    "align": 84,
    "red_left_pad": 88,
    "name": 96,
    "list": 104,
    "kobj": 120,
    "remote_node_defrag_ratio": 184,
    "node": 192,
}

KMEM_CACHE_NODE_OFFSET = {
    "list_lock": 0,
    "nr_partial": 8,
    "partial": 16,
    "nr_slabs": 32,
    "total_objects": 40,
    "full": 48,
}

SLAB_STRUCT_OFFSET = {
    "__page_flags": 0,
    "slab_cache": 8,

    # slab_list 和 next/slabs 是 union，實際視使用情境而定
    "slab_list": 16,    # struct list_head { next, prev }
    "next": 16,         # struct slab *next
    "slabs": 24,

    # freelist + counters 的 union
    "freelist": 32,
    "counters": 40,
    "inuse": 40,        # 位於 counters 的 bitfield (低16位)
    "objects": 42,      # bitfield 第16~30位
    "frozen": 43,       # bitfield 第31位

    # callback_head 也是 union 的其中一個成員
    "callback_head_next": 16,
    "callback_head_func": 24,

    "__page_type": 48,
    "__page_refcount": 52,
}

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

gef> ptype /o struct kmem_cache_node
/* offset      |    size */  type = struct kmem_cache_node {
/*      0      |       4 */    spinlock_t list_lock;
/* XXX  4-byte hole      */
/*      8      |       8 */    unsigned long nr_partial;
/*     16      |      16 */    struct list_head {
/*     16      |       8 */        struct list_head *next;
/*     24      |       8 */        struct list_head *prev;

                                   /* total size (bytes):   16 */
                               } partial;
/*     32      |       8 */    atomic_long_t nr_slabs;
/*     40      |       8 */    atomic_long_t total_objects;
/*     48      |      16 */    struct list_head {
/*     48      |       8 */        struct list_head *next;
/*     56      |       8 */        struct list_head *prev;

                                   /* total size (bytes):   16 */
                               } full;

                               /* total size (bytes):   64 */
                             }


gef> ptype /o struct slab
/* offset      |    size */  type = struct slab {
/*      0      |       8 */    unsigned long __page_flags;
/*      8      |       8 */    struct kmem_cache *slab_cache;
/*     16      |      32 */    union {
/*                    32 */        struct {
/*     16      |      16 */            union {
/*                    16 */                struct list_head {
/*     16      |       8 */                    struct list_head *next;
/*     24      |       8 */                    struct list_head *prev;

                                               /* total size (bytes):   16 */
                                           } slab_list;
/*                    16 */                struct {
/*     16      |       8 */                    struct slab *next;
/*     24      |       4 */                    int slabs;
/* XXX  4-byte padding   */

                                               /* total size (bytes):   16 */
                                           };

                                           /* total size (bytes):   16 */
                                       };
/*     32      |      16 */            union {
/*                    16 */                struct {
/*     32      |       8 */                    void *freelist;
/*     40      |       8 */                    union {
/*                     8 */                        unsigned long counters;
/*                     4 */                        struct {
/*     40: 0   |       4 */                            unsigned int inuse : 16;
/*     42: 0   |       4 */                            unsigned int objects : 15;
/*     43: 7   |       4 */                            unsigned int frozen : 1;

                                                       /* total size (bytes):    4 */
                                                   };

                                                   /* total size (bytes):    8 */
                                               };

                                               /* total size (bytes):   16 */
                                           };
/*                    16 */                freelist_aba_t freelist_counter;

                                           /* total size (bytes):   16 */
                                       };

                                       /* total size (bytes):   32 */
                                   };
/*                    16 */        struct callback_head {
/*     16      |       8 */            struct callback_head *next;
/*     24      |       8 */            void (*func)(struct callback_head *);

                                       /* total size (bytes):   16 */
                                   } callback_head;
/* XXX 16-byte padding   */

                                   /* total size (bytes):   32 */
                               };
/*     48      |       4 */    unsigned int __page_type;
/*     52      |       4 */    atomic_t __page_refcount;
/* XXX  8-byte padding   */

                               /* total size (bytes):   64 */
                             }
'''
