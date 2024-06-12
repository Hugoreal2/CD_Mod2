import struct
import serial

DEFAULT_TARGET_NUMBER = 50
DEFAULT_PORT = "COM4"
DEFAULT_BAUDRATE = 9600

# ------------------------------------------------------
#                       UTILS FUNCTIONS
# ------------------------------------------------------
def prompt_target_number() -> int:
    returned = input(f"Target Number (blank for {DEFAULT_TARGET_NUMBER}): ")

    if returned == "":
        return DEFAULT_TARGET_NUMBER
    elif returned.isdigit():
        number = int(returned)
        # check if its between 0 and 255
        if 0 <= number <= 255:
            return number
        else:
            raise ValueError("Target Number must be between 0 and 255")
    else:
        raise ValueError("Target Number must be a number")

def prompt_port() -> str:
    returned = input(f"Serial Port to use (blank for {DEFAULT_PORT}): ")

    if returned == "":
        return DEFAULT_PORT
    else:
        return returned

def prompt_baudrate() -> int:
    returned = input(f"Baudate to use (blank for {DEFAULT_BAUDRATE}): ")

    if returned == "":
        return DEFAULT_BAUDRATE
    else:
        return int(returned)

def prompt_do_checksum() -> bool:
    returned = input("Perform Checksum? (y/n): ")

    return returned.lower() == "y"

def send_data(ser: serial.Serial, target_number: int, do_checksum: bool):
    """
    Sends one byte with the target number and one byte to command to do checksum
    """

    ser.write(struct.pack("B", target_number))
    ser.write(struct.pack("B", 1 if do_checksum else 0))

def receive_data(ser: serial.Serial) -> bytes:
    """
    Receives 2 byte ints and puts them in a byte array
    Until 4 bytes of 1s are received.
    """

    prime_numbers = bytearray()

    while True:
        received = ser.read(2)

        if received == b"\xFF\xFF":
            break

        prime_numbers += received

    return prime_numbers

def receive_checksum(ser: serial.Serial) -> int:
    """
    Reads two bytes from the serial and returns them as an int
    """

    received = ser.read(2)

    return struct.unpack("H", received)[0]


def ip_checksum(data: bytes) -> int:
    """
    Calculates the IP checksum of the given data.

    :param data: the data to calculate the checksum

    :return: the checksum
    """
    if len(data) % 2 != 0:
        raise ValueError("data length must be a multiple of 2")

    words = [data[i] << 8 | data[i + 1] for i in range(0, len(data), 2)]

    checksum = sum(words)

    while checksum > 0xffff:
        checksum = (checksum & 0xffff) + (checksum >> 16)

    return ~checksum & 0xffff

# ------------------------------------------------------
#                       MAIN
# ------------------------------------------------------

target_number = prompt_target_number()
port = prompt_port()
baudrate = prompt_baudrate()
do_checksum = prompt_do_checksum()

with serial.Serial(port, baudrate) as ser:
    send_data(ser, target_number, do_checksum)

    prime_numbers_bytes = receive_data(ser)
    print("Prime Numbers:")
    for i in range(0, len(prime_numbers_bytes), 4):
        number = struct.unpack("I", prime_numbers_bytes[i:i+4])[0]
        print(number)

    # if do_checksum:
    #     checksum = ip_checksum(prime_numbers_bytes)
    #     received_checksum = receive_checksum(ser)
    #
    #     print(f"Received checksum: {hex(received_checksum)}")
    #     print(f"Calculated checksum: {hex(checksum)}")
    #
    #     if(received_checksum == checksum):
    #         print("Checksums match!")
    #     else:
    #         print("Checksums don't match!")

