def binary_to_hex_file(input_file, output_file):
    """Convert binary strings in input_file to hex strings in output_file."""
    with open(input_file, "r") as bin_f:
        lines = bin_f.readlines()
    with open(output_file, "w+") as hex_f:
        for line in lines:
            binary_code = line.replace(" ", "").strip()
            if not binary_code:
                continue
            hex_code = hex(int(binary_code, 2))
            hex_code = hex_code.replace("0x", "").upper().zfill(4)
            hex_f.write(hex_code + "\n")


def binary_save(binary_string, output_file="walletpassphrase.txt"):
    """Write a walletpassphrase command with the given binary string."""
    with open(output_file, 'w') as f:
        f.write("walletpassphrase " + binary_string + " 60" + "\n")
        f.write("" + "\n")
