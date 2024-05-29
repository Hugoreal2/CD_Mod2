import struct

import serial
import time

arduino_port = 'COM4'
baud_rate = 9600  # Match this with the baud rate set on the Arduino

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(1)  # Wait for the connection to be established


def ip_checksum(data: bytes) -> int:
    """
  Calculates the IP checksum for a given byte array.

  Args:
      data: A byte array representing the IP header or data.

  Returns:
      An integer representing the 16-bit checksum.
  """
    if len(data) % 2 != 0:
        raise ValueError("data length must be a multiple of 2")

    words = [data[i] << 8 | data[i + 1] for i in range(0, len(data), 2)]

    checksum = sum(words)

    while checksum > 0xffff:
        checksum = (checksum & 0xffff) + (checksum >> 16)

    return (~checksum) & 0xffff

    # Example usage
    # data = bytes([0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111, 0b11111111])
    # checksum = ip_checksum(data)
    # print(f"Checksum: {checksum:04X}")


def send_data(number: int):
    """Send a 2-byte number to the Arduino."""
    data = struct.pack('<H', number)  # '<H' means little-endian unsigned short (2 bytes)
    ser.write(data)


def receive_data() -> list[int]:
    """Receive 2-byte numbers from Arduino."""
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

    primes_python = calculate_prime_numbers(number)
    print(f"Prime numbers calculated in Python: {primes_python}")

    # each prime number needs to ocupy 2 bytes
    primes_arduino_bytes = struct.pack(f'>{len(primes_arduino)}H', *primes_arduino)

    primes_python_bytes = struct.pack(f'>{len(primes_python)}H', *primes_python)
    python_checksum = ip_checksum(primes_python_bytes)
    print(f"Checksum calculated in Python: {python_checksum:04X}")

finally:
    ser.close()
