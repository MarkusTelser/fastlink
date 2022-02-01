def convert_bits(bits: int):
    if bits < 1000:
        return f"{bits} B"
    if bits / 1024 < 1000:
        return f"{int(round(bits / 1024, 0))} KiB"
    elif bits / (1024 ** 2) < 1000:
        return f"{round(bits / (1024 ** 2), 1)} MiB"
    elif bits  / (1024 ** 3) < 1000:
        return f"{round(bits / (1024 ** 3), 2)} GiB"
    elif bits / (1024 ** 4) < 1000: 
        return f"{round(bits / (1024 ** 4), 2)} TiB"
    elif bits / (1024 ** 5) < 1000:
        return f"{round(bits / (1024 ** 5), 3)} PiB"