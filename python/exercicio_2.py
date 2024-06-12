import random
import crcmod
from bitarray import bitarray

# Constants
l_values = [
    1, 
    2, 
    3, 
    4, 
    8, 
    16, 
    32, 
    64, 
    128
]

k = 1024 // 8  # 1024 bits - 128 bytes
poly_crc_32 = 0x104C11DB7

# ------------------------------------------------------
#                       2 - a)
# ------------------------------------------------------

def burst_error_channel(sequence: bytes, l: int, offset: int = 0) -> bytes:
    """
    Simulate a burst error channel with l errors.

    :param sequence: the sequence of bytes to be transmitted
    :param l: the number of errors
    :param offset: the offset at which to start the burst error

    :return: the received sequence
    """
    if l < 0 or l > len(sequence) * 8:
        raise ValueError("l must be between 0 and the length of the sequence in bits")

    new_sequence = bitarray()
    new_sequence.frombytes(sequence)

    for i in range(l):
        new_sequence[offset + i] = not new_sequence[offset + i]

    return new_sequence.tobytes()

# ------------------------------------------------------
#                       2 - b)
# ------------------------------------------------------

def calculate_crc(sequence: bytes) -> int:
    """
    Calculate the CRC of the given sequence.

    :param sequence: the sequence of bytes

    :return: the CRC
    """
    crc_func = crcmod.mkCrcFun(poly_crc_32, initCrc=0, xorOut=0xFFFFFFFF)    
    return crc_func(sequence)

def verify_crc(sequence: bytes, crc: int) -> bool:
    """
    Verify the CRC of the given sequence.

    :param sequence: the sequence of bytes
    :param crc: the CRC

    :return: True if the CRC is correct, False otherwise
    """
    return calculate_crc(sequence) == crc

def generate_random_block() -> bytes:
    """
    Generate a random block of k bytes.

    :return: the random block
    """
    return bytes([random.randint(0, 255) for _ in range(k)])


# ------------------------------------------------------
#                        MAIN
# ------------------------------------------------------

# 2 - a)
for l in l_values:
    block = generate_random_block()
    received_block = burst_error_channel(block, l)
    original_crc = calculate_crc(block)
    calculated_crc = calculate_crc(received_block)
    is_correct = verify_crc(block, calculated_crc)
    print(f"For L = {l}")
    print(f"\tWith block size {k}")
    print(f"\tOriginal CRC: {hex(original_crc)}")
    print(f"\tReceived CRC: {hex(calculated_crc)}")
    print(f"\tError detectected: {not is_correct}")

