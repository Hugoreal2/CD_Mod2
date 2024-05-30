import random
import crcmod

l_values = [0, 1, 2, 3, 4]  ## VALUE IN BYTES
k = 1024 // 8  # 1024 bits to bytes
poly = 0x104C11DB7  # hexa of CRC Poly X32+X26+X23+X22+X16+X12+X11+X10+X8+X7+X5+X4+X2+X+1

# Função para calcular CRC
def calculate_crc(data: bytes, poly: int) -> int:
    crc_func = crcmod.mkCrcFun(poly, initCrc=0, xorOut=0xFFFFFFFF)
    return crc_func(data)


# Teste de detecção de erros com CRC

def burst_error_channel(data: bytes, L: int) -> bytes:
    new_data = bytearray(data)
    for i in range(L):
        new_data[i] = new_data[i] ^ 0b11111111

    return bytes(new_data)


for L in l_values:
    print(f"\n\nL = {L}")
    data = bytes([0b11111111, 0b10000001, 0b11110000, 0b00001111])
    data_string = " ".join([f"{bin(byte)[2:]:>08}" for byte in data])
    print(f"Original data: {data_string}")

    data_with_errors = burst_error_channel(data, L)
    data_with_errors_string = " ".join([f"{bin(byte)[2:]:>08}" for byte in data_with_errors])
    print(f"Data with errors: {data_with_errors_string}")

# Gerar dados aleatórios de 1024 bits
data = bytes([random.getrandbits(8) for _ in range(k)])

for L in l_values:
    print(f"Testing with burst length L = {L}")
    crc_original = calculate_crc(data, poly)
    data_with_errors = burst_error_channel(data, L)
    crc_with_errors = calculate_crc(data_with_errors, poly)

    print(f"CRC original: {crc_original:08X}")
    print(f"CRC with errors: {crc_with_errors:08X}")
    if crc_original == crc_with_errors:
        print("Errors not detected!")
    else:
        print("Errors detected!")
    print()
