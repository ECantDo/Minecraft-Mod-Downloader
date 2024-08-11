with open("C:\\Users\\15875\\PycharmProjects\\modrinthAPI\\dist\\mod_downloader.exe", "rb") as f:
    buf = f.read()

with open("C:\\Users\\15875\\PycharmProjects\\modrinthAPI\\dist\\output.txt", "w") as o:
    binary = bin(int.from_bytes(buf, byteorder='big'))[2:] # or byteorder='little' as necessary
    o.write(binary)