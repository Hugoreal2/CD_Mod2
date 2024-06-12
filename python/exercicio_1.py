import random
import numpy as np
import matplotlib.pyplot as plt
from bitarray import bitarray

file_path = "test_files_cd/"
output_path = "output/"

files_to_be_tested = [
    "a.txt", 
    # "alice29.txt", 
    "arrays.kt", 
    # "barries.jpg", 
    # "barries.tif", 
    # "bird.gif", 
    # "cp.htm", 
    "fibonacci.kt", 
    "maximumSubarray.kt", 
    "person.java", 
    "progc.c",
    "view.kt", 
]

P_VALUES = [
    0.0001,
    0.001,
    0.01,
    0.05,
    0.1,
    0.15,
    0.2,

]

NUM_ITERATIONS = 5


## ------------------------------------------------------
#                       UTILS
## ------------------------------------------------------

def binary_symmetric_channel(sequence: bytes, p: float) -> bytes:
    """
    Simulate a binary symmetric channel with error probability p.

    :param sequence: the sequence of bytes to be transmitted
    :param p: the error probability

    :return: the received sequence
    """
    if p < 0 or p > 1:
        raise ValueError("p must be between 0 and 1")

    # NOTE: this uses numpy to convert the bytes to bits and back
    bit_sequence = np.unpackbits(np.frombuffer(sequence, dtype=np.uint8))
    errors = np.random.rand(bit_sequence.size) < p
    bit_sequence ^= errors
    received_sequence = np.packbits(bit_sequence).tobytes()

    return received_sequence

def count_errors(original: bytes, received: bytes) -> int:
    """
    Count the number of errors between two sequences of bytes.

    :param original: the original sequence
    :param received: the received sequence

    :return: the number of errors
    """
    count = 0
    for i in range(len(original)):
        count += bin(original[i] ^ received[i]).count("1")

    return count

def bit_error_rate(original: bytes, received: bytes) -> float:
    """
    Calculate the bit error rate between two sequences of bytes.

    :param original: the original sequence
    :param received: the received sequence

    :return: the bit error rate
    """
    if len(original) != len(received):
        raise ValueError("The sequences must have the same length")

    return count_errors(original, received) / (len(original) * 8)

## ------------------------------------------------------
#                       1 - a) (i)
## ------------------------------------------------------

def transmit_no_error_correction(input: bytes, p: float) -> bytes:
    return binary_symmetric_channel(input, p)

## ------------------------------------------------------
#                       1 - a) (ii)
## ------------------------------------------------------

def repetition_3_1_encode(message: bytes) -> bytes:
    """
    Encode a message using repetition code with each bit being tripled (3,1).

    :param message: the message to be encoded

    :return: the encoded message
    """
    input_bits = bitarray()
    input_bits.frombytes(message)

    # Preallocate output_bits with three times the length of input_bits
    output_bits = bitarray(len(input_bits) * 3)
    
    for i, bit in enumerate(input_bits):
        output_bits[i * 3:i * 3 + 3] = bitarray([bit, bit, bit])

    return output_bits.tobytes()

def repetition_3_1_decode(message: bytes) -> bytes:
    """
    Decode a message using repetition code. Each bit that appears more than half of the time is considered as the correct bit.

    :param message: the message to be decoded

    :return: the decoded message
    """
    input_bits = bitarray()
    input_bits.frombytes(message)

    output_bits = bitarray(len(input_bits) // 3)

    for i in range(0, len(input_bits), 3):
        bit_slice = input_bits[i:i + 3]
        output_bits[i // 3] = bit_slice.count(True) > 1

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

def hamming_74_decode(message: bytes, original_length: int) -> bytes:
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

        if error != 0 and i + error - 1 < len(input_bits):
            input_bits[i + error - 1] ^= 1

        # Re-extract the data bits after potential correction
        d1 = input_bits[i+2] if i+2 < len(input_bits) else 0
        d2 = input_bits[i+4] if i+4 < len(input_bits) else 0
        d3 = input_bits[i+5] if i+5 < len(input_bits) else 0
        d4 = input_bits[i+6] if i+6 < len(input_bits) else 0

        output_bits.extend([d1, d2, d3, d4])

    # Trim the output_bits to the original length
    output_bits = output_bits[:original_length]

    return output_bits.tobytes()

def transmit_hamming_74_correction(input: bytes, p: float) -> bytes:
    encoded = hamming_74_encode(input)
    sent_through_bsc = binary_symmetric_channel(encoded, p)
    return hamming_74_decode(sent_through_bsc, len(input) * 8)

## ------------------------------------------------------
#                       1 - b)
## ------------------------------------------------------



## ------------------------------------------------------
#                        MAIN
## ------------------------------------------------------

# dictionary to store the methods and lookup by name
methods = {
    "Sem Correcção": transmit_no_error_correction,
    "Repetição(3,1)": transmit_repetition_31_correction,
    "Hamming(7,4)": transmit_hamming_74_correction,
}

for file_name in files_to_be_tested:
    print(f"Testing {file_name}")
    with open(file_path + file_name, "rb") as file:
        original = file.read()

    plt.figure()
    plt.title(f"BSC Simulation for {file_name}")
    plt.xlabel("Error Probability (p)")
    plt.ylabel("Bit Error Rate (BER)")

    for method_name, method in methods.items():
        bers = []
        for p in P_VALUES:
            print(f"Testing {method_name} with p={p}")
            ber = 0
            for _ in range(NUM_ITERATIONS):
                received = method(original, p)
                ber += bit_error_rate(original, received)
            ber /= NUM_ITERATIONS
            bers.append(ber)

        
        # Plot the line graph for each method
        plt.plot(P_VALUES, bers, marker='o', label=method_name)

    plt.legend()
    plt.savefig(output_path + file_name + ".png")

