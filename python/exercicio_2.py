l_values = [1, 2, 3, 4]  ## VALUE IN BYTES


def burst_error_channel(data: bytes, L: int) -> bytes:
    new_data = bytearray(data)
    for i in range(L):
        new_data[i] = new_data[i] ^ 0b11111111

    return bytes(new_data)


for L in l_values:
    print(f"L = {L}")
    data = bytes([0b11111111, 0b10000001, 0b11110000, 0b00001111])
    for i in range(len(data)):
        print(f"Data: {bin(data[i])}")
    data_with_errors = burst_error_channel(data, L)
    for i in range(len(data_with_errors)):
        print(f"Data with errors: {bin(data_with_errors[i])}")
    print()
