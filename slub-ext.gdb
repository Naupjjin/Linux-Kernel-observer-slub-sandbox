python
import sys
sys.path.insert(0, 'gdbext')  # or use absolute path
end

source gdbext/find_slub_cache_l.py
source gdbext/find_slub_cache.py
source gdbext/kmem_cache_dumper.py
source gdbext/kmem_cache_info.py
source gdbext/qemu_monitor.py
source gdbext/va_split.py