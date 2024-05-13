import random

p_values = [0.0001, 0.001, 0.01, 0.1, 0.5]
test_file = "testFilesCD/alice29.txt"


## ------------------------------------------------------
#                       UTIL FUNCTIONS
## ------------------------------------------------------

def binary_string_to_bytes(encoded_bits: str) -> bytes:
    """
    Convert a string of bits to a bytearray.

    :param encoded_bits: the string of bits

    :return: the bytearray
    """
    byte_data = []
    for i in range(0, len(encoded_bits), 8):

        if i + 8 > len(encoded_bits):
            byte = int(encoded_bits[i:], 2)
            remaining_bits = 8 - len(encoded_bits[i:])
            byte <<= remaining_bits
            byte_data.append(byte)
            break

        byte = int(encoded_bits[i:i + 8], 2)
        byte_data.append(byte)
    return bytes(byte_data)


def bytes_to_binary_string(byte_data: bytes) -> str:
    binary_string = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_string


def int_to_binary_string(number: int, length: int) -> str:
    return format(number, f'0{length}b')


def calculate_error_rate(original: bytes, received: bytes) -> float:
    if len(original) != len(received):
        raise ValueError("Original and received data must have the same length")

    total_bit_size = len(original) * 8

    difference = bytes([a ^ b for a, b in zip(original, received)])

    return sum(bin(byte).count('1') for byte in difference) / total_bit_size


def calculate_total_errors(original: bytes, received: bytes) -> float:
    if len(original) != len(received):
        raise ValueError("Original and received data must have the same length")

    total_bit_size = len(original) * 8

    difference = bytes([a ^ b for a, b in zip(original, received)])

    return sum(bin(byte).count('1') for byte in difference) / 8


def read_bytes_from_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


def write_bytes_to_file(file_path: str, data: bytes):
    with open(file_path, "wb") as file:
        file.write(data)


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


def repetition_encode_bits_3_1(message: bytes) -> bytes:
    """
    Encode a message using repetition code. with each bit being tripled (3,1).

    :param message: the message to be encoded
    :param repetitions: the number of repetitions for each bit

    :return: the encoded message
    """

    encoded_string = bytes_to_binary_string(message)

    ## foreach char in the string, repeat it 3 times

    encoded_string = ''.join([char * 3 for char in encoded_string])

    return binary_string_to_bytes(encoded_string)


def repetition_decode_bits_3_1(message: bytes) -> bytes:
    """
    Decode a message using repetition code. each bit that appears more than half of the time is considered as the correct bit.

    :param message: the message to be decoded
    :param repetitions: the number of repetitions for each bit

    :return: the decoded message
    """

    binary_string = ''.join(format(byte, '08b') for byte in message)

    decoded_string = ''

    for i in range(0, len(binary_string), 3):
        three_values = binary_string[i:i + 3]
        decoded_string += get_more_common_bit(three_values)

    return binary_string_to_bytes(decoded_string)


def get_more_common_bit(string: str) -> str:
    count_ones = string.count('1')
    count_zeros = string.count('0')

    if count_ones > count_zeros:
        return '1'
    return '0'


def hamming_encode_bits(message: bytes) -> bytes:
    """
    Encode a message using Hamming code for 7,3. 3 parity bits and 4 bits of data.

    :param message: the message to be encoded

    :return: the encoded message
    """

    encoded_hamming_data = ""

    for message_byte in message:
        data1 = message_byte >> 4
        data2 = message_byte & 0b1111
        encoded_hamming_data += hamming_encode(data1)
        encoded_hamming_data += hamming_encode(data2)

    return binary_string_to_bytes(encoded_hamming_data)


def hamming_encode(data: int) -> str:
    bit0 = (data >> 0) & 1
    bit1 = (data >> 1) & 1
    bit2 = (data >> 2) & 1
    bit3 = (data >> 3) & 1

    b0 = bit1 ^ bit2 ^ bit3
    b1 = bit0 ^ bit1 ^ bit3
    b2 = bit0 ^ bit2 ^ bit3

    encoded_bits = (data << 3) | (b0 << 2) | (b1 << 1) | b2

    return int_to_binary_string(encoded_bits, 7)


