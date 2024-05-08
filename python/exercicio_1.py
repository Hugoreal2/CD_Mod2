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

    binary_string = ''.join(format(byte, '08b') for byte in message)

    decoded_string = ''

    for i in range(0, len(binary_string), repetitions):
        decoded_string += str(int(binary_string[i]) ^ int(binary_string[i + 1]) ^ int(binary_string[i + 2]))

    return bits_to_bytes(decoded_string)


def hamming_encode_bits(message: bytes) -> bytes:
    """
    Encode a message using Hamming code for 7,3. 3 parity bits and 4 bits of data.

    :param message: the message to be encoded

    :return: the encoded message
    """

    encoded_hamming_data = ""

    for byte in message:
        data1 = byte >> 4
        data2 = byte & 0b1111
        encoded_byte = hamming_encode(data1)
        encoded_hamming_data += format(encoded_byte, '08b')
        encoded_byte = hamming_encode(data2)
        encoded_hamming_data += format(encoded_byte, '08b')

    return bits_to_bytes(encoded_hamming_data)

def hamming_encode(byte: int) -> int:
    bit0 = (byte >> 0) & 1
    bit1 = (byte >> 1) & 1
    bit2 = (byte >> 2) & 1
    bit3 = (byte >> 3) & 1

    b0 = bit1 ^ bit2 ^ bit3
    b1 = bit0 ^ bit1 ^ bit3
    b2 = bit0 ^ bit2 ^ bit3

    encoded_hamming_data = (byte << 3) | (b0 << 2) | (b1 << 1) | b2

    return encoded_hamming_data


def check_and_correct_hamming_code(byte: int) -> int:
    # get the first 4 bits of the byte and calculate its parity bits then compare it with the parity bits of the byte

    data = byte >> 3

    print("data " + bin(data))
    print("byte " + bin(byte))

    parity_bits = byte & 0b0000111

    calculated_parity_bits = hamming_encode(data)

    error = 0
    for i in range(3):
        if calculated_parity_bits[i] != parity_bits[i]:
            error += 1

    if error == 0:
        print("No error detected")
        return data

    # error detected
    # correct the error
    error_bit = 0
    for i in range(3):
        error_bit |= (calculated_parity_bits[i] ^ parity_bits[i]) << i


def hamming_decode_bits(message: bytes) -> bytes:
    """
    Decode a message using Hamming code for 7,3. 3 parity bits and 4 bits of data.

    :param message: the message to be decoded

    :return: the decoded message
    """

    binary_string = ''.join(format(byte, '08b') for byte in message)

    decoded_string = ''

    print("binary_string " + binary_string)

    for i in range(0, len(binary_string), 7):
        hamming_code_byte = int(binary_string[i:i + 7], 2)
        print("hamming_code_byte " + bin(hamming_code_byte))
        corrected_code = check_and_correct_hamming_code(hamming_code_byte)

        print("corrected_code " + bin(corrected_code))
        data = corrected_code >> 3
        decoded_string += format(data, '04b')

    print("decoded_string " + decoded_string)
    return bits_to_bytes(decoded_string)

sample_bytes = bytes([255, 0b10101010, 0])

# encoded_repetition_data = repetition_encode_bits(sample_bytes, 3)

print("Original data:")
for byte in sample_bytes:
    print(bin(byte), end=", ")
print("\n")

# print("Encoded repetition data:")
# for byte in encoded_repetition_data:
#     print(bin(byte), end=", ")
# print("\n")
#
# print("Decoded repetition  data:")
# decoded_data = repetition_decode_bits(encoded_repetition_data, 3)
# for byte in decoded_data:
#     print(bin(byte), end=", ")
# print("\n")

encoded_hamming_data = hamming_encode_bits(sample_bytes)

print("Encoded hamming data:")
for byte in encoded_hamming_data:
    print(bin(byte), end=", ")
print("\n")

print("Decoded hamming data:")
decoded_data = hamming_decode_bits(encoded_hamming_data)
for byte in decoded_data:
    print(bin(byte), end=", ")
print("\n")
