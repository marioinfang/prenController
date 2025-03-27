# TODO: Use an environment variable instead of this workaround
def is_raspberry_pi() -> bool:
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read()
        return "Raspberry Pi" in cpuinfo
    except FileNotFoundError:
        return False