def check_and_correct_hamming_code(byte: int) -> int:
    data = byte >> 3

    parity_bits_str = int_to_binary_string(byte & 0b0000111, 3)

    calculated_parity_bits_str = hamming_encode(data)[-3:]

    error = 0
    for i in range(3):
        if calculated_parity_bits_str[i] != parity_bits_str[i]:
            error += 1

    if error == 0:
        return data

    # can only detect up to 1 error code
    if error > 1:
        return data

    # error detected
    # correct the error

    calculated_parity_bits = binary_string_to_bytes(calculated_parity_bits_str)
    parity_bits = binary_string_to_bytes(parity_bits_str)

    sindroma = calculated_parity_bits[0] ^ parity_bits[0]

    # Síndroma
    # 1.º bit em erro 011
    # 2.º bit em erro 110
    # 3.º bit em erro 101
    # 4.º bit em erro 111
    # 5.º bit em erro 100
    # 6.º bit em erro 010
    # 7.º bit em erro 001

    if sindroma == 0b011:
        data ^= 0b1000000
    elif sindroma == 0b110:
        data ^= 0b0100000
    elif sindroma == 0b101:
        data ^= 0b0010000
    elif sindroma == 0b111:
        data ^= 0b0001000
    elif sindroma == 0b100:
        data ^= 0b0000100
    elif sindroma == 0b010:
        data ^= 0b0000010
    elif sindroma == 0b001:
        data ^= 0b0000001

    return check_and_correct_hamming_code(data)


def hamming_decode_bits(message: bytes) -> bytes:
    """
    Decode a message using Hamming code for 7,3. 3 parity bits and 4 bits of data.

    :param message: the message to be decoded

    :return: the decoded message
    """

    message_str = bytes_to_binary_string(message)

    message_sliced = [message_str[i:i + 7] for i in range(0, len(message_str), 7)]

    data = bytes()

    for i in range(0, len(message_sliced) - 1, 2):
        first_part = message_sliced[i]
        second_part = message_sliced[i + 1]

        first_4_bits = check_and_correct_hamming_code(int(first_part, 2))
        second_4_bits = check_and_correct_hamming_code(int(second_part, 2))

        first_4_bits <<= 4
        data += bytes([first_4_bits | second_4_bits])

    return data


def test_repetition_code():
    sample_bytes = read_bytes_from_file(test_file)

    encoded_repetition_data = repetition_encode_bits_3_1(sample_bytes)
    print(f"Repetition Code (3,1)")
    print(f"File: {test_file}")
    print(f"Total Symbols: {len(sample_bytes)}")

    for p in p_values:
        received_data = binary_symmetric_channel(encoded_repetition_data, p)
        decoded_data = repetition_decode_bits_3_1(received_data)

        error_rate = calculate_error_rate(sample_bytes, decoded_data)
        number_of_different_bytes = calculate_total_errors(sample_bytes, decoded_data)

        print(f"BER ={p}")
        print(f"BER': {error_rate}")
        print(f"Number of different symbols: {int(number_of_different_bytes)}")

        write_bytes_to_file(f"outputSamples/decoded_repetition_{p}.txt", decoded_data)


def test_hamming_code():
    sample_bytes = read_bytes_from_file(test_file)

    encoded_hamming_data = hamming_encode_bits(sample_bytes)
    print(f"Hamming Code (7,3)")
    print(f"File: {test_file}")
    print(f"Total Symbols: {len(sample_bytes)}")

    for p in p_values:
        received_data = binary_symmetric_channel(encoded_hamming_data, p)
        decoded_data = hamming_decode_bits(received_data)

        error_rate = calculate_error_rate(sample_bytes, decoded_data)
        number_of_different_bytes = calculate_total_errors(sample_bytes, decoded_data)
        print(f"BER ={p}")
        print(f"BER': {error_rate}")
        print(f"Number of different symbols: {int(number_of_different_bytes)}")

        write_bytes_to_file(f"outputSamples/decoded_hamming_{p}.txt", decoded_data)


test_repetition_code()
test_hamming_code()
