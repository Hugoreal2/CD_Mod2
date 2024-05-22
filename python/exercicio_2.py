import random
import crcmod

l_values = [0, 1, 2, 3, 4]  ## VALUE IN BYTES
k = 1024 // 8  # 1024 bits to bytes
poly = 0x104C11DB7  # Exemplo de polinômio CRC-32

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
    print(f"L = {L}")
    data = bytes([0b11111111, 0b10000001, 0b11110000, 0b00001111])
    for i in range(len(data)):
        print(f"Data: {bin(data[i])}")
    data_with_errors = burst_error_channel(data, L)
    for i in range(len(data_with_errors)):
        print(f"Data with burst errors: {bin(data_with_errors[i])}")
    print()

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



