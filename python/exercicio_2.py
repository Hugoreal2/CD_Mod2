import random
import crcmod
from bitarray import bitarray

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
k = 1024 // 8 # 1024 bits - 128 bytes
poly = 0x107

## ------------------------------------------------------
#                       2 - a)
## ------------------------------------------------------

def burst_error_channel(sequence: bytes, l: int, offset: int = 0) -> bytes:
    """
    Simulate a burst error channel with l errors.

    :param sequence: the sequence of bytes to be transmitted
    :param l: the number of errors

    :return: the received sequence
    """
    if l < 0 or l > len(sequence):
        raise ValueError("l must be between 0 and the length of the sequence")

    new_sequence = bitarray()
    new_sequence.frombytes(sequence)

    for i in range(l):
        new_sequence[offset + i] = not new_sequence[offset + i]

    return new_sequence.tobytes()

## ------------------------------------------------------
#                       2 - b)
## ------------------------------------------------------

def calculate_crc(sequence: bytes) -> int:
    """
    Calculate the CRC of the given sequence.

    :param sequence: the sequence of bytes

    :return: the CRC
    """
    crc8 = crcmod.mkCrcFun(poly, initCrc=0, xorOut=0xFFFFFFFF)
    return crc8(sequence)

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


## ------------------------------------------------------
#                       2 - c)
## ------------------------------------------------------

def undetectable_scenario():
    """
    Simulate the undetectable scenario.
    By using burst error channel with different offsets

    """
    while True:
        block = generate_random_block()
        original_crc = calculate_crc(block)
        print(f"Original CRC: {original_crc:08X}")

        for l in l_values:
            for offset in range(k - l + 1):
                received_block = burst_error_channel(block, l, offset)
                received_crc = calculate_crc(received_block)
                if received_crc == original_crc:
                    print(f"Undetectable scenario found with L = {l} and offset = {offset}")
                    print(f"Original block: {block}")
                    print(f"Received block: {received_block}")
                    print(f"Received CRC: {received_crc:08X}")
                    return
        print("No undetectable scenario found")

## ------------------------------------------------------
#                        MAIN
## ------------------------------------------------------

# 2 - a)
block = generate_random_block()
for l in l_values:
    received_block = burst_error_channel(block, l)
    crc = calculate_crc(received_block)
    is_correct = verify_crc(block, crc)
    print(f"With L = {l}, an error has occurred: {not is_correct}")

# 2 - b) 
undetectable_scenario()


