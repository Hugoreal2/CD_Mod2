import struct

import serial
import time

# possible baud_rates include: 9600, 19200, 31250, 38400, 57600, 74880, 115200, 230400, 250000, 500000, 921600

ARDUINO_PORT = 'COM4'
BAUD_RATE = 9600
l_values = [0, 1, 2, 3, 4]  ## VALUE IN BYTES
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(1)  # Wait for the connection to be established

def ip_checksum(data: bytes) -> int:
    """
    Calculates the IP checksum for a given byte array.

    @data A byte array representing the IP header or data.

    Returns: An integer representing the 16-bit checksum.
    """
    if len(data) % 2 != 0:
        raise ValueError("data length must be a multiple of 2")

    words = [data[i] << 8 | data[i + 1] for i in range(0, len(data), 2)]

    checksum = sum(words)

    while checksum > 0xffff:
        checksum = (checksum & 0xffff) + (checksum >> 16)

    return (~checksum) & 0xffff

def burst_error_channel(data: bytes, L: int) -> bytes:
    """
    Simulate a burst error channel with L errors.

    :param data: the data to be transmitted
    :param L: the number of errors

    :return: the received data
    """
    new_data = bytearray(data)
    for i in range(L):
        new_data[i] = new_data[i] ^ 0b11111111

    return bytes(new_data)

def send_data(number: int):
    """
    Send a 2-byte number to the Arduino.

    :param number: the number to be sent
    """
    data = struct.pack('<H', number)  # '<H' means little-endian unsigned short (2 bytes)
    ser.write(data)


def receive_data() -> list[int]:
    """
    Receive 2-byte numbers from Arduino.

    :return: a list of numbers received from the Arduino
    """
    prime_numbers = []
    while True:
        bytes_read = ser.read(2)
        if len(bytes_read) == 2:
            number_from_arduino = struct.unpack('<H', bytes_read)[0]  # Convert 2 bytes back to an integer
            prime_numbers.append(number_from_arduino)
        else:
            break
    return prime_numbers


def calculate_prime_numbers(N: int) -> list[int]:
    """
    Calculate the prime numbers up to N.
    """
    prime_numbers = []
    for i in range(1, N + 1):
        if i > 1:
            for j in range(2, i):
                if i % j == 0:
                    break
            else:
                prime_numbers.append(i)
    return prime_numbers


try:
    number = int(input("Enter a number: "))
    send_data(number)

    # Receive data from the Arduino
    primes_arduino_and_checksum = receive_data()

    primes_arduino = primes_arduino_and_checksum[:-1]
    checksum = primes_arduino_and_checksum[-1]
    print(f"Prime numbers received from Arduino: {primes_arduino}")
    print(f"Checksum received from Arduino: {checksum:04X}")

    # each prime number needs to ocupy 2 bytes
    primes_arduino_bytes = struct.pack(f'>{len(primes_arduino)}H', *primes_arduino)

    python_checksum = ip_checksum(primes_arduino_bytes)
    print(f"Checksum calculated in Python: {python_checksum:04X}")

    if python_checksum == checksum:
        print("Checksums match!")
    else:
        print("Checksums do not match!")

    for L in l_values:
        print(f"Testing with burst length L = {L}")
        data_with_errors = burst_error_channel(primes_arduino_bytes, L)
        checksum_with_errors = ip_checksum(data_with_errors)
        print(f"Checksum with errors: {checksum_with_errors:04X}")

        if checksum == checksum_with_errors:
            print("Errors not detected with burst length L = {L}!")
        else:
            print("Errors detected with burst length L = {L}!")
        print()

finally:
    ser.close()
