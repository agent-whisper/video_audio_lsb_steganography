from decrypt import Decrypt

d = Decrypt()
filebytes = d.read_encrypted_file("coba.wav")
lsb = d.get_lsb(filebytes,"test")
length, ext = d.get_info_message(lsb)
d.print_message(length, ext, lsb, "test-aja")
