import math
import random
from bitarray import bitarray

files_to_be_tested = [
    "testFilesCD/a.txt", 
    "testFilesCD/abbccc.txt", 
    "testFilesCD/alice29.txt", 
    "testFilesCD/arrays.kt", 
    "testFilesCD/barries.jpg", 
    "testFilesCD/barries.tif", 
    "testFilesCD/bird.gif", 
    "testFilesCD/cp.htm", 
    "testFilesCD/fibonacci.kt", 
    "testFilesCD/lena.bmp", 
    "testFilesCD/maximumSubarray.kt", 
    "testFilesCD/perosn.java", 
    "testFilesCD/progc.c", 
    "testFilesCD/view.kt", 
]

p_values = [10 ** -6, 10 ** -5, 10 ** -4, 10 ** -3, 10 ** -2]

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

## ------------------------------------------------------
#                       1 - a) (i)
## ------------------------------------------------------

def transmit_no_hamming(input: bytes, p: float) -> bytes:
    return binary_symmetric_channel(input, p)

## ------------------------------------------------------
#                       1 - a) (ii)
## ------------------------------------------------------

def repetition_3_1_encode(message: bytes) -> bytes:
    """
    Encode a message using repetition code. with each bit being tripled (3,1).

    :param message: the message to be encoded
    :param repetitions: the number of repetitions for each bit

    :return: the encoded message
    """

    input_bits = bitarray()
    input_bits.frombytes(message)

    output_bits = bitarray()

    for bit in input_bits:
        for _ in range(3):
            output_bits.append(bit)

    return output_bits.tobytes()
    

def repetition_3_1_decode(message: bytes) -> bytes:
    """
    Decode a message using repetition code. each bit that appears more than half of the time is considered as the correct bit.

    :param message: the message to be decoded
    :param repetitions: the number of repetitions for each bit

    :return: the decoded message
    """

    input_bits = bitarray()
    input_bits.frombytes(message)

    output_bits = bitarray()

    for i in range(0, len(input_bits), 3):
        bit = input_bits[i:i+3]
        if bit.count(True) > 1:
            output_bits.append(True)
        else:
            output_bits.append(False)

    return output_bits.tobytes()

    
def transmit_repetition_31_correction(input: bytes, p: float) -> bytes:
    encoded = repetition_3_1_encode(input)
    sent_through_bsc = binary_symmetric_channel(encoded, p)
    return repetition_3_1_decode(sent_through_bsc)

## ------------------------------------------------------
#                       1 - a) (iii)
## ------------------------------------------------------

def hamming_74_encode(message: bytes) -> bytes:
    """
    Encode a message using Hamming code for 7,4. 3 parity bits and 4 bits of data.

    :param message: the message to be encoded

    :return: the encoded message
    """
    input_bits = bitarray()
    input_bits.frombytes(message)

    output_bits = bitarray()

    for i in range(0, len(input_bits), 4):
        d1 = input_bits[i]
        d2 = input_bits[i+1] if i+1 < len(input_bits) else 0
        d3 = input_bits[i+2] if i+2 < len(input_bits) else 0
        d4 = input_bits[i+3] if i+3 < len(input_bits) else 0

        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p3 = d2 ^ d3 ^ d4

        output_bits.extend([p1, p2, d1, p3, d2, d3, d4])

    return output_bits.tobytes()

def hamming_74_decode(message: bytes) -> bytes:
    """
    Decode a message using Hamming code for 7,4. 3 parity bits and 4 bits of data.

    :param message: the message to be decoded

    :return: the decoded message
    """

    input_bits = bitarray()
    input_bits.frombytes(message)

    output_bits = bitarray()

    for i in range(0, len(input_bits), 7):
        p1 = input_bits[i]
        p2 = input_bits[i+1] if i+1 < len(input_bits) else 0
        d1 = input_bits[i+2] if i+2 < len(input_bits) else 0
        p3 = input_bits[i+3] if i+3 < len(input_bits) else 0
        d2 = input_bits[i+4] if i+4 < len(input_bits) else 0
        d3 = input_bits[i+5] if i+5 < len(input_bits) else 0
        d4 = input_bits[i+6] if i+6 < len(input_bits) else 0

        c1 = p1 ^ d1 ^ d2 ^ d4
        c2 = p2 ^ d1 ^ d3 ^ d4
        c3 = p3 ^ d2 ^ d3 ^ d4
        
        error = c1 | (c2 << 1) | (c3 << 2)

        if error != 0:
            input_bits[i + error - 1] ^= 1

        # Re-extract the data bits after potential correction
        d1 = input_bits[i+2] if i+2 < len(input_bits) else 0
        d2 = input_bits[i+4] if i+4 < len(input_bits) else 0
        d3 = input_bits[i+5] if i+5 < len(input_bits) else 0
        d4 = input_bits[i+6] if i+6 < len(input_bits) else 0

        output_bits.extend([d1, d2, d3, d4])


    return output_bits.tobytes()

def transmit_hamming_74_correction(input: bytes, p: float) -> bytes:
    encoded = hamming_74_encode(input)
    sent_through_bsc = binary_symmetric_channel(encoded, p)
    return hamming_74_decode(sent_through_bsc)

## ------------------------------------------------------
#                       1 - b)
## ------------------------------------------------------

