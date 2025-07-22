set pagination off
set confirm off

source gdb_script/find_slub_cache_link.py
source gdb_script/find_slub_cache.py

define load_trace_slub
    set $text = 0xffffffffc0000000
    set $data = 0xffffffffc0201040
    set $bss = 0xffffffffc0201090   

    add-symbol-file sysfile/trace_slub.ko $text \
        -s .data $data \
        -s .exit.text 0xffffffffc0000180 \
        -s .rodata 0xffffffffc0203100 \
        -s .text 0xffffffffc0000000
end

document load_trace_slub
Load trace_slub.ko symbols with correct section addresses
end

load_trace_slub
