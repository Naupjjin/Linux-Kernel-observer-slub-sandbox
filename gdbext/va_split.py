import gdb

class VaSplitCommand(gdb.Command):
    """Split x86_64 virtual address into page table indices.

    Usage: va-split [-4kb|-2mb] <va>
    Example:
        va-split -4kb 0xffffffff82b6a3a0
        va-split -2mb 0xffffffff82b6a3a0
        va-split 0xffffffff82b6a3a0    # show both
    """

    def __init__(self):
        super(VaSplitCommand, self).__init__("va-split", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        argv = gdb.string_to_argv(arg)

        if not argv:
            gdb.write("\033[31m[!] Usage: va-split [-4kb|-2mb] <va>\033[0m\n", gdb.STDERR)
            return

        show_4kb = True
        show_2mb = True
        va_expr = None

        if argv[0] == "-4kb":
            show_2mb = False
            if len(argv) < 2:
                gdb.write("\033[31m[!] Missing virtual address.\033[0m\n", gdb.STDERR)
                return
            va_expr = argv[1]
        elif argv[0] == "-2mb":
            show_4kb = False
            if len(argv) < 2:
                gdb.write("\033[31m[!] Missing virtual address.\033[0m\n", gdb.STDERR)
                return
            va_expr = argv[1]
        else:
            va_expr = argv[0]

        try:
            va = int(gdb.parse_and_eval(va_expr))
        except Exception as e:
            gdb.write(f"\033[31m[!] Invalid input:\033[0m {e}\n", gdb.STDERR)
            return

        def split_4kb(va):
            return {
                "Unused (bits 63–48)": (va >> 48) & 0xffff,
                "PML4 Index": (va >> 39) & 0x1ff,
                "PDPT Index": (va >> 30) & 0x1ff,
                "PD Index": (va >> 21) & 0x1ff,
                "PT Index": (va >> 12) & 0x1ff,
                "Offset": va & 0xfff
            }

        def split_2mb(va):
            return {
                "Unused (bits 63–48)": (va >> 48) & 0xffff,
                "PML4 Index": (va >> 39) & 0x1ff,
                "PDPT Index": (va >> 30) & 0x1ff,
                "PD Index": (va >> 21) & 0x1ff,
                "Offset (2MB page)": va & 0x1fffff
            }

        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

        if show_4kb:
            gdb.write(f"{BLUE}4KB Page:{RESET}\n")
            for k, v in split_4kb(va).items():
                gdb.write(f"{GREEN}{k:22}:{RESET} {YELLOW}0x{v:x}{RESET} ({v})\n")

        if show_2mb:
            gdb.write(f"{BLUE}2MB Page:{RESET}\n")
            for k, v in split_2mb(va).items():
                gdb.write(f"{GREEN}{k:22}:{RESET} {YELLOW}0x{v:x}{RESET} ({v})\n")

VaSplitCommand()
