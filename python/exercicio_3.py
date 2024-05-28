import struct

import serial
import time

arduino_port = 'COM4'
baud_rate = 9600  # Match this with the baud rate set on the Arduino

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(5)  # Wait for the connection to be established


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
def send_data(number):
    """Send a 2-byte number to the Arduino."""
    data = struct.pack('<H', number)  # '<H' means little-endian unsigned short (2 bytes)
    ser.write(data)
    print(f"Sent: {number} as bytes: {data}")

def receive_data():
    """Receive 2-byte numbers from Arduino."""
    primes = []
    while True:
        bytes_read = ser.read(2)
        if len(bytes_read) == 2:
            number = struct.unpack('<H', bytes_read)[0]  # Convert 2 bytes back to an integer
            primes.append(number)
            print(f"Received: {number}")
        else:
            break
    return primes

try:
    number = 50  # Example number to send to Arduino
    send_data(number)
    time.sleep(2)  # Wait a bit before checking for a response

    # Receive data from the Arduino
    primes = receive_data()
    print(f"Prime numbers received from Arduino: {primes}")

except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    ser.close()