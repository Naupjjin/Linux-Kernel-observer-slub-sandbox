import gdb
import re

def remove_ansi_colors(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

class FindSlubCache(gdb.Command):
    """Find which SLUB kmem_cache a given address belongs to.
    Usage: find_slub_cache <address>
    by. naup96321
    """

    def __init__(self):
        super(FindSlubCache, self).__init__("find_slub_cache", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        if not arg:
            print("Usage: find_slub_cache <address>")
            return

        try:
            target = int(arg.strip(), 0)
        except ValueError:
            print("Invalid address format.")
            return

        print(f"[*] Looking for address 0x{target:x} in SLUB caches...")
        try:
            output = gdb.execute("slub-dump -n", to_string=True)
        except gdb.error as e:
            print(f"Error running slub-dump: {e}")
            return

        cache_blocks = []
        a = output.strip().split("\n\n")[1:]
        for i in a:
            cache_blocks.append(remove_ansi_colors(i))
        
        caches = []

        for block in cache_blocks:
            cache_info = {
                "kmem_cache": None,
                "name": None,
                "object_size": None,
                "active_page": None,
                "pages": [],
            }
            lines = block.splitlines()
            for line in lines:
                line = line.strip()
                if line.startswith("kmem_cache:"):
                    m = re.search(r"kmem_cache:\s+(0x[0-9a-fA-F]+)", line)
                    if m:
                        cache_info["kmem_cache"] = hex(int(m.group(1), 16))
                elif line.startswith("name:"):
                    m = re.search(r"name:\s+(\S+)", line)
                    if m:
                        cache_info["name"] = m.group(1)
                elif line.startswith("object size:"):
                    m = re.search(r"object size:\s+0x([0-9a-fA-F]+)", line)
                    if m:
                        cache_info["object_size"] = int(m.group(1), 16)
                elif line.startswith("active page:"):
                    m = re.search(r"active page:\s+(0x[0-9a-fA-F]+)", line)
                    if m:
                        cache_info["active_page"] = int(m.group(1), 16)
                elif line.startswith("page "):
                    m = re.search(r"page\s+(0x[0-9a-fA-F]+)", line)
                    if m:
                        cache_info["pages"].append(int(m.group(1), 16))

            caches.append(cache_info)

        for c in caches:
            if int(c['kmem_cache'],16) == target:
                print("find!, {}".format(c['name']))
        
        
FindSlubCache()
