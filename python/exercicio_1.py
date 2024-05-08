import random

p_values = [0.01, 0.05, 0.1, 0.2, 0.5]


## ------------------------------------------------------
#                       UTIL FUNCTIONS
## ------------------------------------------------------

def bits_to_bytes(encoded_bits: str) -> bytes:
    """
    Convert a string of bits to a bytearray.

    :param encoded_bits: the string of bits

    :return: the bytearray
    """
    bytes_array = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = 0
        for j in range(8):
            byte |= int(encoded_bits[i + j]) << (7 - j)
        bytes_array.append(byte)
    return bytes_array


def calculate_error_rate(original: bytes, received: bytes) -> float:
    if len(original) != len(received):
        raise ValueError("Original and received data must have the same length")

    total_bit_size = len(original) * 8

    difference = bytes([a ^ b for a, b in zip(original, received)])

    return sum(bin(byte).count('1') for byte in difference) / total_bit_size


def read_bytes_from_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


## ------------------- BSC FUNCTIONS ------------------- ##

def binary_symmetric_channel(sequence: bytes, p: float) -> bytes:
    """
    Simulate a binary symmetric channel with error probability p.

    :param sequence: the sequence of bytes to be transmitted
    :param p: the error probability

    :return: the received sequence
    """
    if p < 0 or p > 1:
        raise ValueError("p must be between 0 and 1")

    count_errors = 0
    new_sequence = bytearray(sequence)
    for i in range(len(sequence)):
        byte = 0

        # a byte with random ones is generated
        # that acts as a mask to flip the bits

        for j in range(8):
            if random.random() < p:
                count_errors += 1
                byte |= 1 << j

        new_sequence[i] ^= byte

    return new_sequence


def repetition_encode_bits(message: bytes, repetitions: int) -> bytes:
    """
    Encode a message using repetition code.

    :param message: the message to be encoded
    :param repetitions: the number of repetitions for each bit

    :return: the encoded message
    """
    encoded_bits = ''
    for byte in message:
        for i in range(8):  # 8 bits in a byte
            encoded_bits += str((byte >> i) & 1) * repetitions
    return bits_to_bytes(encoded_bits)

def repetition_decode_bits(message: bytes, repetitions: int) -> bytes:
    """
    Decode a message using repetition code.

    :param message: the message to be decoded
    :param repetitions: the number of repetitions for each bit

    :return: the decoded message
    """

    message_index = 0
    decoded_string = ''

    while message_index < len(message):
        byte = message[message_index]
        bit_index = 0

        # get the first bit of the byte

        while bit_index < 8:
            bit = (byte >> bit_index) & 1
            count = 0
            while count < repetitions:
                decoded_string += str(bit)
                count += 1
            bit_index += 1


    return bits_to_bytes(decoded_string)


sample_bytes = bytes([171, 255, 0])

encoded_data = repetition_encode_bits(sample_bytes, 3)

print("Original data:")
for byte in sample_bytes:
    print(bin(byte), end=", ")
print("\n")

print("Encoded data:")
for byte in encoded_data:
    print(bin(byte), end=", ")
print("\n")

print("Decoded data:")

decoded_data = repetition_decode_bits(encoded_data, 3)
for byte in decoded_data:
    print(bin(byte), end=", ")
print("\n")
